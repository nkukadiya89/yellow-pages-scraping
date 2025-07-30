# YellowPages.ca Business Scraper

This Python script scrapes business listing data (e.g., restaurants, dentists, etc.) from [YellowPages.ca](https://www.yellowpages.ca) using **Selenium** and **BeautifulSoup**, and saves the results into a CSV file.

---

## Features

- Scrapes:
  - Business Name
  - Address
  - Phone Number
  - Rating (with fallback to "N/A" if missing)
  - Review Count
- Headless Chrome browser
- Adjustable category and city
- Saves results in CSV file
- Supports pagination (first 10 pages)

---

## Requirements

Install the required libraries with:

```bash
pip install selenium beautifulsoup4 pandas webdriver-manager
