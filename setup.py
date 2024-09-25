import sys
import os
from cx_Freeze import setup, Executable

build_exe_options = {
    "packages": ["os", "PIL", "subprocess", "threading", "webbrowser", "tkinter"],
    "include_files": [
        ("resources/video_optimizer.ico", "resources/video_optimizer.ico"),
        ("resources/twitter_icon.png", "resources/twitter_icon.png"),
        ("resources/github_icon.png", "resources/github_icon.png"),
        ("resources/video_optimizer.png", "resources/video_optimizer.png"),
    ],
    "include_msvcr": True,
    "build_exe": "build/AVOptimizer",
}

base = None
if sys.platform == "win32":
    base = "Win32GUI"

# Create the target
target = Executable(
    script="optimizer.py",
    base=base,
    icon="resources/video_optimizer.ico",
    target_name="AVOptimizer.exe",
    shortcut_name="Advanced Video Optimizer",
    shortcut_dir="DesktopFolder"
)

setup(
    name="AVOptimizer",
    version="0.1",
    description="Advanced Video Optimizer - Compress and optimize your videos for streaming and sharing",
    author="Serhat Kıldacı",
    author_email="taserdeveloper@gmail.com",
    url="https://github.com/serhatkildaci",
    project_urls={
        "Twitter": "https://twitter.com/sreaht",
        "GitHub": "https://github.com/serhatkildaci",
    },
    long_description="""
    Advanced Video Optimizer is a powerful tool designed to compress and optimize videos for streaming and sharing.
    Key features:
    - Easy-to-use graphical interface
    - Support for multiple video formats
    - Customizable compression settings
    - Batch processing capabilities
    - Preview function to compare before and after
    """,
    options={"build_exe": build_exe_options},
    executables=[target]
)
