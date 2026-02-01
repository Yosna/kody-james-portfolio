"""A module for creating and managing the UI.

Includes:
- Fonts: A class for loading and managing fonts.
- Toast: A class to display toast messages.
- InputText: A class to create input text.
- Button: A class to create buttons.
- ButtonRow: A class to create dynamically resizable button rows.
- Table: A class to create tables.
- ResizeHandler: A class to handle custom resizing calculations.
"""

import sys
import threading
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable

import dearpygui.dearpygui as dpg


@dataclass(slots=True)
class FontSettings:
    """A class to contain the font settings."""

    size: int = 16
    path: str = "assets/fonts/DejaVuSans.ttf"


@dataclass(slots=True)
class ToastSettings:
    """A class to contain the toast settings."""

    width: int = 250
    height: int = 50
    width_padding: int = 16
    word_wrap: int = width - width_padding
    pos_x_offset: int = width + width_padding
    pos_y: int = 100


@dataclass(slots=True)
class ConfigSettings:
    """A class to contain the config settings."""

    width: int = 540
    height: int = 800
    height_padding: int = 8


@dataclass(slots=True)
class ControlPanelSettings:
    """A class to contain the control panel settings."""

    height: int = 100
    height_padding: int = 16


@dataclass(slots=True)
class TerminalSettings:
    """A class to contain the terminal settings."""

    width_ratio: float = 0.8
    height_ratio: float = 0.8
    button_ratio: float = 0.1
    button_min_height: int = 30
    width_padding: int = 16
    height_padding: int = 42


@dataclass(slots=True)
class SelectionSettings:
    """A class to contain the selection settings."""

    height: int = 40
    models: tuple = ("Bigram", "LSTM", "GRU", "Transformer")
    exports: tuple = ("Architecture", "Package", "Framework", "Application")


@dataclass(slots=True)
class UISettings:
    """A class to contain the UI settings."""

    title: str = "Pipeline"
    title_height: int = 40
    width: int = 1200
    height: int = 900
    font: FontSettings = field(default_factory=FontSettings)
    toast: ToastSettings = field(default_factory=ToastSettings)
    config: ConfigSettings = field(default_factory=ConfigSettings)
    control_panel: ControlPanelSettings = field(default_factory=ControlPanelSettings)
    terminal: TerminalSettings = field(default_factory=TerminalSettings)
    selection: SelectionSettings = field(default_factory=SelectionSettings)


class Fonts:
    """A class for loading and managing fonts.

    Attributes:
    - root (str): The root directory of the fonts.
    - path (str): The path to the font file.
    """

    root: Path
    path: Path

    def __init__(self):
        """Initialize the fonts."""
        self.settings = FontSettings()

        if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
            self.root = Path(getattr(sys, "_MEIPASS")) / "run"
        else:
            self.root = Path(__file__).parents[1]

        self.path = self.root / self.settings.path

    def load(self) -> None:
        """Load the fonts and status icons."""
        with dpg.font_registry() as registry:
            font = dpg.add_font(str(self.path), self.settings.size, parent=registry)
            dpg.add_font_chars([0x2714, 0x26A0, 0x2716], parent=font)
            dpg.bind_font(font)


class Toast:
    """A class to display toasts.

    Attributes:
    - status (str): The status to use for the toast message.
    - message (str): The message to display formatted with the status.
    - timeout (int): The timeout in milliseconds to remove the toast.
    - tag (str): A generated tag for the toast.

    Notes:
    - Toasts are automatically displayed when initialized.
    """

    status: str
    message: str
    timeout: int
    tag: int | str

    def __init__(self, status: str, message: str, timeout: int = 3000):
        """Initialize the toast.

        Args:
            status (str): The status of the toast message.
            message (str): The message to display.
            timeout (int): The timeout in milliseconds.
        """
        icons = ["\u2714 Success\n\n", "\u26a0 Warning\n\n", "\u2716 Error\n\n"]
        self.status = next(icon for icon in icons if status.lower() in icon.lower())
        self.message = f"{self.status}{message}"
        self.timeout = timeout
        self.tag = dpg.generate_uuid()
        self.settings = ToastSettings()
        self.show()

    def _position(self) -> tuple[int, int]:
        """Get the position to display the toast.

        Returns:
            tuple[int, int]: The position to display the toast.
        """
        return (
            dpg.get_viewport_width() - self.settings.pos_x_offset,
            self.settings.pos_y,
        )

    def show(self) -> None:
        """Creates and displays the toast window.

        Notes:
        - The toast removal is added to a background thread to run separately.
        """
        with dpg.window(
            label="##toast",
            tag=self.tag,
            no_close=True,
            no_title_bar=True,
            no_resize=True,
            no_move=True,
            no_background=False,
            pos=self._position(),
            width=self.settings.width,
            height=self.settings.height,
        ):
            dpg.add_text(self.message, wrap=self.settings.word_wrap)
            threading.Thread(target=self.remove, daemon=True).start()

    def remove(self) -> None:
        """Removes the toast window after the timeout."""
        time.sleep(self.timeout / 1000)
        if dpg.does_item_exist(self.tag):
            dpg.delete_item(self.tag)


