"""A module for handling UI event handlers."""

import dearpygui.dearpygui as dpg

from run.ui.ui import UISettings


def resize_terminal_items(ui: UISettings) -> None:
    """Dynamically resize the terminal items."""
    default_width = int(ui.width * ui.terminal.width_ratio)
    default_height = int(ui.height * ui.terminal.height_ratio)

    width = dpg.get_item_width("terminal") or default_width
    height = dpg.get_item_height("terminal") or default_height

    button_h = int(height * ui.terminal.button_ratio)
    if button_h < ui.terminal.button_min_height:
        button_h = ui.terminal.button_min_height

    output_w = width - ui.terminal.width_padding
    output_h = height - button_h - ui.terminal.height_padding
    text_wrap = output_w - ui.terminal.width_padding

    dpg.configure_item("terminal_buttons", height=button_h)
    dpg.configure_item("terminal_output", width=output_w, height=output_h)
    dpg.configure_item("terminal_log", wrap=text_wrap)
