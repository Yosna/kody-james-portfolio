from unittest.mock import patch

from run.pipeline import run_pipeline


def test_run_pipeline():
    with patch("run.pipeline.dpg") as dpg, patch("run.pipeline.Fonts") as fonts, patch(
        "run.pipeline.init_config"
    ) as init_config, patch(
        "run.pipeline.init_selection_window"
    ) as init_selection_window, patch(
        "run.pipeline.init_terminal"
    ) as init_terminal, patch(
        "run.pipeline.build_control_panel"
    ) as build_control_panel, patch(
        "run.pipeline.init_gui"
    ) as init_gui:
        run_pipeline()
        dpg.create_context.assert_called_once()
        dpg.set_primary_window.assert_called_once()
        dpg.set_exit_callback.assert_called_once()
        fonts.assert_called_once()
        init_config.assert_called_once()
        init_terminal.assert_called_once()
        init_selection_window.assert_called()
        assert init_selection_window.call_count == 2
        build_control_panel.assert_called_once()
        init_gui.assert_called_once()
