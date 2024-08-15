import os
import re

# Maximum height for thumbnails in pixels
thumbnail_height = 300

# Predefined colors (meeting contrast requirement of 4.5:1 against white background)
colors = [
    '#000000', '#003366', '#003d3f', '#003e3b', '#003f4f',
    '#004d00', '#005a4c', '#005c5c', '#006400', '#006d77',
    '#007a7a', '#008080', '#004d00', '#006600', '#003c00',
    '#003f5c', '#003d34', '#006700', '#003f7f', '#00336e'
]

# Regex pattern to match attachments
attachment_regex = re.compile(r'‎\[?(\d{1,2}\.\d{1,2}\.\d{4}, \d{2}:\d{2}:\d{2})]?\s*(.*?):\s*‎?<załączono: (.*?)>')

# Regex pattern to match message sender and time
message_regex = re.compile(r'\[(\d{1,2}\.\d{1,2}\.\d{4}, \d{2}:\d{2}:\d{2})\] (.*?): (.*)')

def get_color(user):
    """Returns a color assigned to the user, cyclically selecting from the predefined list."""
    # Use hash of the user's name to ensure different colors for different users
    index = hash(user) % len(colors)
    return colors[index]

def parse_chat_to_html(chat_file_path, folder_name):
    """Parses the _chat.txt file and converts it to HTML format."""
    with open(chat_file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    html_content = f"<html><head><title>{folder_name}</title></head><body>\n"

    for line in lines:
        attachment_match = attachment_regex.match(line)
        message_match = message_regex.match(line)
        
        if attachment_match:
            # If the line contains an attachment
            timestamp, user, attachment = attachment_match.groups()
            ext = os.path.splitext(attachment)[1].lower()

            if ext in ['.jpg', '.jpeg', '.png', '.gif']:
                # Image
                html_content += (
                    f'<p><strong>{timestamp} {user}:</strong> <br>'
                    f'<a href="{attachment}" target="_blank">'
                    f'<img src="{attachment}" style="max-height:{thumbnail_height}px;"></a></p>\n'
                )
            elif ext in ['.mp4', '.mov', '.webm']:
                # Video
                html_content += (
                    f'<p><strong>{timestamp} {user}:</strong> <br>'
                    f'<a href="{attachment}" target="_blank">'
                    f'<video width="auto" height="{thumbnail_height}" controls>'
                    f'<source src="{attachment}" type="video/{ext[1:]}">'
                    'Your browser does not support this video format.'
                    '</video></a></p>\n'
                )
            else:
                # Other file types
                html_content += (
                    f'<p><strong>{timestamp} {user}:</strong> <br>'
                    f'<a href="{attachment}" target="_blank">{attachment}</a></p>\n'
                )
        elif message_match:
            # If the line contains a message
            timestamp, user, message = message_match.groups()
            color = get_color(user)  # Generate color based on the sender
            html_content += (
                f'<p style="color:{color};"><strong>{timestamp} {user}:</strong> {message}</p>\n'
            )
        else:
            # Line does not match any pattern
            html_content += f'<p>{line.strip()}</p>\n'

    html_content += "</body></html>\n"
    return html_content

# Get the current directory (where the script is located)
current_directory = os.getcwd()

# Flag to check if there are any files to process
files_found = False

# Iterate through all subfolders and _chat.txt files
for root, dirs, files in os.walk(current_directory):
    for file in files:
        if file == '_chat.txt':
            files_found = True
            full_path = os.path.join(root, file)

            # Get the name of the parent folder as the HTML title
            folder_name = os.path.basename(root)
            if folder_name.startswith("WhatsApp Chat - "):
                folder_name = folder_name[len("WhatsApp Chat - "):]

            html_content = parse_chat_to_html(full_path, folder_name)

            # Save the processed chat as an HTML file
            html_file_path = os.path.join(root, 'chat.html')
            with open(html_file_path, 'w', encoding='utf-8') as html_file:
                html_file.write(html_content)

if not files_found:
    print("No '_chat.txt' files found in the directory.")
else:
    print("Processing completed.")
