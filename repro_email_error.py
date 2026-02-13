import requests

BASE_URL = "http://127.0.0.1:8000"

def test_send_email():
    payload = {
        "receiver_email": "srimanyuacharya@gmail.com",
        "subject": "Test Email",
        "content": "This is a test email from the reproduction script."
    }
    try:
        response = requests.post(f"{BASE_URL}/send-email", json=payload)
        print(f"Status Code: {response.status_code}")
        print(f"Response Body: {response.text}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_send_email()
