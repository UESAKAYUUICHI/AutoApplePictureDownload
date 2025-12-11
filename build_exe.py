"""
打包脚本，用于将苹果照片重命名工具打包成exe文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_gui():
    """打包GUI版本"""
    cmd = [
        "pyinstaller",
        "--noconfirm",
        "--onedir",
        "--windowed",
        "--name", "ApplePhotoRenamer",
        "--icon", "NONE",
        "run_gui.py"
    ]
    
    print("正在打包GUI版本...")
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        print("GUI版本打包成功！")
        print("可执行文件位于: dist/ApplePhotoRenamer/")
    else:
        print("GUI版本打包失败:")
        print(result.stderr)

def build_cli():
    """打包CLI版本"""
    cmd = [
        "pyinstaller",
        "--noconfirm",
        "--onedir",
        "--console",
        "--name", "ApplePhotoRenamerCLI",
        "--icon", "NONE",
        "run_cli.py"
    ]
    
    print("正在打包CLI版本...")
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        print("CLI版本打包成功！")
        print("可执行文件位于: dist/ApplePhotoRenamerCLI/")
    else:
        print("CLI版本打包失败:")
        print(result.stderr)

def build_single_gui():
    """打包单文件GUI版本"""
    cmd = [
        "pyinstaller",
        "--noconfirm",
        "--onefile",
        "--windowed",
        "--name", "ApplePhotoRenamer",
        "--icon", "NONE",
        "run_gui.py"
    ]
    
    print("正在打包单文件GUI版本...")
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        print("单文件GUI版本打包成功！")
        print("可执行文件位于: dist/ApplePhotoRenamer.exe")
    else:
        print("单文件GUI版本打包失败:")
        print(result.stderr)

def build_single_cli():
    """打包单文件CLI版本"""
    cmd = [
        "pyinstaller",
        "--noconfirm",
        "--onefile",
        "--console",
        "--name", "ApplePhotoRenamerCLI",
        "--icon", "NONE",
        "run_cli.py"
    ]
    
    print("正在打包单文件CLI版本...")
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        print("单文件CLI版本打包成功！")
        print("可执行文件位于: dist/ApplePhotoRenamerCLI.exe")
    else:
        print("单文件CLI版本打包失败:")
        print(result.stderr)

def main():
    print("苹果照片重命名工具打包脚本")
    print("=" * 40)
    print("请选择打包选项:")
    print("1. 打包GUI版本 (文件夹形式)")
    print("2. 打包CLI版本 (文件夹形式)")
    print("3. 打包单文件GUI版本")
    print("4. 打包单文件CLI版本")
    print("5. 打包所有版本")
    
    try:
        choice = int(input("请输入选择 (1-5): "))
    except ValueError:
        print("无效输入，请输入数字 1-5")
        return
    
    if choice == 1:
        build_gui()
    elif choice == 2:
        build_cli()
    elif choice == 3:
        build_single_gui()
    elif choice == 4:
        build_single_cli()
    elif choice == 5:
        build_gui()
        build_cli()
        build_single_gui()
        build_single_cli()
    else:
        print("无效选择，请输入 1-5 之间的数字")

if __name__ == "__main__":
    main()