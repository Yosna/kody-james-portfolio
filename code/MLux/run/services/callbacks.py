"""A module for handling UI callbacks.

Includes:
- toggle_window: Toggle the visibility of a window.
- select_model: Select a model to train.
- toggle_model: Toggle the training or evaluation mode.
- _watch_training: Watch the training process to update the respective button label.
"""

import os
import threading

import dearpygui.dearpygui as dpg

from run.services.terminal import Terminal
from run.ui.ui import Toast
from services.exporter import ModelExporter


def refresh_log(
    messages: list[str], log_tag: str = "terminal_log", win_tag: str = "terminal_output"
) -> None:
    """Update the log and scroll to the bottom.

    Args:
        messages (list[str]): A list of messages to show in the log.
        log_tag (str): The tag of the log text area.
        win_tag (str): The tag of the parent window for the text area.
    """
    dpg.set_value(log_tag, "\n".join(messages))
    dpg.set_y_scroll(win_tag, -1.0)


def toggle_window(window: str) -> None:
    """Toggle for the selected window.

    Args:
        window (str): The window tag to toggle.
    """
    if dpg.does_item_exist(window):
        visible = dpg.is_item_visible(window)
        dpg.configure_item(window, show=not visible)


def select_model(model: str, terminal: Terminal) -> None:
    """Select the model to train.

    Args:
        model (str): The selected model name.
        terminal (Terminal): The terminal instance.
    """
    terminal.model = model.lower()
    label = f"Model Selected: {model}"
    dpg.configure_item("models_button", label=label)
    toggle_window("models")


def toggle_model(terminal: Terminal, mode: str) -> None:
    """Toggle for the selected model run mode (train or eval).

    Args:
        terminal (Terminal): The terminal instance.
        mode (str): The mode to run the model in.
    """
    if terminal.process:
        if mode == "train" and terminal._mode == mode:
            terminal.stop()
            dpg.configure_item("train_button", label="Start Training")
        elif mode == "train" or mode == "eval":
            process = "training" if terminal._mode == "train" else "evaluation"
            error = f"Model {process} is already in progress"
            terminal.log(error)
            Toast("error", error)
        return
    elif not terminal.model:
        error = "Select a model to start training"
        terminal.log(error)
        Toast("error", error)
        return

    terminal.run_model(mode=mode)

    if mode == "train":
        threading.Thread(target=_watch_training, args=(terminal,), daemon=True).start()
    elif mode == "eval":
        threading.Thread(target=terminal.watch_process, daemon=True).start()


def _watch_training(terminal: Terminal) -> None:
    """Watch the training process to update the respective button label.

    Args:
        terminal (Terminal): The terminal instance.
    """
    dpg.configure_item("train_button", label="Stop Training")
    terminal.watch_process()
    dpg.configure_item("train_button", label="Start Training")


def export_model(format: str, terminal: Terminal, directory: str = "exports") -> None:
    """Export the trained model.

    Args:
        format (str): The format to export the model in.
        terminal (Terminal): The terminal instance.
        directory (str): The directory to export the model.
    """
    if not terminal.model:
        Toast("error", "No selected model to export")
        return
    elif terminal.process:
        output = terminal.process.stdout
        if output and not output.closed:
            process = "training" if terminal._mode == "train" else "evaluation"
            Toast("error", f"{process} is still in progress")
            return

    export_dir = os.path.join(terminal.root, directory)
    os.makedirs(export_dir, exist_ok=True)

    cfg_path = os.path.join(terminal.root, "config.json")
    exporter = ModelExporter(terminal.model, cfg_path)

    try:
        exp_dir, exp_name = exporter.export(format)
        exported = f"{format} exported to {exp_dir}\nas {exp_name}"
        Toast("success", exported, timeout=5000)
    except ValueError as e:
        Toast("error", str(e))

    toggle_window("export")
