import argparse
import zeps.footage as footage
from typing import Dict, Callable


def main():
    parser = argparse.ArgumentParser(description="Zyxir's everyday Python scripts")
    subparsers = parser.add_subparsers(dest="command", help="Subcommands")

    # 添加 subparsers
    subparsers.add_parser("footage", parents=[footage.create_parser()], add_help=False)
    main_dict: Dict[str, (argparse.Namespace) -> int] = {
        "footage": footage.main
    }

    # 運行主程序
    args = parser.parse_args()
