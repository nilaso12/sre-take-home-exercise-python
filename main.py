import yaml
import requests
import time
from collections import defaultdict
from urllib.parse import urlparse
import threading


domain_stats = defaultdict(lambda: {"up": 0, "total": 0})
domain_stats_lock = threading.Lock()

# Function to load configuration from the YAML file
def load_config(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

# Normalize domain 
def get_domain(url):
    return urlparse(url).hostname

# Function to perform health checks
def check_health(endpoint):
    url = endpoint['url']
   # adding GET method
    method = endpoint.get("method", "GET")
    headers = endpoint.get('headers',{})
    body = endpoint.get('body')
    domain = get_domain(url)

    try:
        # response = requests.request(method, url, headers=headers, json=body)
        start = time.time()
        response = requests.request(method, url, headers=headers, data=body, timeout=0.5)
        response_time = (time.time() - start) * 1000
        is_up = 200 <= response.status_code < 300 and response_time <= 500

    except requests.RequestException:
            is_up = False
    with domain_stats_lock:
        domain_stats[domain]["total"] += 1
        if is_up:
            domain_stats[domain]["up"] += 1
            
# Main function to monitor endpoints
def monitor_endpoints(file_path):
    config = load_config(file_path)
    domain_stats = defaultdict(lambda: {"up": 0, "total": 0})

    while True:
        threads = []
        for endpoint in config:
            # domain = endpoint["url"].split("//")[-1].split("/")[0]
            t = threading.Thread(target=check_health, args=(endpoint,))
            threads.append(t)
            t.start()
            # result = check_health(endpoint)

            domain_stats[domain]["total"] += 1
            if result == "UP":
                domain_stats[domain]["up"] += 1

        # Log cumulative availability percentages
        for domain, stats in domain_stats.items():
            availability = round(100 * stats["up"] / stats["total"])
            print(f"{domain} has {availability}% availability percentage")

        print("---")
        time.sleep(15)

# Entry point of the program
if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python monitor.py <config_file_path>")
        sys.exit(1)

    config_file = sys.argv[1]
    try:
        monitor_endpoints(config_file)
    except KeyboardInterrupt:
        print("\nMonitoring stopped by user.")
