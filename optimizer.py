import tkinter as tk
from tkinter import filedialog, ttk
import os
import subprocess
import threading
import webbrowser
from PIL import Image, ImageTk

def choose_file():
    input_file_path.set(filedialog.askopenfilename(title="Select video file", filetypes=[("Video files", "*.mp4 *.avi *.mov *.mkv")]))

def choose_folder():
    output_folder_path.set(filedialog.askdirectory(title="Select output folder"))

def optimize_video():
    input_file = input_file_path.get()
    output_folder = output_folder_path.get()
    crf_value = get_crf_value(crf_var.get())
    resolution = resolution_var.get()
    framerate = framerate_var.get()
    audio_bitrate = audio_bitrate_var.get()
    mega_optimize = mega_optimize_var.get()

    if not input_file or not output_folder:
        result_label.config(text="Please select input file and output folder")
        return

    # Disable the optimize button and show progress bar
    optimize_button.config(state=tk.DISABLED)
    progress_bar.grid(row=8, column=0, columnspan=3, pady=5, padx=20, sticky="ew")
    progress_bar.start()

    # Run the optimization in a separate thread
    thread = threading.Thread(target=run_optimization, args=(input_file, output_folder, crf_value, resolution, framerate, audio_bitrate, mega_optimize))
    thread.start()

def run_optimization(input_file, output_folder, crf_value, resolution, framerate, audio_bitrate, mega_optimize):
    try:
        reduce_video_size(input_file, output_folder, crf_value, resolution, framerate, audio_bitrate, mega_optimize)
        window.after(0, update_ui, "Video optimized successfully!")
    except Exception as e:
        window.after(0, update_ui, f"Error: {e}")

def update_ui(message):
    result_label.config(text=message)
    progress_bar.stop()
    progress_bar.grid_remove()
    optimize_button.config(state=tk.NORMAL)

def reduce_video_size(input_file, output_folder, crf, resolution, framerate, audio_bitrate, mega_optimize):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    filename_without_ext = os.path.splitext(os.path.basename(input_file))[0]
    output_file = os.path.join(output_folder, f"{filename_without_ext}_optimized.mp4")

    if mega_optimize:
        command = [
            "ffmpeg", "-i", input_file,
            "-c:v", "libx264", "-crf", "51",
            "-preset", "ultrafast",
            "-vf", "scale=320:240",
            "-r", "15",
            "-c:a", "aac", "-b:a", "32k",
            "-ac", "1",
            "-movflags", "+faststart",
            output_file
        ]
    else:
        command = [
            "ffmpeg", "-i", input_file,
            "-c:v", "libx264", "-crf", str(crf),
            "-preset", "veryslow",
            "-vf", f"scale={resolution}:force_original_aspect_ratio=decrease,fps={framerate}",
            "-c:a", "aac", "-b:a", audio_bitrate,
            "-movflags", "+faststart",
            output_file
        ]
    
    subprocess.run(command, check=True)

def open_twitter():
    webbrowser.open("https://twitter.com/sreaht")

def open_github():
    webbrowser.open("https://github.com/serhatkildaci")

def get_crf_value(quality):
    crf_map = {
        "Very High": 18,
        "High": 21,
        "Medium": 23,
        "Low": 26,
        "Very Low": 28
    }
    return crf_map.get(quality, 23)

# UI setup
window = tk.Tk()
window.title("Advanced Video Optimizer")
window.geometry("700x400")  # Reduced height
window.resizable(False, False)  # Allow resizing
window.minsize(700, 400)  # Reduced minimum size

if os.name == 'nt':
    window.iconbitmap('video_optimizer.ico')
else:
    img = tk.PhotoImage(file='video_optimizer.png')
    window.tk.call('wm', 'iconphoto', window._w, img)

# Define colors
bg_color = "#1E1E2E"
fg_color = "#FFFFFF"
accent_color = "#BD93F9"
entry_bg_color = "#2E2E3E"
button_bg_color = "#44475A"

style = ttk.Style()
style.theme_use("clam")

