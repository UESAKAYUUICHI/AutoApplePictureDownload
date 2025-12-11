"""
苹果重命名器应用程序的文件过滤模块
处理文件扩展名过滤
"""
from typing import Dict, Set


class FileFilter:
    """处理文件扩展名过滤的类"""
    
    def __init__(self, extensions_config: Dict[str, bool]):
        """
        使用扩展名配置初始化
        
        参数:
            extensions_config: 将扩展名映射到布尔值的字典（启用/禁用）
        """
        self.extensions_config = extensions_config
    
    def get_enabled_extensions(self) -> Set[str]:
        """
        获取启用的扩展名集合
        
        返回:
            启用的扩展名集合（不带点号）
        """
        return {ext for ext, enabled in self.extensions_config.items() if enabled}
    
    def set_extension(self, extension: str, enabled: bool):
        """
        启用或禁用扩展名
        
        参数:
            extension: 要修改的扩展名（不带点号）
            enabled: 是否启用或禁用
        """
        self.extensions_config[extension] = enabled