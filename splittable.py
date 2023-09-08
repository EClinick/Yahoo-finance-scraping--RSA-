from selenium import webdriver
from bs4 import BeautifulSoup
import time
from datetime import datetime, timedelta
# Set up the web driver
driver = webdriver.Edge()

# Get the HTML content from the link

def get_week_dates():
    today = datetime.today()
    #today=+1
    # Calculate the Sunday and Saturday dates of the current week
    sunday = today - timedelta(days=today.weekday())
    saturday = sunday + timedelta(days=6)
    return sunday.strftime('%Y-%m-%d'), saturday.strftime('%Y-%m-%d')

if __name__ == "__main__":
    start_date, end_date = get_week_dates()
    
    # Set start date to be one day ahead of the current date
    start_date = (datetime.today() + timedelta(days=1)).strftime('%Y-%m-%d')
    
    target_date = datetime.today().strftime('%Y-%m-%d')
    
    print("Start Date:", start_date)
    print("End Date:", end_date)
    print("Target Date:", target_date)
    


url = f"https://finance.yahoo.com/calendar/splits?from={start_date}&to={end_date}&day={start_date}"
driver.get(url)

# Wait for the page to fully load
driver.implicitly_wait(10)

# Wait for 5 seconds before closing the web browser window
time.sleep(2)
driver.quit()

# Prompt the user to filter the tickers by their length
filter_by_length = input("Do you want to filter by tickers that only have 3-4 characters? (yes/no): ")

# Set up the web driver again
driver = webdriver.Edge()

# Get the HTML content from the link again
driver.get(url)

# Wait for the page to fully load again
driver.implicitly_wait(10)

# Get the page source
html = driver.page_source

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(html, "html.parser")

# Find all the <a> elements with the data-test attribute set to "quoteLink"
links = soup.find_all("a", {"data-test": "quoteLink"})

# Extract the symbols/tickers and links from the <a> elements
symbols_and_links = []
for link in links:
    symbol = link.text
    href = 'https://finance.yahoo.com' + link["href"]
    symbols_and_links.append((symbol, href))

# Print the symbols/tickers and links
print("The symbols/tickers and their links on that page are:")
for symbol, href in symbols_and_links:
    # Check if the user wants to filter by length and if the symbol has 3-4 characters
    if filter_by_length.lower() == "yes" and len(symbol) not in [3, 4]:
        continue # Skip this symbol if it doesn't meet the criteria
    print(f"{symbol}: {href}")

# Close the web driver again
driver.quit()
