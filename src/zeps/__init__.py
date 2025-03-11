import argparse
import zeps.footage as footage
from typing import Dict, Callable, Union


type MainFn = Callable[[argparse.Namespace], int]


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="zeps", description="Zyxir's everyday Python scripts"
    )
    subparsers = parser.add_subparsers(dest="command", help="Subcommands")

    # 添加 subparsers
    subparsers.add_parser("footage", parents=[footage.create_parser()], add_help=False)
    main_fn_dict: Dict[str, MainFn] = {"footage": footage.main}

    # 運行主程序
    args = parser.parse_args()
    command: Union[str, None] = args.command
    if command is None:
        parser.print_help()
        return 1
    else:
        return main_fn_dict[command](args)
