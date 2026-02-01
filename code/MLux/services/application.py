"""A module to build standalone applications for trained models."""

from dataclasses import dataclass
from typing import Any

import dearpygui.dearpygui as dpg
import torch

from models.base_model import BaseLanguageModel as BaseLM
from run.core.dpg_utils import init_gui
from run.ui.ui import Button, ButtonRow, Fonts, InputText, Table


@dataclass(slots=True)
class ApplicationUI:
    """A class to store the UI elements for the application."""

    width: int = 1200
    height: int = 900
    width_padding: int = 16
    height_padding: int = 20
    title_height: int = 40
    window_width: int = width - width_padding
    window_height: int = height - title_height
    child_width: int = window_width - width_padding
    control_height: int = 60
    output_height: int = window_height - control_height - height_padding
    output_wrap: int = window_width - 32
    log_limit: int = 250


class Application:
    """An exporter to build applications with trained models."""

    def __init__(self, model: BaseLM):
        """Initialize the application.

        Args:
            model (BaseLM): The model to compile into the application.
        """
        model.device = (
            torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
        )
        self.model = model
        models = ("Bigram", "LSTM", "GRU", "Transformer")
        self.name = next(m for m in models if m.lower() == model.name.lower())
        self.generator = model.metadata["generator"].capitalize()
        self.title = f"{self.name} {self.generator} Generation Interface"
        self.tag = self.title.lower().replace(" ", "_")
        self.log = []
        self.log_limit = 0
        self.launch = lambda: self._compile()

    def _compile(self) -> None:
        """Compile the application."""
        dpg.create_context()

        Fonts().load()

        ui = ApplicationUI()

        self.log_limit = ui.log_limit
        self._model_metadata(ui)

        win_w = ui.window_width
        win_h = ui.window_height
        with dpg.window(
            label=self.title, tag=self.tag, width=win_w, height=win_h, no_title_bar=True
        ):
            self._output_window(ui)
            self._control_panel(ui)

        dpg.set_primary_window(self.tag, True)

        init_gui(title=self.title, width=ui.width, height=ui.height)

    def _output_window(self, ui: ApplicationUI) -> None:
        """Build the output window.

        Args:
            ui (ApplicationUI): The UI elements.
        """
        with dpg.child_window(
            tag="output_window", width=ui.child_width, height=ui.output_height
        ):
            dpg.add_text(tag="output", wrap=ui.output_wrap)

    def _control_panel(self, ui: ApplicationUI) -> None:
        """Build the control panel.

        Args:
            ui (ApplicationUI): The UI elements.
        """
        panels = {
            "Random": self._random_control_panel,
            "Prompt": self._prompt_control_panel,
        }

        with dpg.child_window(
            tag="control_panel", width=ui.child_width, height=ui.control_height
        ):
            panels[self.generator]()

    def _random_control_panel(self) -> None:
        """Build the random control panel."""
        buttons = [
            Button("Generate", "generate", self._generate),
            Button("Metadata", "metadata", self._toggle_window, ("model_metadata",)),
        ]
        weights = [0.8, 0.2]
        ButtonRow(tag="buttons", buttons=buttons, weights=weights).build()

    def _prompt_control_panel(self) -> None:
        """Build the prompt control panel."""
        weights = [0.75, 0.15, 0.1]
        prompt_table = Table(columns=3, weights=weights, header_row=False)

        prompt = InputText("prompt")
        prompt_table.row_item(prompt.build, padding=6)

        generate = lambda: self._generate(prompt.get_input())
        buttons = [
            Button("Generate", "generate", generate),
            Button("Metadata", "metadata", self._toggle_window, ("model_metadata",)),
        ]
        for button in buttons:
            prompt_table.row_item(button.build)

        prompt_table.add_row()

    def _model_metadata(self, ui: ApplicationUI) -> None:
        """Display the model metadata.

        Args:
            ui (ApplicationUI): The UI elements.
        """
        with dpg.window(label="Model Metadata", tag="model_metadata", autosize=True):
            meta_table = Table(columns=2, header_row=False)

            for attr in self.model.__annotations__:
                self.model.metadata[attr] = getattr(self.model, attr)

            for key, value in self.model.metadata.items():
                meta_table.row_item(dpg.add_text, key)
                meta_table.row_item(dpg.add_text, value)
                meta_table.add_row()

        self._pos_center(ui, "model_metadata", "output_window")

    def _generate(self, *args: Any) -> None:
        """Generate text from the model."""
        text = self.model.generate(*args)
        self.log.append(f"{text}\n")
        if len(self.log) > self.log_limit:
            self.log.pop(0)
        dpg.set_value("output", "\n".join(self.log))
        dpg.set_y_scroll("output_window", -1.0)

    def _toggle_window(self, window: str) -> None:
        """Toggle the visibility of a window.

        Args:
            window (str): The tag of the window to toggle.
        """
        if dpg.does_item_exist(window):
            visible = dpg.is_item_visible(window)
            dpg.configure_item(window, show=not visible)

    def _pos_center(
        self, ui: ApplicationUI, tag: str, parent: str, show: bool = False
    ) -> None:
        """Center a window.

        Args:
            ui (ApplicationUI): The UI elements.
            tag (str): The tag of the window to center.
            parent (str): The tag of the parent window to center relative to.
            show (bool): The visibility of the window.
        """
        dpg.configure_item(tag, show=True)
        width, height = dpg.get_item_rect_size(tag)

        if (width, height) == (0, 0):
            frame = dpg.get_frame_count()
            args = (ui, tag, parent, show)
            # Two frames: one to render the window and one to get a correct size
            dpg.set_frame_callback(frame + 2, lambda: self._pos_center(*args))
            return

        parent_w, parent_h = dpg.get_item_rect_size(parent)
        pos_x = int((parent_w - width) / 2)
        pos_y = int((parent_h - height + ui.title_height) / 2)
        dpg.configure_item(tag, pos=(pos_x, pos_y), show=show)
