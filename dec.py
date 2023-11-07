import os

# Replace with your Android directory path
ANDROID_DIRECTORY = "/storage/emulated/0/"

# Get the encryption key from the user
key_hex = input("Enter the encryption key in hexadecimal format: ")
try:
    key = bytes.fromhex(key_hex)
except ValueError:
    print("Invalid key format. Please enter a valid hexadecimal key.")
    exit(1)

# Function to decrypt a file
def decrypt_file(file_path, key):
    try:
        with open(file_path, "rb") as file:
            file_data = file.read()
        decrypted_data = bytes([b ^ key for b in file_data])

        with open(file_path, "wb") as file:
            file.write(decrypted_data)
        print(f"File decrypted successfully: {file_path}")
    except Exception as e:
        print(f"Decryption failed: {file_path}, Error: {str(e)}")

if __name__ == '__main__':
    action = input("Enter 'decrypt' to decrypt files: ")
    if action != "decrypt":
        print("Invalid action. Please enter 'decrypt' to decrypt files.")
    else:
        target_directory = input("Enter the directory path for file processing: ")
        for root, dirs, files in os.walk(target_directory):
            for file_name in files:
                file_path = os.path.join(root, file_name)
                decrypt_file(file_path, key)
