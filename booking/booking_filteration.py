from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException
import time

class BookingFilteration:
    def __init__(self, driver: WebDriver):
        self.driver = driver
    

    def check_and_close_popup(self):
        try:
            print("檢查是否有彈跳視窗")


            popup_selectors = [
                (By.CSS_SELECTOR, "button[aria-label='關閉']"),
                (By.XPATH, "//button[contains(text(), '關閉') or contains(text(), 'Close')]"),
                (By.CLASS_NAME, "modal-mask-closeBtn"),
                (By.CSS_SELECTOR, "button[data-testid='overlay-close']"),
            ]

            for by, selector in popup_selectors:
                try:
                    close_button = WebDriverWait(self.driver, 5).until(
                        EC.element_to_be_clickable((by, selector))
                    )
                    self.driver.execute_script("arguments[0].click();", close_button)
                    print(f"已關閉彈跳視窗：{selector}")
                    time.sleep(1) 
                    break
                except TimeoutException:
                    continue

            else:
                print("沒有發現可關閉的彈跳視窗")
        except Exception as e:
            print(f"檢查彈跳視窗時發生錯誤：{str(e)}")

    def scroll_until_visible(self, element, max_attempts=50, scroll_increment=100):
        
        for attempt in range(max_attempts):
            if element.is_displayed():
                try:
                    
                    WebDriverWait(self.driver, 2).until(
                        EC.element_to_be_clickable((By.XPATH, f".//*[contains(@id, '{element.get_attribute('id')}')]"))
                    )
                    print(f"元素已在可視範圍，滾動 {attempt} 次")
                    return True
                except (TimeoutException, NoSuchElementException):
                    pass
            
            self.driver.execute_script(f"window.scrollBy(0, {scroll_increment});")
            time.sleep(0.1) 
        
        return False
    
    def apply_star_rating(self, star_values=[4]):
        try:
            star_filter = WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "[data-filters-group='class']"))
            )
            expand_buttons = star_filter.find_elements(
                By.XPATH, 
                ".//div[@data-testid='filter-group-title' and contains(., '星級') or contains(., 'Star') or contains(., '星')] | "
                ".//button[contains(., '星級') or contains(., 'Star') or contains(., 'Show')]"
            )
            for button in expand_buttons:
                try:
                    if self.scroll_until_visible(button):
                        self.driver.execute_script("arguments[0].click();", button)
                        WebDriverWait(self.driver, 5).until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, "[data-filters-group='class'] div"))
                        )
                        break
                except (TimeoutException, ElementClickInterceptedException):
                    self.driver.execute_script("""
                        var images = document.querySelectorAll('[data-testid="lazy-image-image"]');
                        images.forEach(img => img.style.display = 'none');
                    """)
                    try:
                        if self.scroll_until_visible(button):
                            self.driver.execute_script("arguments[0].click();", button)
                            break
                    except:
                        continue
            language = self.driver.execute_script("return document.documentElement.lang")
            star_text = {
                "en": "stars",
                "zh-TW": "星級",
                "zh-CN": "星"
            }.get(language[:5], "星級")
            for star in star_values:
                try:
                    star_child_elements = star_filter.find_elements(
                        By.XPATH, ".//div | .//label | .//span[contains(@class, 'aa225776f2')]"
                    )
                    for star_element in star_child_elements:
                        try:
                            inner_html = star_element.get_attribute('innerHTML').strip()
                            target_texts = [f"{star} {star_text}", f"{star}{star_text}", f"{star} stars"]
                            if any(target in inner_html for target in target_texts):
                                if self.scroll_until_visible(star_element):
                                    self.driver.execute_script("arguments[0].click();", star_element)
                                    svg_span = star_element.find_element(
                                        By.XPATH, 
                                        ".//span[contains(@class, 'fc70cba028')] | "
                                        "./following-sibling::label//span[contains(@class, 'fc70cba028')]"
                                    )
                                    if svg_span.is_displayed():
                                        break
                        except (NoSuchElementException, TimeoutException):
                            continue
                except Exception as e:
                    print(f"處理 {star} 星級時發生錯誤：{str(e)}")
        except TimeoutException:
            print("Error")
        except NoSuchElementException:
            print("Error")
        except Exception as e:
            print(f"Error：{str(e)}")
            
    