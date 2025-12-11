"""
苹果重命名器应用程序的命名工具
"""
from pathlib import Path
from typing import List


def sanitize_filename(filename: str) -> str:
    """
    通过删除无效字符来清理文件名
    
    参数:
        filename: 原始文件名
        
    返回:
        清理后的文件名
    """
    # Windows文件名中的无效字符
    invalid_chars = '<>:"/\\|?*'
    
    for char in invalid_chars:
        filename = filename.replace(char, '_')
        
    return filename


def resolve_filename_conflict(desired_path: Path, existing_paths: List[Path]) -> Path:
    """
    通过添加计数器来解决文件名冲突
    
    参数:
        desired_path: 期望的文件路径
        existing_paths: 现有文件路径列表
        
    返回:
        解决冲突后的文件路径
    """
    if desired_path not in existing_paths and not desired_path.exists():
        return desired_path
        
    counter = 1
    stem = desired_path.stem
    suffix = desired_path.suffix
    parent = desired_path.parent
    
    while True:
        new_name = f"{stem}({counter}){suffix}"
        new_path = parent / new_name
        if new_path not in existing_paths and not new_path.exists():
            return new_path
        counter += 1