style.configure("TFrame", background=bg_color)
style.configure("TLabel", background=bg_color, foreground=fg_color, font=("Segoe UI", 12))
style.configure("TButton", background=button_bg_color, foreground=fg_color, font=("Segoe UI", 12))
style.configure("TCheckbutton", background=bg_color, foreground=fg_color, font=("Segoe UI", 12))
style.configure("TScale", background=bg_color, troughcolor=entry_bg_color)
style.configure("TProgressbar", background=accent_color)
style.configure("TCombobox", fieldbackground=entry_bg_color, background=button_bg_color, foreground=fg_color, font=("Segoe UI", 12))

style.map("TButton", background=[("active", accent_color)], foreground=[("active", bg_color)])
style.map("TCombobox", fieldbackground=[("readonly", entry_bg_color)])
style.map("TCheckbutton", background=[("active", bg_color)])

# Custom style for the Optimize button
style.configure("Accent.TButton", foreground=bg_color, background=accent_color, font=("Segoe UI", 14, "bold"))
style.map("Accent.TButton", background=[("active", "#A679E0")], foreground=[("active", bg_color)])

# Configure the main window
window.configure(bg=bg_color)

# Set the window top bar color (this works on Windows)
window.tk.call('tk', 'windowingsystem')
if window.tk.call('tk', 'windowingsystem') == 'win32':
    window.tk.call('set', '::tk::WindowingsystemTheme', 'dark')
    window.tk.call('set', '::tk::WindowingsystemThemeName', 'dark')

# Main content frame
content_frame = ttk.Frame(window, style="TFrame")
content_frame.grid(row=0, column=0, sticky="nsew")

# Branding frame (footer)
branding_frame = ttk.Frame(window, style="Branding.TFrame")
branding_frame.grid(row=1, column=0, sticky="ew")

# Configure window grid
window.grid_rowconfigure(0, weight=1)
window.grid_rowconfigure(1, weight=0)
window.grid_columnconfigure(0, weight=1)

# Variables for input and output paths
input_file_path = tk.StringVar()
output_folder_path = tk.StringVar()

