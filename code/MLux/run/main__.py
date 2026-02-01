"""Entry point for running tools in the run package.

This module allows you to run available tools using `python -m run <tool>`.

Tools:
    - pipeline: End-to-end pipeline
    - config: Configuration editor
    - dashboard: Optuna dashboard
    - profiler: cProfile profiler

Examples:
    python -m run pipeline
    python -m run config
    python -m run dashboard
    python -m run profiler
"""

import argparse
import sys

from . import config, dashboard, pipeline, profiler


def get_tool() -> str:
    """Parse and return the tool name from command-line arguments.

    Returns:
        str: The name of the tool to run.
    """
    tools = ["pipeline", "config", "dashboard", "profiler"]
    parser = argparse.ArgumentParser()
    parser.add_argument("tool", type=str, choices=tools)
    args = parser.parse_args()
    return args.tool


def run_tool(tool: str) -> None:
    """Run the selected tool based on the provided tool name.

    Args:
        tool (str): The name of the tool to run.

    Raises:
        ValueError: If an invalid tool name is provided.
    """
    sys.argv = [sys.argv[0][:-3]]
    match tool:
        case "pipeline":
            pipeline.run_pipeline()
        case "config":
            config.run_config()
        case "dashboard":
            dashboard.run_dashboard()
        case "profiler":
            profiler.run_profiler()
        case _:
            raise ValueError(f"Invalid tool: {tool}")


if __name__ == "__main__":
    run_tool(get_tool())
