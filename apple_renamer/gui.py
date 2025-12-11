"""
使用tkinter的苹果重命名器应用程序简单GUI
"""
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
from .config import DEFAULT_INPUT_PATH, DEFAULT_OUTPUT_PATH, DEFAULT_EXTENSIONS, NUMBERING_MODES
from .core.file_ops import find_apple_directories, copy_files_to_destination
from .core.file_filter import FileFilter
from .core.renamer import Renamer


class AppleRenamerGUI:
    """苹果重命名器应用程序的GUI类"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("苹果照片重命名器v1.0.0")
        self.root.geometry("600x500")
        
        # 变量
        self.input_path_var = tk.StringVar(value=DEFAULT_INPUT_PATH)
        self.output_path_var = tk.StringVar(value=DEFAULT_OUTPUT_PATH)
        self.start_number_var = tk.StringVar(value="1")
        self.custom_prefix_var = tk.StringVar(value="IMG")
        self.extension_vars = {}
        
        # 创建UI
        self.create_widgets()
        
        # 初始化文件过滤器
        self.file_filter = FileFilter(DEFAULT_EXTENSIONS.copy())
        
    def create_widgets(self):
        """创建GUI控件"""
        # 主框架
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 配置网格权重
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # 标题
        title_label = ttk.Label(main_frame, text="苹果照片重命名器(先把图片拷贝到电脑的目录下再输入路径)", font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # 输入路径
        ttk.Label(main_frame, text="输入路径:").grid(row=1, column=0, sticky=tk.W, pady=5)
        ttk.Entry(main_frame, textvariable=self.input_path_var).grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5, padx=(0, 5))
        ttk.Button(main_frame, text="浏览...", command=self.browse_input).grid(row=1, column=2, pady=5)
        
        # 输出路径
        ttk.Label(main_frame, text="输出路径:").grid(row=2, column=0, sticky=tk.W, pady=5)
        ttk.Entry(main_frame, textvariable=self.output_path_var).grid(row=2, column=1, sticky=(tk.W, tk.E), pady=5, padx=(0, 5))
        ttk.Button(main_frame, text="浏览...", command=self.browse_output).grid(row=2, column=2, pady=5)
        
        # 扩展名框架
        extensions_frame = ttk.LabelFrame(main_frame, text="文件扩展名", padding="10")
        extensions_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        extensions_frame.columnconfigure(1, weight=1)
        
        extensions = list(DEFAULT_EXTENSIONS.keys())
        for i, ext in enumerate(extensions):
            var = tk.BooleanVar(value=DEFAULT_EXTENSIONS[ext])
            self.extension_vars[ext] = var
            chk = ttk.Checkbutton(extensions_frame, text=f".{ext}", variable=var)
            chk.grid(row=i//4, column=i%4, sticky=tk.W, padx=5, pady=2)
        
        # 编号模式框架
        numbering_frame = ttk.LabelFrame(main_frame, text="编号模式", padding="10")
        numbering_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        
        self.mode_var = tk.StringVar(value="1")  # 默认为序列
        
        ttk.Radiobutton(numbering_frame, text="序列编号", variable=self.mode_var, value="1").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.start_number_entry = ttk.Entry(numbering_frame, textvariable=self.start_number_var, width=10)
        self.start_number_entry.grid(row=0, column=1, padx=(10, 0))
        ttk.Label(numbering_frame, text="起始编号").grid(row=0, column=2, sticky=tk.W, padx=(5, 0))
        
        ttk.Radiobutton(numbering_frame, text="日期编号", variable=self.mode_var, value="2").grid(row=1, column=0, sticky=tk.W, pady=2)
        
        ttk.Radiobutton(numbering_frame, text="自定义前缀", variable=self.mode_var, value="3").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.custom_prefix_entry = ttk.Entry(numbering_frame, textvariable=self.custom_prefix_var, width=10)
        self.custom_prefix_entry.grid(row=2, column=1, padx=(10, 0))
        ttk.Label(numbering_frame, text="前缀").grid(row=2, column=2, sticky=tk.W, padx=(5, 0))
        
        # 处理按钮
        self.process_button = ttk.Button(main_frame, text="处理文件", command=self.process_files)
        self.process_button.grid(row=5, column=0, columnspan=3, pady=20)
        
        # 进度文本
        self.progress_text = tk.Text(main_frame, height=10, state=tk.DISABLED)
        self.progress_text.grid(row=6, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        # 文本控件的滚动条
        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=self.progress_text.yview)
        scrollbar.grid(row=6, column=3, sticky=(tk.N, tk.S))
        self.progress_text.configure(yscrollcommand=scrollbar.set)
        
        # 配置行权重
        main_frame.rowconfigure(6, weight=1)
        
    def browse_input(self):
        """打开输入路径的文件对话框"""
        path = filedialog.askdirectory()
        if path:
            self.input_path_var.set(path)
            
    def browse_output(self):
        """打开输出路径的文件对话框"""
        path = filedialog.askdirectory()
        if path:
            self.output_path_var.set(path)
            
    def update_progress(self, message):
        """更新进度文本控件"""
        self.progress_text.config(state=tk.NORMAL)
        self.progress_text.insert(tk.END, message + "\n")
        self.progress_text.config(state=tk.DISABLED)
        self.progress_text.see(tk.END)
        self.root.update_idletasks()
        
    def process_files(self):
        """根据选定的选项处理文件"""
        try:
            # 禁用处理按钮
            self.process_button.config(state=tk.DISABLED)
            self.progress_text.config(state=tk.NORMAL)
            self.progress_text.delete(1.0, tk.END)
            self.progress_text.config(state=tk.DISABLED)
            
            # 获取路径
            input_path = Path(self.input_path_var.get())
            output_path = Path(self.output_path_var.get())
            
            # 更新扩展名
            for ext, var in self.extension_vars.items():
                self.file_filter.set_extension(ext, var.get())
            
            # 查找苹果目录
            self.update_progress("查找苹果目录...")
            self.update_progress(f"正在搜索路径: {input_path}")
            apple_dirs = find_apple_directories(input_path)
            
            if not apple_dirs:
                self.update_progress("未找到苹果目录！")
                self.update_progress("提示：请确保您的苹果设备已连接，并且路径正确。")
                self.update_progress("您也可以尝试使用“浏览...”按钮手动选择包含照片的目录。")
                return
                
            self.update_progress(f"找到 {len(apple_dirs)} 个苹果目录")
            
            # 复制文件
            self.update_progress("复制文件...")
            enabled_extensions = self.file_filter.get_enabled_extensions()
            copied_files = copy_files_to_destination(apple_dirs, output_path, enabled_extensions)
            self.update_progress(f"复制了 {len(copied_files)} 个文件")
            
            # 根据模式重命名文件
            mode = int(self.mode_var.get())
            renamer = Renamer(copied_files)
            
            if mode == NUMBERING_MODES['SEQUENCE']:
                start_num = int(self.start_number_var.get() or "1")
                self.update_progress("使用序列编号重命名文件...")
                renamed = renamer.rename_with_sequence(start_num)
                self.update_progress(f"重命名了 {len(renamed)} 个文件")
                
            elif mode == NUMBERING_MODES['DATE']:
                self.update_progress("使用日期编号重命名文件...")
                renamed = renamer.rename_with_date()
                self.update_progress(f"重命名了 {len(renamed)} 个文件")
                
            elif mode == NUMBERING_MODES['CUSTOM']:
                prefix = self.custom_prefix_var.get().strip()
                if not prefix:
                    prefix = "file"
                self.update_progress(f"使用自定义前缀 '{prefix}' 重命名文件...")
                renamed = renamer.rename_with_custom_prefix(prefix)
                self.update_progress(f"重命名了 {len(renamed)} 个文件")
                
            self.update_progress("处理完成！")
            
        except Exception as e:
            messagebox.showerror("错误", f"发生错误: {str(e)}")
            self.update_progress(f"错误: {str(e)}")
        finally:
            # 启用处理按钮
            self.process_button.config(state=tk.NORMAL)


def main():
    """运行GUI应用程序"""
    root = tk.Tk()
    app = AppleRenamerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()