from robocorp.tasks import task
from robocorp import browser
from RPA.Tables import Tables
from RPA.HTTP import HTTP
from RPA.PDF import PDF
import time
import zipfile
import os
from playwright.sync_api import sync_playwright
import subprocess
import sys

@task
def order_robots_from_RobotSpareBin():
    """Orders robots from RobotSpareBin Industries Inc.
        Saves the order HTML receipt as a PDF file.
        Saves the screenshot of the ordered robot.
        Embeds the screenshot of the robot to the PDF receipt.
        reates ZIP archive of the receipts and the images."""
    
    install_chromium()
    #setup()
    browser.configure(browser_engine="chrome", slowmo=1000)
    
    try:
        open_robot_order_website()
        #fill_order_robot()
        download_order_csv_file()
        read_order_file()
    except:
        browser.page().screenshot(path="output/Error Screenshot.png")


def open_robot_order_website():
    """Open robot order website"""
    browser.goto("https://robotsparebinindustries.com/#/robot-order")


def fill_order_robot(order):
    order_num = str(order["Order number"])
    page = browser.page()
    page.click("text=OK")
    page.select_option("#head", str(order["Head"]))
    idval = str(order["Body"])
    page.click(f"#id-body-{idval}")
    page.fill("input[placeholder='Enter the part number for the legs']", str(order["Legs"]))
    page.fill("#address", str(order["Address"]))
    page.click("#order")
    # print("waiting start")
    # time.sleep(5)
    # print("waiting end")
    #error_indicator = page.query_selector_all(".alert alert-danger")
    try:
        print("printing type")
        print(type(page.wait_for_selector("#order-another", timeout=3000)))
        print("printed type")
        page.wait_for_selector("#order-another", timeout=3000)
        get_robot_details_pfd(order_num)
        '''page.wait_for_selector("#order-another")'''
        page.click("#order-another")

    except:
        while_count = 1
        while while_count < 5:
            #page.screenshot(path=str(f"output/Runtime error_{while_count}.pdf"))
            print(f"while counter value is : {while_count}")
            page.click("#order")
            try:
                page.wait_for_selector("#order-another", timeout=3000)
                get_robot_details_pfd(order_num)
                page.click("#order-another")
                break
            #error_indicator = page.wait_for_selector(".alert alert-danger")
            except:
                while_count+=1

        # error_indicator = page.wait_for_selector(".alert alert-danger")
        # print(f"value of error indicator is : str{error_indicator}")
        # if error_indicator:
        #     while_count = 1
        #     while error_indicator or while_count < 5:
        #         page.screenshot(path=str(f"output/Runtime error_{while_count}.pdf"))
        #         print(f"while counter value is : {while_count}")
        #         page.click("#order")
        #         error_indicator = page.wait_for_selector(".alert alert-danger")
        #         while_count+=1
        # else:
        #     get_robot_details_pfd(order_num)
        #     '''page.wait_for_selector("#order-another")'''
        #     page.click("#order-another")


def download_order_csv_file():
    """This will download Order csv"""
    http = HTTP()
    http.download("https://robotsparebinindustries.com/orders.csv", overwrite=True)


def read_order_file():
    """This will read Order csv as a table"""
    table = Tables()
    dt = table.read_table_from_csv("orders.csv", header=True)

    for row in dt:
        fill_order_robot(row)

    # row_count = 1
    # for row in dt:
    #     if row_count<=5:
    #         fill_order_robot(row)
    #         row_count+=1
    #     else:
    #         pass
        

def get_robot_details_pfd(value):
    """Get robot details and put in PDF"""
    page = browser.page()
    page.wait_for_selector("#receipt", timeout=5000)
    order_result_html = page.locator("#receipt").inner_html()
    screenshot_path = str(f"output/Robot Screenshot_{value}.png")
    screenshot = page.screenshot(path= screenshot_path)
    #robot_image_html = page.locator("#robot-preview-image").inner_html()

    pdf = PDF()
    generated_pdf_name = str(f"output/Order result for order_{value}.pdf")
    pdf.html_to_pdf(order_result_html, generated_pdf_name)
    
    embed_screenshot_to_receipt(screenshot_path, generated_pdf_name)
    create_zip(generated_pdf_name)


def embed_screenshot_to_receipt(xx, yy):
    """add image to pdf"""
    pdf = PDF()
    pdf.add_files_to_pdf(files = [xx], target_document= yy, append = True)


def create_zip(file_name):
    zip_file_name = "output/Output_pdf.zip"
    with zipfile.ZipFile(zip_file_name, 'a') as zipf:
        zipf.write(file_name, os.path.basename(file_name))


# # Function to install Chromium browser using Playwright
# def install_chromium():
#     with sync_playwright() as p:
#         p.chromium.install()

# # Setup step to ensure Chromium is installed
# def setup():
#     print("Setting up environment...")
#     install_chromium()


def install_playwright():
    subprocess.run(["pip", "install", "playwright"], check=True)
    subprocess.run(["playwright", "install", "chromium"], check=True)

def setup():
    print("Installing Playwright and Chromium...")
    install_playwright()


def install_chromium():
    try:
        # Install Playwright if not installed
        subprocess.check_call([sys.executable, "-m", "pip", "install", "playwright"])
        # Install Chromium via Playwright
        subprocess.check_call([sys.executable, "-m", "playwright", "install", "chromium"])
        print("Chromium has been installed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to install Chromium: {e}")









    


    

