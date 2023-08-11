#!/usr/bin/env python3
from nicegui import Client, ui, app

from pygments import *

from leaflet import leaflet
from db import spatialite

from sentinelAPI import *
from uploadCropStack import *

from counter import Counter

#from weather import Weather

from climate import mouse_handler

# ui.label("Hello World")
app.add_static_files('/pics', 'pics')

locations = {
    (1.7412757745740912, 37.31536534666663): 'Ngurunit',
    (2.322920338801376, 37.99268689194787): 'Marsabit',
    (-18.176413901509832, 20.91621324764841): 'somewhere in Namibia',
    (51.350300480813004, 9.855289171837422): 'WIZ Agrartechnik'

}

@ui.page('/')
async def main_page(client: Client):

    ui.markdown('### Should I stay or should I go?')

    with ui.row():
### weather ####
        #Weather()
### climate ####
        with ui.expansion('Marsabit climate diagram!', icon='open_with').classes('w-full'):
            with ui.card():
                src = 'https://images.climate-data.org/location/11138/climate-graph.png'
                ii = ui.interactive_image(src, on_mouse=mouse_handler, events=['mousedown', 'mouseup'], cross=True)
            
### Map ###    
    map = leaflet().classes('w-full h-96 ')
    ui.markdown('#### Choose your location')
    selection = ui.select(locations,value= (1.7412757745740912, 37.31536534666663), on_change=lambda e: map.set_location(e.value)).classes('w-40')
    
    await client.connected()  # wait for websocket connection

 
#####################################################################################################################   
### DB interaction ###
    #db =  spatialite()
#####################################################################################################################
    with ui.tabs().classes('w-full') as tabs:
        one = ui.tab('get Data')
        two = ui.tab('process Data')
    with ui.tab_panels(tabs).classes('w-full'):
        with ui.tab_panel(one):
    ### Query Sentinel API ###   
            days = 10
            
            ui.markdown('### Get some data..')
            days = ui.number(label='for the last ... days.', value=days)
            #print (days.value)
            #print(selection.value)
            
            ui.button('Query Sentinel API!', on_click=lambda: queryAPI (int(days.value),float(selection.value[1]),float(selection.value[0])))
            imageID = ui.number(label='Image ID')
            
            ui.button('Download!', on_click=lambda: getSatelliteData(int(imageID.value)))
            # ui.button('Download Sentinel Image'on_click=lambda: ui.download(downloadLink))
        with ui.tab_panel(two):
            #ui.upload(on_upload=lambda e: uploadAOI()).classes('max-w-full')
            ui.label('Upload your AreaOfInterest:')
            aoi = uploadAOI()
            ui.label('Upload Band 2,3,4,8:')
            aoi = uploadband()

#####################################################################################################################
### Custom ###
    #ui.link('Checkout the custom vue component', '/counter')

    #await client.connected()  # wait for websocket connection
    #selection.set_value(next(iter(locations)))  # trigger map.set_location with first location in selection

################################################

@ui.page('/counter')
async def counter_page(client: Client):

    ui.markdown('''
    #### Try the new click counter!
    Click to increment its value.
    ''')
    with ui.card():
        counter = Counter('Clicks', on_change=lambda msg: ui.notify(f'The value changed to {msg["args"]}.'))


    ui.button('Reset', on_click=counter.reset).props('small outline')

################################################

ui.run()