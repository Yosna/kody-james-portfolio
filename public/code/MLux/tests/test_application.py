import json
from unittest.mock import Mock, patch

import pytest

from models.registry import ModelRegistry as Model
from services.application import Application, ApplicationUI


class MockModel(Model.BaseLM):
    batch_size: int
    block_size: int
    lr: float

    def __init__(self, tmp_path, model, config):
        model_name_lower = model.lower()
        model_config = {**config["models"][model]}
        model_config["vocab"] = {"vocab_size": 1, "stoi": {"1": 1}, "itos": {1: "1"}}
        super().__init__(model_name_lower, model_config, tmp_path / "config.json")
        self.ckpt_path = (
            tmp_path / "checkpoints" / model / "checkpoint_1" / "checkpoint.pt"
        )


def get_test_config(model, tmp_path):
    return {
        "datasets": {
            "source": "local",
            "locations": {
                "local": {
                    "directory": build_test_dataset(tmp_path),
                    "extension": "txt",
                },
            },
        },
        "generator_options": {
            "generator": "random",
            "context_length": 32,
            "sampler": "multinomial",
            "temperature": 1.0,
        },
        "model_options": {
            "save_model": False,
            "token_level": "char",
            "patience": 10,
            "max_checkpoints": 1,
        },
        "models": {
            model: get_model_config(model),
        },
    }


def get_model_config(model):
    return {
        "runtime": get_test_runtime(),
        "hparams": get_test_hparams(model),
    }


def get_test_runtime():
    return {
        "training": True,
        "steps": 10000,
        "interval": 100,
        "max_new_tokens": 128,
    }


def get_test_hparams(model):
    hparams = {"batch_size": 16, "block_size": 32, "lr": 0.001}
    if model != "bigram":
        hparams.update({"embedding_dim": 8, "num_layers": 2})
    if model == "lstm" or model == "gru":
        hparams.update({"hidden_size": 16})
    if model == "transformer":
        hparams.update({"max_seq_len": 32, "num_heads": 2, "ff_dim": 32})
    return hparams


def build_test_dataset(tmp_path):
    dataset_dir = tmp_path / "dataset"
    dataset_dir.mkdir(exist_ok=True)
    for i in range(100):
        content = "".join([str(i) for i in range(100)])
        build_file(dataset_dir, f"input_{i}.txt", content)
    return str(dataset_dir)


def build_file(tmp_path, file_name, content):
    file = tmp_path / file_name
    file.parent.mkdir(parents=True, exist_ok=True)
    file.write_text(content)
    return file


def app_setup(tmp_path, model_name):
    config = get_test_config(model_name, tmp_path)
    build_file(tmp_path, "config.json", json.dumps(config))
    model = MockModel(tmp_path, model_name, config)
    return model


def test_application_ui():
    ui = ApplicationUI()
    assert ui.width == 1200
    assert ui.height == 900
    assert ui.width_padding == 16
    assert ui.height_padding == 20
    assert ui.title_height == 40
    assert ui.window_width == 1184
    assert ui.window_height == 860
    assert ui.child_width == 1168
    assert ui.control_height == 60
    assert ui.output_height == 780
    assert ui.output_wrap == 1152
    assert ui.log_limit == 250


@pytest.mark.parametrize("model_name", ["Bigram", "LSTM", "GRU", "Transformer"])
def test_application_init(tmp_path, model_name):
    model = app_setup(tmp_path, model_name)
    app = Application(model)
    assert app.model == model
    assert app.name == model_name
    assert app.generator == "Random"
    assert app.title == f"{model_name} Random Generation Interface"
    assert app.tag == f"{model_name.lower()}_random_generation_interface"
    assert app.log == []
    assert app.log_limit == 0
    assert callable(app.launch)


@patch("services.application.init_gui")
@patch("services.application.Fonts")
@patch("services.application.dpg")
def test_application_compile(dpg, fonts, init_gui, tmp_path):
    app = Application(app_setup(tmp_path, "Bigram"))
    app._model_metadata = Mock()
    app._output_window = Mock()
    app._control_panel = Mock()

    app._compile()

    dpg.create_context.assert_called_once()
    dpg.window.assert_called_once()
    dpg.set_primary_window.assert_called_once()
    fonts.assert_called_once()
    app._model_metadata.assert_called_once()
    app._output_window.assert_called_once()
    app._control_panel.assert_called_once()
    init_gui.assert_called_once()


