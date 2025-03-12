"""原始錄像壓縮。"""

from typing import List
from pathlib import Path
import subprocess
import logging

from zeps.footage.recognition import get_recordings


def compress(src: Path, dst: Path) -> int:
    """壓縮單個錄像。"""
    cmd = [
        "ffmpeg",
        # 只打印 warning 以上信息
        "-loglevel",
        "warning",
        # 使用 CUDA 硬件加速
        "-hwaccel",
        "cuda",
        # 輸入視頻
        "-i",
        str(src),
        # 使用 NEVC/h265 硬件編碼，文件體積更小
        "-codec:v",
        "hevc_nvenc",
        # 更慢的 preset 產生更小的文件（默認爲 medium）
        "-preset",
        "slow",
        # 1080p 分辨率
        "-s",
        "1920x1080",
        # 帧率 30 以減小文件體積（錄像和成品皆爲 60）
        "-filter:v",
        "fps=30",
        # 輸出視頻
        str(dst),
    ]
    result = subprocess.run(cmd, shell=False, text=True, capture_output=True)
    if result.stdout is not None:
        for line in result.stdout.splitlines():
            logging.debug(line)
    return result.returncode


def compress_all(src: Path, dst: Path, total: int = 0) -> int:
    """將源目錄的所有錄像壓縮到目標目錄，並記錄日誌到 `logfile`。

    一次最多壓縮 `total` 個錄像；若 `total` 爲 0 則無限制。

    若被打斷，返回 130, 否則返回 0。
    """
    # 獲取所有源和目的文件
    recordings: List[Path] = []
    compressed: List[Path] = []
    for r in get_recordings(src):
        c = dst.joinpath(r.name)
        if not c.exists():
            recordings.append(r)
            compressed.append(c)
    logging.info(f"{len(recordings)} uncompressed recordings found")

    # 進行最多 total 次壓縮
    total = len(recordings) if total == 0 else total
    count = 0
    while count < total and len(recordings) > 0:
        r, c = recordings.pop(), compressed.pop()
        if c.exists():
            continue
        logging.info(f'Start compressing "{str(r)}" ({count+1}/{total})')
        try:
            compress(r, c)
            logging.info(f'Finished compressing "{str(r)}"')
        except KeyboardInterrupt:
            print("Compressing interrupted by Ctrl-C")
            c.unlink(missing_ok=True)
            return 130
    logging.info(f"Compressing complete.")
    return 0
