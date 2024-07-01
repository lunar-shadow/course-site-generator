import os
import re
from datetime import datetime

def generate_html(course_dir, course_name, output_file):
    # Remove only the first occurrence of leading numbers, dots, and spaces
    display_course_name = re.sub(r'^(\d+\.\s*)', '', course_name, 1)
    
    # Get the current year
    current_year = datetime.now().year

    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{display_course_name}</title>
        <link rel="icon" type="image/x-icon" href="/site_generator/favicon.ico">
        <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap" rel="stylesheet">
        <style>
            body {{
                display: flex;
                flex-direction: column;
                height: 100vh;
                margin: 0;
                font-family: 'Roboto', sans-serif;;
                background-color: #f8f9fa;
                color: #343a40;
            }}
            body.dark-mode {{
                background-color: #121212;
                color: #e0e0e0;
            }}
            #header {{
                display: flex;
                align-items: center;
                background-color: #ffffff;
                box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
                padding: 10px 20px;
                z-index: 1000;
            }}
            .dark-mode #header {{
                background-color: #1c1c1c;
            }}
            #toggleSidebar {{
                margin-left: 8px;
                margin-top: 0px;
                font-size: 24px;
                cursor: pointer;
                background: none;
                border: none;
                color: #343a40;
            }}
            .dark-mode #toggleSidebar {{
                color: #e0e0e0;
            }}
            #courseTitle {{
                margin-left: 8px;
                margin-top: 3px;
                font-size: 22px;
                font-weight: 500;
                color: #005ec2;
            }}
            .dark-mode #courseTitle {{
                color: #8f9dff;
            }}
            #homeIcon {{
                font-size: 24px;
                margin-top: 0px;
                cursor: pointer;
                background: none;
                border: none;
                color: #343a40;
            }}
            .dark-mode #homeIcon {{
                color: #e0e0e0;
            }}
            #container {{
                display: flex;
                flex: 1;
                overflow: hidden;
            }}
            #sidebar {{
                width: 20%;
                background-color: #ffffff;
                padding: 20px;
                box-shadow: 2px 0 5px rgba(0, 0, 0, 0.1);
                overflow-y: auto;
                transition: width 0.3s;
                font-size: 14px; /* Adjust the font size as needed */
            }}
            .dark-mode #sidebar {{
                background-color: #1c1c1c;
                /*color: #8db8cb; somehow this isn't refelcting from body */
            }}
            #sidebar.collapsed {{
                width: 0;
                padding: 0;
                overflow: hidden;
            }}
            #content {{
                flex: 1;
                padding: 0px 20px 20px 20px;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                background-color: #ffffff;
                box-shadow: -2px 0 5px rgba(0, 0, 0, 0.1);
                transition: margin-left 0.3s;
            }}
            .dark-mode #content {{
                background-color: #121212;
                color: #8f9dff;
            }}
            .section-title {{
                font-weight: bold;
                font-size: 1.1em;
                margin-top: 20px;
                margin-bottom: 10px;
            }}
            .video-item {{
                margin-bottom: 10px;
                padding: 8px;
                border-radius: 5px;
                transition: background-color 0.3s, color 0.3s;
                font-weight: 100;
                cursor: pointer;
                display: flex;
                align-items: center;
            }}
            .video-item.active, .video-item:hover {{
                background-color: #4876a7;
                color: #ffffff;
            }}
            .dark-mode .video-item.active, .dark-mode .video-item:hover {{
                background-color: #0056b3;
            }}
            iframe {{
                width: 100%;
                height: 80vh;
                /*border: 1px solid #dee2e6;*/
                border-radius: 5px;
            }}
            .radio-button {{
                margin-right: 10px;
            }}
            #toggleDarkMode {{
                margin-left: auto;
                margin-right: 20px;
                font-size: 24px;
                cursor: pointer;
                background: none;
                border: none;
                color: #343a40;
            }}
            .dark-mode #toggleDarkMode {{
                color: #e0e0e0;
            }}
            h2 {{
               font-weight: 400;
               font-size: larger;
            }}
            footer {{
                text-align: center;
                padding: 20px;
                font-size: 0.9em;
                color: #6c757d;
            }}
            .dark-mode footer {{
                color: #adb5bd;
            }}
            footer a {{
                color: #005ec2;
                /*text-decoration: none;*/
            }}
            .dark-mode footer a {{
                color: #ffffff;
            }}
        </style>
    </head>
    <body>
        <div id="header">
            <a id="homeIcon" href="index.html" style="text-decoration:none">&#8962;</a>
            <button id="toggleSidebar">&#9776;</button>
            <div id="courseTitle">{display_course_name}</div>
            <button id="toggleDarkMode">🌙</button>
        </div>
        <div id="container">
            <div id="sidebar">
    """

    sections = [d for d in os.listdir(course_dir) if os.path.isdir(os.path.join(course_dir, d))]
    sections = sorted(sections, key=lambda x: int(x.split('.')[0]) if x.split('.')[0].isdigit() else float('inf'))
    first_video_src = None
    first_video_name= None

    for section in sections:
        section_path = os.path.join(course_dir, section)
        if os.path.isdir(section_path):
            html_content += f'<div class="section-title">{section}</div>\n'
            files = [f for f in os.listdir(section_path) if f.endswith('.mp4')]
            files = sorted(files, key=lambda x: int(x.split('.')[0]) if x.split('.')[0].isdigit() else float('inf'))
            for file in files:
                if file.endswith('.mp4'):
                    relative_path = os.path.relpath(os.path.join(section_path, file), 'site_generator/generated_html')
                    display_name = os.path.splitext(file)[0]
                    if not first_video_src:
                        first_video_src = relative_path
                        html_content += f'<div class="video-item active" data-video-src="{relative_path}">{display_name}</div>\n'
                        first_video_name = display_name # Store the first vido name to be played and assign it in videoTitle
                    else:
                        html_content += f'<div class="video-item" data-video-src="{relative_path}">{display_name}</div>\n'

    html_content += f"""
            </div>
            <div id="content">
                <h2 id="videoTitle">{first_video_name}</h2>
                <iframe id="videoPlayer" src="{first_video_src}" frameborder="0" allowfullscreen></iframe>
            </div>
        </div>
        <footer>
             &copy; {current_year} <a href="https://github.com/lunar-shadow" target="_blank">lunar-shadow</a>. All rights reserved. 
             Licensed under the <a href="https://opensource.org/licenses/MIT" target="_blank" style="color: inherit;">MIT License</a>.
        </footer>
        <script src="../assets/js/script.js"></script> 
    </body>
    </html>
    """

    with open(output_file, 'w') as file:
        file.write(html_content)
