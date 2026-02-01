import inspect
import json
from pathlib import Path
from pickle import UnpicklingError
from unittest.mock import Mock, patch

import pytest

from models.registry import ModelRegistry as Model
from services.architecture import Architecture
from services.exporter import ModelExporter


class MockModel(Model.BaseLM):
    def __init__(self, tmp_path, model):
        config = get_test_config(model)
        config["vocab"] = {"vocab_size": 1, "stoi": {"1": 1}, "itos": {1: "1"}}
        super().__init__(model, config, tmp_path / "config.json")
        self.ckpt_path = (
            tmp_path / "checkpoints" / model / "checkpoint_1" / "checkpoint.pt"
        )

    def load_state_dict(self, *_, **__):
        return None

    def eval(self):
        return self

    def cpu(self):
        return self


def exporter_test_setup(tmp_path, model):
    config = get_test_config(model)
    path = build_file(tmp_path, "config.json", json.dumps(config))
    export_dir = str(tmp_path / "exports")
    exporter = ModelExporter(model, cfg_path=path, directory=export_dir)
    return exporter


def build_file(tmp_path, file_name, content):
    file = tmp_path / file_name
    file.parent.mkdir(parents=True, exist_ok=True)
    file.write_text(content)
    return file


def get_test_config(model):
    return {
        "datasets": {
            "source": "huggingface",
            "locations": {
                "huggingface": {
                    "data_name": "Yosna/test-dataset",
                    "config_name": None,
                    "split": "train",
                    "field": "text",
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


def mock_exporter_model_loading(tmp_path, model, torch_load, load_model):
    ckpt_path = f"checkpoints/{model}/checkpoint_1/checkpoint.pt"
    build_file(tmp_path, ckpt_path, "test")
    torch_load.return_value = {}
    exporter = exporter_test_setup(tmp_path, model)
    mock_model = MockModel(tmp_path, model)
    load_model.return_value = mock_model
    return exporter


@pytest.mark.parametrize("model", ["bigram", "lstm", "gru", "transformer"])
def test_model_exporter_init(tmp_path, model):
    config = get_test_config(model)

    exporter = exporter_test_setup(tmp_path, model)

    assert exporter.model_name == model
    assert exporter.cfg_path == tmp_path / "config.json"
    assert exporter.config == config
    assert exporter.directory == tmp_path / "exports"


@pytest.mark.parametrize("model", ["bigram", "lstm", "gru", "transformer"])
def test_model_exporter_load_model(tmp_path, model):
    exporter = exporter_test_setup(tmp_path, model)
    path = tmp_path / "config.json"

    model = exporter._load_model(model, exporter.config, path)

    vocab = sorted(set(list("Hello, World!")))
    hparams = exporter.config["models"][model.name]["hparams"]
    assert model.vocab_size == len(vocab)
    assert model.stoi == {char: i for i, char in enumerate(vocab)}
    assert model.itos == {i: char for i, char in enumerate(vocab)}
    for key, value in hparams.items():
        assert getattr(model, key) == value


def test_load_model_no_vocab(tmp_path):
    exporter = exporter_test_setup(tmp_path, "bigram")
    path = tmp_path / "config.json"

    model = exporter._load_model("bigram", exporter.config, path, load_vocab=False)

    assert model.vocab_size == 1
    assert model.stoi == {"1": 1}
    assert model.itos == {1: "1"}


@pytest.mark.parametrize(
    "format", ["architecture", "package", "framework", "application"]
)
def test_model_exporter_export(tmp_path, format):
    exporter = exporter_test_setup(tmp_path, "bigram")
    exporter.application = Mock(return_value=("", ""))
    exporter.package = Mock(return_value=("", ""))
    exporter.architecture = Mock(return_value=("", ""))
    architecture_call_count = 1 if format == "architecture" else 0
    package_call_count = 1 if format == "package" or format == "framework" else 0
    application_call_count = 1 if format == "application" else 0

    exporter.export(format)

    assert architecture_call_count == exporter.architecture.call_count
    assert package_call_count == exporter.package.call_count
    assert application_call_count == exporter.application.call_count


def test_model_exporter_export_invalid_format(tmp_path):
    exporter = exporter_test_setup(tmp_path, "bigram")
    with pytest.raises(ValueError):
        exporter.export("invalid")


@pytest.mark.parametrize("model", ["bigram", "lstm", "gru", "transformer"])
def test_model_exporter_architecture(tmp_path, model):
    exporter = exporter_test_setup(tmp_path, model)

    hparams = exporter.config["models"][model]["hparams"]
    import_dataclasses = "from dataclasses import dataclass\n\n"
    import_torch = "import torch\nimport torch.nn as nn\n\n"
    imports = import_dataclasses + import_torch
    config = f"config = {json.dumps(hparams, indent=4)}\n\n\n"
    dataclass_body = "\n".join(
        [f"    {key}: {type(value).__name__}" for key, value in hparams.items()]
    )
    dataclass = f"@dataclass\nclass HParams:\n{dataclass_body}\n\n\n"
    architecture = str(Architecture(model))
    module = imports + config + dataclass + architecture

    arch_dir, arch_name = exporter.architecture()

    assert arch_name == f"{model}_architecture.py"
    assert arch_dir == tmp_path / "exports" / "architecture" / model
    assert Path(arch_dir, arch_name).exists()
    with open(Path(arch_dir, arch_name)) as f:
        content = f.read()
        assert content == module


@patch("services.exporter.PackageExporter.save_pickle")
@patch("services.exporter.PackageExporter.intern")
@patch("services.exporter.torch.load")
@patch("services.exporter.ModelExporter._load_model")
@pytest.mark.parametrize("model", ["bigram", "lstm", "gru", "transformer"])
def test_model_exporter_package(
    load_model, torch_load, pkg_intern, pkg_pickle, model, tmp_path
):
    exporter = mock_exporter_model_loading(tmp_path, model, torch_load, load_model)

    pkg_dir, pkg_name = exporter.package()

    assert pkg_name == f"{model}_package.pkg"
    assert pkg_dir == tmp_path / "exports" / "packages" / model
    assert Path(pkg_dir, pkg_name).exists()
    assert pkg_intern.call_count == 5
    pkg_pickle.assert_called_once()


@patch("services.exporter.ModelExporter._load_model")
def test_package_export_unpickling_error(load_model, tmp_path):
    exporter = exporter_test_setup(tmp_path, "bigram")
    ckpt_path = f"checkpoints/bigram/checkpoint_1/checkpoint.pt"
    build_file(tmp_path, ckpt_path, "invalid")
    load_model.return_value = MockModel(tmp_path, "bigram")
    with pytest.raises(UnpicklingError):
        exporter.package()


@patch("services.exporter.ModelExporter._build_compiler_wrapper")
@patch("services.exporter.torch.load")
@patch("services.exporter.ModelExporter._load_model")
@pytest.mark.parametrize("model", ["bigram", "lstm", "gru", "transformer"])
def test_model_exporter_application(load_model, torch_load, wrapper, model, tmp_path):
    exporter = mock_exporter_model_loading(tmp_path, model, torch_load, load_model)

    app_dir, app_name = exporter.application()

    assert app_name == f"{model}_random_generation"
    assert app_dir == tmp_path / "exports" / "applications" / model
    wrapper.assert_called_once()


@patch("services.exporter.run")
@patch("services.exporter.compiler_wrapper")
@pytest.mark.parametrize("model", ["bigram", "lstm", "gru", "transformer"])
def test_build_compiler_wrapper(compiler_wrapper, run, model, tmp_path):
    exporter = exporter_test_setup(tmp_path, model)
    app_dir = tmp_path / "exports" / "applications" / model
    app_dir.mkdir(parents=True, exist_ok=True)
    app_name = f"{model}_random_generation"
    build_dir = app_dir / app_name
    build_dir.mkdir(parents=True, exist_ok=True)
    spec_file = app_dir / f"{app_name}.spec"
    spec_file.touch()
    wrapper_file = app_dir / "app_compiler_wrapper.py"
    wrapper_file.touch()

    exporter._build_compiler_wrapper(app_dir, app_name)

    compiler_wrapper.assert_called_once()
    run.assert_called_once()
    assert not build_dir.exists()
    assert not spec_file.exists()
    assert not wrapper_file.exists()
