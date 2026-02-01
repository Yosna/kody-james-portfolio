"""A module for building file wrappers with ModelExporter.

Includes:
    - package_wrapper: Used by ModelExporter.package() for bundled models.
    - compiler_wrapper: Used by ModelExporter.application() for standalone applications.
"""

import inspect
import pprint
import textwrap
from pathlib import Path
from typing import Any, Callable

import torch.nn as nn

from utils.model_utils import build_vocab, create_mappings


def package_wrapper(
    file: Path,
    pkg_name: str,
    model_name: str,
    model_stub: type[nn.Module],
    load_model: Callable,
) -> None:
    """Build a model wrapper for bundled models with PackageExporter.

    This module provides a wrapper to easily run the bundled model
    after importing the run_model function into the codebase.

    Args:
        file (Path): The path to the file to write the wrapper to.
        pkg_name (str): The name of the package.
        model_name (str): The name of the model.
        model_stub (type[nn.Module]): A class stub for type hints.
        load_model (Callable): A function to load the model.
    """
    with open(file, "w") as f:
        imports = "from pathlib import Path\n\n"
        imports += "import torch\n"
        imports += "import torch.nn as nn\n"
        imports += "from torch.package.package_importer "
        imports += "import PackageImporter\n\n"
        imports += "from torchao import quantize_\n"
        imports += "from torchao.quantization "
        imports += "import Int8DynamicActivationInt8WeightConfig\n\n\n"

        model_stub_source = inspect.getsource(model_stub)
        _model_stub = f"{textwrap.dedent(model_stub_source)}\n\n"
        load_model_source = inspect.getsource(load_model)
        _load_model = f"{textwrap.dedent(load_model_source)}\n\n"
        _load_model = _load_model.replace("pkg_replace", pkg_name)
        _load_model = _load_model.replace("model_replace", model_name)
        _load_model = _load_model.replace("Model.BaseLM", "_Model")
        sources = _model_stub + _load_model

        main = "def main():\n"
        main += "    model = load_model()\n"
        main += "    output = model.generate()\n"
        main += "    print(output)\n\n\n"

        runner = "if __name__ == '__main__':\n    main()\n"

        module = imports + sources + main + runner
        f.write(module)


def compiler_wrapper(
    file: Path,
    root: str,
    model_name: str,
    model_config: dict[str, Any],
    cfg_path: str,
    get_model: Callable,
    load_model: Callable,
) -> None:
    """Build a file entry point for compilation with PyInstaller.

    This module builds a temporary wrapper to use as the central source
    of all model logic required to avoid compiling the entire framework.

    Args:
        file (Path): The path to the file to write the wrapper to.
        root (str): The root path of the project.
        model_name (str): The name of the model.
        model_config (dict[str, Any]): The configuration for the model.
        cfg_path (str): The path to the configuration file.
        get_model (Callable): The function to get the model.
        load_model (Callable): The function to load the model.
    """
    models = {
        "bigram": "BigramLanguageModel",
        "lstm": "LSTMLanguageModel",
        "gru": "GRULanguageModel",
        "transformer": "TransformerLanguageModel",
    }

    with open(file, "w") as f:
        root = f"root = '{root}'\n\n"

        imports = "import logging\nimport sys\n"
        imports += "from typing import Any\n\n"
        imports += "sys.path.insert(0, root)\n\n"
        imports += f"from models.{model_name}_model "
        imports += f"import {models[model_name]}\n"
        imports += "from library import get_dataset\n"
        imports += "from services.application import Application\n\n"

        logger = "logger = logging.getLogger(__name__)\n\n"

        config = f"config = {pprint.pformat(model_config)}\n\n"

        cfg_path = cfg_path.replace("\\", "/")
        cfg_path = f"cfg_path = '{cfg_path}'\n\n"

        _build_vocab = f"{inspect.getsource(build_vocab)}\n\n\n"
        _create_mappings = f"{inspect.getsource(create_mappings)}\n\n\n"
        get_model_source = f"{inspect.getsource(get_model)}\n\n\n"
        get_model_source = textwrap.dedent(get_model_source)
        model_class = models[model_name]
        _get_model = get_model_source.replace("model = ", f"model = {model_class}")
        _get_model = _get_model.replace("tuple", model_class)
        load_model_source = f"{inspect.getsource(load_model)}\n\n"
        load_model_source = textwrap.dedent(load_model_source)
        _load_model = load_model_source.replace("Model.BaseLM", model_class)
        _load_model = _load_model.replace("self, ", "")
        sources = _build_vocab + _create_mappings + _get_model + _load_model

        model = f"model = _load_model('{model_name}', config, cfg_path)\n\n\n"

        runner = "if __name__ == '__main__':\n    Application(model).launch()"

        module = root + imports + logger + config + cfg_path + sources + model + runner
        f.write(module)
