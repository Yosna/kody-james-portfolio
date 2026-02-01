from unittest.mock import patch

import pytest

from run.ui.layout import init_config, init_selection_window, init_terminal
from run.ui.ui import UISettings as ui


@pytest.mark.parametrize(
    "patch_func, init_func",
    [
        ("run_config", lambda: init_config(ui(), "config.json")),
        ("build_terminal", lambda: init_terminal(ui())),
        (
            "build_selection_window",
            lambda: init_selection_window(ui(), "", "", [], lambda: None),
        ),
    ],
)
def test_initializations(patch_func, init_func):
    patch_func = f"run.ui.layout.{patch_func}"
    with patch("run.ui.layout.dpg") as dpg, patch(patch_func) as builder:
        init_func()
        builder.assert_called_once()
        dpg.configure_item.assert_called_once()
