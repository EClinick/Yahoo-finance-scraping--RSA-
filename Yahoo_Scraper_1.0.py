#Old version

from selenium import webdriver
from bs4 import BeautifulSoup
import time
from datetime import datetime, timedelta
import sys
# Set up the web driver
driver = webdriver.Edge()

# Get the HTML content from the link

def get_week_dates():
    today = datetime.today()
    # Calculate the next Sunday date
    days_ahead = 6 - today.weekday()  # Number of days until next Sunday
    if days_ahead < 0:  # If today is Sunday, get date for next Sunday
        days_ahead += 7
    sunday = today + timedelta(days=days_ahead)
    # Calculate the Saturday date of the next week
    saturday = sunday + timedelta(days=6)
    return sunday.strftime('%Y-%m-%d'), saturday.strftime('%Y-%m-%d')

if __name__ == "__main__":
    start_date, end_date = get_week_dates()
    
    # Set start date to be one day ahead of the current date
    start_date = (datetime.today() + timedelta(days=1)).strftime('%Y-%m-%d')
    
    target_date = datetime.today().strftime('%Y-%m-%d')
    
    print("Start Date:", start_date)
    print("End Date:", end_date)# end_date= 2023-12-09
    print("Target Date:", target_date) #target_date= 2023-12-02
    
    


url = f"https://finance.yahoo.com/calendar/splits?from={start_date}&to={end_date}&day={start_date}"
#url=f"https://finance.yahoo.com/calendar/splits?from=2023-12-03&to=2023-12-09"
driver.get(url)
print(url)
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
filtered_symbols_and_links = []
for symbol, href in symbols_and_links:
    # Check if the user wants to filter by length and if the symbol has 3-4 characters
    if filter_by_length.lower() == "yes" and len(symbol) not in [3, 4]:
        continue # Skip this symbol if it doesn't meet the criteria
    filtered_symbols_and_links.append((symbol, href))

if not filtered_symbols_and_links:
    print("None closing program...") # Print "None" if there are no stocks with 3-4 characters
    sys.exit() # Exit the program if there are no stocks with 3-4 characters
for symbol, href in filtered_symbols_and_links:
    print(f"{symbol}: {href}")

# Close the web driver again
driver.quit()
