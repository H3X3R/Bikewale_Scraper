import requests
from bs4 import BeautifulSoup as BS
import pandas as pd

base = "https://www.bikewale.com/new-bike-search/"

# first request to get total bikes
r = requests.get(base, headers={"User-Agent":"Mozilla/5.0"})
soup = BS(r.text, "lxml")
count_text = soup.find("h2", {"data-skin":"title"}).get_text(strip=True)
total_bikes = int(count_text.split()[0])

# now build correct URL only once
url = f"{base}?&pageSize={total_bikes}"

# retry loop for this full page
for attempt in range(5):  
    try:
        r = requests.get(url, headers={"User-Agent":"Mozilla/5.0"}, timeout=10)
        if r.status_code == 200:
            break
    except Exception as e:
        print(f"Attempt {attempt+1} failed:", e)
else:
    raise Exception("Failed after 5 tries")

soup = BS(r.text, "lxml")
print("Total bikes on page:", len(soup.select("li.o-em.o-hk")))

def parse_specs(li):
    """Extract cc, bhp, and weight based on units. Skip if any contains 'kWh'."""
    spans = li.select("div.o-o.onOEBQ.o-iT.o-ei span.o-iZ.o-jf")
    values = [s.get_text(strip=True).rstrip("|") for s in spans]
    
    cc, bhp, weight = None, None, None

    for val in values:
        if "kWh" in val:   # skip electric bikes
            return None
        elif val.endswith("cc"):
            num = val.removesuffix("cc").strip()
            cc = float(num) if num.replace(".", "", 1).isdigit() else None
        elif val.endswith("bhp"):
            num = val.removesuffix("bhp").strip()
            bhp = float(num) if num.replace(".", "", 1).isdigit() else None
        elif val.endswith("kg"):
            num = val.removesuffix("kg").strip()
            weight = float(num) if num.replace(".", "", 1).isdigit() else None
            
    if(cc==None or bhp==None or weight==None): return None
    ptw = round(bhp / weight, 3) if weight else None
    return cc, bhp, weight, ptw

def parse_price(price_raw):
    price_str = price_raw.get_text(strip=True) if price_raw else None
    price_num = float(price_str.replace("₹", "").replace(",", "").strip())
    return price_str, price_num

bikes = []

for li in soup.select("li.o-em.o-hk"):
    
    name_tag = li.select_one("div.o-f7.o-o a")
    name = name_tag["title"].strip() if name_tag and name_tag.has_attr("title") else None
    
    price_raw = li.select_one("div.o-ei span.o-f span.o-jJ")
    price_str, price_num = parse_price(price_raw)
    
    specs = parse_specs(li)
    
    if specs is None:
        continue 
    
    cc, bhp, weight, ptw = specs

    normalised_price = float(price_num/100000)
    ppp = round(bhp/normalised_price, 3)
        
    bike = {
        "name": name,
        "cc": cc,
        "bhp": bhp,
        "weight": weight,
        "price": price_str,
        "power-to-weight": ptw,
        "power-per-price": ppp
    }
    bikes.append(bike)

print("Extracted:", len(bikes), "bikes")

df = pd.DataFrame(bikes)
# df.to_csv("bikes.csv", index=False, encoding="utf-8-sig")
df.to_excel("bikes.xlsx", index=False)
print("Data saved the sheet")