"""
苹果重命名器应用程序的主入口点
"""
import sys
from pathlib import Path
from .config import DEFAULT_INPUT_PATH, DEFAULT_OUTPUT_PATH, DEFAULT_EXTENSIONS, NUMBERING_MODES
from .core.file_ops import find_apple_directories, copy_files_to_destination
from .core.file_filter import FileFilter
from .core.renamer import Renamer


def main():
    """运行苹果重命名器应用程序的主函数"""
    print("苹果照片重命名器")
    print("=" * 50)
    
    # 获取输入路径
    input_path = input(f"请输入输入路径 (默认: {DEFAULT_INPUT_PATH}): ").strip()
    if not input_path:
        input_path = DEFAULT_INPUT_PATH
    
    input_path = Path(input_path)
    
    # 获取输出路径
    output_path = input(f"请输入输出路径 (默认: {DEFAULT_OUTPUT_PATH}): ").strip()
    if not output_path:
        output_path = DEFAULT_OUTPUT_PATH
    
    output_path = Path(output_path)
    
    # 查找苹果目录
    print("\n正在搜索苹果目录...")
    apple_dirs = find_apple_directories(input_path)
    
    if not apple_dirs:
        print("未找到苹果目录!")
        print("提示：请确保您的苹果设备已连接，并且路径正确。")
        print("常见解决方案：")
        print("  1. 检查设备是否已正确连接到电脑")
        print("  2. 尝试手动输入正确的路径")
        print("  3. 确认文件夹名称中包含'apple'关键词")
        return
    
    print(f"找到了 {len(apple_dirs)} 个苹果目录:")
    for i, dir_path in enumerate(apple_dirs, 1):
        print(f"  {i}. {dir_path.name}")
    
    # 设置文件过滤器
    file_filter = FileFilter(DEFAULT_EXTENSIONS.copy())
    
    # 让用户选择扩展名
    print("\n选择要处理的文件扩展名:")
    extensions = list(DEFAULT_EXTENSIONS.keys())
    for i, ext in enumerate(extensions, 1):
        status = "[x]" if DEFAULT_EXTENSIONS[ext] else "[ ]"
        print(f"  {i}. {status} .{ext}")
    
    print("输入要切换的扩展名编号(逗号分隔)，或按Enter继续:")
    choice = input().strip()
    
    if choice:
        try:
            indices = [int(x.strip()) - 1 for x in choice.split(',')]
            for idx in indices:
                if 0 <= idx < len(extensions):
                    ext = extensions[idx]
                    file_filter.set_extension(ext, not DEFAULT_EXTENSIONS[ext])
        except ValueError:
            print("输入无效，使用默认扩展名。")
    
    # 复制文件到目标位置
    print("\n正在复制文件...")
    enabled_extensions = file_filter.get_enabled_extensions()
    copied_files = copy_files_to_destination(apple_dirs, output_path, enabled_extensions)
    print(f"已复制 {len(copied_files)} 个文件到 {output_path}")
    
    # 选择编号模式
    print("\n选择编号模式:")
    print("1. 顺序编号")
    print("2. 基于日期的编号")
    print("3. 自定义前缀编号")
    
    try:
        mode_choice = int(input("请输入选择 (1-3): "))
    except ValueError:
        print("选择无效，使用顺序编号。")
        mode_choice = 1
    
    # 根据编号模式处理文件
    renamer = Renamer(copied_files)
    
    if mode_choice == NUMBERING_MODES['SEQUENCE']:
        try:
            start_num = int(input("请输入起始编号 (默认: 1): ") or "1")
        except ValueError:
            start_num = 1
            
        print("正在使用顺序编号重命名文件...")
        renamed = renamer.rename_with_sequence(start_num)
        print(f"已重命名 {len(renamed)} 个文件")
        
    elif mode_choice == NUMBERING_MODES['DATE']:
        print("正在使用基于日期的编号重命名文件...")
        renamed = renamer.rename_with_date()
        print(f"已重命名 {len(renamed)} 个文件")
        
    elif mode_choice == NUMBERING_MODES['CUSTOM']:
        prefix = input("请输入自定义前缀: ").strip()
        if not prefix:
            prefix = "文件"
            
        print(f"正在使用自定义前缀 '{prefix}' 重命名文件...")
        renamed = renamer.rename_with_custom_prefix(prefix)
        print(f"已重命名 {len(renamed)} 个文件")
        
    else:
        print("选择无效，使用顺序编号。")
        print("正在使用顺序编号重命名文件...")
        renamed = renamer.rename_with_sequence()
        print(f"已重命名 {len(renamed)} 个文件")
    
    print("\n重命名完成!")


if __name__ == "__main__":
    main()