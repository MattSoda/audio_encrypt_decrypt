from cryptography.fernet import Fernet

# Generate an AES encryption key
key = Fernet.generate_key()

# Save the key to a file
with open("audio_encryption/keys/secret.key", "wb") as key_file:
    key_file.write(key)

print("✅ AES Key Generated: keys/secret.key")

import numpy as np
from scipy.fft import fft, ifft
from cryptography.fernet import Fernet

# Load AES encryption key
def load_aes_key():
    with open("keys/secret.key", "rb") as key_file:
        return Fernet(key_file.read())

# Fourier Transform + AES Encryption
def encrypt_audio(data):
    transformed = fft(data.flatten())  # Convert to frequency domain
    aes = load_aes_key()
    encrypted_bytes = aes.encrypt(transformed.tobytes())  # AES encryption
    return encrypted_bytes

# Fourier Transform + AES Decryption
def decrypt_audio(encrypted_bytes):
    aes = load_aes_key()
    decrypted_bytes = aes.decrypt(encrypted_bytes)  # AES decryption
    decrypted_data = np.frombuffer(decrypted_bytes, dtype=np.complex128)
    return ifft(decrypted_data).real.astype(np.int16)  # Convert back to time domain
