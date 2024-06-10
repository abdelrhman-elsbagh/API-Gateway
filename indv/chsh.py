import subprocess

def clear_cache():
    subprocess.run(["chromium-browser", "--headless", "--disable-gpu", "--remote-debugging-port=9222", "--user-data-dir=$(mktemp -d)", "about:blank"])
