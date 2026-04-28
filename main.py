from DrissionPage import ChromiumPage, ChromiumOptions
import json

def extract_seat_data(page):
    print(page.url)


# co = ChromiumOptions()
# co.headless(False)

page = ChromiumPage()                     
page.get('https://in.bookmyshow.com/movies/ahmedabad/bhooth-bangla/buytickets/ET00411383/20260427')

container=page.eles("css:div.ReactVirtualized__Grid__innerScrollContainer div")
for i in container:
    for j in i.eles("css:div.sc-1la7659-0"):
        print(j)
        tab=j.click()
        extract_seat_data(tab)

    break   
page.close()    