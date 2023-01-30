#!/usr/bin/env python3
from nicegui import Client, ui

from leaflet import leaflet

# ui.label("Hello World")





locations = {
    (2.3357, 37.9573): 'Marsabit',
    (-18.373, 18.073): 'somewhere in Namibia',

}


@ui.page('/')
async def main_page(client: Client):

    heading = ui.markdown('## this is a heading')

    map = leaflet().classes('w-full h-96')
 
    ui.markdown('Choose your location')
 
    selection = ui.select(locations, on_change=lambda e: map.set_location(e.value)).classes('w-40')
    
    
    
    await client.connected()  # wait for websocket connection
    selection.set_value(next(iter(locations)))  # trigger map.set_location with first location in selection





ui.run()