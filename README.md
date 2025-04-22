# Fetch SRE Take-Home Exercise

## Overview

This project is a solution to the Site Reliability Engineering take-home exercise provided by Fetch. It monitors the availability of HTTP endpoints defined in a YAML file and logs their cumulative availability every 15 seconds. The program ensures that endpoints are only considered available if they respond with a 2xx status code **and** within 500ms.

---

## Features

- Accepts a YAML configuration file as input
- Makes HTTP requests using optional method, headers, and body
- Normalizes domains (ignores port numbers) to group availability stats
- Checks all endpoints **concurrently** every 15 seconds
- Tracks cumulative availability per domain
- Drops decimal places from availability percentages as per requirements
- Logs availability in a readable format to stdout

---

## Requirements

- Python 3.8+
- `requests` module
- `PyYAML`

Install dependencies using:

```bash
pip install -r requirements.txt



### Identified Issues and Fixes from Original Code

## How the Script Works

- The script loads endpoint definitions from a YAML file passed as a command-line argument.
- Every 15 seconds, it sends HTTP requests to all endpoints concurrently.
- It tracks whether each response meets the criteria (2xx status code and ≤ 500ms).
- It groups results by domain (ignoring ports) and prints cumulative availability for each.
- Availability is printed as an integer percentage (decimals are dropped).

## Key Fixes and Improvements from the Original Code

1. Added a 0.5-second timeout to each HTTP request to ensure quick responsiveness.
2. Measured response duration using timestamps to validate that the endpoint responded within the required 500ms.
3. Implemented a default HTTP method of "GET" in case it is not specified in the YAML configuration.
4. Removed port numbers when determining the domain by using Python's `urllib.parse` to normalize the hostname.
5. Replaced the original sequential request logic with multithreaded execution so that all endpoints are checked concurrently and efficiently.
6. Used a thread lock (`threading.Lock`) to prevent race conditions when updating the shared `domain_stats` dictionary.
7. Updated the availability percentage calculation to use `int()` instead of `round()`, so decimal values are dropped, as per the assignment requirements.
8. Changed the request body handling from `json=` to `data=` to properly send raw JSON string bodies.
9. Improved the log output format by adding clear headers and separators to distinguish between check cycles.

## Example of a Key Change

To meet the requirement of dropping decimal places in the availability percentage:

```python
# Drop decimals in availability percentage as required by the Fetch instructions
availability = int((stats["up"] / stats["total"]) * 100)





