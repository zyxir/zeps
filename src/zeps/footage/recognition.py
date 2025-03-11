"""素材文件識别與分類。"""

import re
from pathlib import Path

# 錄像名正則表达式
RE_RECORDING = re.compile("^[0-9]+_day[0-9]+_.*\\.(mp4|mov|mkv)$")

# 用於取出錄像 ID 的正則表达式。
RE_ID = re.compile("^([0-9]+).*$")

# 延時攝影名正則表头式。
RE_TIMELAPSE = re.compile("^[0-9]+[a-z]+_.*\\.(mp4|mov|mkv)")


def is_recording(file: Path) -> bool:
    return file.is_file() and RE_RECORDING.fullmatch(file.name) is not None


def get_recordings(dir: Path) -> filter[Path]:
    """獲取目錄內的全部原始錄像文件。"""
    return filter(is_recording, dir.iterdir())


def get_recording_index(file: Path) -> int:
    """獲取錄像數字編號。

    若找不到編號，返回 -1。
    """
    match = RE_ID.search(file.name)
    if match is None:
        return -1
    return int(match.group(1))


def is_timelapse(file: Path) -> bool:
    return file.is_file() and RE_TIMELAPSE.fullmatch(file.name) is not None


def get_timelapses(dir: Path) -> filter[Path]:
    """獲取目錄數字編號。"""
    return filter(is_timelapse, dir.iterdir())
