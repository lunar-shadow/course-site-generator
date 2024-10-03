import os
import re
import datetime

def generate_index_html(courses, current_directory):
    # Extract the base name of the current directory to use as the title
    directory_name = os.path.basename(current_directory)

    # Get the current year
    current_year = datetime.datetime.now().year

    # HTML content for the index page
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{directory_name}</title> 
        <link rel="icon" type="image/x-icon" href="/site_generator/favicon.ico">
        <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap" rel="stylesheet">
        <script src="../assets/js/script.js"></script>
        <style>
            body {{
                font-family: 'Roboto', sans-serif;
                background-color: #d7d9da; /* previously f8f9fa */
                color: #343a40;
                margin: 0;
                padding: 20px;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                transition: background-color 0.3s;
            }}
            body.dark-mode {{
                background-color: #121212;
                color: #e0e0e0;
            }}
            h1 {{
                color: #4876a7;
                font-weight: 400;
            }}
            .dark-mode h1 {{
                color: #818ee5;
            }}
            .course-container {{
                display: flex;
                flex-wrap: wrap;
                justify-content: center;
                gap: 20px;
            }}
            .course-card {{
                background-color: #ffffff;
                border-radius: 10px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                overflow: hidden;
                width: 200px;
                text-align: center;
                transition: transform 0.2s;
            }}
            .dark-mode .course-card {{
                background-color: #4f578d;
                color: #e0e0e0;
                box-shadow: 0 4px 6px rgba(255, 255, 255, 0.1);
            }}
            .course-card:hover {{
                transform: scale(1.05);
            }}
            .course-card a {{
                display: block;
                color: #343a40;
                text-decoration: none;
                padding: 20px;
            }}
            .dark-mode .course-card a {{
                color: #e0e0e0;
            }}
            .course-card h3 {{
                margin: 0;
                font-size: 1.2em;
                font-weight: 400;
            }}
            .course-card img {{
                width: 60px;
                height: 60px;
                margin-bottom: 10px;
            }}
            .dark-icon {{
                display: none;
            }}
            .dark-mode .light-icon {{
                display: none;
            }}
            .dark-mode .dark-icon {{
                display: inline;
            }}
            .switch {{
                position: fixed;
                top: 9px;
                right: 20px;
                width: 60px;
                height: 34px;
            }}
            .switch input {{
                opacity: 0;
                width: 0;
                height: 0;
            }}
            .slider {{
                position: absolute;
                cursor: pointer;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background-color: #969696;
                transition: .4s;
                border-radius: 34px;
            }}
            .slider:before {{
                position: absolute;
                content: "";
                height: 26px;
                width: 26px;
                left: 4px;
                bottom: 4px;
                background-color: black;
                transition: .4s;
                border-radius: 50%;
            }}
            input:checked + .slider {{
                background-color: #6190fe;
            }}
            input:checked + .slider:before {{
                transform: translateX(26px);
            }}
            .slider:before {{
                content: '\\263E';  /* Unicode for moon */
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 18px;
                color: #ffeb3b;
            }}
            input:checked + .slider:before {{
                content: '\\2600';  /* Unicode for sun */
                color: #ffeb3b;
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
            }}
            .dark-mode footer a {{
                color: #ffffff;
            }}
        </style>
    </head>
    <body>
        <h1>{directory_name}</h1>
        <div class="course-container">
    """

    # Sort courses based on the number in their names
    sorted_courses = sorted(courses, key=lambda x: int(x['name'].split('.')[0]) if x['name'].split('.')[0].isdigit() else float('inf'))

    for course in sorted_courses:
        course_name = course['name']
        course_file = course['file']
        
        # Remove only the first occurrence of leading numbers, dots, and spaces
        display_course_name = re.sub(r'^(\d+\.\s*)', '', course_name, 1)

        # Make sure the link points directly to the course file within the generated_html directory
        html_content += f"""
            <div class="course-card">
                <a href="{os.path.basename(course_file)}">
                    <img src="../assets/images/light-video-icon.svg" alt="Light Video Icon" class="light-icon">
                    <img src="../assets/images/dark-video-icon.svg" alt="Dark Video Icon" class="dark-icon">
                    <h3>{display_course_name}</h3>
                </a>
            </div>
        """

    # Add footer with copyright notice
    html_content += f"""
        </div>
        <label class="switch">
            <input type="checkbox" id="darkModeToggle">
            <span class="slider"></span>
        </label>
        <footer>
             &copy; {current_year} <a href="https://github.com/lunar-shadow" target="_blank">lunar-shadow</a>. All rights reserved. 
             Licensed under the <a href="https://github.com/lunar-shadow/course-site-generator/blob/main/LICENSE.txt" target="_blank" style="color: inherit;">MIT License</a>.
        </footer>
    </body>
    </html>
    """

    # Write the generated HTML content to the index.html file in the generated_html directory
    output_file = os.path.join('site_generator/generated_html', 'index.html')
    with open(output_file, 'w') as file:
        file.write(html_content)

    print(f"Generated {output_file} successfully.")
