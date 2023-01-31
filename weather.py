from nicegui import ui
from nicegui.dependencies import register_component
from nicegui.element import Element

register_component('weather', __file__, 'weather.js')

class Weather(Element):

    def __init__(self) -> None:
        super().__init__('weather')
        # ui.add_head_html('<link href="https://use.fontawesome.com/ba56542055.css" rel="stylesheet"/>')
        # ui.add_head_html('<script src="https://use.fontawesome.com/ba56542055.js"></script>')
        ui.add_head_html('<script src="https://kit.fontawesome.com/cc869f066a.js"></script>')
        # self._props['text'] = text
        
