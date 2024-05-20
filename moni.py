import json
import time
import requests

API_URL = "https://skeapp.jacadix.net/api/live-data"
CHECK_INTERVAL = 10

def fetch_accounts(api_url):
    response = requests.get(api_url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch accounts: {response.status_code}")
        return []

def monitor_status(accounts, status_dict, stop_event):
    while not stop_event.is_set():
        updated_accounts = fetch_accounts(API_URL)
        for updated_account in updated_accounts:
            bigos = json.loads(updated_account['bigos'])
            for bigo in bigos:
                account_key = f"{bigo['phone']}-{bigo['country']}"
                if account_key in status_dict and status_dict[account_key] != bigo['status']:
                    status_dict[account_key] = bigo['status']
                    if bigo['status'] != 'active':
                        print(f"Stopping process for account {account_key}")
                        status_dict['processes'][account_key].terminate()
                        del status_dict['processes'][account_key]
        time.sleep(CHECK_INTERVAL)

def main():
    accounts_data = fetch_accounts(API_URL)
    accounts = []
    for account_data in accounts_data:
        bigos = json.loads(account_data['bigos'])
        for bigo in bigos:
            account = {
                'phone': bigo['phone'],
                'password': bigo['password'],
                'country': bigo['country'],
                'live_id': '1003946142',
            }
            accounts.append(account)
            account_key = f"{bigo['phone']}-{bigo['country']}"
    print(accounts)

if __name__ == "__main__":
    main()
