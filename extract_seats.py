import requests
import jmespath
import re
url = "https://services-in.bookmyshow.com/doTrans.aspx"

payload = {
'lngTransactionIdentifier': '0',
'strCommand': 'GETSEATLAYOUT',
'strVenueCode': '',
'strParam1': '',
'strParam2': 'WEB',
'strParam3': '',
'strParam4': '',
'strParam5': 'Y',
'strParam6': '',
'strParam7': '',
'strParam8': '',
'strParam9': '',
'strParam10': '',
'strFormat': 'json'}
files=[

]
headers = {
  'x-app-code': 'WEB',
  'sec-ch-ua-platform': '"Windows"',
  'x-geohash': 'ts5',
  'sec-ch-ua': '"Google Chrome";v="141", "Not?A_Brand";v="8", "Chromium";v="141"',
  'sec-ch-ua-mobile': '?0',
  'x-latitude': '23.039568',
  'x-region-slug': 'ahmedabad',
  'Accept': 'application/json, text/plain, */*',
  'x-platform-code': 'WEB',
  'x-longitude': '72.566005',
  'x-platform': 'WEB',
  'Referer': 'https://in.bookmyshow.com/',
  'x-segments': '',
  'true-client-ip': '45.114.65.131',
  'x-bms-id': '1.578357421.1761913251158',
  'x-advertiser-id': '1487880242782616638',
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36',
  'x-location-selection': 'manual',
  'x-region-code': 'AHD',
#   'Cookie': '__cf_bm=Vb1r4R.xf.QW7jKnEHCoD6pyVlKg9qUA4VFS7AOcBHU-1761913317-1.0.1.1-eTDLnynQlGNs.JhB8idNWIVYLunb8LoEUuwjm40ACpcoRcyENQftWPFNM3SzO1Xu7zy5mvamW3HdF6KK3bM7ExGsR9B4_4Rd0ERres1GEws; _cfuvid=iHIthRC3j6gQWBQrgRfBRLKjjYtNzp4hMhBJoukbsfU-1761913317297-0.0.1.1-604800000'
}

def extract_seat_layout(session,code,param1):
    payload['strVenueCode'] = code
    payload['strParam1'] = param1
    response = session.post(url, headers=headers, data=payload, files=files)

    print(response.status_code)
 

    s= jmespath.search('BookMyShow.strData', response.json())
    try:
        s = s.split('||', 1)[1]
    except Exception as e:
        print("Error occurred while extracting seat layout.")
        return None

    # parts = [
    #     part for part in re.split(r'[,:|+]', s)
    #     if len(part) == 4 and not part.endswith('000') and part[1] in {'1', '4'}
    # ]

    parts = [
        part for part in re.split(r'[, :|+]', s)
    ]

    available_seats = [
        part for part in parts
        if len(part) == 4 and not part.endswith('000') and part[1] not in {'2'}
    ]

    booked_seats = [
        part for part in parts
        if len(part) == 4 and not part.endswith('000') and part[1] in {'2'}
    ]

    # print("*"*20)
    # print("Available Seats: ", len(available_seats))
    # print("Booked Seats: ", len(booked_seats))
    # print("Total Seats: ", len(available_seats) + len(booked_seats))
    # print("*"*20)
    return {
        "available_seats": len(available_seats),
        "booked_seats": len(booked_seats),
        "total_seats": len(available_seats) + len(booked_seats)
        }
    