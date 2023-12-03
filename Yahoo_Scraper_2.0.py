from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
from datetime import datetime, timedelta
import pandas as pd
import sys

class StockSplitScraper:
    def __init__(self):
        self.symbols_and_links = []
        # URL initialization commented as it's not used here

    def get_week_dates(self):
        today = datetime.today()
        # Calculate the next Sunday date
        days_ahead = 6 - today.weekday()  # Number of days until next Sunday
        if days_ahead < 0:  # If today is Sunday, get date for next Sunday
            days_ahead += 7
        sunday = today + timedelta(days=days_ahead)
        # Calculate the Saturday date of the next week
        saturday = sunday + timedelta(days=6)
        return sunday.strftime('%Y-%m-%d'), saturday.strftime('%Y-%m-%d')

    def get_page_content(self, url):
        options = Options()
        options.add_argument("--headless")  # Run in headless mode
        options.add_argument("--log-level=3")  # Suppress logging
        options.add_experimental_option('excludeSwitches', ['enable-logging'])  # Suppress logging
        self.driver = webdriver.Edge()
        self.driver.get(url)
        # Wait for the page to fully load
        self.driver.implicitly_wait(10)
        # Wait for 5 seconds before closing the web browser window
        time.sleep(2)
        # Get the page source
        return self.driver.page_source

    def parse_page_content(self, html):
        soup = BeautifulSoup(html, "html.parser")
        # Find all the <a> elements with the data-test attribute set to "quoteLink"
        links = soup.find_all("a", {"data-test": "quoteLink"})
        # Extract the symbols/tickers and links from the <a> elements
        for link in links:
            symbol = link.text
            href = 'https://finance.yahoo.com' + link["href"]
            self.symbols_and_links.append((symbol, href))

    def filter_symbols_and_links(self, filter_by_length):
        filtered_symbols_and_links = []
        
        for symbol, href in self.symbols_and_links:
            # Check if the user wants to filter by length and if the symbol has 3-4 characters
            if filter_by_length.lower() == "yes" and len(symbol) not in [3, 4]:
                continue  # Skip this symbol if it doesn't meet the criteria
            filtered_symbols_and_links.append((symbol, href))
        
        if not filtered_symbols_and_links:
            print("None closing program...")  # Print "None" if there are no stocks with 3-4 characters
            return []
        else:
            return filtered_symbols_and_links

    def run(self):
        all_symbols_and_links = []  # Using a list for collected symbols and links
        see_week_splits = input("Do you want to see the stock splits for the week? (yes/no): ")
        if see_week_splits.lower() == "yes":
            filter_by_length = input("Do you want to filter by tickers that only have 3-4 characters? (yes/no): ")
            start_date, end_date = self.get_week_dates()
            for day in range(7):
                self.symbols_and_links = []  # Reset the list for each day
                date = datetime.strptime(start_date, '%Y-%m-%d') + timedelta(days=day)
                date_str = date.strftime('%Y-%m-%d')
                print("Date:", date_str)
                url = f"https://finance.yahoo.com/calendar/splits?from={start_date}&to={end_date}&day={date_str}"
                print(url)
                html = self.get_page_content(url)
                self.parse_page_content(html)
                day_symbols_and_links = self.filter_symbols_and_links(filter_by_length)
                
                # Manually check for duplicates before adding
                for symbol, href in day_symbols_and_links:
                    if (symbol, href) not in all_symbols_and_links:
                        all_symbols_and_links.append((symbol, href))
            
            self.driver.quit()
            
            # Print the final list
            for symbol, href in all_symbols_and_links:
                print(f"{symbol}: {href}")

            # Ask user if they want to save the data to an Excel file
            save_to_excel = input("Do you want to save the stock splits data to an Excel file? (yes/no): ")
            if save_to_excel.lower() == 'yes':
                df = pd.DataFrame(all_symbols_and_links, columns=['Symbol', 'Link'])
                filename = 'stock_splits.xlsx'
                df.to_excel(filename, index=False)
                print(f"Data saved to {filename}")
        else:
            # Your existing code to print all tickers here
            pass



if __name__ == "__main__":
    scraper = StockSplitScraper()
    scraper.run()
