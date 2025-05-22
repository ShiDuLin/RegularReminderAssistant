#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import random
import datetime
import sys
import os
from pathlib import Path

try:
    import winsound
    HAS_SOUND = True
except ImportError:
    print("警告：未找到 winsound 模块，将使用系统提示音代替")
    HAS_SOUND = False

# 可自定义参数
MIN_REMINDER_INTERVAL = 3  # 最短提醒间隔（分钟）
MAX_REMINDER_INTERVAL = 5  # 最长提醒间隔（分钟）
FOCUS_PERIOD = 90  # 专注周期（分钟）
LONG_BREAK_PERIOD = 20  # 长休息时间（分钟）
SHORT_BREAK_PERIOD = 10  # 短休息时间（秒）

# 确定资源文件路径（支持打包和非打包环境）
def resource_path(relative_path):
    """获取资源的绝对路径，支持开发环境和PyInstaller打包后的环境"""
    try:
        # PyInstaller创建临时文件夹，将路径存储在_MEIPASS中
        base_path = sys._MEIPASS
    except Exception:
        # 非打包环境，使用当前文件的目录
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relative_path)

# 音频文件目录
SOUNDS_DIR = Path(resource_path("sounds"))


def get_random_sound():
    """随机获取一个提示音文件"""
    try:
        sound_files = list(SOUNDS_DIR.glob("*.wav"))  # winsound 只支持 WAV 格式
        if not sound_files:
            return None
        return str(random.choice(sound_files))
    except Exception as e:
        print(f"获取音频文件失败：{e}")
        return None


def get_random_interval():
    """获取随机间隔时间（秒）"""
    return random.randint(MIN_REMINDER_INTERVAL * 60, MAX_REMINDER_INTERVAL * 60)


def format_time(seconds):
    """格式化时间"""
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    if hours > 0:
        return f"{hours}小时{minutes}分钟{seconds}秒"
    elif minutes > 0:
        return f"{minutes}分钟{seconds}秒"
    else:
        return f"{seconds}秒"


def countdown(seconds, message):
    """倒计时"""
    for i in range(seconds, 0, -1):
        sys.stdout.write(f"\r{message}：{format_time(i)}  ")
        sys.stdout.flush()
        time.sleep(1)
    sys.stdout.write("\r" + " " * 50 + "\r")
    sys.stdout.flush()


def play_sound_if_available():
    """播放提示音（如果有）"""
    if HAS_SOUND:
        sound_file = get_random_sound()
        if sound_file:
            try:
                winsound.PlaySound(sound_file, winsound.SND_FILENAME)
            except Exception as e:
                print(f"播放音频文件失败：{e}")
                winsound.Beep(800, 500)
        else:
            winsound.Beep(800, 500)
            print("提示：未找到音频文件")
    else:
        print("\a")
        print("提示：没有可用的声音模块，使用系统提示音代替")


def main():
    """主函数"""
    print("=" * 50)
    print("专注时间管理助手已启动")
    print(f"- 每隔 {MIN_REMINDER_INTERVAL}~{MAX_REMINDER_INTERVAL} 分钟提醒休息 {SHORT_BREAK_PERIOD} 秒")
    print(f"- 每完成 {FOCUS_PERIOD} 分钟专注，休息 {LONG_BREAK_PERIOD} 分钟")
    print("=" * 50)
    
    # 检查声音文件
    sound_file = get_random_sound()
    if not sound_file:
        print("提示：未找到音频文件")
        if HAS_SOUND:
            print("      将使用系统蜂鸣声代替")
        else:
            print("      将使用系统提示音代替")
    else:
        print(f"已加载音频文件目录：{SOUNDS_DIR}")
    
    cycle_count = 0
    try:
        while True:
            cycle_count += 1
            focus_start_time = datetime.datetime.now()
            print(f"\n开始第 {cycle_count} 个专注周期 ({focus_start_time.strftime('%H:%M:%S')})")
            
            elapsed_time = 0
            next_reminder_time = get_random_interval()
            
            # 专注时间循环
            while elapsed_time < FOCUS_PERIOD * 60:
                remaining_time = min(next_reminder_time, FOCUS_PERIOD * 60 - elapsed_time)
                
                # 等待至下一次提醒
                time.sleep(remaining_time)
                elapsed_time += remaining_time
                
                # 检查是否该结束专注周期
                if elapsed_time >= FOCUS_PERIOD * 60:
                    break
                
                # 短休息提醒
                play_sound_if_available()
                print(f"\n[{datetime.datetime.now().strftime('%H:%M:%S')}] 请短暂休息 {SHORT_BREAK_PERIOD} 秒")
                countdown(SHORT_BREAK_PERIOD, "休息时间")
                print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] 继续专注！")
                
                # 设置下一次提醒时间
                next_reminder_time = get_random_interval()
            
            # 完成一个专注周期
            focus_end_time = datetime.datetime.now()
            duration = (focus_end_time - focus_start_time).total_seconds() / 60
            
            print(f"\n完成第 {cycle_count} 个专注周期！")
            print(f"专注时间：{duration:.1f} 分钟 ({focus_start_time.strftime('%H:%M:%S')} - {focus_end_time.strftime('%H:%M:%S')})")
            
            # 长休息提醒
            play_sound_if_available()
            print(f"\n[{datetime.datetime.now().strftime('%H:%M:%S')}] 请休息 {LONG_BREAK_PERIOD} 分钟")
            countdown(LONG_BREAK_PERIOD * 60, "长休息时间")
            print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] 休息结束，准备下一个专注周期")
            time.sleep(3)  # 给用户一点准备时间
            
    except KeyboardInterrupt:
        print("\n\n程序已退出。祝您工作愉快！")


if __name__ == "__main__":
    main()