class InputText:
    """A class to create input text.

    Attributes:
    - tag (str): A tag to add to the input text.
    - group_tag (str | None): A tag to add to the input group.
    - kwargs (Any): The keyword arguments to pass to the input text.
    """

    tag: str
    group_tag: str

    def __init__(self, tag: str, group_tag: str | None = None, **kwargs: Any):
        """Initialize the input text.

        Args:
            tag (str): A tag to add to the input text.
            group_tag (str | None): A tag to add to the input group.
            kwargs (Any): The keyword arguments to pass to the input text.
        """
        self.tag = tag
        self.group_tag = group_tag or f"{tag}_group"
        self.kwargs = kwargs

    def get_input(self) -> str:
        """Get the text from the input text.

        Returns:
            str: The text from the input text.
        """
        return dpg.get_value(self.tag)

    def build(self, width: int = -1, padding: int = 0) -> None:
        """Build the input text.

        Args:
            width (int): The width of the input text.
            padding (int): The padding for the top spacer.
        """
        with dpg.group(tag=self.group_tag, horizontal=False):
            dpg.add_spacer(height=padding)
            dpg.add_input_text(tag=self.tag, width=width, **self.kwargs)


class Button:
    """A class to create buttons.

    Attributes:
    - label (str): The label to display on the button.
    - tag (str): A tag to add to the button.
    - on_click (Callable[[Any], None]): The callback to execute when clicked.
    - args (tuple | None): The arguments to pass to the callback.
    """

    label: str
    tag: str
    on_click: Callable
    args: tuple | None

    def __init__(
        self, label: str, tag: str, on_click: Callable, args: tuple | None = None
    ):
        """Initialize the button.

        Args:
            label (str): The label to display on the button.
            tag (str): A tag to add to the button.
            on_click (Callable[[Any], None]): The callback to execute when clicked.
            args (tuple | None): The arguments to pass to the callback.
        """
        self.label = label
        self.tag = tag
        self.on_click = lambda: on_click(*(args or ()))

    def build(self, width: int = -1, height: int = -1, **kwargs: Any) -> None:
        """Build the button.

        Args:
            width (int): The width of the button.
            height (int): The height of the button.
            kwargs (Any): The keyword arguments to pass to the button.
        """
        dpg.add_button(
            label=self.label,
            tag=self.tag,
            width=width,
            height=height,
            callback=self.on_click,
        )


class ButtonRow:
    """A class to create button rows.

    Attributes:
    - tag (str): A tag to add to the button row.
    - buttons (list[Button]): The buttons to add to the button row.
    - weights (list[float] | None): The proportional weights for the buttons.
    """

    tag: str
    buttons: list[Button]
    weights: list[float]

    def __init__(
        self, tag: str, buttons: list[Button], weights: list[float] | None = None
    ):
        """Initialize the button row.

        Args:
            tag (str): A tag to add to the button row.
            buttons (list[Button]): The buttons to add to the button row.
            weights (list[float] | None): The proportional weights for the buttons.
        """
        self.tag = tag
        self.buttons = buttons
        self.weights = weights or [1.0] * len(buttons)

    def build(self, width: int = -1, height: int = -1, **kwargs: Any) -> None:
        """Build the button row.

        Args:
            width (int): The width of the button row.
            height (int): The height of the button row.
            kwargs (Any): The keyword arguments to pass to the button row.
        """
        with dpg.table(
            tag=self.tag,
            header_row=False,
            resizable=True,
            policy=dpg.mvTable_SizingStretchProp,
            width=width,
            height=height,
            **kwargs,
        ):
            for weight in self.weights:
                dpg.add_table_column(init_width_or_weight=weight)

            with dpg.table_row():
                for button in self.buttons:
                    button.build(parent=self.tag)


class Table:
    """A class to create tables.

    Attributes:
    - columns (int): The number of columns to add.
    - weights (list[float] | None): The weights for the columns.
    - tag (str): A tag to add to the table.
    - row_items (list[Callable[[], None]] | None): The items to add to the row.
    """

    columns: int
    weights: list[float]
    tag: int | str
    row_items: list[Callable[[], None]] | None

    def __init__(
        self,
        columns: int = 1,
        weights: list[float] | None = None,
        **kwargs: Any,
    ):
        """Initialize the table.

        Args:
            columns (int): The number of columns to add.
            weights (list[float] | None): The weights for the columns.
            kwargs (Any): The keyword arguments to pass to the table.
        """
        self.columns = columns
        self.weights = weights or [1.0] * columns
        self.tag = dpg.add_table(**kwargs)
        self.row_items: list[Callable[[], None]] | None = None
        self._add_columns()

    def _add_columns(self) -> None:
        """Add columns to the table.

        Args:
            count (int): The number of columns to add.
            weights (list[float] | None): The weights for the columns.
        """
        for i in range(self.columns):
            weight = self.weights[i] if self.weights else 1.0
            dpg.add_table_column(parent=self.tag, init_width_or_weight=weight)

    def row_item(self, func: Callable, *args: Any, **kwargs: Any) -> None:
        """Add a row item to the table.

        Args:
            func (Callable): The function to add to the row.
            args (Any): The arguments to pass to the function.
            kwargs (Any): The keyword arguments to pass to the function.
        """
        if not self.row_items:
            self.row_items = []

        self.row_items.append(lambda: func(*args, **kwargs))

    def add_row(self, height: int = -1) -> None:
        """Add a row to the table.

        Args:
            height (int): The height of the row.
        """
        if not self.row_items:
            return

        with dpg.table_row(parent=self.tag, height=height):
            for item in self.row_items:
                item()

        self.row_items = None


class ResizeHandler:
    """A class to handle resizing of windows.

    Attributes:
    - tag (str): A tag to add to the resize handler.
    """

    tag: str

    def __init__(self, window_tag: str, callback: Callable):
        """Initialize the resize handler.

        Args:
            window_tag (str): A tag to add to the resize handler.
            callback (Callable): The callback to execute when the window is resized.
        """
        self.tag = f"{window_tag}_handler"
        with dpg.item_handler_registry(tag=self.tag):
            dpg.add_item_resize_handler(callback=callback)
        dpg.bind_item_handler_registry(window_tag, self.tag)
