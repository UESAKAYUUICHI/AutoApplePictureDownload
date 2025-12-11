"""
苹果重命名器应用程序的配置模块
"""
import os
from pathlib import Path

# 默认路径
DEFAULT_INPUT_PATH = r"此电脑\Apple iPhone\Internal Storage\DCIM"
DEFAULT_OUTPUT_PATH = str(Path.cwd() / "已重命名文件")

# 要处理的文件扩展名（默认选择）
DEFAULT_EXTENSIONS = {
    'jpg': True,
    'png': True,
    'mp4': True,
    'aee': False  # 默认排除
}

# 编号模式
NUMBERING_MODES = {
    'SEQUENCE': 1,      # 顺序编号
    'DATE': 2,          # 基于日期的编号
    'CUSTOM': 3         # 自定义前缀编号
}