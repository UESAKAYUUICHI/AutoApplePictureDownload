"""
苹果重命名器应用程序的文件操作模块
处理文件复制和目录操作
"""
import os
import shutil
from pathlib import Path
from typing import List, Set


def copy_files_to_destination(source_dirs: List[Path], destination: Path, extensions: Set[str]) -> List[Path]:
    """
    将具有指定扩展名的文件从源目录复制到目标目录
    
    参数:
        source_dirs: 要从中复制的源目录列表
        destination: 目标目录
        extensions: 要复制的文件扩展名集合（不带点号）
        
    返回:
        复制的文件路径列表
    """
    # 如果目标目录不存在则创建它
    destination.mkdir(parents=True, exist_ok=True)
    
    copied_files = []
    
    # 遍历每个源目录
    for src_dir in source_dirs:
        if not src_dir.exists():
            continue
            
        # 遍历目录中的文件
        for file_path in src_dir.iterdir():
            # 检查文件是否具有所需的扩展名之一
            if file_path.is_file() and file_path.suffix.lower()[1:] in extensions:
                # 在目标中创建新文件路径
                new_file_path = destination / file_path.name
                
                # 通过添加计数器来处理文件名冲突
                counter = 1
                original_name = new_file_path.stem
                original_suffix = new_file_path.suffix
                
                while new_file_path.exists():
                    new_file_path = destination / f"{original_name}({counter}){original_suffix}"
                    counter += 1
                
                # 复制文件
                shutil.copy2(file_path, new_file_path)
                copied_files.append(new_file_path)
                
    return copied_files


def find_apple_directories(base_path: Path) -> List[Path]:
    """
    查找基本路径中所有包含'apple'的目录
    
    参数:
        base_path: 要搜索的基本目录
        
    返回:
        包含'apple'的目录列表
    """
    apple_dirs = []
    
    if not base_path.exists():
        print(f"路径不存在: {base_path}")
        return apple_dirs
        
    print(f"正在搜索路径: {base_path}")
    print("目录内容:")
    
    # 列出所有目录以供调试
    for item in base_path.iterdir():
        if item.is_dir():
            print(f"  文件夹: {item.name}")
            
    # 查找包含'apple'的目录（不区分大小写）
    for item in base_path.iterdir():
        if item.is_dir():
            if 'apple' in item.name.lower():
                apple_dirs.append(item)
                print(f"  找到匹配的苹果目录: {item.name}")
            
    return apple_dirs