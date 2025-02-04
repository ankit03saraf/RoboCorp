from robocorp import browser
from playwright.sync_api import sync_playwright

def install_chromium():
    with sync_playwright() as p:
        # This will install Chromium if it's not already installed
        p.chromium.install()

def setup():
    print("Installing Chromium browser...")
    install_chromium()

if __name__ == "__main__":
    setup()