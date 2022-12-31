# Project 2: Web Scrapper using BeautifulSoup4 and requests
import requests
from bs4 import BeautifulSoup
import pandas
import argparse
import connect

parser = argparse.ArgumentParser()
parser.add_argument("--page_num_max", help="Enter the number of pages to parse", type=int)
parser.add_argument("--dbname", help="Enter the name of db", type=str)
args = parser.parse_args()

trivago_url = "https://www.trivago.com/en-US/srl/hotels-agra-india?search=200-73666;dr-20230106-20230107"
page_num_MAX = args.page_num_max
scraped_info_list = []
connect.connect(args.dbname)

for page_num in range(1, page_num_MAX):
    url = trivago_url + str(page_num)
    print("Get Request for: " + url)
    req = requests.get(url)
    content = req.content

    soup = BeautifulSoup(content, "html.parser")

    all_hotels = soup.find_all("li", {"class": "py-1"})

    for hotel in all_hotels:
        hotel_dict = {}
        hotel_dict["name"] = hotel.find("span", {"itemprop": "name"}).txt
        hotel_dict["address"] = hotel.find("span", {"class": "block"}).txt
        hotel_dict["price"] = hotel.find("div", {"itemprop": "price"}).txt
        # try.....except
        try:
            hotel_dict["ratings"] = hotel.find("span", {"itemprop": "ratingValue"}).txt
        except AttributeError:
            #pass
            hotel_dict["ratings"] = None

        parent_discounted_element = hotel.find("div", {"class": "leading-none"})

        discount_list = []
        for discount in parent_discounted_element.find_all("span", {"class": "inline-flex"}):
            discount_list.append(discount.find("span", {"class": "px-1"}).txt.strip())
                                                                                    # |--->to remove extra spaces in the output   
        
        hotel_dict["discounted"] = ', '.join(discount_list[:-1])
                                                         # |---> called 'slicing' {for last element,-1; for last 2 elements,-2;.....}

        scraped_info_list.append(hotel_dict)
        connect.insert_into_table(args.dbname, tuple(hotel_dict.values()))

        #print(hotel_name, hotel_address, hotel_price, hotel_rating, discount_list)

dataFrame = pandas.DataFrame(scraped_info_list)
print("Creating csv file.....")
dataFrame.to_csv("Trivago.csv")
connect.get_hotel_info(args.dbname)