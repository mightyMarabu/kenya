from nicegui import ui
from nicegui.events import MouseEventArguments

def mouse_handler(e: MouseEventArguments):
    color = 'SkyBlue' if e.type == 'mousedown' else 'SteelBlue'
    ii.content += f'<circle cx="{e.image_x}" cy="{e.image_y}" r="15" fill="none" stroke="{color}" stroke-width="4" />'
    ui.notify(f'{e.type} at ({e.image_x:.1f}, {e.image_y:.1f})')

# src = 'https://images.climate-data.org/location/11138/climate-graph.png'
# ii = ui.interactive_image(src, on_mouse=mouse_handler, events=['mousedown', 'mouseup'], cross=True)
