"""Command-line interface for running the Climetrix workflow."""
from __future__ import annotations

import argparse
import json
import logging
from pathlib import Path
from typing import Any, Dict

from .config import WorkflowConfig
from .workflow import run_pipeline

LOGGER = logging.getLogger(__name__)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("config", type=Path, help="Path to workflow configuration JSON file")
    parser.add_argument(
        "--log-level",
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        help="Logging verbosity",
    )
    return parser.parse_args(argv)


def load_config(path: Path) -> WorkflowConfig:
    with path.open() as fp:
        payload: Dict[str, Any] = json.load(fp)
    return WorkflowConfig.from_dict(payload)


def main(argv: list[str] | None = None) -> None:
    args = parse_args(argv)
    logging.basicConfig(level=getattr(logging, args.log_level))
    LOGGER.info("Loading configuration from %s", args.config)
    config = load_config(args.config)
    outputs = run_pipeline(config)
    LOGGER.info("Pipeline produced outputs: %s", list(outputs))


if __name__ == "__main__":
    main()
