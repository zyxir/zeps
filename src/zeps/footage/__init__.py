"""本子命令批量處理源目錄內的遊戲錄像素材，將處理结果置於目標目錄。功能有三：一
是壓縮所有原始錄像爲碼率更低的格式；二是將各錄像的“亮點”部分提取爲高清錄像方便復
用；三是收集所有 Replay Mod 生成的延時攝影。
"""

import argparse
import logging
from datetime import datetime
from pathlib import Path

from zeps.footage.compress import compress_all
from zeps.footage.copy import copy_all


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Game footage processing")
    parser.add_argument(
        "src", type=str, default=".", nargs="?", help="source directory"
    )
    parser.add_argument(
        "dst",
        type=str,
        default="",
        nargs="?",
        help="destination directory, default: <src>_archive",
    )
    parser.add_argument(
        "--total", type=int, default=0, help="total recordings to compress"
    )
    return parser


def main(args: argparse.Namespace) -> int:
    # 提取命令行參數。
    src: Path = Path(args.src)
    dst: Path = Path(args.dst)
    total: int = args.total

    # 配置日誌：命令行簡單輸出+文件詳細日誌。
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    index = datetime.now().strftime("%Y%m%d%H%M")
    file_handler = logging.FileHandler(f"footage_{index}.txt")
    file_handler.setFormatter(
        logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    )
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    # 執行各項任務，同時接受 Ctrl-C 打斷。
    returncode = compress_all(src, dst, total)
    if returncode != 0:
        return returncode
    returncode = copy_all(src, dst)
    if returncode != 0:
        return returncode
    return 0
