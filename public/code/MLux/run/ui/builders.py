"""A module for building the UI components.

Includes:
- build_control_panel: Build the control panel.
- build_terminal: Build the terminal window.
- build_selection_window: Build a window to select from a list of options.
"""

from typing import Callable

import dearpygui.dearpygui as dpg

from run.services.callbacks import toggle_model, toggle_window
from run.services.terminal import Terminal
from run.ui.handlers import resize_terminal_items
from run.ui.ui import Button, ButtonRow, ResizeHandler, UISettings


def build_control_panel(ui: UISettings) -> None:
    """Build the control panel.

    Args:
        ui (UISettings): The UI settings dataclass.
    """
    with dpg.child_window(width=-1, height=ui.control_panel.height):
        table_h = ui.control_panel.height - ui.control_panel.height_padding

        buttons = [
            Button("Config", "config_button", toggle_window, ("config",)),
            Button("Select Model", "models_button", toggle_window, ("models",)),
            Button("Terminal", "terminal_button", toggle_window, ("terminal",)),
            Button("Export", "export_button", toggle_window, ("export",)),
        ]

        ButtonRow("control_panel", buttons).build(height=table_h)


def build_terminal(ui: UISettings, terminal: Terminal, width: int, height: int) -> None:
    """Build the terminal window.

    Args:
        ui (UISettings): The UI settings dataclass.
        terminal (Terminal): The terminal instance.
        width (int): The width of the window.
        height (int): The height of the window.
    """
    with dpg.window(label="Terminal", tag="terminal", width=width, height=height):
        with dpg.child_window(tag="terminal_output"):
            text_wrap = width - ui.terminal.width_padding
            dpg.add_text(tag="terminal_log", wrap=text_wrap)

        buttons = [
            Button("Start Training", "train_button", toggle_model, (terminal, "train")),
            Button("Generate Sample", "eval_button", toggle_model, (terminal, "eval")),
            Button("Clear", "clear_terminal", terminal.clear),
            Button("Close", "close_terminal", toggle_window, ("terminal",)),
        ]

        ButtonRow("terminal_buttons", buttons).build()
        ResizeHandler("terminal", lambda: resize_terminal_items(ui))


def build_selection_window(
    label: str,
    tag: str,
    options: list[str] | tuple,
    width: int,
    height: int,
    callback: Callable,
    args: tuple | None = None,
) -> None:
    """Build a window to select from a list of options.

    Args:
        label (str): The label of the window.
        tag (str): The tag of the window.
        options (list[str] | tuple): The options to select from.
        width (int): The width of the window.
        height (int): The height of the selection buttons.
        callback (Callable): The callback function to call when the button is clicked.
        args (tuple | None): The arguments to pass to the callback function.

    Notes:
        The option is sent as the first argument to the callback function.
    """
    with dpg.window(label=label, tag=tag, width=width):
        with dpg.table(header_row=False):
            dpg.add_table_column(init_width_or_weight=1.0)
            for option in options:
                with dpg.table_row():
                    args = args if args is not None else ()
                    button = Button(option, option, callback, args=(option, *args))
                    button.build(height=height)
