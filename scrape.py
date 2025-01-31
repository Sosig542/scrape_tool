import os
import time
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from urllib.parse import urljoin
import requests

# Set up Selenium WebDriver with Microsoft Edge
edge_options = Options()
edge_options.add_argument("--headless")  # Run in headless mode (no browser window)
edge_options.add_argument("--disable-gpu")
edge_driver_path = (
    r".\msedgedriver.exe"  # Update this to the location of your msedgedriver
)

# Initialize WebDriver for Edge
driver = webdriver.Edge(service=Service(edge_driver_path), options=edge_options)


# Function to download images from a dynamic page using Selenium
def download_images(url):
    # Open the webpage using Selenium
    driver.get(url)

    # Wait for the page to fully load (adjust time if needed)
    time.sleep(5)  # Wait 5 seconds for images to load

    # Get all list item elements on the page
    items = driver.find_elements(By.TAG_NAME, "li")

    # Create a directory to save images
    if not os.path.exists("images"):
        os.makedirs("images")

    # Loop through all list items
    for item in items:
        try:
            # Get the image element and product name element
            img = item.find_element(By.TAG_NAME, "img")
            product_name_element = item.find_element(By.XPATH, ".//strong/span")

            # Get the image URL and product name
            img_url = img.get_attribute("src")
            product_name = product_name_element.text.strip().replace(
                " ", "_"
            )  # Replace spaces with underscores
            img_name = os.path.join("images", f"{product_name}.jpg")

            # Download the image
            img_data = requests.get(img_url).content

            # Save the image
            with open(img_name, "wb") as f:
                f.write(img_data)
            print(f"Downloaded {img_name}")
        except Exception as e:
            print(f"Failed to download image: {e}")


# URL of the product page you want to scrape
url = "https://www.gsmarena.com/apple-phones-48.php"

# Call the function to download images
download_images(url)

# Close the driver after scraping
driver.quit()
