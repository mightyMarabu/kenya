#sentinel API

from nicegui import ui, Client, app 
from nicegui.events import ValueChangeEventArguments

import requests
from zipfile import ZipFile

import pandas as pd
from pandas.api.types import is_bool_dtype, is_numeric_dtype



from requests.auth import HTTPBasicAuth


def queryAPI(day):
    #LatLng = ('37.30488,01.85034') # Ngurunit
    #LatLng = ('37.898626114941905,2.27305876687853') # near Marsabit
    footprint = 'POLYGON((37.32548632535571 1.8491098129258177,38.06615104713074 1.8491098129258177,38.06615104713074 2.582527953220037,37.32548632535571 2.582527953220037,37.32548632535571 1.8491098129258177))'
    #prodType = 'SLC'
    prodType = 'S2MSI2A' #,S2MSI1C, S2MS2Ap
    days = str(day)

    API = 'https://scihub.copernicus.eu/dhus/search?q=ingestiondate:[NOW-'+days+'DAY%20TO%20NOW]%20AND%20producttype:'+prodType+'%20AND%20footprint:"Intersects('+footprint+')"&%20rows=100&start=0&format=json'
    r = requests.get(API,auth=('sebastiannormann', 'Goatscanfly_2022'))
    #print(r)
    searchResult = r.json()
    #searchResult
    #searchResult['feed']['entry']
     
    df = pd.DataFrame(data={
        'ID': [i for i in range(len(searchResult['feed']['entry']))],
     #   'Title': [scene['title'] for scene in searchResult['feed']['entry']],
        'Summary': [scene['summary'] for scene in searchResult['feed']['entry']],
        'Cloud cover I': [scene['double'][6]['content'] for scene in searchResult['feed']['entry']],
        'Cloud cover II': [scene['double'][7]['content'] for scene in searchResult['feed']['entry']],
     #   'Downloadlink': [[scene['link'][0]['href']] for scene in searchResult['feed']['entry']],
     #   'Quicklook': '<a href='+[[scene['link'][2]['href']] for scene in searchResult['feed']['entry']]+'</a>',
        'Quicklook': [scene['link'][2]['href'] for scene in searchResult['feed']['entry']],
    })
 
    # with ui.grid(rows=len(df.index)+1).classes('grid-flow-col auto-cols-max'):
    #     for c, col in enumerate(df.columns):
    #         ui.label(col).classes('font-bold')
    #         for r, row in enumerate(df.loc[:, col]):
    #             if is_bool_dtype(df[col].dtype):
    #                 cls = ui.checkbox
    #             elif is_numeric_dtype(df[col].dtype):
    #                 cls = ui.number
    #             else:
    #                 cls = ui.input
    #             cls(value=row, on_change=lambda event, r=r, c=c: update(df=df, r=r, c=c, value=event.value))
    
    
    ### ag grid from dataframe
    #ui.aggrid.from_pandas(df).classes('max-h-40')
    
    def create_url_link(row):
        return f'<a target="_blank" href="{row["Quicklook"]}">{row["Quicklook"]}</a>'

    df['Quicklook'] = df.apply(create_url_link, axis=1)

    column_defs = [
        {'headerName': 'ID', 'field': 'ID'},
        {'headerName': 'Summary', 'field': 'Summary'},
        {'headerName': 'Cloud cover I', 'field': 'Cloud cover I'},
        {'headerName': 'Cloud cover II', 'field': 'Cloud cover II'},
        {'headerName': 'Quicklook', 'field': 'Quicklook'},
    ]

    row_data = df.to_dict(orient='records')

    result = {
        'columnDefs': column_defs,
        'rowData': row_data,
    }

    #html_columns = [1]

    ui.aggrid(result, html_columns=[4])
    
    return searchResult


def getSatelliteData(ID):
    fileName = searchResult['feed']['entry'][ID]['title']
    downloadLink = searchResult['feed']['entry'][ID]['link'][0]['href']
    file = requests.get(downloadLink,auth=('sebastiannormann', 'Goatscanfly_2022'))
    with open('/satData/'+fileName+'.zip','wb') as f:
        f.write(file.content)
    
    with ZipFile("/satData/"+fileName+".zip", 'r') as zObject:
        zObject.extractall(
        path="/satData/")
