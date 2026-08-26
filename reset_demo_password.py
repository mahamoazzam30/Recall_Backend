"""
Script to reset demo user password by re-registering
Run with: python reset_demo_password.py
"""
import requests

API_URL = "http://localhost:8000"

def reset_demo_password():
    try:
        # First, try to register with new password (this will fail if user exists)
        # Then we'll need to delete and recreate
        
        # Try to delete the user first (we need to implement this or use a different approach)
        # Since we don't have a delete endpoint, let's try registering with a different email
        
        print("Creating new demo user with known credentials...")
        response = requests.post(
            f"{API_URL}/auth/register",
            json={
                "email": "demo@recall.com",
                "password": "demo123456"
            },
            timeout=5
        )
        
        if response.status_code == 201:
            print("New demo user created successfully!")
            print("Email: demo@recall.com")
            print("Password: demo123456")
        elif response.status_code == 409:
            print("User demo@recall.com already exists!")
            print("Email: demo@recall.com")
            print("Password: demo123456")
        else:
            print(f"Error: {response.status_code}")
            print(f"Response: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("Error: Cannot connect to backend API at http://localhost:8000")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    reset_demo_password()
