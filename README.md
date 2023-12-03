# Yahoo-finance-scraping--RSA-
Scraping RSA from yahoo finance

In order for this program to run, please ensure that you have the selenium, bs4 (beautifulsoup), time, datetime, pandas, and openpyxl libraries.
From there, all you need to do is run the program and it'll use yahoo to find upcoming reverse splits!

# How to use
1. Run the program,

    Currently there is two programs: one for finding the reverse splits for the week, and one for finding the reverse splits for that day. 

    Yahoo_Scraper_1.0.py is for finding the reverse splits for the day, and Yahoo_Scraper_2.0.py is for finding the reverse splits for the week.

2. Enter yes if you want to search for the week's reverse splits, or no if you want to search for a specific date (no is not currently implemented)
3. Enter yes if you want only Nasdaq/Nyse stocks, or no if you want all stocks 
4. Wait for it to parse through each day, then it'll print out the results at the end
5. If you want to save the results to an excel file, enter yes, otherwise enter no

# Warning:

I've been coding in C++ for a couple months and I'm a little rusty with python, so I'm not sure if this is the most efficient way to do this. If you have suggestions please let me know!

# Future plans:

I hope to add a feature where it will obtain the stock ticker, look up the SEC filings to determine if the reverse split will be beneficial or not, and then filter the beneficial stocks. 

I also hope to add more financial websites to parse.