# Input file selection
ttk.Label(content_frame, text="Input Video:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
ttk.Entry(content_frame, textvariable=input_file_path, width=40, style="Dark.TEntry").grid(row=0, column=1, padx=5, pady=5)
ttk.Button(content_frame, text="Browse", command=choose_file).grid(row=0, column=2, padx=5, pady=5)

# Output folder selection
ttk.Label(content_frame, text="Output Folder:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
ttk.Entry(content_frame, textvariable=output_folder_path, width=40, style="Dark.TEntry").grid(row=1, column=1, padx=5, pady=5)
ttk.Button(content_frame, text="Browse", command=choose_folder).grid(row=1, column=2, padx=5, pady=5)

# CRF dropdown
ttk.Label(content_frame, text="Quality:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
crf_var = tk.StringVar(value="Medium")
crf_choices = ["Very High", "High", "Medium", "Low", "Very Low"]
crf_menu = ttk.Combobox(content_frame, textvariable=crf_var, values=crf_choices, width=15)
crf_menu.grid(row=2, column=1, padx=5, pady=5, sticky="w")

# Resolution dropdown
ttk.Label(content_frame, text="Resolution:").grid(row=3, column=0, padx=5, pady=5, sticky="e")
resolution_var = tk.StringVar(value="1280:720")
resolution_choices = ["640:360", "854:480", "1280:720", "1920:1080"]
resolution_menu = ttk.Combobox(content_frame, textvariable=resolution_var, values=resolution_choices, width=15)
resolution_menu.grid(row=3, column=1, padx=5, pady=5, sticky="w")

# Framerate dropdown
ttk.Label(content_frame, text="Framerate:").grid(row=4, column=0, padx=5, pady=5, sticky="e")
framerate_var = tk.StringVar(value="30")
framerate_choices = ["24", "30", "60"]
framerate_menu = ttk.Combobox(content_frame, textvariable=framerate_var, values=framerate_choices, width=15)
framerate_menu.grid(row=4, column=1, padx=5, pady=5, sticky="w")

# Audio bitrate dropdown
ttk.Label(content_frame, text="Audio Bitrate:").grid(row=5, column=0, padx=5, pady=5, sticky="e")
audio_bitrate_var = tk.StringVar(value="128k")
audio_bitrate_choices = ["64k", "96k", "128k", "192k"]
audio_bitrate_menu = ttk.Combobox(content_frame, textvariable=audio_bitrate_var, values=audio_bitrate_choices, width=15)
audio_bitrate_menu.grid(row=5, column=1, padx=5, pady=5, sticky="w")

# Mega Optimize checkbox
mega_optimize_var = tk.BooleanVar()
mega_optimize_checkbox = ttk.Checkbutton(content_frame, text="Mega Optimize (Extreme Compression)", variable=mega_optimize_var)
mega_optimize_checkbox.grid(row=6, column=0, columnspan=3, pady=10)

# Optimize button
optimize_button = ttk.Button(content_frame, text="Optimize Video", command=optimize_video, style="Accent.TButton")
optimize_button.grid(row=7, column=0, columnspan=3, pady=15)

# Progress bar (hidden by default)
progress_bar = ttk.Progressbar(content_frame, mode="indeterminate", length=500)
progress_bar.grid(row=8, column=0, columnspan=3, pady=5, padx=20, sticky="ew")
progress_bar.grid_remove()

# Result label
result_label = ttk.Label(content_frame, text="", font=("Segoe UI", 12))
result_label.grid(row=9, column=0, columnspan=3, pady=5)

# Branding frame content
branding_bg_color = "#1A1A28"  # Slightly darker shade
style.configure("Branding.TFrame", background=branding_bg_color)
style.configure("Branding.TLabel", background=branding_bg_color, foreground=fg_color, font=("Segoe UI", 10))
style.configure("Branding.TButton", background=branding_bg_color)
style.map("Branding.TButton", background=[("active", branding_bg_color)])

developed_by_label = ttk.Label(branding_frame, text="Developed by Serhat", style="Branding.TLabel")
developed_by_label.pack(side="right", padx=5, pady=3)

twitter_icon = Image.open("twitter_icon.png").resize((24, 24))
github_icon = Image.open("github_icon.png").resize((24, 24))

twitter_icon = ImageTk.PhotoImage(twitter_icon)
github_icon = ImageTk.PhotoImage(github_icon)

twitter_button = ttk.Button(branding_frame, image=twitter_icon, command=open_twitter, style="Branding.TButton")
twitter_button.pack(side="left", padx=5, pady=3)

github_button = ttk.Button(branding_frame, image=github_icon, command=open_github, style="Branding.TButton")
github_button.pack(side="left", padx=5, pady=3)

for i in range(10):
    content_frame.rowconfigure(i, weight=1)
for i in range(3):
    content_frame.columnconfigure(i, weight=1)

style.configure("Dark.TEntry", fieldbackground=entry_bg_color, foreground=fg_color, font=("Segoe UI", 12))

def create_tooltip(widget, text):
    def enter(event):
        tooltip = tk.Toplevel(widget)
        tooltip.wm_overrideredirect(True)
        tooltip.wm_geometry(f"+{event.x_root+10}+{event.y_root+10}")
        label = tk.Label(tooltip, text=text, background="#44475A", foreground=fg_color, relief="solid", borderwidth=1)
        label.pack()
        widget.tooltip = tooltip

    def leave(event):
        if hasattr(widget, "tooltip"):
            widget.tooltip.destroy()

    widget.bind("<Enter>", enter)
    widget.bind("<Leave>", leave)

create_tooltip(crf_menu, "Select the desired quality level")
create_tooltip(resolution_menu, "Output video resolution")
create_tooltip(framerate_menu, "Output video frame rate")
create_tooltip(audio_bitrate_menu, "Output audio bitrate")
create_tooltip(mega_optimize_checkbox, "Enable extreme compression (lowest quality, smallest file size)")
create_tooltip(optimize_button, "Start the video optimization process")
create_tooltip(twitter_button, "@sreaht")
create_tooltip(github_button, "github.com/serhatkildaci")

window.mainloop()