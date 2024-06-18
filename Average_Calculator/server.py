from flask import Flask, jsonify, request
import requests
from collections import deque
import time

app = Flask(__name__)

# Configuration
WINDOW_SIZE = 10
TIMEOUT = 0.5  # 500 milliseconds
TOKEN =     "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJNYXBDbGFpbXMiOnsiZXhwIjoxNzE4NjkwMjYzLCJpYXQiOjE3MTg2ODk5NjMsImlzcyI6IkFmZm9yZG1lZCIsImp0aSI6ImQ2MjliNjU5LThlMjUtNGY0Yi1hMzI3LWY4ZmEwZTA5MTUxMiIsInN1YiI6InZhaWJoYXYucHVyaTI2QGdtYWlsLmNvbSJ9LCJjb21wYW55TmFtZSI6IlNwZW5kU2Vuc2UiLCJjbGllbnRJRCI6ImQ2MjliNjU5LThlMjUtNGY0Yi1hMzI3LWY4ZmEwZTA5MTUxMiIsImNsaWVudFNlY3JldCI6Ind1ekJBTXRpenRNRHdUeGciLCJvd25lck5hbWUiOiJWYWliaGF2UHVyaSIsIm93bmVyRW1haWwiOiJ2YWliaGF2LnB1cmkyNkBnbWFpbC5jb20iLCJyb2xsTm8iOiIxLzIxL0ZFVC9CQ1MvMDMzIn0.vpKBKTJssbGgeP9iaZAZcX_2_n-DkLUnp_6MqkcQ9Hg"

# Storage for numbers
numbers_deque = deque(maxlen=WINDOW_SIZE)

# Test server URLs
TEST_SERVER_URLS = {
    'p': "http://20.244.56.144/test/primes",
    't': "http://20.244.56.144/test/fibonacci",
    'e': "http://20.244.56.144/test/even",
    'r': "http://20.244.56.144/test/random"
}

def fetch_numbers(url):
   # try:
        headers = {
            'Authorization': f'Bearer {TOKEN}',
            'Content-Type': 'application/json'
        }
        response = requests.get(url, headers=headers, timeout=TIMEOUT)
        print(response)
        if response.status_code == 200:
            return response.json().get("numbers", [])
    # except requests.RequestException:
    #     print('Request.request')
    #     pass
        return []

def calculate_average(numbers):
    return sum(numbers) / len(numbers) if numbers else 0.0

@app.route('/numbers/<number_id>', methods=['GET'])
def get_numbers(number_id):
    if number_id not in TEST_SERVER_URLS:
        return jsonify({"error": "Invalid number ID"}), 400

    # Fetch numbers from the test server
    fetched_numbers = fetch_numbers(TEST_SERVER_URLS[number_id])
    
    if not fetched_numbers:
        return jsonify({"error": "Failed to fetch numbers"}), 500

    # Store unique numbers and maintain the window size
    window_prev_state = list(numbers_deque)
    for number in fetched_numbers:
        if number not in numbers_deque:
            numbers_deque.append(number)
    
    window_curr_state = list(numbers_deque)
    average = calculate_average(numbers_deque)

    response = {
        "windowPrevState": window_prev_state,
        "windowCurrState": window_curr_state,
        "numbers": fetched_numbers,
        "avg": round(average, 2)
    }

    return jsonify(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9876,debug= True)