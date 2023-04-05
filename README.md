## Baiduwp-PHP 项目程序文件导出工具

为 Baiduwp-PHP 项目制作的程序文件导出工具，由 Python 编写。
方便上传 assets，也为未来的自动更新做准备。

### 使用方法
将此项目中的 `ProgramFilesExporter` 文件夹放入 Baiduwp-PHP 项目的根目录下，然后运行 `./ProgramFilesExporter/export.py` 即可。

### 注意事项
生成的压缩包在 `./ProgramFiles/` 目录下，文件名为 `ProgramFiles.zip`。

运行此脚本时，该文件夹下的所有文件都会被删除，需要压缩的文件会被复制到该文件夹下。
