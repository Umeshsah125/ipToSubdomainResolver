import re
import sys
import requests

# Disable certificate verification
requests.packages.urllib3.disable_warnings()

# Check if URL argument is provided
if len(sys.argv) < 2:
    print("Please provide a URL as a command line argument.")
    exit(1)

# Get URL from command line argument
cidr = sys.argv[1]

# Send GET request to URL
base_url = 'https://rapiddns.io/s/'+ cidr + '?page='  # Replace with the actual URL of the RapidDNS domain
num_pages = 10

# Loop through each page and fetch the content
sample_data = ""
for page in range(0, num_pages):
    try:
        # Fetch the content of the page
        url = base_url + str(page)
        response = requests.get(url, verify=False)
        response.raise_for_status()  # Raise an exception if response status code is not 200 (OK)
        page_content = response.content.decode("utf-8")
        sample_data += page_content
    except requests.exceptions.HTTPError as e:
        print(f"Error fetching page {page}: {e}")
        continue
    except Exception as e:
        print(f"Error fetching page {page}: {e}")
        continue

# Define regular expressions pattern to match first <td> values, IPs from title, and date pattern
first_td_pattern = r"<td>(.*?)</td>"
ip_title_pattern = r"title=\"(.*?) same ip website\""
date_pattern = r"<td>\d{4}-\d{2}-\d{2}</td>"
a_pattern = r"<td>A</td>"

# Remove the date pattern from the sample data
sample_data_without_date = re.sub(date_pattern, "", sample_data)

# Remove the value "A" from the URLs in the sample data
sample_data_without_a = re.sub(a_pattern, "", sample_data_without_date)

# Extract all the first <td> values
first_td_values = re.findall(first_td_pattern, sample_data_without_a)

# Extract all the IPs from title
ip_addresses = re.findall(ip_title_pattern, sample_data_without_a)

# Create and write the results to a text file
with open("results.txt", "w") as file:
    for value, ip in zip(first_td_values, ip_addresses):
    	file.write(f"{ip}:{value}\n")	
