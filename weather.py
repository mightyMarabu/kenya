from nicegui.dependencies import register_component
from nicegui.element import Element

register_component('weather',__file__,'weather.js')

class Weather(Element):
    def __init__(self, title: str) -> None:
        super().__init__('weather')
        self._props['title'] = title
        
