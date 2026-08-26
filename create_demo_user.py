"""
Script to create a demo user for testing using the API
Run with: python create_demo_user.py
"""
import requests
import sys

API_URL = "http://localhost:8000"

def create_demo_user():
    try:
        # Try to register the demo user
        response = requests.post(
            f"{API_URL}/auth/register",
            json={
                "email": "demo.recall@gmail.com",
                "password": "demo123456"
            },
            timeout=5
        )
        
        if response.status_code == 201:
            print("Demo user created successfully!")
            print(f"Email: demo.recall@gmail.com")
            print(f"Password: demo123456")
        elif response.status_code == 409:
            print("Demo user already exists!")
            print(f"Email: demo.recall@gmail.com")
            print(f"Password: demo123456")
        else:
            print(f"Error creating demo user: {response.status_code}")
            print(f"Response: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("Error: Cannot connect to backend API at http://localhost:8000")
        print("Make sure the backend is running before executing this script.")
    except Exception as e:
        print(f"Error creating demo user: {e}")


if __name__ == "__main__":
    create_demo_user()
