from nicegui import ui
from nicegui.dependencies import register_component
from nicegui.element import Element

register_component('weather', __file__, 'weather.js')

class Weather(Element):

    def __init__(self) -> None:
        super().__init__('weather')
        # ui.add_head_html('<link href="https://use.fontawesome.com/ba56542055.css" rel="stylesheet"/>')
        ui.add_head_html('<script>!function(d,s,id){var js,fjs=d.getElementsByTagName(s)[0];if(!d.getElementById(id)){js=d.createElement(s);js.id=id;js.src="https://weatherwidget.io/js/widget.min.js";fjs.parentNode.insertBefore(js,fjs);}}(document,"script","weatherwidget-io-js"); </script>')
        #ui.add_head_html('<script src="https://kit.fontawesome.com/cc869f066a.js"></script>')
        ui.add_body_html('<a class="weatherwidget-io" href="https://forecast7.com/en/2d4437d98/marsabit-county/" data-label_1="MARSABIT COUNTY" data-label_2="WEATHER" data-theme="original" >MARSABIT COUNTY WEATHER</a>')
        # self._props['text'] = text
        
