"""
苹果重命名器应用程序的重命名模块
处理不同的重命名策略
"""
import os
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Callable
from ..utils.exif_utils import get_photo_date


class Renamer:
    """处理不同重命名策略的主要重命名器类"""
    
    def __init__(self, files: List[Path]):
        """
        使用要重命名的文件初始化
        
        参数:
            files: 要重命名的文件路径列表
        """
        self.files = files
    
    def rename_with_sequence(self, start_number: int = 1) -> Dict[Path, Path]:
        """
        使用顺序数字重命名文件
        
        参数:
            start_number: 序列开始的数字
            
        返回:
            将原始路径映射到新路径的字典
        """
        renamed_files = {}
        counter = start_number
        
        for file_path in self.files:
            if not file_path.exists():
                continue
                
            # 创建带有序列号的新名称
            new_name = f"{counter:04d}{file_path.suffix}"  # 4位数字零填充
            new_path = file_path.parent / new_name
            
            # 处理冲突
            while new_path.exists():
                counter += 1
                new_name = f"{counter:04d}{file_path.suffix}"
                new_path = file_path.parent / new_name
            
            # 重命名文件
            file_path.rename(new_path)
            renamed_files[file_path] = new_path
            counter += 1
            
        return renamed_files
    
    def rename_with_date(self) -> Dict[Path, Path]:
        """
        使用基于日期的名称重命名文件
        
        返回:
            将原始路径映射到新路径的字典
        """
        renamed_files = {}
        
        for file_path in self.files:
            if not file_path.exists():
                continue
                
            # 尝试获取照片日期，回退到文件修改时间
            try:
                date = get_photo_date(file_path)
            except Exception:
                date = datetime.fromtimestamp(file_path.stat().st_mtime)
            
            # 将日期格式化为YYYY-MM-DD
            date_str = date.strftime("%Y-%m-%d")
            base_name = date_str
            counter = 1
            
            # 使用日期创建新名称
            new_name = f"{base_name}{file_path.suffix}"
            new_path = file_path.parent / new_name
            
            # 通过添加(计数器)处理冲突
            while new_path.exists():
                new_name = f"{base_name}({counter}){file_path.suffix}"
                new_path = file_path.parent / new_name
                counter += 1
            
            # 重命名文件
            file_path.rename(new_path)
            renamed_files[file_path] = new_path
            
        return renamed_files
    
    def rename_with_custom_prefix(self, prefix: str) -> Dict[Path, Path]:
        """
        使用自定义前缀重命名文件
        
        参数:
            prefix: 文件名的自定义前缀
            
        返回:
            将原始路径映射到新路径的字典
        """
        renamed_files = {}
        counter = 1
        
        for file_path in self.files:
            if not file_path.exists():
                continue
                
            # 使用自定义前缀创建新名称
            new_name = f"{prefix}-{counter}{file_path.suffix}"
            new_path = file_path.parent / new_name
            
            # 处理冲突
            while new_path.exists():
                counter += 1
                new_name = f"{prefix}-{counter}{file_path.suffix}"
                new_path = file_path.parent / new_name
            
            # 重命名文件
            file_path.rename(new_path)
            renamed_files[file_path] = new_path
            counter += 1
            
        return renamed_files