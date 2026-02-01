from unittest.mock import Mock, patch

from run.services.terminal import Terminal
from run.ui.builders import (
    build_control_panel,
    build_selection_window,
    build_terminal,
)
from run.ui.ui import UISettings as ui


class MockTerminal(Terminal):
    def __init__(self, tmp_path, process=None):
        self.process = process
        self.root = tmp_path
        self.start_training = Mock()
        self.stop = Mock()
        self.log = Mock()


@patch("run.ui.builders.ButtonRow.build")
@patch("run.ui.builders.Button")
@patch("run.ui.builders.dpg")
def test_build_control_panel(dpg, button, button_row_build):
    build_control_panel(ui())
    dpg.child_window.assert_called_once()
    button.assert_called()
    assert button.call_count == 4
    button_row_build.assert_called_once()


@patch("run.ui.builders.ResizeHandler")
@patch("run.ui.builders.ButtonRow.build")
@patch("run.ui.builders.Button")
@patch("run.ui.builders.dpg")
def test_build_terminal(dpg, button, button_row_build, resize_handler, tmp_path):
    build_terminal(ui(), MockTerminal(tmp_path), 100, 100)
    dpg.window.assert_called_once()
    dpg.child_window.assert_called_once()
    dpg.add_text.assert_called_once()
    button.assert_called()
    assert button.call_count == 4
    button_row_build.assert_called_once()
    resize_handler.assert_called_once()


@patch("run.ui.builders.Button.build")
@patch("run.ui.builders.dpg")
def test_build_selection_window(dpg, build):
    options = ["test", "test2", "test3"]
    build_selection_window("", "", options, 100, 100, lambda: None, None)
    dpg.window.assert_called_once()
    dpg.table.assert_called_once()
    dpg.add_table_column.assert_called_once()
    dpg.table_row.assert_called()
    build.assert_called()
    assert dpg.table_row.call_count == len(options)
    assert build.call_count == len(options)
