"""Model pipeline for model building, training, exporting, and deployment.

Includes:
- A configuration wrapper using the config editor.
- Model architecture selection for training and evaluation.
- A terminal for logging and debugging.
- User control to start and stop training and evaluation.

Example:
    To run the pipeline GUI:
    python -m run pipeline
"""

import dearpygui.dearpygui as dpg

from run.core.dpg_utils import init_gui
from run.services.callbacks import export_model, select_model
from run.ui.builders import build_control_panel
from run.ui.layout import init_config, init_selection_window, init_terminal
from run.ui.ui import Fonts, UISettings


def run_pipeline(cfg_path: str = "config.json") -> None:
    """Run the model pipeline GUI.

    Args:
        cfg_path (str): The path to the config file.
    """
    dpg.create_context()

    ui = UISettings()
    Fonts().load()

    terminal = init_terminal(ui)
    init_config(ui, cfg_path)

    selection_windows = [
        ["Select Model", "models", ui.selection.models, select_model, (terminal,)],
        ["Export Formats", "export", ui.selection.exports, export_model, (terminal,)],
    ]
    for selection in selection_windows:
        init_selection_window(ui, *selection)

    with dpg.window(
        label=ui.title, tag=ui.title.lower(), width=ui.width, height=ui.height
    ):
        build_control_panel(ui)

    dpg.set_primary_window(ui.title.lower(), True)
    dpg.set_exit_callback(terminal.stop)

    init_gui(title=ui.title, width=ui.width, height=ui.height)


if __name__ == "__main__":
    run_pipeline()
