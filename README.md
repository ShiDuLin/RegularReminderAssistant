# 专注时间管理助手 (Regular Reminder Assistant)

一个简单的专注时间管理工具，帮助你保持专注并定时休息。

## 功能

1. 每隔3~5分钟随机播放提示音，提醒你短暂休息10秒钟
2. 每完成90分钟的专注时间后，提示你休息20分钟
3. 休息结束后自动进入下一个周期

## 使用方法

### 方法一：直接运行可执行文件（推荐）

1. 在根目录中找到已打包好的可执行文件 `ReminderAssistent.exe`
2. 双击运行该文件即可启动程序，无需安装Python环境

### 方法二：通过Python运行

1. 不需要安装额外依赖，直接运行程序：`python main.py`
2. 将提示音文件（.wav格式）放入`sounds`目录
3. 程序会在Windows系统中使用内置的winsound模块播放声音

## 获取音效文件

你可以通过以下方式获取 .wav 格式的提示音文件：

1. **使用Windows系统音效**：从 `C:\Windows\Media` 目录复制 .wav 文件
2. **从网上下载**：Freesound、SoundBible等网站提供免费音效
3. **格式转换**：使用在线转换工具将其他格式的音频转为 .wav 格式

## 自定义设置

可以在`main.py`中修改以下参数：
- 短提醒间隔：`MIN_REMINDER_INTERVAL`和`MAX_REMINDER_INTERVAL`（单位：分钟）
- 专注周期时长：`FOCUS_PERIOD`（单位：分钟）
- 长休息时长：`LONG_BREAK_PERIOD`（单位：分钟）
- 短休息时长：`SHORT_BREAK_PERIOD`（单位：秒）

## 关于打包

本项目使用 PyInstaller 打包，可执行文件位于 dist 目录下。

### 完整打包命令（含音频文件）

按照以下步骤将音频文件一起打包到exe中：

1. 首先在项目根目录下创建 `sounds` 文件夹（如果不存在）
   ```
   mkdir sounds
   ```

2. 将 .wav 格式的音频文件放入 sounds 目录

3. 使用以下命令打包应用：
   ```
   pyinstaller -F -n ReminderAssistent --icon=icon.ico --add-data "sounds;sounds" main.py
   ```

4. 打包完成后，可以直接运行 `dist/ReminderAssistent.exe`，音频文件会包含在可执行文件中

### 命令参数说明

- `-F`：生成单个可执行文件
- `-n ReminderAssistent`：指定生成的可执行文件名称
- `--icon=icon.ico`：指定应用图标
- `--add-data "sounds;sounds"`：将sounds目录中的所有文件添加到打包结果中
  - 格式为"源路径;目标路径"，其中目标路径是相对于程序运行时临时目录的路径

### 注意事项

1. 打包前确保 sounds 目录中已有音频文件，否则打包后程序将使用默认的蜂鸣声
2. 打包后的程序会将音频文件解压到临时目录，程序已做了相应处理以支持访问
3. 如果希望在运行后更新音频文件，建议使用非打包方式运行
