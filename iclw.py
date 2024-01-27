import csv
import sys
import time

import requests
from bs4 import BeautifulSoup

base_url = "https://www.kernsheriff.org/Inmate_Info?page="
data = []

def fetch_page(url):
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return response
    except requests.exceptions.HTTPError as errh:
        print(f"HTTP Error: {errh}")
    except requests.exceptions.ConnectionError as errc:
        print(f"Error Connecting: {errc}")
    except requests.exceptions.Timeout as errt:
        print(f"Timeout Error: {errt}")
    except requests.exceptions.RequestException as err:
        print(f"Oops: Something Else: {err}")
    return None

try:
    for page_num in range(1, 5):
        url = base_url + str(page_num)
        response = fetch_page(url)

        if response:
            soup = BeautifulSoup(response.text, 'html.parser')
            rows = soup.find_all('tr')
            print(f"Processing page {page_num}")

            for row in rows:
                cols = row.find_all('td')
                if len(cols) == 5:
                    try:
                        record = {
                            'SO Number': cols[0].text.strip(),
                            'First Name': cols[1].text.strip(),
                            'Middle Name': cols[2].text.strip(),
                            'Last Name': cols[3].text.strip(),
                            'Date of Birth': cols[4].text.strip()
                        }
                        data.append(record)
                    except Exception as e:
                        print(f"Error parsing row data: {e}")
        else:
            print(f"Failed to fetch page {page_num}. Skipping.")

        # Delay to prevent overwhelming the server
        time.sleep(1)  # Adjust delay as needed
except KeyboardInterrupt:
    print("Script interrupted by user. Exiting.")
    sys.exit(1)

# Writing data to CSV
with open('output.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=['SO Number', 'First Name', 'Middle Name', 'Last Name', 'Date of Birth'])
    writer.writeheader()
    for entry in data:
        writer.writerow(entry)

print("Data scraping complete and saved to output.csv")

