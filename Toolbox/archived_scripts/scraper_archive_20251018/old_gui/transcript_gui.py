#!/usr/bin/env python3
"""
Simple GUI for YouTube Transcript Downloader
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
import os
from pathlib import Path
import sys
import re
from youtube_transcript_api import YouTubeTranscriptApi
import yt_dlp

class TranscriptGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube Transcript Downloader")
        self.root.geometry("600x500")
        self.root.resizable(True, True)

        # Default output directory to current folder
        self.output_dir = os.getcwd()

        self.setup_ui()

    def setup_ui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(4, weight=1)

        # Channel URL input
        ttk.Label(main_frame, text="YouTube Channel URL:").grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        self.url_entry = ttk.Entry(main_frame, width=50)
        self.url_entry.grid(row=0, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 5))
        self.url_entry.insert(0, "https://youtube.com/@")

        # Output directory selection
        ttk.Label(main_frame, text="Save to:").grid(row=1, column=0, sticky=tk.W, pady=(5, 5))
        self.output_label = ttk.Label(main_frame, text=self.output_dir, foreground="blue")
        self.output_label.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=(5, 5))

        browse_btn = ttk.Button(main_frame, text="Browse", command=self.browse_output_dir)
        browse_btn.grid(row=1, column=2, padx=(5, 0), pady=(5, 5))

        # Download button
        self.download_btn = ttk.Button(main_frame, text="Download Latest Transcript",
                                     command=self.start_download, style="Accent.TButton")
        self.download_btn.grid(row=2, column=0, columnspan=3, pady=(10, 10), sticky=(tk.W, tk.E))

        # Progress bar
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))

        # Output text area
        ttk.Label(main_frame, text="Output:").grid(row=4, column=0, sticky=(tk.W, tk.N), pady=(0, 5))
        self.output_text = scrolledtext.ScrolledText(main_frame, height=15, width=70)
        self.output_text.grid(row=4, column=1, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 5))

        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN)
        status_bar.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(5, 0))

    def browse_output_dir(self):
        """Browse for output directory"""
        directory = filedialog.askdirectory(initialdir=self.output_dir)
        if directory:
            self.output_dir = directory
            self.output_label.config(text=directory)
            self.log_message(f"Output directory set to: {directory}")

    def log_message(self, message):
        """Add message to output text area"""
        self.output_text.insert(tk.END, f"{message}\n")
        self.output_text.see(tk.END)
        self.root.update_idletasks()

    def set_status(self, status):
        """Update status bar"""
        self.status_var.set(status)
        self.root.update_idletasks()

    def start_download(self):
        """Start download in a separate thread"""
        url = self.url_entry.get().strip()

        if not url or url == "https://youtube.com/@":
            messagebox.showerror("Error", "Please enter a valid YouTube channel URL")
            return

        # Disable button and start progress
        self.download_btn.config(state='disabled')
        self.progress.start()
        self.output_text.delete(1.0, tk.END)

        # Start download in separate thread
        thread = threading.Thread(target=self.download_transcript, args=(url,))
        thread.daemon = True
        thread.start()

    def download_transcript(self, channel_url):
        """Download transcript (runs in separate thread)"""
        try:
            self.set_status("Getting latest video...")
            self.log_message(f"Fetching latest video from: {channel_url}")

            # Get latest video
            video_id, title = self.get_latest_video(channel_url)

            if not video_id:
                self.log_message("❌ Failed to get latest video")
                return

            self.log_message(f"✅ Found: {title}")
            self.log_message(f"Video ID: {video_id}")

            # Download transcript
            self.set_status("Downloading transcript...")
            filename = self.get_transcript(video_id, title)

            if filename:
                self.log_message(f"✅ Success! Transcript saved to: {filename}")
                self.set_status("Download complete")

                # Ask if user wants to open the file
                self.root.after(0, lambda: self.ask_open_file(filename))
            else:
                self.log_message("❌ Failed to download transcript")
                self.set_status("Download failed")

        except Exception as e:
            self.log_message(f"❌ Error: {str(e)}")
            self.set_status("Error occurred")
        finally:
            # Re-enable button and stop progress
            self.root.after(0, self.download_complete)

    def download_complete(self):
        """Called when download is complete"""
        self.download_btn.config(state='normal')
        self.progress.stop()

    def ask_open_file(self, filename):
        """Ask user if they want to open the downloaded file"""
        result = messagebox.askyesno("Download Complete",
                                   f"Transcript downloaded successfully!\n\nOpen the file now?")
        if result:
            try:
                os.startfile(filename)  # Windows
            except:
                try:
                    os.system(f'open "{filename}"')  # macOS
                except:
                    os.system(f'xdg-open "{filename}"')  # Linux

    def get_latest_video(self, channel_url):
        """Get the latest video from a YouTube channel"""
        # Make sure we're looking at the videos page
        if not channel_url.endswith('/videos'):
            channel_url = channel_url.rstrip('/') + '/videos'

        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
                info = ydl.extract_info(channel_url, download=False)

                if 'entries' in info and info['entries']:
                    latest = info['entries'][0]
                    video_id = latest.get('id')
                    title = latest.get('title', 'Unknown Title')
                    return video_id, title
                else:
                    self.log_message("No videos found in channel")
                    return None, None

            except Exception as e:
                self.log_message(f"Error fetching channel: {str(e)}")
                return None, None

    def get_transcript(self, video_id, title):
        """Download transcript for a video"""
        try:
            # Create API instance
            ytt_api = YouTubeTranscriptApi()

            # Get available transcripts
            transcript_list = ytt_api.list(video_id)

            # Try English first (manual, then auto-generated)
            transcript = None
            transcript_type = ""

            try:
                transcript = transcript_list.find_manually_created_transcript(['en'])
                transcript_type = " (Manual English)"
            except:
                try:
                    transcript = transcript_list.find_generated_transcript(['en'])
                    transcript_type = " (Auto-generated English)"
                except:
                    # Use first available
                    available = list(transcript_list)
                    if available:
                        transcript = available[0]
                        transcript_type = f" ({transcript.language})"

            if transcript:
                self.log_message(f"Using transcript{transcript_type}")

                # Get the transcript text
                data = transcript.fetch()
                text = ' '.join([item.text for item in data])

                # Create safe filename with timestamp
                from datetime import datetime
                timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
                safe_title = re.sub(r'[<>:"/\\|?*]', '_', title)
                filename = os.path.join(self.output_dir, f"{timestamp}_{safe_title}.md")

                # Create markdown content
                markdown_content = f"""# {title}

## Video Information
- **Video URL**: https://youtube.com/watch?v={video_id}
- **Downloaded**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- **Transcript Length**: {len(text)} characters

---

## Transcript

{text}

---

*Downloaded using YouTube Transcript Downloader*
"""

                # Save to file
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(markdown_content)

                self.log_message(f"Transcript length: {len(text)} characters")
                return filename
            else:
                self.log_message("No transcript available for this video")
                return None

        except Exception as e:
            self.log_message(f"Error getting transcript: {str(e)}")
            return None

def main():
    root = tk.Tk()
    app = TranscriptGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()