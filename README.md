# BikeWale Scraper

This is a personal project that was done overnight, fueled by --> idk I forgot why I did it the next morning.

This project scrapes bike data from [BikeWale](https://www.bikewale.com/new-bike-search/) and exports it to a CSV file. It collects key specifications such as engine capacity (cc), power (bhp), weight (kg), and calculates the power-to-weight ratio for each bike.

**Note**: Electric bikes are not added in the sheet and are automatically skipped cuz fugg'em.

## Features

- Fetches all new bikes listed on the website.
- Extracts:
  - Bike Name
  - Engine Capacity (cc)
  - Power (bhp)
  - Weight (kg)
  - Price (INR ₹)
  - Power-to-Weight Ratio (bhp/kg)
- Skips electric bikes automatically.
- Handles dynamic number of bikes and retries requests in case of failure.
- Outputs results in **.csv** or **.xlsx** format for easy analysis.

## Installation

1. Clone the repository:

```bash
git clone https://github.com/H3X3R/Bikewale_Scraper.git
cd BikeWale-Scraper
```

2. Install required Python packages from requirements.txt:

```bash
pip install -r requirements.txt
```

Alternatively, you can install packages manually:

```bash
pip install requests beautifulsoup4 lxml
```

## Usage

Run the scraper:

```bash
python bikewale_spider.py
```

The output sheet will be saved in the project directory.

## Notes

- The prices mentioend in the final sheet are ex-showroom prices.
- RTO and insurance are not scraped. These can be calculated separately if needed.

- On-road price = ex-showroom price + RTO + insurance
- The scraper works with the static HTML delivered by the server, without using Selenium or browser automation.

## License

This project is open-source and free to use.
