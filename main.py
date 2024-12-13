import tkinter as tk
from tkinter import ttk, messagebox
from yt_dlp import YoutubeDL 
import threading

def download_video(ydl_opts, success_message, error_message):
    video_url = video_link_entry.get()
    if video_url:
        try:
          
            def hook(d):
                if d['status'] == 'downloading':
                    downloaded = d.get('downloaded_bytes', 0)
                    total = d.get('total_bytes', 1)
                    progress['value'] = (downloaded / total) * 100
                    root.update_idletasks()


            ydl_opts['nocheckcertificate'] = True

            ydl_opts['progress_hooks'] = [hook]

            with YoutubeDL(ydl_opts) as ydl:
                ydl.download([video_url])
            messagebox.showinfo("نجاح", success_message)
        except Exception as e:
            messagebox.showerror("خطأ", f"{error_message}: {e}")
        finally:
            progress['value'] = 0 
    else:
        messagebox.showwarning("تحذير", "يرجى إدخال رابط الفيديو.")

def download_high():
    threading.Thread(target=download_video, args=(
        {'format': 'bestvideo+bestaudio/best'},
        "تم تنزيل الفيديو بجودة عالية بنجاح!",
        "حدث خطأ أثناء تنزيل الفيديو"
    )).start()

def download_low():
    threading.Thread(target=download_video, args=(
        {'format': 'worst'},
        "تم تنزيل الفيديو بجودة منخفضة بنجاح!",
        "حدث خطأ أثناء تنزيل الفيديو"
    )).start()

def download_audio():
    threading.Thread(target=download_video, args=(
        {
            'format': 'bestaudio/best',
            'postprocessors': [
                {'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '192'}
            ]
        },
        "تم تنزيل الصوت فقط بنجاح!",
        "حدث خطأ أثناء تنزيل الصوت"
    )).start()




root = tk.Tk()
root.title("YouTube Downloader")


tk.Label(root, text="Enter the video link").pack(pady=10)
video_link_entry = tk.Entry(root, width=50)
video_link_entry.pack(pady=5)

frame = tk.Frame(root)
frame.pack(pady=10)

high_quality_button = tk.Button(frame, text="High quality download", command=download_high)
high_quality_button.grid(row=0, column=0, padx=5)

low_quality_button = tk.Button(frame, text="Low quality download", command=download_low)
low_quality_button.grid(row=0, column=1, padx=5)

audio_button = tk.Button(frame, text="Only audio", command=download_audio)
audio_button.grid(row=0, column=2, padx=5)

progress = ttk.Progressbar(root, orient="horizontal", length=400, mode="determinate")
progress.pack(pady=10)

control_frame = tk.Frame(root)
control_frame.pack(pady=10)

root.mainloop()