import os
import http.server
import socketserver
import subprocess
import platform
import shutil
import sys
import webbrowser
from site_generator.generate_pages import generate_html 
from site_generator.generate_homepage import generate_index_html
from functools import lru_cache

# Create generated_html directory if it doesn't exist
html_dir = 'site_generator/generated_html'
if not os.path.exists(html_dir):
    os.makedirs(html_dir)

# Define a custom request handler to handle BrokenPipeError
class CustomRequestHandler(http.server.SimpleHTTPRequestHandler):
    def handle_one_request(self):
        try:
            super().handle_one_request()
        except BrokenPipeError:
            # Client closed the connection unexpectedly
            pass

# Function to check if the browser is available
def is_browser_available(browser_path):
    return os.path.exists(browser_path) or shutil.which(browser_path) is not None

# Dictionary to store browser paths for different platforms
browser_paths = {
    '2': {
        "Darwin": "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser",
        "Windows": "C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe",
        "Linux": "/usr/bin/brave-browser"
    },
    '3': {
        "Darwin": "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "Windows": "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
        "Linux": "/usr/bin/google-chrome"
    },
    '4': {
        "Darwin": "/Applications/Firefox.app/Contents/MacOS/firefox",
        "Windows": "C:\\Program Files\\Mozilla Firefox\\firefox.exe",
        "Linux": "/usr/bin/firefox"
    }
}

# Function to open the URL in the specified browser
def open_in_browser(url, browser_choice):
    if browser_choice in browser_paths:
        browser_path = browser_paths[browser_choice].get(platform.system())
        if browser_path and is_browser_available(browser_path):
            subprocess.Popen([browser_path, url])
            return True
        else:
            raise Exception(f"Browser path not found or browser is not installed: {browser_path}")
    else:
        return False

# Automatically find course directories
current_directory = os.path.dirname(os.path.abspath(__file__))
directories = [d for d in os.listdir(current_directory) if os.path.isdir(os.path.join(current_directory, d)) and d not in ('site_generator') and not d.startswith('.')]

if not directories:
    raise Exception("No course directories found.")

# Cache the results of generating HTML files
@lru_cache(maxsize=None)
def generate_html_cached(course_dir, output_file):
    generate_html(course_dir, course_dir, output_file)

# Generate HTML files for courses
courses = []
for course_dir in directories:
    output_file = os.path.join(html_dir, f"{course_dir}.html")
    generate_html_cached(course_dir, output_file)
    courses.append({'name': course_dir, 'file': output_file})

# Generate homepage (index.html) file
generate_index_html(courses, current_directory)

print(f'Course site generated successfully with {len(courses)} courses.')

# Prompt the user for browser selection
print("Select the browser you want to use:")
print("1. Default (Safari on Mac OS / Edge on Windows)")
print("2. Brave")
print("3. Google Chrome")
print("4. Firefox")
browser_choice = input("Choose a browser to open: ").strip()

# Check if the selected browser is available
if browser_choice in browser_paths:
    browser_path = browser_paths[browser_choice].get(platform.system())
    if not is_browser_available(browser_path):
        print(f"Browser {browser_path} not found or not installed. Exiting...")
        sys.exit(1)

# Start an HTTP server to serve the course site
port = 8000
httpd = None
while True:
    try:
        handler = CustomRequestHandler
        httpd = socketserver.ThreadingTCPServer(("", port), handler)  # Use ThreadingTCPServer for threaded handling
        print(f"HTTP server started at port {port}")

        # Update URL with the current port
        url = f"http://localhost:{port}/site_generator/generated_html/index.html"

        # Open the course site in the specified web browser
        if browser_choice == '1':
            # Default browser handling
            if not webbrowser.open(url):
                raise Exception("Failed to open default browser.")
        else:
            # Open in selected browser
            if not open_in_browser(url, browser_choice):
                print(f"Failed to open the selected browser ({browser_choice}). Opening in default browser.")
                webbrowser.open(url)  # Fallback to default browser

        # Serve the course site indefinitely
        httpd.serve_forever()
    except OSError as e:
        if e.errno == 48:  # Address already in use
            print(f"Port {port} is already in use, trying the next port...")
            port += 1
            if httpd:
                httpd.server_close()
        else:
            raise Exception(f"Error: {e}")
    except KeyboardInterrupt:
        print("\nShutting down server...")
        if httpd:
            httpd.shutdown()
            httpd.server_close()
        print("Server stopped.")
        sys.exit(0)
    except Exception as e:
        print(e)
        if httpd:
            httpd.shutdown()
            httpd.server_close()
        print("Exiting...")
        sys.exit(1)
