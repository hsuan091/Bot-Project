
from booking.booking import Booking

def main():
    try:
        with Booking(teardown=True) as bot:
            bot.land_first_page()
            bot.select_place_to_go("台中")
            bot.select_dates(check_in_date="2025-05-19", check_out_date = "2025-05-25")
            bot.select_adults(10)
            bot.click_search()
            bot.apply_filterations()
            bot.sort_by_price()
            results = bot.scrape_results()
            for result in results:
                print(result)
    except Exception as e:
        print(f"Error：{str(e)}")

if __name__ == "__main__":
    main()