from unittest.mock import Mock, patch

import pytest

from run.services.callbacks import (
    _watch_training,
    export_model,
    refresh_log,
    select_model,
    toggle_model,
    toggle_window,
)
from run.services.terminal import Terminal


class MockTerminal(Terminal):
    def __init__(self, tmp_path, process=None, mode="train"):
        super().__init__()
        self.process = process
        self.root = tmp_path
        self.run_model = Mock()
        self.stop = Mock()
        self.log = Mock()
        self.model: str | None = "Mock"
        self._mode = mode


@patch("run.services.callbacks.dpg")
def test_refresh_log(dpg):
    refresh_log(["test"])
    dpg.set_value.assert_called_once()
    dpg.set_y_scroll.assert_called_once()


@patch("run.services.callbacks.dpg")
def test_toggle_window(dpg):
    toggle_window("test")
    dpg.does_item_exist.assert_called_once()
    dpg.is_item_visible.assert_called_once()
    dpg.configure_item.assert_called_once()


@patch("run.services.callbacks.dpg")
def test_select_model(dpg, tmp_path):
    terminal = MockTerminal(tmp_path)
    select_model("test", terminal)
    dpg.is_item_visible.assert_called_once()
    dpg.configure_item.assert_called()
    assert dpg.configure_item.call_count == 2


@patch("run.services.callbacks.threading")
@patch("run.services.callbacks.dpg")
@pytest.mark.parametrize("mode", ["train", "eval"])
def test_toggle_model_modes(_, threading, tmp_path, mode):
    terminal = MockTerminal(tmp_path)
    toggle_model(terminal, mode)
    terminal.run_model.assert_called_once()
    threading.Thread.assert_called_once()


@patch("run.services.callbacks.Toast")
@patch("run.services.callbacks.dpg")
@pytest.mark.parametrize("mode", ["train", "eval"])
def test_toggle_model_process_open(dpg, Toast, tmp_path, mode):
    terminal = MockTerminal(tmp_path, process=Mock(), mode=mode)
    toggle_model(terminal, mode)
    stop_call_count = 1 if mode == "train" else 0
    dpg_call_count = 1 if mode == "train" else 0
    log_call_count = 1 if mode == "eval" else 0
    toast_call_count = 1 if mode == "eval" else 0
    assert terminal.stop.call_count == stop_call_count
    assert dpg.configure_item.call_count == dpg_call_count
    assert terminal.log.call_count == log_call_count
    assert Toast.call_count == toast_call_count


@patch("run.services.callbacks.Toast")
@patch("run.services.callbacks.dpg")
def test_toggle_model_no_model(dpg, Toast, tmp_path):
    terminal = MockTerminal(tmp_path)
    terminal.model = ""
    toggle_model(terminal, "train")
    terminal.log.assert_called_once()
    Toast.assert_called_once()
    terminal.run_model.assert_not_called()


@patch("run.services.callbacks.dpg")
def test_watch_training(dpg, tmp_path):
    terminal = MockTerminal(tmp_path, process=Mock(stdout=Mock(closed=True)))
    terminal.stop.side_effect = lambda: setattr(terminal, "process", None)
    _watch_training(terminal)
    dpg.configure_item.assert_called()
    assert dpg.configure_item.call_count == 2
    terminal.stop.assert_called_once()


@patch("run.services.callbacks.ModelExporter")
@patch("run.services.callbacks.Toast")
@patch("run.services.callbacks.dpg")
@pytest.mark.parametrize(
    "format", ["Architecture", "Package", "Framework", "Application"]
)
def test_export_model(dpg, toast, exporter, tmp_path, format):
    terminal = MockTerminal(tmp_path)
    exporter.return_value.export.return_value = ("", "")
    export_model(format, terminal, tmp_path)
    exporter.return_value.export.assert_called_once()
    toast.assert_called_once()
    dpg.configure_item.assert_called_once()


@patch("run.services.callbacks.ModelExporter")
@patch("run.services.callbacks.Toast")
def test_export_model_no_model(toast, exporter, tmp_path):
    terminal = MockTerminal(tmp_path)
    terminal.model = None
    export_model("Architecture", terminal, tmp_path)
    toast.assert_called_once()
    exporter.assert_not_called()


@patch("run.services.callbacks.toggle_window")
@patch("run.services.callbacks.Toast")
def test_export_model_invalid_format(toast, toggle_window, tmp_path):
    terminal = MockTerminal(tmp_path)
    (tmp_path / "config.json").write_text("{}")
    export_model("Invalid", terminal, str(tmp_path))
    toast.assert_called_once()
    toggle_window.assert_called_once()


@patch("run.services.callbacks.ModelExporter")
@patch("run.services.callbacks.Toast")
def test_export_model_open_process(toast, exporter, tmp_path):
    terminal = MockTerminal(tmp_path, process=Mock(stdout=Mock(closed=False)))
    export_model("Architecture", terminal, tmp_path)
    toast.assert_called_once()
    exporter.assert_not_called()
