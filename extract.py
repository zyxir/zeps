"""提取精彩片段。"""

import csv
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import List


@dataclass
class Job:
    """一個提取工作。"""
    # 錄像編號。
    index: int = 0
    # 開始時間
    ss: str = "00:00:00"
    # 結束時間
    to: str = "00:00:01"
    # 片段標題
    title: str = "untitled"


def read_extract_txt(file: Path) -> List[Job]:
    """讀取 extract.txt 以獲取所有提取任務。"""
    try:
        with open(file, newline="", encoding="utf-8") as f:
            reader = csv.reader(f, delimiter=" ")
            jobs: List[Job] = []
            for line in reader:
                jobs.append(Job(int(line[0]), line[1], line[2], line[3]))
            return jobs
    except Exception:
        logging.error(f"Failed to read \"{file.name}\"")
        return []


# def extract(src: Path, dst: Path, ss: str, to: str) -> int:
#     """提取單個片段。"""
#     cmd = [
#         "ffmpeg",
#         "-i",
#         str(src),
#         "-loglevel",
#         "warning",
#         # 使用 H.265 編碼，文件體積更小。
#         "-codec:v",
#         "libx265",
#         # 更慢的 preset 產生更小的文件（默認爲 medium）。
#         "-preset",
#         "slow",
#         # CRF 越小，視頻質量越差，體積也越小（默認爲 28）。
#         "-crf",
#         "26",
#         # 1080p 分辨率。
#         "-s",
#         "1920x1080",
#         # 帧率 30 以減小文件體積（錄製和成品皆爲 60）。
#         "-filter:v",
#         "fps=30",
#         str(dst),
#     ]
