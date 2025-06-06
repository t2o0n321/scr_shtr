import time
import pyautogui
import yaml
from PIL import Image
import os
from datetime import datetime
from img2pdf import convert
import random

def load_config(config_file):
    with open(config_file, 'r') as file:
        return yaml.safe_load(file)

def take_screenshots(config):
    # Create output directory with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = f"screenshots_{timestamp}"
    os.makedirs(output_dir, exist_ok=True)

    # Get config values
    delay_start = config['Times']['delay_to_start']
    min_delay = config['Times'].get('min_delay_between', 2.5)  # Default min delay
    max_delay = config['Times'].get('max_delay_between', 90)  # Default max delay
    pages = config['General']['pages_count']
    next_x = config['Position']['next_page_x']
    next_y = config['Position']['next_page_y']
    # Get screenshot region
    x1 = config['Position']['book_pos_1_x']
    y1 = config['Position']['book_pos_1_y']
    x2 = config['Position']['book_pos_2_x']
    y2 = config['Position']['book_pos_2_y']
    width = x2 - x1
    height = y2 - y1

    # Initial delay
    print(f"Starting in {delay_start} seconds...")
    time.sleep(delay_start)

    image_files = []
    for i in range(pages):
        # Take screenshot of specific region
        screenshot_path = os.path.join(output_dir, f"page_{i+1}.jpg")
        screenshot = pyautogui.screenshot(region=(x1, y1, width, height))
        # Save as JPEG with high quality but smaller size
        screenshot.save(screenshot_path, format="JPEG", quality=85, optimize=True)
        image_files.append(screenshot_path)
        
        print(f"Captured page {i+1}/{pages}")

        # Click next page
        pyautogui.click(next_x, next_y)
        
        # Wait for page load with random delay
        random_delay = random.uniform(min_delay, max_delay)
        print(f"Waiting {random_delay:.2f} seconds before next screenshot...")
        time.sleep(random_delay)

    return output_dir, image_files

def convert_to_pdf(output_dir, image_files):
    pdf_path = os.path.join(output_dir, "output.pdf")
    with open(pdf_path, "wb") as f:
        f.write(convert(image_files))
    return pdf_path

def main():
    try:
        # Load configuration
        config = load_config('conf.yaml')
        
        # Take screenshots
        output_dir, image_files = take_screenshots(config)
        
        # Convert to PDF
        pdf_path = convert_to_pdf(output_dir, image_files)
        
        print(f"PDF created successfully at: {pdf_path}")
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()