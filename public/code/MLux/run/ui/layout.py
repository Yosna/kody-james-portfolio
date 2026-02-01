"""A module for initializing the UI components.

Includes:
- init_config: Initialize the config editor.
- init_model_selection: Initialize the model selection.
- init_terminal: Initialize the terminal.
- init_export_selection: Initialize the export selection.
"""

from typing import Callable

import dearpygui.dearpygui as dpg

from run.config import run_config
from run.services.callbacks import refresh_log
from run.services.terminal import Terminal
from run.ui.builders import build_selection_window, build_terminal
from run.ui.ui import UISettings


def init_config(ui: UISettings, path: str = "config.json") -> None:
    """Initialize the config editor.

    Args:
        ui (UISettings): The UI settings dataclass.
        path (str): The path to the config file.
    """
    config_h = ui.config.height - ui.config.height_padding

    run_config(path=path, height=config_h, init=False)

    config_x = (ui.width - ui.config.width) / 2
    config_y = ui.height - config_h
    dpg.configure_item("config", pos=(config_x, config_y), show=False)


def init_terminal(ui: UISettings) -> Terminal:
    """Initialize the terminal.

    Args:
        ui (UISettings): The UI settings dataclass.
    """
    terminal = Terminal()
    terminal.log_callback = lambda: refresh_log(terminal.log_history)

    terminal_w = int(ui.width * ui.terminal.width_ratio)
    terminal_h = int((ui.height - ui.control_panel.height) * ui.terminal.height_ratio)

    build_terminal(ui, terminal, terminal_w, terminal_h)

    terminal_x = (ui.width - terminal_w) / 2
    terminal_y = (ui.height - terminal_h + ui.title_height) / 2
    dpg.configure_item("terminal", pos=(terminal_x, terminal_y), show=False)

    return terminal


def init_selection_window(
    ui: UISettings,
    label: str,
    tag: str,
    options: list[str] | tuple,
    callback: Callable,
    args: tuple | None = None,
) -> None:
    """Initialize the selection window.

    Args:
        ui (UISettings): The UI settings dataclass.
        label (str): The label of the window.
        tag (str): The tag of the window.
        options (list[str] | tuple): The options to select from.
        callback (Callable): The callback function to call when the button is clicked.
        args (tuple | None): The arguments to pass to the callback function.
    """
    window_w = int(ui.width / 4)
    btn_h = ui.selection.height

    build_selection_window(label, tag, options, window_w, btn_h, callback, args)

    window_h = dpg.get_item_height(tag) or (len(options) * btn_h)
    window_x = (ui.width - window_w) / 2
    window_y = (ui.height - window_h - ui.title_height) / 2
    dpg.configure_item(tag, pos=(window_x, window_y), show=False)
