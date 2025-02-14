import tkinter as tk
from tkinter import messagebox, filedialog, simpledialog
import numpy as np
from audio_utils import record_audio, play_audio, save_audio
from encryptor import encrypt_audio, decrypt_audio, view_key, save_custom_key

# Global variables
sample_rate = None
recorded_audio = None
encrypted_audio = None
decrypted_audio = None

def start_recording():
    global sample_rate, recorded_audio
    sample_rate, recorded_audio = record_audio()
    messagebox.showinfo("Success", "Recording complete! You can now encrypt the audio.")

def encrypt():
    global encrypted_audio
    if recorded_audio is None:
        messagebox.showwarning("Warning", "Record audio first!")
        return
    encrypted_audio = encrypt_audio(recorded_audio)
    messagebox.showinfo("Success", "Audio encrypted!")

def decrypt():
    global decrypted_audio
    if encrypted_audio is None:
        messagebox.showwarning("Warning", "Encrypt audio first!")
        return
    decrypted_audio = decrypt_audio(encrypted_audio)
    messagebox.showinfo("Success", "Audio decrypted!")

def play_original():
    if recorded_audio is not None:
        play_audio(recorded_audio, sample_rate)
    else:
        messagebox.showwarning("Warning", "Record audio first!")

def play_encrypted():
    messagebox.showwarning("Warning", "Encrypted audio is secured and cannot be played directly!")

def play_decrypted():
    if decrypted_audio is not None:
        play_audio(decrypted_audio, sample_rate)
    else:
        messagebox.showwarning("Warning", "Decrypt audio first!")

def save_encrypted():
    if encrypted_audio is not None:
        file_path = filedialog.asksaveasfilename(defaultextension=".enc", filetypes=[("Encrypted Files", "*.enc")])
        if file_path:
            with open(file_path, "wb") as f:
                f.write(encrypted_audio)
            messagebox.showinfo("Success", "Encrypted audio saved successfully!")
    else:
        messagebox.showwarning("Warning", "Encrypt audio first!")

def save_decrypted():
    if decrypted_audio is not None:
        file_path = filedialog.asksaveasfilename(defaultextension=".wav", filetypes=[("WAV Files", "*.wav")])
        if file_path:
            save_audio(file_path, sample_rate, decrypted_audio)
            messagebox.showinfo("Success", "Decrypted audio saved successfully!")
    else:
        messagebox.showwarning("Warning", "Decrypt audio first!")

def upload_and_decrypt():
    global decrypted_audio
    file_path = filedialog.askopenfilename(filetypes=[("Encrypted Files", "*.enc")])
    
    if file_path:
        with open(file_path, "rb") as f:
            encrypted_data = f.read()
        
        decrypted_audio = decrypt_audio(encrypted_data)
        messagebox.showinfo("Success", "Encrypted file decrypted successfully!")

def play_uploaded_decrypted():
    if decrypted_audio is not None:
        play_audio(decrypted_audio, sample_rate)
    else:
        messagebox.showwarning("Warning", "Upload and decrypt an audio file first!")

def show_key():
    key = view_key()
    if key:
        messagebox.showinfo("Secret Key", f"🔑 Current Key:\n{key}")

def change_key():
    # Ask the user to input a custom key
    custom_key = simpledialog.askstring("Change Key", "Enter a new key (must be a valid Fernet key):")
    if custom_key:
        if save_custom_key(custom_key.encode()):  # Convert the key to bytes
            messagebox.showinfo("Success", "Custom key saved successfully!")
        else:
            messagebox.showerror("Error", "Invalid key! Please enter a valid Fernet key.")

# GUI Setup
window = tk.Tk()
window.title("Real-Time AES Audio Encryption")
window.geometry("400x800")

tk.Button(window, text="🎤 Record Audio", command=start_recording, width=20, height=2).pack(pady=10)
tk.Button(window, text="🔒 Encrypt Audio", command=encrypt, width=20, height=2).pack(pady=10)
tk.Button(window, text="🔓 Decrypt Audio", command=decrypt, width=20, height=2).pack(pady=10)
tk.Button(window, text="▶️ Play Original", command=play_original, width=20, height=2).pack(pady=10)
tk.Button(window, text="🚫 Play Encrypted", command=play_encrypted, width=20, height=2).pack(pady=10)
tk.Button(window, text="▶️ Play Decrypted", command=play_decrypted, width=20, height=2).pack(pady=10)
tk.Button(window, text="💾 Save Encrypted", command=save_encrypted, width=20, height=2).pack(pady=10)
tk.Button(window, text="💾 Save Decrypted", command=save_decrypted, width=20, height=2).pack(pady=10)
tk.Button(window, text="📂 Upload & Decrypt", command=upload_and_decrypt, width=20, height=2).pack(pady=10)
tk.Button(window, text="▶️ Play Decrypted File", command=play_uploaded_decrypted, width=20, height=2).pack(pady=10)

# Add buttons for key management
tk.Button(window, text="🔑 View Key", command=show_key, width=20, height=2).pack(pady=10)
tk.Button(window, text="🔄 Change Key", command=change_key, width=20, height=2).pack(pady=10)

window.mainloop()