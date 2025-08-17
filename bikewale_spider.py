###############################################################################################
################################ Authored by: Swastik Kashyap #################################
###############################################################################################
########################## Solves some kind of a world problem. idk. ##########################
###############################################################################################

import requests
from bs4 import BeautifulSoup as BS
import pandas as pd

base = "https://www.bikewale.com/new-bike-search/"

# finds the total number of bikes to dynamically construct the query.
r = requests.get(base, headers={"User-Agent":"Mozilla/5.0"})
soup = BS(r.text, "lxml")
count_text = soup.find("h2", {"data-skin":"title"}).get_text(strip=True)
total_bikes = int(count_text.split()[0])
url = f"{base}?&pageSize={total_bikes}"

# tries to fetch the webpage with the query. Can increase the range number to more than 5, if you've questionable internet.
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

# As the function name says. It parses the specifications of a bike. Extract cc, bhp, and weight based on units.
def parse_specs(li):
    spans = li.select("div.o-o.onOEBQ.o-iT.o-ei span.o-iZ.o-jf")
    values = [s.get_text(strip=True).rstrip("|") for s in spans]
    
    cc, bhp, weight = None, None, None

    for val in values:
        if "kWh" in val:
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
    ptw = round(bhp / weight, 3) if weight else None    # power-to-wieght calculation
    return cc, bhp, weight, ptw

# As the name says bro. It parses the price XD. Used later on to find power-per-price (New unit I discovered that night).
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

    normalised_price = float(price_num/100000)  # Is done due to the fact that price is in 10^5 and power is below 10^2 mostly. Better than seeing bunch of 0.0000....
    ppp = round(bhp/normalised_price, 3)        # the power-per-price calculation.
        
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
# df.to_csv("bikes.csv", index=False, encoding="utf-8-sig")         # uncomment to save the sheet as csv. pretty obv idk why im commenting this.
df.to_excel("bikes.xlsx", index=False)
print("Data saved the sheet")