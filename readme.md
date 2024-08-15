# WhatsApp Chat Log to HTML Converter

This Python script converts WhatsApp chat logs from `_chat.txt` files into formatted HTML files. It processes the chat logs to display messages and attachments in a readable format, assigning unique colors to different users and creating clickable thumbnails for images and videos.

## Features

- **Color-Coded Messages**: Each user is assigned a unique color for their messages, ensuring easy distinction between different participants.
- **Thumbnail Generation**: Images and videos are displayed with a thumbnail preview. Clickable links allow users to view full-size versions or play videos in a new tab.
- **Dynamic HTML Title**: The HTML title is set based on the name of the parent folder, providing context for each chat log.
- **Attachment Handling**: Supports common image formats (`.jpg`, `.jpeg`, `.png`, `.gif`) and video formats (`.mp4`, `.mov`, `.webm`).

## Prerequisites

- Python 3.x

## Usage

1. **Place the Script**: Ensure the script is located in the main directory containing the subfolders with `_chat.txt` files.
2. **Run the Script**: Execute the script using Python. It will automatically process all `_chat.txt` files in the subfolders and generate corresponding `chat.html` files.
   
   ```bash
   python chat_log_to_html.py
