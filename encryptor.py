from cryptography.fernet import Fernet
import os
import numpy as np
from scipy.fft import fft, ifft

# Path to the key file
KEY_FILE_PATH = "keys/secret.key"

# Ensure the keys directory exists
os.makedirs(os.path.dirname(KEY_FILE_PATH), exist_ok=True)

# Generate and save a new AES encryption key
def generate_key():
    key = Fernet.generate_key()
    with open(KEY_FILE_PATH, "wb") as key_file:
        key_file.write(key)
    print("✅ New AES Key Generated and Saved!")
    return key

# Save a custom key provided by the user
def save_custom_key(custom_key):
    try:
        # Validate the custom key
        Fernet(custom_key)  # This will raise an exception if the key is invalid
        with open(KEY_FILE_PATH, "wb") as key_file:
            key_file.write(custom_key)
        print("✅ Custom Key Saved!")
        return True
    except Exception as e:
        print(f"❌ Invalid Key: {e}")
        return False

# Load the current AES encryption key
def load_aes_key():
    if not os.path.exists(KEY_FILE_PATH):
        generate_key()  # Generate a key if it doesn't exist
    with open(KEY_FILE_PATH, "rb") as key_file:
        return Fernet(key_file.read())

# View the current key
def view_key():
    if not os.path.exists(KEY_FILE_PATH):
        generate_key()  # Generate a key if it doesn't exist
    with open(KEY_FILE_PATH, "rb") as key_file:
        return key_file.read().decode()

# Fourier Transform + AES Encryption
def encrypt_audio(data):
    # Ensure data is flattened and in the correct format
    data = np.array(data, dtype=np.int16).flatten()
    transformed = fft(data)  # Convert to frequency domain
    aes = load_aes_key()
    encrypted_bytes = aes.encrypt(transformed.tobytes())  # AES encryption
    return encrypted_bytes

# Fourier Transform + AES Decryption
def decrypt_audio(encrypted_bytes):
    try:
        aes = load_aes_key()
        decrypted_bytes = aes.decrypt(encrypted_bytes)  # AES decryption
        # Convert back to complex numbers for inverse FFT
        decrypted_data = np.frombuffer(decrypted_bytes, dtype=np.complex128)
        # Perform inverse FFT and ensure the output is in int16 format
        audio_data = ifft(decrypted_data).real.astype(np.int16)
        return audio_data
    except Exception as e:
        raise Exception(f"Decryption failed: {str(e)}")