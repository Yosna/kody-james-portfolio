from pathlib import Path
from typing import Union
from unittest.mock import patch

import pytest

from run.ui.ui import (
    Button,
    ButtonRow,
    ConfigSettings,
    ControlPanelSettings,
    Fonts,
    FontSettings,
    InputText,
    ResizeHandler,
    SelectionSettings,
    Table,
    TerminalSettings,
    Toast,
    ToastSettings,
    UISettings,
)


def test_font_settings():
    font = FontSettings()
    assert font.size == 16
    assert font.path == "assets/fonts/DejaVuSans.ttf"


def test_toast_settings():
    toast = ToastSettings()
    assert toast.width == 250
    assert toast.height == 50
    assert toast.width_padding == 16
    assert toast.word_wrap == 234
    assert toast.pos_x_offset == 266
    assert toast.pos_y == 100


def test_config_settings():
    config = ConfigSettings()
    assert config.width == 540
    assert config.height == 800
    assert config.height_padding == 8


def test_control_panel_settings():
    control_panel = ControlPanelSettings()
    assert control_panel.height == 100
    assert control_panel.height_padding == 16


def test_terminal_settings():
    terminal = TerminalSettings()
    assert terminal.width_ratio == 0.8
    assert terminal.height_ratio == 0.8
    assert terminal.button_ratio == 0.1
    assert terminal.button_min_height == 30
    assert terminal.width_padding == 16
    assert terminal.height_padding == 42


def test_selection_settings():
    selection = SelectionSettings()
    assert selection.height == 40
    assert selection.models == ("Bigram", "LSTM", "GRU", "Transformer")
    assert selection.exports == ("Architecture", "Package", "Framework", "Application")


def test_ui_settings():
    ui = UISettings()
    assert ui.title == "Pipeline"
    assert ui.title_height == 40
    assert ui.width == 1200
    assert ui.height == 900
    assert isinstance(ui.font, FontSettings)
    assert isinstance(ui.toast, ToastSettings)
    assert isinstance(ui.config, ConfigSettings)
    assert isinstance(ui.control_panel, ControlPanelSettings)
    assert isinstance(ui.terminal, TerminalSettings)
    assert isinstance(ui.selection, SelectionSettings)


@patch("run.ui.ui.dpg")
def test_fonts(dpg):
    fonts = Fonts()
    fonts.load()
    base_path = Path(__file__).parent.parent
    assert fonts.root == base_path / "run"
    assert fonts.path == fonts.root / "assets" / "fonts" / "DejaVuSans.ttf"
    dpg.font_registry.assert_called_once()
    dpg.add_font.assert_called_once()
    dpg.add_font_chars.assert_called_once()
    dpg.bind_font.assert_called_once()


@patch("run.ui.ui.sys")
@patch("run.ui.ui.dpg")
def test_fonts_frozen(_, sys):
    sys.frozen = True
    sys._MEIPASS = str(Path(__file__).parent.parent)
    fonts = Fonts()
    fonts.load()
    assert fonts.root == Path(__file__).parent.parent / "run"
    assert fonts.path == fonts.root / "assets" / "fonts" / "DejaVuSans.ttf"


@patch("run.ui.ui.time")
@patch("run.ui.ui.threading")
@patch("run.ui.ui.dpg")
@pytest.mark.parametrize(
    "status, formatted",
    [
        ("success", "\u2714 Success\n\n"),
        ("warning", "\u26a0 Warning\n\n"),
        ("error", "\u2716 Error\n\n"),
    ],
)
def test_toast(dpg, threading, time, status, formatted):
    toast = Toast(status, "test", timeout=1000)
    toast.remove()
    assert toast.status == formatted
    assert toast.message == f"{formatted}test"
    assert toast.timeout == 1000
    dpg.generate_uuid.assert_called_once()
    dpg.get_viewport_width.assert_called_once()
    dpg.window.assert_called_once()
    dpg.add_text.assert_called_once()
    threading.Thread.assert_called_once()
    time.sleep.assert_called_once()
    dpg.does_item_exist.assert_called_once()
    dpg.delete_item.assert_called_once()


@patch("run.ui.ui.dpg")
def test_input_text(dpg):
    input_text = InputText("test")
    input_text.build()
    input_text.get_input()
    assert input_text.tag == "test"
    assert input_text.group_tag == "test_group"
    dpg.group.assert_called_once()
    dpg.add_spacer.assert_called_once()
    dpg.add_input_text.assert_called_once()
    dpg.get_value.assert_called_once()


@patch("run.ui.ui.dpg")
def test_button(dpg):
    button = Button("test", "test", lambda: None)
    button.build(100, 100)
    assert button.label == "test"
    assert button.tag == "test"
    assert callable(button.on_click)
    assert not hasattr(button, "args")
    dpg.add_button.assert_called_once()


@patch("run.ui.ui.dpg")
def test_button_row(dpg):
    button = Button("test", "test", lambda: None)
    button_row = ButtonRow("test", [button])
    button_row.build(100, 100)
    assert button_row.tag == "test"
    assert button_row.buttons == [button]
    assert button_row.weights == [1.0]
    dpg.table.assert_called_once()
    dpg.add_table_column.assert_called_once()
    dpg.add_button.assert_called_once()


@patch("run.ui.ui.dpg")
def test_table(dpg):
    table = Table(tag="test")
    table.row_item(lambda: None)
    table.add_row()
    assert table.columns == 1
    assert table.weights == [1.0]
    assert table.row_items == None
    dpg.add_table.assert_called_once()
    dpg.add_table_column.assert_called_once()
    dpg.table_row.assert_called_once()


@patch("run.ui.ui.dpg")
def test_table_no_row_items(dpg):
    table = Table(tag="test")
    table.add_row()
    dpg.table_row.assert_not_called()


@patch("run.ui.ui.dpg")
def test_resize_handler(dpg):
    resize_handler = ResizeHandler("test", lambda: None)
    assert resize_handler.tag == "test_handler"
    dpg.item_handler_registry.assert_called_once()
    dpg.add_item_resize_handler.assert_called_once()
    dpg.bind_item_handler_registry.assert_called_once()
