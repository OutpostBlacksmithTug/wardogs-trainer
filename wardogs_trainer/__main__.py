import argparse
import sys
from pathlib import Path

from wardogs_trainer.bootstrap.runtime import TrainerRuntime
from wardogs_trainer.utils.logger import setup_logger


def main() -> int:
    parser = argparse.ArgumentParser(prog="wardogs-trainer")
    parser.add_argument("--config", type=Path, default=Path("config/default.toml"))
    parser.add_argument("--pid", type=int, default=None, help="attach to explicit PID")
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()

    logger = setup_logger(verbose=args.verbose)
    runtime = TrainerRuntime(config_path=args.config, logger=logger)

    try:
        runtime.attach(pid=args.pid)
        runtime.run()
    except KeyboardInterrupt:
        logger.info("detach requested (ctrl-c)")
        runtime.detach()
        return 0
    except Exception as exc:  # noqa: BLE001
        logger.exception("trainer crashed: %s", exc)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())