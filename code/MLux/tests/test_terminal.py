import os
from subprocess import TimeoutExpired
from unittest.mock import Mock, PropertyMock, patch

import pytest

from run.services.terminal import Terminal


class MockProcess(Mock):
    def __init__(self):
        super().__init__()
        self.stdout = Mock(readline=Mock(side_effect=["test", ""]))
        type(self.stdout).closed = PropertyMock(side_effect=[False, True])
        self.stdin = Mock(write=Mock(), flush=Mock())
        self.terminate = Mock()
        self.wait = Mock(side_effect=TimeoutExpired("test", 1.0))
        self.kill = Mock()


def test_init():
    terminal = Terminal(log_length=100)
    tests = os.path.dirname(__file__)
    root = os.path.abspath(os.path.join(tests, ".."))
    path = os.path.join(root, "run", "services")
    assert terminal.path == path
    assert terminal.root == root
    assert terminal.process is None
    assert terminal._running is False
    assert terminal.log_length == 100
    assert terminal.log_history == []


@patch("run.services.terminal.threading")
@patch("run.services.terminal.subprocess.Popen")
def test_run_terminal(popen, threading):
    terminal = Terminal()
    terminal._run_terminal("echo 'test'")
    popen.assert_called_once()
    threading.Thread.assert_called()
    assert terminal._thread is not None
    terminal._thread.start.assert_called_once()


def test_run_terminal_process_exists():
    terminal = Terminal()
    terminal.process = MockProcess()
    terminal._run_terminal("echo 'test'")
    terminal.process.assert_not_called()
    assert terminal._running is False
    assert terminal._thread is None


def test_read_output():
    terminal = Terminal()
    terminal.process = MockProcess()
    terminal.log = Mock()
    terminal._read_output()
    terminal.process.stdout.readline.assert_called()
    assert terminal.process.stdout.readline.call_count == 2
    terminal.log.assert_called_once()
    terminal.process.stdout.close.assert_called_once()


def test_read_output_no_process():
    terminal = Terminal()
    terminal.process = None
    terminal.log = Mock()
    terminal._read_output()
    terminal.log.assert_not_called()


def test_log():
    log_callback_count = []
    terminal = Terminal(log_callback=lambda: log_callback_count.append(1))
    lines = terminal.log_length + 1
    for _ in range(lines):
        terminal.log("test")
    assert len(terminal.log_history) == terminal.log_length
    assert terminal.log_history[-1] == "Pipeline GUI - test"
    assert len(log_callback_count) == lines


def test_clear():
    terminal = Terminal()
    terminal.process = MockProcess()
    terminal.log_history = ["test"]
    terminal.log = Mock()
    terminal.clear()
    assert terminal.log_history == []
    terminal.log.assert_called_once()
    terminal.process.stdin.write.assert_called_once()
    terminal.process.stdin.flush.assert_called_once()


@pytest.mark.parametrize("mode", ["train", "eval"])
def test_run_model(mode):
    terminal = Terminal()
    terminal.model = "mock"
    terminal._run_terminal = Mock()
    terminal.log = Mock()
    terminal.run_model(mode=mode)
    terminal._run_terminal.assert_called_once()
    terminal.log.assert_called_once()


@pytest.mark.parametrize(
    "model, mode, error_message",
    [
        (None, "train", "No model selected"),
        ("mock", "test", "test\nValid modes: train, eval"),
    ],
)
def test_run_model_value_errors(model, mode, error_message):
    terminal = Terminal()
    terminal.model = model
    with pytest.raises(ValueError, match=error_message):
        terminal.run_model(mode=mode)


@patch("run.services.terminal.time.sleep")
def test_watch_process(sleep):
    terminal = Terminal()
    terminal.process = MockProcess()
    terminal.stop = Mock()
    terminal.watch_process()
    sleep.assert_called_once()
    terminal.stop.assert_called_once()


def test_stop():
    terminal = Terminal()
    terminal._running = True
    terminal.process = MockProcess()
    terminal._thread = Mock(is_alive=Mock(), join=Mock())
    terminal.log = Mock()
    terminal.stop()
    assert terminal._running is False
