"""複製延時攝影。"""


import logging
import shutil
from pathlib import Path
from typing import List

from zeps.footage.recognition import get_timelapses


def copy(src: Path, dst: Path) -> int:
    """複製一個文件。"""
    shutil.copyfile(src, dst)
    return 0


def copy_all(src: Path, dst: Path) -> int:
    """複製全部延時攝影到目標位置。

    若被打斷，返回 130, 否則返回 0。
    """
    # 獲取所有源和目的文件。
    timelapses: List[Path] = []
    copied: List[Path] = []
    for t in get_timelapses(src):
        c = dst.joinpath(t.name)
        if not c.exists():
            timelapses.append(t)
            copied.append(c)
    logging.info(f"{len(timelapses)} uncopied timelapses found")

    # 複製全部文件。
    for r, c in zip(timelapses, copied):
        try:
            copy(r, c)
            logging.info(f'Finished copying "{str(r)}"')
        except KeyboardInterrupt:
            print("Copying interrupted by Ctrl-C")
            c.unlink(missing_ok=True)
            return 130
    logging.info(f"Copying complete.")
    return 0