@patch("services.application.dpg")
def test_application_output_window(dpg, tmp_path):
    app = Application(app_setup(tmp_path, "Bigram"))
    app._output_window(ApplicationUI())
    dpg.child_window.assert_called_once()
    dpg.add_text.assert_called_once()


@patch("services.application.dpg")
@pytest.mark.parametrize("generator", ["Random", "Prompt"])
def test_application_control_panel(dpg, tmp_path, generator):
    app = Application(app_setup(tmp_path, "Bigram"))
    app.generator = generator
    app._random_control_panel = Mock()
    app._prompt_control_panel = Mock()
    random_call_count = 1 if generator == "Random" else 0
    prompt_call_count = 1 if generator == "Prompt" else 0

    app._control_panel(ApplicationUI())

    dpg.child_window.assert_called_once()
    assert app._random_control_panel.call_count == random_call_count
    assert app._prompt_control_panel.call_count == prompt_call_count


@patch("services.application.ButtonRow")
@patch("services.application.Button")
def test_application_random_control_panel(button, button_row, tmp_path):
    app = Application(app_setup(tmp_path, "Bigram"))
    app._random_control_panel()
    assert button.call_count == 2
    button_row.assert_called_once()
    button_row.return_value.build.assert_called_once()


@patch("services.application.InputText")
@patch("services.application.Table")
@patch("services.application.Button")
def test_application_prompt_control_panel(button, table, input_text, tmp_path):
    app = Application(app_setup(tmp_path, "Bigram"))
    app.generator = "Prompt"
    app._prompt_control_panel()
    table.assert_called_once()
    input_text.assert_called_once()
    assert table.return_value.row_item.call_count == 3
    assert button.call_count == 2


@patch("services.application.Table")
@patch("services.application.dpg")
def test_application_model_metadata(dpg, table, tmp_path):
    app = Application(app_setup(tmp_path, "Bigram"))
    app._pos_center = Mock()
    app._model_metadata(ApplicationUI())
    dpg.window.assert_called_once()
    table.assert_called_once()
    assert table.return_value.row_item.call_count == len(app.model.metadata) * 2
    assert table.return_value.add_row.call_count == len(app.model.metadata)
    app._pos_center.assert_called_once()


@patch("services.application.dpg")
def test_application_generate(dpg, tmp_path):
    app = Application(app_setup(tmp_path, "Bigram"))
    app.log_limit = 99
    app.model.generate = Mock(return_value="test")
    for _ in range(app.log_limit + 1):
        app._generate()
    assert len(app.log) == app.log_limit
    assert dpg.set_value.call_count == 100
    assert dpg.set_y_scroll.call_count == 100


@patch("services.application.dpg")
def test_toggle_window(dpg, tmp_path):
    app = Application(app_setup(tmp_path, "Bigram"))
    app._toggle_window("test")
    dpg.does_item_exist.assert_called_once()
    dpg.is_item_visible.assert_called_once()
    dpg.configure_item.assert_called_once()


@patch("services.application.dpg")
def test_pos_center(dpg, tmp_path):
    app = Application(app_setup(tmp_path, "Bigram"))
    dpg.get_item_rect_size.return_value = (100, 100)
    app._pos_center(ApplicationUI(), "test", "parent")
    assert dpg.configure_item.call_count == 2
    assert dpg.get_item_rect_size.call_count == 2


@patch("services.application.dpg")
def test_pos_center_frame_callback(dpg, tmp_path):
    app = Application(app_setup(tmp_path, "Bigram"))
    dpg.get_item_rect_size.return_value = (0, 0)
    app._pos_center(ApplicationUI(), "test", "parent")
    dpg.configure_item.assert_called_once()
    dpg.get_item_rect_size.assert_called_once()
    dpg.get_frame_count.assert_called_once()
    dpg.set_frame_callback.assert_called_once()
