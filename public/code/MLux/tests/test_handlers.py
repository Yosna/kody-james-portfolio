from unittest.mock import patch

from run.ui.handlers import resize_terminal_items
from run.ui.ui import UISettings as ui


@patch("run.ui.handlers.dpg")
def test_resize_terminal_items(dpg):
    resize_terminal_items(ui())
    dpg.get_item_width.assert_called_once()
    dpg.get_item_height.assert_called_once()
    dpg.configure_item.assert_called()
    assert dpg.configure_item.call_count == 3
