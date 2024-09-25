# AVOptimizer Advanced Video Optimizer

Advanced Video Optimizer is a powerful tool designed to compress and optimize videos for streaming and sharing. It provides an easy-to-use graphical interface for customizing video compression settings and processing multiple files.

## Features

- User-friendly graphical interface
- Support for multiple video formats (MP4, AVI, MOV, MKV)
- Customizable compression settings:
  - Quality (CRF)
  - Resolution
  - Framerate
  - Audio bitrate
- Mega Optimize option for extreme compression
- Progress tracking with a progress bar
- Tooltips for easy understanding of options

## Requirements

- Python 3.6+
- FFmpeg (must be installed and accessible in the system PATH)
- Pillow (PIL) for image processing

## Python Libraries Used

This project uses the following Python libraries:

- `tkinter`: Standard GUI library for Python
- `os`: Provides a way of using operating system dependent functionality
- `subprocess`: Allows you to spawn new processes, connect to their input/output/error pipes, and obtain their return codes
- `threading`: Higher-level threading interface
- `webbrowser`: Provides a high-level interface to allow displaying Web-based documents to users
- `PIL` (Python Imaging Library): Adds support for opening, manipulating, and saving many different image file formats

All libraries except PIL (Pillow) are part of the Python standard library.

## Installation

### Option 1: Install from source

1. Clone this repository:
   ```
   git clone https://github.com/serhatkildaci/AV-Optimizer.git
   ```

2. Navigate to the project directory:

3. Install the required dependencies:
   ```
   pip install pillow
   ```

4. Ensure FFmpeg is installed and accessible in your system PATH.

### Option 2: Windows pre-built executable (Recommended)

1. Go to the [Releases](https://github.com/serhatkildaci/AV-Optimizer/releases) page.
2. Download the latest `.msi` installer.
3. Run the installer and follow the prompts.

Note: The pre-built executable is only available for Windows. For other platforms, please install from source.

## Usage

Run the optimizer script:

Follow the on-screen instructions to select your input video, output folder, and optimization settings.


## Acknowledgments

- FFmpeg for video processing capabilities
- Tkinter for the graphical user interface
- PIL (Pillow) for image processing
- cx_Freeze for creating standalone executables
- Inno Setup for creating the Windows installer

## Contact

- Developer: Serhat Kıldacı
- Twitter: [@sreaht](https://twitter.com/sreaht)
- GitHub: [serhatkildaci](https://github.com/serhatkildaci)
