#sentinel API

from nicegui import ui, Client, app 
from nicegui.events import ValueChangeEventArguments

import requests
from zipfile import ZipFile

import pandas as pd
from pandas.api.types import is_bool_dtype, is_numeric_dtype



from requests.auth import HTTPBasicAuth


def queryAPI():
    #LatLng = ('37.30488,01.85034') # Ngurunit
    #LatLng = ('37.898626114941905,2.27305876687853') # near Marsabit
    footprint = 'POLYGON((37.32548632535571 1.8491098129258177,38.06615104713074 1.8491098129258177,38.06615104713074 2.582527953220037,37.32548632535571 2.582527953220037,37.32548632535571 1.8491098129258177))'
    #prodType = 'SLC'
    prodType = 'S2MSI2A' #,S2MSI1C, S2MS2Ap
    days = '20'

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
        'Cloud cover II': [[scene['double'][7]['content']] for scene in searchResult['feed']['entry']],
     #   'Downloadlink': [[scene['link'][0]['href']] for scene in searchResult['feed']['entry']],
        'Quicklook': [[scene['link'][2]['href']] for scene in searchResult['feed']['entry']],
    })
    ####
    def update(*, df: pd.DataFrame, r: int, c: int, value):
        df.iat[r, c] = value
        ui.notify(f'Set ({r}, {c}) to {value}')

    with ui.grid(rows=len(df.index)+1).classes('grid-flow-col auto-cols-max'):
        for c, col in enumerate(df.columns):
            ui.label(col).classes('font-bold')
            for r, row in enumerate(df.loc[:, col]):
                if is_bool_dtype(df[col].dtype):
                    cls = ui.checkbox
                elif is_numeric_dtype(df[col].dtype):
                    cls = ui.number
                else:
                    cls = ui.input
                cls(value=row, on_change=lambda event, r=r, c=c: update(df=df, r=r, c=c, value=event.value))
    ### ag grid from dataframe
    ui.aggrid.from_pandas(df,html_columns=[4]).classes('max-h-40')
    #### table
    ui.aggrid({
        'columnDefs': [
            {'headerName': 'Name', 'field': 'name'},
            {'headerName': 'URL', 'field': 'url'},
        ],
        'rowData': [
            {'name': 'Google', 'url': '<a href="https://google.com">https://google.com</a>'},
            {'name': 'Facebook', 'url': '<a href="https://facebook.com">https://facebook.com</a>'},
        ],
    }, html_columns=[1])

    return df


def getSatelliteData(entry):
    fileName = searchResult['feed']['entry'][entry]['title']
    downloadLink = searchResult['feed']['entry'][4]['link'][entry]['href']
    file = requests.get(downloadLink,auth=('sebastiannormann', 'Goatscanfly_2022'))
    with open('../satData/'+fileName+'.zip','wb') as f:
        f.write(file.content)
    
    with ZipFile("../satData/"+fileName+".zip", 'r') as zObject:
        zObject.extractall(
        path="../satData/")
