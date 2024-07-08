import requests
import os
import json

# Function to get the endpoint from the user
def get_endpoint():
    endpoint = input("Enter the API endpoint (e.g., HOST:IP): ")
    if not endpoint.startswith("http://") and not endpoint.startswith("https://"):
        endpoint = f"http://{endpoint}"
    return endpoint

# Function to get the API secret from the user
def get_api_secret():
    apiSecret = input("Enter the API secret: ")
    return apiSecret

# Function to test the API connection using the ping endpoint
def test_api_connection(endpoint, apiSecret):
    ping_url = f"{endpoint}/ping?key={apiSecret}"
    try:
        result = requests.get(ping_url)
        if result.text == "ALIVE":
            return True
        else:
            print("\nAPI connection test failed. Please check the endpoint and API secret.")
            return False
    except Exception as e:
        print(f"\nError testing API connection: {e}")
        return False

# Function to save the API credentials to a file
def save_credentials(endpoint, apiSecret):
    credentials = {"endpoint": endpoint, "apiSecret": apiSecret}
    with open("credentials.json", "w") as f:
        json.dump(credentials, f)

# Function to load the API credentials from a file
def load_credentials():
    try:
        with open("credentials.json", "r") as f:
            credentials = json.load(f)
            return credentials["endpoint"], credentials["apiSecret"]
    except FileNotFoundError:
        return None, None

# Function to change the API credentials
def change_credentials():
    global endpoint, apiSecret
    endpoint = get_endpoint()
    apiSecret = get_api_secret()

    # Test API connection and save credentials if successful
    if test_api_connection(endpoint, apiSecret):
        save_credentials(endpoint, apiSecret)
        print("\nCredentials changed successfully.")
    else:
        print("\nError changing credentials. Please try again.")

# Function to normalize the endpoint
def normalize_endpoint(endpoint):
    if not endpoint.startswith("http://") and not endpoint.startswith("https://"):
        endpoint = f"http://{endpoint}"
    if endpoint.endswith("/"):
        endpoint = endpoint[:-1]
    return endpoint

# Main program loop
while True:
    # Load credentials from file if available
    endpoint, apiSecret = load_credentials()

    # If credentials are not loaded, prompt the user for input
    if not endpoint or not apiSecret:
        endpoint = get_endpoint()
        apiSecret = get_api_secret()

        # Test API connection and save credentials if successful
        if test_api_connection(endpoint, apiSecret):
            save_credentials(endpoint, apiSecret)
        else:
            continue

    # Main Menu
    def main_menu():
        print("\nAutorayBot Console Program")
        print("1. Generate a new key")
        print("2. Ping the VPN and Discord bot")
        print("3. List all active keys")
        print("4. Delete a key")
        print("5. Add a key")
        print("6. Change credentials")
        print("7. Exit")

        choice = input("Enter your choice: ")
        return choice

    # Function to generate a new key (same as before)
    def generate_key():
        try:
            result = requests.get(APIE['new_key'])
            print(f"\nNew key: {result.text}")
        except Exception as e:
            print(f"\nError generating key: {e}")

    # Function to ping the VPN and Discord bot (same as before)
    def ping():
        try:
            result = requests.get(APIE['ping'])
            print(f"\nDiscord Bot: `ALIVE`\nVPN: `{result.text}`")
        except Exception as e:
            print(f"\nError pinging: {e}")

    # Function to list all active keys (same as before)
    def list_keys():
        try:
            result = requests.get(APIE['key_list'])
            print(f"\nList of all active keys:\n{result.text}")
        except Exception as e:
            print(f"\nError fetching key list: {e}")

    # Function to delete a key (same as before)
    def delete_key():
        key_to_delete = input("\nEnter the key to delete: ")
        try:
            result = requests.get(APIE['delete_key'] + key_to_delete)
            print(f"\nResult: {result.text}")
        except Exception as e:
            print(f"\nError deleting key: {e}")

    # Function to add a key (same as before)
    def add_key():
        key_to_add = input("\nEnter the key to add: ")
        try:
            result = requests.get(APIE['append_key'] + key_to_add)
            print(f"\nResult: {result.text}")
        except Exception as e:
            print(f"\nError adding key: {e}")

    # Main program loop
    while True:
        choice = main_menu()

        if choice == '1':
            generate_key()
        elif choice == '2':
            ping()
        elif choice == '3':
            list_keys()
        elif choice == '4':
            delete_key()
        elif choice == '5':
            add_key()
        elif choice == '6':
            change_credentials()
        elif choice == '7':
            print("\nExiting...")
            break
        else:
            print("\nInvalid choice. Please try again.")
