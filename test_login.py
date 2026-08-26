"""
Script to test login with demo credentials
Run with: python test_login.py
"""
import requests

API_URL = "http://localhost:8000"

def test_login():
    try:
        # Test login with demo credentials
        response = requests.post(
            f"{API_URL}/auth/login",
            json={
                "email": "demo.recall@gmail.com",
                "password": "demo123456"
            },
            timeout=5
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            print("Login successful!")
        else:
            print("Login failed!")
            
    except requests.exceptions.ConnectionError:
        print("Error: Cannot connect to backend API at http://localhost:8000")
        print("Make sure the backend is running.")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    test_login()
