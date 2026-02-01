"""A terminal helper module.

Includes:
- Terminal: A class to interact with a hidden terminal.
"""

import os
import shlex
import subprocess
import sys
import threading
import time
from typing import Callable


class Terminal:
    """A class to interact with a hidden terminal."""

    def __init__(self, log_length: int = 250, log_callback: Callable | None = None):
        """Initialize the terminal.

        Args:
            log_length (int): The max line length for the log output.
            log_callback (Callable | None): A callback to call when the log is updated.
        """
        self.path = os.path.dirname(__file__)
        self.root = os.path.abspath(os.path.join(self.path, "..", ".."))
        self.process = None
        self._running = False
        self._thread = None
        self.model = ""
        self._mode = ""
        self.log_length = log_length
        self.log_history = []
        self.log_callback = log_callback

    def _run_terminal(self, cmd: str) -> None:
        """Run the terminal.

        Args:
            cmd (str): The command to run.
        """
        if self.process:
            return

        self.process = subprocess.Popen(
            [sys.executable, "-u", *shlex.split(cmd)],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            cwd=self.root,
            creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0,
        )
        self._running = True
        self._thread = threading.Thread(target=self._read_output, daemon=True)
        self._thread.start()

    def _read_output(self) -> None:
        """Read the output from the terminal."""
        if not self.process or not self.process.stdout:
            return

        output = self.process.stdout
        lines = iter(output.readline, "")

        for line in lines:
            self.log(line, stdout=True)

        if output:
            output.close()

    def log(self, line: str, stdout: bool = False) -> None:
        """Update the log.

        Args:
            line (str): The line to log.
            stdout (bool): Whether the line is from stdout.
        """
        prefix = "Pipeline GUI - " if not stdout else ""
        self.log_history.append(f"{prefix}{line.rstrip()}")

        if len(self.log_history) > self.log_length:
            self.log_history.pop(0)

        if self.log_callback:
            self.log_callback()

    def clear(self) -> None:
        """Clear the log."""
        self.log_history = []
        self.log("", stdout=True)

        if self.process and self.process.stdin:
            self.process.stdin.write("clear")
            self.process.stdin.flush()

    def run_model(self, mode: str) -> None:
        """Run the selected model mode.

        Args:
            mode (str): The mode to run.

        Raises:
            ValueError: If no model is selected.
            ValueError: If an invalid mode is provided.
        """
        if not self.model:
            raise ValueError("No model selected")

        match mode:
            case "train":
                log_msg = f"Training {self.model} model..."
            case "eval":
                log_msg = f"Generating sample from {self.model} model..."
            case _:
                raise ValueError(f"{mode}\nValid modes: train, eval")

        self._mode = mode
        cmd = f"main.py --model {self.model} --training {mode == 'train'}"
        self._run_terminal(cmd=cmd)
        self.log(log_msg)

    def watch_process(self) -> None:
        """Watch the model process until stdout closes."""
        while self.process:
            output = self.process.stdout
            if output and output.closed:
                break
            time.sleep(0.1)
        self.stop()

    def stop(self) -> None:
        """Stop the model process."""
        self._running = False
        if self.process:
            mode = "training" if self._mode == "train" else "evaluation"
            self.log(f"Model {mode} finished")
            self.process.terminate()

            try:
                self.process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.process.kill()

        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=1)

        self.process = None
        self._mode = ""
