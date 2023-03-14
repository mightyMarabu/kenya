#!/usr/bin/env python3
from nicegui import Client, ui, app

from leaflet import leaflet

from counter import Counter

#from weather import Weather

from climate import mouse_handler

# ui.label("Hello World")
app.add_static_files('/pics', 'pics')

locations = {
    (2.3357, 37.9573): 'Marsabit',
    (-18.373, 18.073): 'somewhere in Namibia',

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
    map = leaflet().classes('w-full h-96')
 
    ui.markdown('Choose your location')
    # select button
    selection = ui.select(locations, on_change=lambda e: map.set_location(e.value)).classes('w-40')
    
    ui.link('Checkout the custom vue component', '/counter')

    await client.connected()  # wait for websocket connection
    selection.set_value(next(iter(locations)))  # trigger map.set_location with first location in selection

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