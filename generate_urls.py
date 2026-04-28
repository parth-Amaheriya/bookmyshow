import json

BASE_URL="https://in.bookmyshow.com"

def build_seat_layout_url(
    region_slug: str,
    event_code: str,
    venue_code: str,
    session_id: str,
    date_code: str,
):
    return (
        f"{BASE_URL}/movies/{region_slug}/seat-layout/"
        f"{event_code}/{venue_code}/{session_id}/{date_code}"
    )


def extract_seat_layout_urls(payload):
    showtimes_event=payload.get("showtimesByEvent", {})
    region_slug=payload.get("cookies", {}).get("rgn", {}).get("regionCodeSlug")
    shared_data=showtimes_event.get("sharedData") or payload.get("sharedData") or {}
    event_code=shared_data.get("selectChildEventData", {}).get("eventCode")
    if not event_code:
        raise KeyError("Missing event code in showtimes payload")

    date_code=showtimes_event.get("currentDateCode") or showtimes_event.get("additionalData", {}).get("dateCode")
    if not date_code:
        raise KeyError("Missing date code in showtimes payload")

    urls=[]
    seen=set()

    def walk(node):
        if isinstance(node, dict):
            if node.get("type") == "venue-card" and isinstance(node.get("showtimes"), list):
                venue_code=node.get("additionalData", {}).get("venueCode") or node.get("id")
                if venue_code:
                    for showtime in node.get("showtimes", []):
                        if not isinstance(showtime, dict):
                            continue

                        additional=showtime.get("additionalData", {})
                        session_id=additional.get("sessionId")
                        if not session_id:
                            continue

                        categories=additional.get("categories", [])
                        if categories and not any(
                            isinstance(category, dict) and category.get("seatLayout")
                            for category in categories
                        ):
                            continue

                        url=build_seat_layout_url(
                            region_slug=str(region_slug),
                            event_code=str(event_code),
                            venue_code=str(venue_code),
                            session_id=str(session_id),
                            date_code=str(date_code),
                        )
                        if url not in seen:
                            seen.add(url)
                            urls.append(url)

            for value in node.values():
                walk(value)

        elif isinstance(node, list):
            for item in node:
                walk(item)

    walk(payload)
    return urls


def load_json(path):
    with open(path,"r", encoding="utf-8") as file:
        return json.load(file)


def main():
    source_path="json_data.json"
    payload=load_json(source_path)

    for url in extract_seat_layout_urls(payload):
        print(url)


if __name__ == "__main__":
    main()