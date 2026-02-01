import inspect
import pprint
import textwrap
from pathlib import Path
from typing import Any

import pytest
import torch
import torch.nn as nn
from torch.package.package_importer import PackageImporter
from torchao import quantize_
from torchao.quantization import Int8DynamicActivationInt8WeightConfig

from services.exporter import ModelExporter
from services.wrappers import compiler_wrapper, package_wrapper
from utils.model_utils import build_vocab, create_mappings


class _ModelClone(nn.Module):
    device: torch.device

    def to(self, _: torch.device): ...
    def generate(self, *_): ...


def load_model_clone(path: Path, pkg: str, quantize: bool = False) -> str:
    path = path or Path(__file__).parent
    pkg = pkg or "pkg_replace"
    pkg_path = path / pkg

    importer = PackageImporter(pkg_path)
    model = importer.load_pickle("model_replace", "model.pkl")

    if quantize:
        quantize_config = Int8DynamicActivationInt8WeightConfig()
        quantize_(model, quantize_config)
    else:
        has_cuda = torch.cuda.is_available()
        model.device = torch.device("cuda") if has_cuda else torch.device("cpu")
        model.to(model.device)

    return model


def get_model_clone(_model: str, config: dict[str, Any], cfg_path: str) -> tuple:
    model_config = {**config[_model], "vocab": config["vocab"]}
    model = (model_config, cfg_path)
    model.to(model.device)  # type: ignore
    return model


@pytest.mark.parametrize("model", ["bigram", "lstm", "gru", "transformer"])
def test_package_wrapper(tmp_path, model):
    pkg_name = f"{model}_package.pkg"
    pkg_dir = tmp_path / "exports" / "packages" / model
    pkg_dir.mkdir(parents=True, exist_ok=True)
    file = pkg_dir / "model.py"

    imports = "from pathlib import Path\n\n"
    imports += "import torch\n"
    imports += "import torch.nn as nn\n"
    imports += "from torch.package.package_importer "
    imports += "import PackageImporter\n\n"
    imports += "from torchao import quantize_\n"
    imports += "from torchao.quantization "
    imports += "import Int8DynamicActivationInt8WeightConfig\n\n\n"
    _model_stub = "class _ModelClone(nn.Module):\n    device: torch.device\n\n"
    _model_stub += "    def to(self, _: torch.device): ...\n"
    _model_stub += "    def generate(self, *_): ...\n\n\n"
    load_model_source = inspect.getsource(load_model_clone)
    _load_model = f"{textwrap.dedent(load_model_source)}\n\n"
    _load_model = _load_model.replace("pkg_replace", pkg_name)
    _load_model = _load_model.replace("model_replace", model)
    sources = _model_stub + _load_model
    main = "def main():\n"
    main += "    model = load_model()\n"
    main += "    output = model.generate()\n"
    main += "    print(output)\n\n\n"
    runner = "if __name__ == '__main__':\n    main()\n"
    module = imports + sources + main + runner

    package_wrapper(file, pkg_name, model, _ModelClone, load_model_clone)

    assert file.exists()
    with open(file) as f:
        content = f.read()
        assert content == module


@pytest.mark.parametrize(
    "model_name, model_cls",
    [
        ("bigram", "BigramLanguageModel"),
        ("lstm", "LSTMLanguageModel"),
        ("gru", "GRULanguageModel"),
        ("transformer", "TransformerLanguageModel"),
    ],
)
def test_compiler_wrapper(tmp_path, model_name, model_cls):
    path = str(Path(__file__).resolve().parents[1]).replace("\\", "/")
    app_dir = tmp_path / "exports" / "applications" / model_name
    app_dir.mkdir(parents=True, exist_ok=True)
    file = app_dir / "app_compiler_wrapper.py"

    root = f"root = '{path}'\n\n"
    imports = "import logging\nimport sys\n"
    imports += "from typing import Any\n\n"
    imports += "sys.path.insert(0, root)\n\n"
    imports += f"from models.{model_name}_model import {model_cls}\n"
    imports += "from library import get_dataset\n"
    imports += "from services.application import Application\n\n"
    logger = "logger = logging.getLogger(__name__)\n\n"
    config = {"test": "test"}
    _config = f"config = {pprint.pformat(config)}\n\n"
    cfg_path = str(tmp_path / "config.json").replace("\\", "/")
    _cfg_path = f"cfg_path = '{cfg_path}'\n\n"
    _build_vocab = f"{inspect.getsource(build_vocab)}\n\n\n"
    _create_mappings = f"{inspect.getsource(create_mappings)}\n\n\n"
    get_model_source = f"{inspect.getsource(get_model_clone)}\n\n\n"
    get_model_source = textwrap.dedent(get_model_source)
    _get_model = get_model_source.replace("model = ", f"model = {model_cls}")
    _get_model = _get_model.replace("tuple", model_cls)
    load_model_source = f"{inspect.getsource(ModelExporter._load_model)}\n\n"
    load_model_source = textwrap.dedent(load_model_source)
    _load_model = load_model_source.replace("Model.BaseLM", model_cls)
    _load_model = _load_model.replace("self, ", "")
    sources = _build_vocab + _create_mappings + _get_model + _load_model
    model = f"model = _load_model('{model_name}', config, cfg_path)\n\n\n"
    runner = "if __name__ == '__main__':\n    Application(model).launch()"
    module = root + imports + logger + _config + _cfg_path + sources + model + runner

    _get_model = get_model_clone
    _load_model = ModelExporter._load_model

    compiler_wrapper(file, path, model_name, config, cfg_path, _get_model, _load_model)

    assert file.exists()
    with open(file) as f:
        content = f.read()
        assert content == module
