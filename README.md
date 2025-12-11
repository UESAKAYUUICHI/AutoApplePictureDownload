# 苹果照片重命名工具 (Apple Photo Renamer)

一个用于批量重命名苹果设备照片的工具，支持多种命名模式和文件格式。

# 注意！！！！ 目前项目可能有bug，识别不到apple手机的路径，此时请先将图片文件夹如 139APPLE 导入到 本机电脑中，输入路径为图片文件夹的父目录 

## 功能特性

- 🔍 自动查找苹果设备照片目录
- 📁 支持多种文件格式 (JPG, PNG, MP4, AEE等)
- 🔄 三种重命名模式:
  - 序列编号 (0001, 0002...)
  - 日期编号 (2025-03-05, 2025-03-05(1)...)
  - 自定义前缀 (MYIMG-1, MYIMG-2...)
- 🖥️ 双界面支持 (命令行和图形界面)
- 🌍 完整中文化界面
- 🛡️ 安全操作 (只复制不修改原文件)

## 安装要求

- Python 3.6+
- 依赖库: `exifread==2.3.2`

## 安装步骤

1. 克隆或下载本项目
2. 安装依赖:
```bash
pip install -r requirements.txt
```

## 使用方法

### 图形界面版本
```bash
python run_gui.py
```

### 命令行版本
```bash
python run_cli.py
```

## 打包为可执行文件

### 安装打包工具
```bash
pip install pyinstaller
```

### 快速打包
```bash
# 打包GUI版本为单个exe文件
pyinstaller --onefile --windowed run_gui.py

# 打包CLI版本为单个exe文件
pyinstaller --onefile --console run_cli.py
```

### 使用打包脚本
项目提供了专用的打包脚本 [build_exe.py](file:///D:/ProgramDevelopment/Code/ArtificialIntelligenceProject/AutoApplePictureDownload/build_exe.py)：
```bash
python build_exe.py
```

打包完成后，可执行文件将位于 `dist/` 目录中。

## 使用流程

1. 连接苹果设备到电脑
2. 运行程序 (GUI或CLI)
3. 设置输入路径 (默认为 `此电脑\Apple iPhone\Internal Storage\DCIM`)
4. 设置输出路径
5. 选择要处理的文件类型
6. 选择重命名模式
7. 开始处理

## 项目结构

```
Apple Photo Renamer/
├── apple_renamer/
│   ├── config.py              # 配置文件
│   ├── main.py                # 命令行主程序
│   ├── gui.py                 # 图形界面程序
│   ├── core/
│   │   ├── file_ops.py        # 文件操作模块
│   │   ├── file_filter.py     # 文件过滤模块
│   │   └── renamer.py         # 重命名模块
│   └── utils/
│       ├── exif_utils.py      # EXIF工具模块
│       └── naming_utils.py    # 命名工具模块
├── requirements.txt           # 依赖包列表
├── run_cli.py                # 运行命令行版本
└── run_gui.py                # 运行图形界面版本
```

## 配置说明

### 默认路径
- 输入路径: `此电脑\Apple iPhone\Internal Storage\DCIM`
- 输出路径: `已重命名文件` (当前目录下的子目录)

### 支持的文件格式
- `.jpg` - JPEG图像文件 (默认启用)
- `.png` - PNG图像文件 (默认启用)
- `.mp4` - MP4视频文件 (默认启用)
- `.aee` - AEE格式文件 (默认禁用)

## 故障排除

### 未找到苹果目录
1. 确保苹果设备已正确连接
2. 检查路径是否正确
3. 确认文件夹名称包含"apple"关键词
4. 尝试手动选择路径

### 其他问题
- 检查Python环境和依赖是否正确安装
- 确保有足够的磁盘空间用于复制文件

## 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 贡献

欢迎提交 Issue 和 Pull Request 来改进本项目。
