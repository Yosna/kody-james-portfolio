"""A module for exporting models.

Includes:
- ModelExporter: A class for exporting models in multiple formats.
    - architecture: A class to export model architecture modules.
    - package: A class to export trained models with required dependencies.
    - framework: A class to export an editable framework.
    - application: A class to export models as standalone applications.
"""

import json
import shutil
from pathlib import Path
from pickle import UnpicklingError
from typing import Any

import torch
import torch.nn as nn
from PyInstaller.__main__ import run
from torch.package.package_exporter import PackageExporter
from torch.package.package_importer import PackageImporter
from torchao import quantize_
from torchao.quantization import Int8DynamicActivationInt8WeightConfig

from library import get_dataset
from models.registry import ModelRegistry as Model
from services.architecture import Architecture
from services.wrappers import compiler_wrapper, package_wrapper
from utils.io_utils import load_config
from utils.model_utils import build_vocab, create_mappings, get_model


class ModelExporter:
    """A class for exporting models in multiple formats.

    This class provides methods to export models in the following formats:
    - Architecture: A Python module of the model with its currently set hyperparameters.
    - Package: A trained model bundled with its required dependencies.
    - Framework: A trained model zipped as a directory to build a custom framework.
    - Application: A trained model compiled as a standalone application.

    Attributes:
        model_name (str): The name of the model to export.
        cfg_path (str): The path to the configuration file.
        config (dict): The configuration dictionary.
        directory (str): The directory to export the model.
    """

    def __init__(
        self, model_name: str, cfg_path: str = "config.json", directory: str = "exports"
    ) -> None:
        """Initialize the model exporter.

        Args:
            model_name (str): The name of the model to export.
            cfg_path (str): The path to the configuration file.
            directory (str): The directory to export the model.
        """
        self.model_name = model_name
        self.cfg_path = cfg_path
        self.config = load_config(cfg_path)
        self.directory = Path(directory)
        self.formats = {
            "architecture": lambda: self.architecture(),
            "package": lambda: self.package(),
            "framework": lambda: self.package(bundle=False),
            "application": lambda: self.application(),
        }

    def _load_model(
        self, name: str, config: dict[str, Any], cfg_path: str, load_vocab: bool = True
    ) -> Model.BaseLM:
        """Load the model from the configuration.

        Args:
            load_vocab (bool): Whether to load the model with the vocabulary.

        Returns:
            Model.BaseLM: The loaded model to export.
        """
        model_options = config.get("model_options", {})
        token_level = model_options.get("token_level", "char")
        vocab_data = {"vocab_size": 1, "stoi": {"1": 1}, "itos": {1: "1"}}

        if load_vocab:
            datasets = config.get("datasets", {})
            text = get_dataset(datasets["source"], datasets["locations"])
            _, vocab, vocab_size = build_vocab(text, token_level)
            stoi, itos = create_mappings(vocab)
            vocab_data = {"vocab_size": vocab_size, "stoi": stoi, "itos": itos}

        model_config = {**config["models"], "vocab": vocab_data}
        model = get_model(name, model_config, cfg_path)
        return model

    def _load_model_weights(self, model: Model.BaseLM) -> None:
        """Load the weights of the model.

        Args:
            model (BaseLM): The model to load the weights into.

        Raises:
            UnpicklingError: If there is an error loading the model.
        """
        try:
            model.load_state_dict(torch.load(model.ckpt_path))
        except UnpicklingError as e:
            raise UnpicklingError(f"Error loading model: {e}")

    def export(self, format: str) -> tuple[Path, str]:
        """Export the model in the specified format.

        Args:
            format (str): The format to export the model in.
                (architecture, package, framework, application)

        Returns:
            tuple[Path, str]: The directory and name of the exported model.
        """
        export_func = self.formats.get(format.lower(), None)
        if export_func is None:
            raise ValueError(
                f"Unknown export format '{format.capitalize()}'\n"
                "Valid formats: 'architecture', 'package', 'framework', 'application'"
            )
        return export_func()

    def architecture(self) -> tuple[Path, str]:
        """Export the architecture of the model.

        This exports a Python module with the model's currently set hyperparameters
        from the config file along with the basic architecture source code.

        Returns:
            tuple[Path, str]: The directory and name of the architecture.
        """
        arch_dir = self.directory / "architecture" / self.model_name
        arch_dir.mkdir(parents=True, exist_ok=True)

        architecture = str(Architecture(self.model_name))
        model_config = self.config.get("models", {}).get(self.model_name, {})
        hparams = model_config.get("hparams", {})

        arch_name = f"{self.model_name}_architecture.py"
        file = arch_dir / arch_name
        with open(file, "w") as f:
            import_dataclasses = "from dataclasses import dataclass\n\n"
            import_torch = "import torch\nimport torch.nn as nn\n\n"
            imports = import_dataclasses + import_torch

            config = f"config = {json.dumps(hparams, indent=4)}\n\n\n"

            dataclass_body = "\n".join(
                [f"    {key}: {type(value).__name__}" for key, value in hparams.items()]
            )
            dataclass = f"@dataclass\nclass HParams:\n{dataclass_body}\n\n\n"

            module = imports + config + dataclass + architecture
            f.write(module)

        return arch_dir, arch_name

    def package(self, bundle: bool = True) -> tuple[Path, str]:
        """Export the trained model with required dependencies.

        The model can be bundled as a package if simple access is desired,
        or zipped as a directory to build a custom framework around.

        Args:
            bundle (bool): Whether to bundle the model as a package.

        Returns:
            tuple[Path, str]: The directory and name of the packaged or zipped model.
        """
        model = self._load_model(self.model_name, self.config, self.cfg_path)
        self._load_model_weights(model)
        model.eval()
        model.cpu()
        model.device = torch.device("cpu")

        sub_dir = "packages" if bundle else "frameworks"
        pkg_dir = self.directory / sub_dir / self.model_name
        pkg_dir.mkdir(parents=True, exist_ok=True)

        pkg_ext = "pkg" if bundle else "zip"
        pkg_name = f"{self.model_name}_package.{pkg_ext}"
        pkg_path = pkg_dir / pkg_name

        with PackageExporter(pkg_path) as pkg:
            pkg.intern(f"{Model.BaseLM.__module__}.**")
            pkg.intern(f"{model.__module__}.**")
            pkg.intern("models.components.generators.**")
            pkg.intern("utils.io_utils.**")
            pkg.intern("utils.data_utils.**")
            pkg.save_pickle(self.model_name, "model.pkl", model)

        if bundle:
            self._build_package_wrapper(pkg_dir, pkg_name)

        return pkg_dir, pkg_name

    def _build_package_wrapper(self, pkg_dir: Path, pkg_name: str) -> None:
        """Build a wrapper for the model to run it from the package.

        Args:
            pkg_dir (Path): The directory of the package.
            pkg_name (str): The name of the package.
        """

        class _Model(nn.Module):
            device: torch.device

            def to(self, _: torch.device): ...
            def generate(self, *_): ...

        def load_model(
            path: Path | None = None, pkg: str | None = None, quantize: bool = False
        ) -> _Model:
            path = path or Path(__file__).parent
            pkg = pkg or "pkg_replace"
            pkg_path = path / pkg

            importer = PackageImporter(pkg_path)
            model: _Model = importer.load_pickle("model_replace", "model.pkl")

            if quantize:
                quantize_config = Int8DynamicActivationInt8WeightConfig()
                quantize_(model, quantize_config)
            else:
                has_cuda = torch.cuda.is_available()
                model.device = torch.device("cuda") if has_cuda else torch.device("cpu")
                model.to(model.device)

            return model

        file = pkg_dir / "model.py"
        package_wrapper(file, pkg_name, self.model_name, _Model, load_model)

    def application(self) -> tuple[Path, str]:
        """Export the model as a standalone application.

        Returns:
            tuple[Path, str]: The directory and name of the compiled application.
        """
        model = self._load_model(self.model_name, self.config, self.cfg_path)
        self._load_model_weights(model)

        app_name = f"{model.name}_{model.metadata['generator']}_generation"
        app_dir = self.directory / "applications" / self.model_name
        app_dir.mkdir(parents=True, exist_ok=True)

        self._build_compiler_wrapper(app_dir, app_name)

        return app_dir, app_name

    def _build_compiler_wrapper(self, app_dir: Path, app_name: str) -> None:
        """Build a wrapper for the model to compile it into a standalone application.

        The file built for PyInstaller to use is deleted after compilation.

        Args:
            app_dir (Path): The directory to export the application.
            app_name (str): The name of the application.
        """

        def get_model(_model: str, config: dict[str, Any], cfg_path: str) -> tuple:
            model_config = {**config[_model], "vocab": config["vocab"]}
            model = (model_config, cfg_path)
            model.to(model.device)  # type: ignore
            return model

        root = Path(__file__).resolve().parents[1]
        root_path = str(root).replace("\\", "/")
        file = app_dir / "app_compiler_wrapper.py"

        compiler_wrapper(
            file,
            root_path,
            self.model_name,
            self.config,
            self.cfg_path,
            get_model,
            self._load_model,
        )

        settings = ["--clean", "--onefile", "--noconfirm", "--noconsole"]

        name = ["--name", app_name]

        distpath = ["--distpath", str(app_dir)]
        workpath = ["--workpath", str(app_dir)]
        specpath = ["--specpath", str(app_dir)]
        paths = [*distpath, *workpath, *specpath]

        font_src = root / "run" / "assets" / "fonts" / "DejaVuSans.ttf"
        font_dest = "run/assets/fonts"
        font_data = ["--add-data", f"{font_src};{font_dest}"]

        run([str(file), *settings, *name, *paths, *font_data])

        build = app_dir / app_name
        spec = app_dir / f"{app_name}.spec"

        shutil.rmtree(build)
        spec.unlink()
        file.unlink()
