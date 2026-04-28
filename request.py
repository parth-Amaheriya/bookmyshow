from curl_cffi.requests import Session
from lxml import html
import json
def main():
    session = Session()
    
    url = "https://in.bookmyshow.com/movies/ahmedabad/bhooth-bangla/buytickets/ET00411383/20260427"
    
    response = session.get(url, impersonate="chrome")
    with open("response.html", "w", encoding="utf-8") as f:
        f.write(response.text)  

    tree=html.fromstring(response.text)

    raw_json_data = tree.xpath("//script[starts-with(normalize-space(text()), 'window.__INITIAL_STATE__')]/text()")
    json_data=raw_json_data[0].split("=", 1)[1].strip().rstrip(";") if raw_json_data else None
    json_data = json.loads(json_data) if json_data else None
    with open("json_data.json", "w", encoding="utf-8") as f:
        json.dump(json_data, f, ensure_ascii=False, indent=4)
    
main()