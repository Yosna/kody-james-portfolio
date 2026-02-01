from unittest.mock import patch

from run.core.dpg_utils import init_gui


def test_initialize_dpg():
    dpg_patch = patch("run.core.dpg_utils.dpg")
    dpg_running_patch = patch("run.core.dpg_utils.dpg.is_dearpygui_running")
    with dpg_patch as dpg, dpg_running_patch as is_dearpygui_running:
        is_dearpygui_running.side_effect = [True, False]
        init_gui("test", 100, 100)
        dpg.create_viewport.assert_called_once()
        dpg.setup_dearpygui.assert_called_once()
        dpg.show_viewport.assert_called_once()
        dpg.start_dearpygui.assert_called_once()
        dpg.get_callback_queue.assert_called_once()
        dpg.run_callbacks.assert_called_once()
        dpg.render_dearpygui_frame.assert_called_once()
        dpg.destroy_context.assert_called_once()
