from pathlib import Path
import json
import re
from lxml import html


def extract_venue_sessions(html_data):

    tree = html.fromstring(html_data)
    script_text = "".join(tree.xpath('//script[contains(., "window.__INITIAL_STATE__")]/text()'))
    if not script_text:
        raise ValueError("window.__INITIAL_STATE__ script not found")

    initial_state_text = re.sub(
        r'^\s*window\.__INITIAL_STATE__\s*=\s*',
        '',
        script_text,
        count=1,
    ).strip()
    initial_state_text = re.sub(r';\s*$', '', initial_state_text)

    state = json.loads(initial_state_text)

    def walk(node):
        if isinstance(node, dict):
            if node.get("type") == "venue-card":
                yield node
            for value in node.values():
                yield from walk(value)
        elif isinstance(node, list):
            for item in node:
                yield from walk(item)

    venues = {}

    for venue_card in walk(state):
        additional_data = venue_card.get("additionalData", {})
        venue_code = additional_data.get("venueCode") or additional_data.get("venue_code")
        venue_name = additional_data.get("venueName")

        if not venue_code:
            continue

        venue_entry = venues.setdefault(
            venue_code,
            {
                "venue_code": venue_code,
                "venue_name": venue_name,
                "sessions": [],
            },
        )

        if not venue_entry["venue_name"]:
            venue_entry["venue_name"] = venue_name

        for showtime in venue_card.get("showtimes", []):
            showtime_additional = showtime.get("additionalData", {})
            session_id = (
                showtime_additional.get("sessionId")
                or showtime.get("cta", {}).get("analytics", {}).get("show_session_id")
            )
            show_time = showtime_additional.get("showTime") or showtime.get("title")

            venue_entry["sessions"].append(
                {
                    "time": show_time,
                    "session_id": session_id,
                }
            )

    return venues

# with open("venues.json", "w", encoding="utf-8") as f:
#     json.dump(venue_records, f, ensure_ascii=False, indent=2)
