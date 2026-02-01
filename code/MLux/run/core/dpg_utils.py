"""A module for DearPyGui utilities.

Includes:
- init_gui: Initialize DearPyGui.
"""

import dearpygui.dearpygui as dpg


def init_gui(title: str, width: int, height: int) -> None:
    """Initialize DearPyGui.

    Args:
        title (str): The title of the window.
        width (int): The width of the window.
        height (int): The height of the window.
    """
    dpg.create_viewport(title=title, width=width, height=height)
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()

    # Allows the GUI to safely handle background threads.
    while dpg.is_dearpygui_running():
        jobs = dpg.get_callback_queue()
        dpg.run_callbacks(jobs)
        dpg.render_dearpygui_frame()

    dpg.destroy_context()
