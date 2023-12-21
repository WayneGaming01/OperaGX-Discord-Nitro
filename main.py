import os
import requests

url = 'https://api.discord.gx.games/v1/direct-fulfillment'
headers = {
    'authority': 'api.discord.gx.games',
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9',
    'content-type': 'application/json',
    'origin': 'https://www.opera.com',
    'referer': 'https://www.opera.com/',
    'sec-ch-ua': '"Opera GX";v="105", "Chromium";v="119", "Not?A_Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'cross-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 OPR/105.0.0.0'
}

payload = {
    'partnerUserId': '' 
}

compile_after_requests = 5000 # As much as you like on how many links you want to generate.

response_dir = "links" # The name of our directory where each link is stored

os.makedirs(response_dir, exist_ok=True)

# It searches for the latest response number, and if it exists, it starts right after it.
def get_latest_response_number():
    response_numbers = [int(filename.split('_')[1].split('.')[0]) for filename in os.listdir(response_dir) if filename.startswith('response_')]
    return max(response_numbers, default=0)

def send_request_and_save():
    latest_response_number = get_latest_response_number()
    response_number = latest_response_number + 1 

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        response_data = response.json()

        token = response_data.get('token', '')

        token_url = f'https://discord.com/billing/partner-promotions/1180231712274387115/{token}'
        response_file_path = os.path.join(response_dir, f"response_{response_number}.txt")

        os.makedirs(os.path.dirname(response_file_path), exist_ok=True)

        with open(response_file_path, "w") as file:
            file.write(token_url)

        print(f'Response {response_number}: {token_url}\n')

    # It handles errors.
    except requests.RequestException as e:
        print(f'Request failed for response number {response_number}.\n{e}\n')

# It compiles all the links after the desired amount is reached.
def compile_responses():
    compiled_responses_file = "compiled_responses.txt"
    with open(compiled_responses_file, "a") as compiled_file:
        latest_response_number = get_latest_response_number()

        for response_number in range(latest_response_number + 1, latest_response_number + compile_after_requests + 1):
            response_file_path = os.path.join(response_dir, f"response_{response_number}.txt")

            if os.path.exists(response_file_path):
                with open(response_file_path, "r") as response_file:
                    compiled_file.write(f'Response {response_number}:\n{response_file.read()}\n')

for _ in range(compile_after_requests):
    send_request_and_save()

compile_responses()

print("Requests completed and responses compiled.")
