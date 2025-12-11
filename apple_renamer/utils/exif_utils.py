"""
苹果重命名器应用程序的EXIF工具
处理照片元数据提取
"""
import exifread
from datetime import datetime
from pathlib import Path


def get_photo_date(photo_path: Path) -> datetime:
    """
    从照片的EXIF数据中提取日期
    
    参数:
        photo_path: 照片文件的路径
        
    返回:
        表示照片拍摄时间的DateTime对象
        
    异常:
        Exception: 如果无法读取或解析EXIF数据
    """
    with open(photo_path, 'rb') as f:
        tags = exifread.process_file(f, details=False)
        
        # 尝试从EXIF获取日期
        for date_tag in ['EXIF DateTimeOriginal', 'Image DateTime']:
            if date_tag in tags:
                date_str = str(tags[date_tag])
                # 解析EXIF中常见的日期格式
                try:
                    return datetime.strptime(date_str, '%Y:%m:%d %H:%M:%S')
                except ValueError:
                    pass
                    
                try:
                    return datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
                except ValueError:
                    pass
        
        # 如果我们无法解析日期，则抛出异常
        raise Exception("无法从EXIF数据中提取日期")


def has_exif_data(photo_path: Path) -> bool:
    """
    检查照片是否有EXIF数据
    
    参数:
        photo_path: 照片文件的路径
        
    返回:
        如果照片有EXIF数据则返回True，否则返回False
    """
    try:
        with open(photo_path, 'rb') as f:
            tags = exifread.process_file(f, details=False)
            return len(tags) > 0
    except Exception:
        return False