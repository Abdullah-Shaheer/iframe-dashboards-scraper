# 🕷️ Power BI Dashboard Scraper - MTGLaw & Logs.com

This Python-based scraper extracts real-time data from **Power BI dashboards** embedded in two foreclosure sales websites:

- [logs.com - All Sales](https://www.logs.com/all-sales.html)
- [mtglaw.com - Foreclosure Sales](https://mtglaw.com/foreclosure-sales/)

The scraper handles dynamic content loading by scrolling through iframe-embedded Power BI tables to extract all visible data.

---

## 📌 Summary

Websites using Power BI dashboards often **do not render all data at once**. Instead, they load rows dynamically as the user scrolls.

This scraper works by:

1. **Switching to the Power BI iframe**
2. **Scrolling down once**
3. **Scraping the currently loaded data**
4. **Repeating scroll → scrape process** until all data is collected

---

## 📂 Target Sites

- 🔗 https://www.logs.com/all-sales.html  
- 🔗 https://mtglaw.com/foreclosure-sales/

---

## 🛠️ Features

- ✅ Handles **iframe navigation** to access Power BI content
- ✅ Scroll-based scraping of dynamically rendered tables
- ✅ Uses `Selenium` to simulate real user scrolling
- ✅ Extracts only **visible HTML elements**, ensuring no empty rows
- ✅ Customizable scroll delay and stopping condition

---

## 🚀 Setup & Installation

### Requirements

```bash
pip install selenium pandas bs4
```
### Make sure you have
1. Google Chrome installed
2. Matching version of ChromeDriver in your system PATH

## 🧠 How it works
1. Load the target page in Selenium.
2. Switch context to the embedded Power BI iframe.
3. Scroll down using JavaScript or Selenium's send_keys.
4. Wait for new rows to load.
5. Parse visible data from the DOM using BeautifulSoup or Selenium selectors.
6. Repeat the scroll + extract loop until end of table is detected.

# Thank you so much
