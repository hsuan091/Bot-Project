import booking.constants as const
import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from datetime import datetime
from booking.booking_filteration import BookingFilteration 


class Booking(webdriver.Chrome):
    def __init__(self, driver_path=r"D:\hsuan\selenium", teardown=False):
        self.driver_path = driver_path
        self.teardown = teardown

        
        os.environ['PATH'] += f";{self.driver_path}"

        super(Booking, self).__init__()
        
        self.maximize_window()

    
    def land_first_page(self):
        self.get(const.BASE_URL)
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.teardown:
            self.quit()
           
    def select_place_to_go(self, place_to_go):
        try:
            
            search_field = WebDriverWait(self, 10).until(
                EC.element_to_be_clickable((By.NAME, "ss"))
            )
            search_field.clear()
            search_field.send_keys(place_to_go)
            print(f"成功輸入地點：{place_to_go}")
            time.sleep(5)
            first_result = self.find_element(By.ID,'autocomplete-result-1')
            first_result.click()
            
            
        except (TimeoutException, NoSuchElementException) as e:
            print(f"錯誤：無法找到搜尋欄或輸入地點，原因：{str(e)}")
            raise
   
    def select_dates(self, check_in_date, check_out_date):
        try:
            checkin_element = WebDriverWait(self, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, f'span[data-date="{check_in_date}"]'))
            )
            checkin_element.click()
            checkout_element = WebDriverWait(self, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, f'span[data-date="{check_out_date}"]'))
            )
            checkout_element.click()
            
        except (TimeoutException, NoSuchElementException) as e:
            print(f"錯誤：無法找到搜尋欄或輸入地點，原因：{str(e)}")
            raise
    
    def select_adults(self, count=1):
        try:
           
            guest_field = WebDriverWait(self, 20).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-testid='occupancy-config']"))
            )
            self.execute_script("arguments[0].scrollIntoView(true);", guest_field)
            guest_field.click()
            

            
            adult_input = WebDriverWait(self, 20).until(
                EC.presence_of_element_located((By.ID, "group_adults"))
            )
            minus_button = WebDriverWait(self, 20).until(
                EC.element_to_be_clickable((By.XPATH, "//input[@id='group_adults']/preceding-sibling::div/button[1]"))
            )
            while True:
                current_count = int(adult_input.get_attribute("value"))
                if current_count <= 1:
                    break
                self.execute_script("arguments[0].scrollIntoView(true);", minus_button)
                minus_button.click()
                

            
            plus_button = WebDriverWait(self, 20).until(
                EC.element_to_be_clickable((By.XPATH, "//input[@id='group_adults']/preceding-sibling::div/button[2]"))
            )
            for i in range(count - 1):
                self.execute_script("arguments[0].scrollIntoView(true);", plus_button)
                plus_button.click()
                

            
            final_count = int(adult_input.get_attribute("value"))
            if final_count == count:
                print(f"成功設置成人數量：{count}")
            else:
                raise ValueError(f"成人數量設置失敗，預期 {count}，實際 {final_count}")
            
            time.sleep(5)
        except (TimeoutException, NoSuchElementException) as e:
            print(f"Error，原因：{str(e)}")
            try:
                guest_field = WebDriverWait(self, 20).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-testid='occupancy-config']"))
                )
                self.execute_script("arguments[0].scrollIntoView(true);", guest_field)
                guest_field.click()
                
                adult_input = WebDriverWait(self, 20).until(
                    EC.presence_of_element_located((By.ID, "group_adults"))
                )
                minus_button = WebDriverWait(self, 20).until(
                    EC.element_to_be_clickable((By.XPATH, "//*[@id=':ri:']/div/div[1]/div[2]/button[2]"))
                )
                while True:
                    current_count = int(adult_input.get_attribute("value"))
                    if current_count <= 1:
                        break
                    self.execute_script("arguments[0].scrollIntoView(true);", minus_button)
                    minus_button.click()
                    
                plus_button = WebDriverWait(self, 20).until(
                    EC.element_to_be_clickable((By.XPATH, "//*[@id=':ri:']/div/div[1]/div[2]/button[1]"))
                )
                for i in range(count - 1):
                    self.execute_script("arguments[0].scrollIntoView(true);", plus_button)
                    plus_button.click()
                    
                final_count = int(adult_input.get_attribute("value"))
                if final_count == count:
                    print(f"{count}")
                else:
                    raise ValueError(f"Error，預期 {count}，實際 {final_count}")
            except Exception as e2:
                print(f" XPath Error，try SVG selector，原因：{str(e2)}")
                
                try:
                    minus_path_d = "M20.25 12.75H3.75a.75.75 0 0 1 0-1.5h16.5a.75.75 0 0 1 0 1.5"
                    plus_path_d = "M20.25 11.25h-7.5v-7.5a.75.75 0 0 0-1.5 0v7.5h-7.5a.75.75 0 0 0 0 1.5h7.5v7.5a.75.75 0 0 0 1.5 0v7.5h7.5a.75.75 0 0 0 0-1.5"
                    minus_button = WebDriverWait(self, 20).until(
                        EC.element_to_be_clickable((By.XPATH, f"//div[@class='e484bb5b7a']//button[.//svg/path[@d='{minus_path_d}']]"))
                    )
                    while True:
                        current_count = int(adult_input.get_attribute("value"))
                        if current_count <= 1:
                            break
                        self.execute_script("arguments[0].scrollIntoView(true);", minus_button)
                        minus_button.click()
                        
                    plus_button = WebDriverWait(self, 20).until(
                        EC.element_to_be_clickable((By.XPATH, f"//div[@class='e484bb5b7a']//button[.//svg/path[@d='{plus_path_d}']]"))
                    )
                    for i in range(count - 1):
                        self.execute_script("arguments[0].scrollIntoView(true);", plus_button)
                        plus_button.click()
                        
                    final_count = int(adult_input.get_attribute("value"))
                    if final_count == count:
                        print(f"SUCCESS：{count}")  
                    else:
                        raise ValueError(f"Error，預期 {count}，實際 {final_count}")
                except Exception as e3:
                    
                    raise
    def click_search(self):
        search_button = self.find_element(By.CSS_SELECTOR, "button[type='submit']")
        self.execute_script("arguments[0].scrollIntoView(true);", search_button)
        search_button.click()
        print("搜尋成功")
        time.sleep(3)
    def close_map_if_open(self):
        try:
            
            close_map_button = WebDriverWait(self, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button.js-map-modal-close"))
            )
            self.execute_script("arguments[0].scrollIntoView(true);", close_map_button)
            close_map_button.click()
            print("MAP CLOSED")
        except TimeoutException:
            print("ERROR")
        except Exception as e:
            print(f"ERROR：{str(e)}")
    def apply_filterations(self):
        self.close_map_if_open()
        time.sleep(5)
        filteration = BookingFilteration(driver=self)
        filteration.apply_star_rating(star_values=[4])
        time.sleep(5)
    
    def sort_by_price(self):
        try:
            
            sorter_dropdown_button = WebDriverWait(self, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-testid='sorters-dropdown-trigger']"))
            )
            self.execute_script("arguments[0].scrollIntoView(true);", sorter_dropdown_button)
            sorter_dropdown_button.click()

            
            price_option_button = WebDriverWait(self, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-id='price']"))
            )
            self.execute_script("arguments[0].scrollIntoView(true);", price_option_button)
            price_option_button.click()
            print("已選擇價格低價優先")
            time.sleep(3)
        except TimeoutException:
            print("ERROR")
        except Exception as e:
            print(f"排序時發生錯誤：{str(e)}")
    def scrape_results(self):
    
        try:
            
            results_container = WebDriverWait(self, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".cca574b93c[data-results-container='1']"))
            )

            
            property_cards = results_container.find_elements(By.CSS_SELECTOR, "[data-testid='property-card']")
            print(f"找到 {len(property_cards)} 個結果")

            results = []
            for card in property_cards:
                try:
                    
                    title = card.find_element(By.CSS_SELECTOR, "[data-testid='title']").text.strip()

                    price = card.find_element(By.CSS_SELECTOR, "[data-testid='price-and-discounted-price']").text.strip()
                    
                    try:
                        review_score = card.find_element(By.CSS_SELECTOR, "[data-testid='review-score'] div.f63b14ab7a.dff2e52086").text.strip()
                    except NoSuchElementException:
                        review_score = "無評分"

                    results.append({
                        "title": title,
                        "price": price,
                        "review_score": review_score,
                    })
                    print(f"房源：{title}, 價格：{price}, 評分：{review_score}")
                except (NoSuchElementException, TimeoutException) as e:
                    print(f"爬取房源失敗，原因：{str(e)}")
                    continue

            return results
        except TimeoutException:
            print("錯誤：無法找到房源容器")
            dom_snapshot = self.execute_script("return document.body.outerHTML")
            return []
        except Exception as e:
            print(f"爬取房源時發生錯誤：{str(e)}")
            return []