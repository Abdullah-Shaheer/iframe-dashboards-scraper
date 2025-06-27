import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime


def set_up_driver():
    options = webdriver.ChromeOptions()
    # options.debugger_address = "localhost:9222"
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    return driver


def scrape_the_content(soup):
    # Extract all headers
    headers = []
    header_elements = soup.find_all('div', {'role': 'columnheader'})[1:]
    for header in header_elements:
        headers.append(header.get_text(strip=True))

    print(f"Found {len(headers)} columns: {headers}")

    scraped_data = []
    row_elements = soup.find_all('div', {'role': 'row'})[1:]  # Skip the header row

    for row in row_elements:
        cells = row.find_all('div', {'role': 'gridcell'})[1:]
        if not cells:
            continue

        row_data = {}
        row_data["time_stamp"] = datetime.now().strftime("%Y:%m:%d %H:%M:%S")
        for idx, cell in enumerate(cells):
            if idx < len(headers):
                row_data[headers[idx]] = cell.get_text(strip=True)

        scraped_data.append(row_data)

    return scraped_data


def random_click_inside_iframe(driver):
    try:
        html = driver.find_element(By.TAG_NAME, 'html')
        ActionChains(driver).move_to_element_with_offset(html, 100, 100).click().perform()
        print("Random click performed inside iframe successfully.")
    except Exception as e:
        print(f"Error while trying random click inside iframe: {str(e)}")


def move_on(driver):
    c = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//a[@class='fusion-button button-flat fusion-button-default-size button-default fusion-button-default button-1 fusion-button-span-yes fusion-button-default-type']")))
    driver.execute_script('arguments[0].scrollIntoView(true);', c)
    driver.execute_script('arguments[0].click();', c)


def check_for_scroller(driver):
    try:
        scroller = driver.find_element(By.CLASS_NAME, "scroll-bar-part-bar")
        print('scrolling required')
        return True
    except:
        print('There is no scrolling required!')
        return False


def go_and_scrape_dashboard(driver, link):
    all_rows = []
    target_url = link
    iframe_locator = (By.TAG_NAME, "iframe")
    try:
        print(f"[INFO] Navigating to: {target_url}")
        driver.get(target_url)
        move_on(driver)
        try:
            element = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//h3[@class='fusion-responsive-typography-calculated']")))
            driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'end'});", element)
            print("[INFO] Page loaded and element brought to top.")
        except Exception as e:
            print(f"[ERROR] Could not locate or scroll to main element: {e}")

        try:
            print(f"[INFO] Waiting for iframe to be available...")
            wait = WebDriverWait(driver, 40)
            wait.until(EC.frame_to_be_available_and_switch_to_it(iframe_locator))
            print("[SUCCESS] Switched into iframe successfully.")

        except Exception as e:
            print(f"[ERROR] Could not find or switch into iframe: {e}")
            return all_rows

        # try:
        #     print("[INFO] Attempting to click inside iframe...")
        #     iframe_element = driver.find_element(*iframe_locator)
        #     ActionChains(driver).move_to_element(iframe_element).click().perform()
        #     print("[SUCCESS] Clicked inside iframe.")
        # except Exception as e:
        #     print(f"[WARNING] Could not click inside iframe: {e}")

        try:
            print("[INFO] Waiting for dashboard content...")
            random_click_inside_iframe(driver)
            WebDriverWait(driver, 500).until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "row ")))
            time.sleep(3)
        except Exception as e:
            print(f"[ERROR] Dashboard main content not found: {e}")
            return all_rows

        try:
            pass
            # print("[INFO] Attempting to enable full-screen mode with REAL click...")
            # full_screen_button = WebDriverWait(driver, 20).until(
            #     EC.presence_of_element_located((By.XPATH, "//button[@aria-label='Open in full-screen mode']"))
            # )
            # full_screen_button.click()
            # actions = ActionChains(driver)
            # actions.move_to_element(full_screen_button)
            # actions.click_and_hold()
            # actions.pause(0.2)
            # actions.release()
            # actions.perform()

            # print("[SUCCESS] Full-screen mode enabled with real user simulation.")
        except Exception as e:
            print(f"[WARNING] Full-screen button not found or could not click: {e}")

        try:
            print("[INFO] Checking for scrollable area...")
            if check_for_scroller(driver):
                print("[INFO] Scrollable area detected. Starting scrolling and scraping...")
                scrollable = WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located((By.CLASS_NAME, "scrollable-cells-viewport"))
                )
                ActionChains(driver).move_to_element(scrollable[1]).click().perform()
                # driver.execute_script('arguments[0].click();', scrollable)
                time.sleep(3)
                # driver.execute_script('arguments[0].click();', scrollable)
                # element = WebDriverWait(driver, 20).until(EC.presence_of_element_located(
                #     (By.XPATH, "//h3[@class='fusion-responsive-typography-calculated']")))
                # driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'end'});", element)
                for _ in range(100):
                    driver.execute_script("""
                        var event = new KeyboardEvent('keydown', {
                            key: 'PageDown',
                            code: 'PageDown',
                            keyCode: 34,
                            which: 34,
                            bubbles: true
                        });
                        document.activeElement.dispatchEvent(event);
                    """)
                    soup = BeautifulSoup(driver.page_source, "lxml")
                    rows = scrape_the_content(soup)
                    all_rows.extend(rows)
                print("[SUCCESS] Scrolling and scraping completed.")
            else:
                print("[INFO] No scrollable detected, scraping current page...")
                soup = BeautifulSoup(driver.page_source, "lxml")
                rows = scrape_the_content(soup)
                all_rows.extend(rows)
                print("[SUCCESS] Scraping without scrolling completed.")
        except Exception as e:
            print(f"[ERROR] Problem while scrolling/scraping: {e}")

    except Exception as e:
        print(f"[FATAL] Unexpected error in main block: {e}")

    finally:
        # try:
        #     print("[INFO] Attempting to exit full-screen mode...")
        #     close_button = driver.find_element(By.XPATH, "//button[@aria-label='Close full-screen mode']")
        #     close_button.click()
        #     print("[SUCCESS] Exited full-screen mode.")
        #     time.sleep(2)
        # except Exception as e:
        #     print(f"[WARNING] Could not exit full-screen mode properly: {e}")

        try:
            print("[INFO] Switching back to main content...")
            driver.switch_to.default_content()
            print("[SUCCESS] Switched back to main page.")
        except Exception as e:
            print(f"[WARNING] Could not switch back to default content: {e}")

    return all_rows


def main():
    dri = set_up_driver()
    sal = go_and_scrape_dashboard(dri, link='https://mtglaw.com/foreclosure-sales/')
    df = pd.DataFrame(sal)
    df.replace('', pd.NA, inplace=True)
    df.dropna(how='all', inplace=True)

    if "time_stamp" in df.columns:
        df_no_timestamp = df.drop(columns=["time_stamp"])
        df = df.loc[~df_no_timestamp.duplicated()].reset_index(drop=True)
    else:
        df.drop_duplicates(inplace=True)
        df.reset_index(drop=True, inplace=True)

    print(df.head())
    df.to_csv('mtglaw_data.csv', index=False)
    df.to_excel('mtglaw_data.xlsx', index=False)
    print('[+] csv and excel files generated')


if __name__ == "__main__":
    main()
