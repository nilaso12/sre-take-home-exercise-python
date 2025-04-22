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
def monitor_endpoints(config):
    while True:
        threads = []
        for endpoint in config:
            t = threading.Thread(target=check_health, args=(endpoint,))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        print("Availability Report")
        with domain_stats_lock:
            for domain, stats in domain_stats.items():
                # Drop decimals in availability as required
                availability = int((stats["up"] / stats["total"]) * 100)
                print(f"{domain} has {availability}% availability")
        time.sleep(15)

# Entry point of the program
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python main.py <config_file_path>")
        sys.exit(1)

    config_file = sys.argv[1]
    try:
        config = load_config(config_file)
        monitor_endpoints(config)
    except KeyboardInterrupt:
        print("\nMonitoring stopped by user.")
