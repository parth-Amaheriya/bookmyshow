from curl_cffi.requests import Session
import json
import time
import random

from parser import extract_venue_sessions
from extract_seats import extract_seat_layout


def main():
    session = Session()

    url = "https://in.bookmyshow.com/movies/ahmedabad/bhooth-bangla/buytickets/ET00411383/20260427"

    response = session.get(url, impersonate="chrome")

    venues = extract_venue_sessions(response.text)
    venue_records = list(venues.values())

    
    with open("venues.json", "w", encoding="utf-8") as f:
        json.dump(venue_records, f, ensure_ascii=False, indent=2)

    data = []

    for venue in venue_records:
        print(f"\nProcessing Venue: {venue['venue_name']} (Code: {venue['venue_code']})")

        code = venue['venue_code']

        venue_obj = {
        "venue_name": venue['venue_name'],
        "venue_code": code,
        "shows": []
        }
        for session_data in venue['sessions']:
            param1 = session_data['session_id']

            print(f"   Session: {param1}")

            seat_layout = extract_seat_layout(session, code, param1)

            venue_obj["shows"].append({
            "time": session_data['time'],
            "session_id": param1,
            "seat_layout": seat_layout
            })

            time.sleep(random.uniform(1.5, 3.5))
        data.append(venue_obj)

    with open("seat_layouts.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()