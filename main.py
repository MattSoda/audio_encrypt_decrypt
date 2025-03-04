import tkinter as tk
from tkinter import messagebox, filedialog, simpledialog
import numpy as np
from audio_utils import record_audio, play_audio, save_audio
from encryptor import encrypt_audio, decrypt_audio, view_key, save_custom_key, generate_key
import matplotlib.pyplot as plt
from scipy.io.wavfile import read as wav_read, write as wav_write

# Global variables
sample_rate = None
recorded_audio = None
encrypted_audio = None
decrypted_audio = None

def start_recording():
    global sample_rate, recorded_audio
    sample_rate, recorded_audio = record_audio()
    messagebox.showinfo("Success", "Recording complete! You can now encrypt the audio.")

# Function to upload an audio file
def upload_audio():
    global sample_rate, recorded_audio
    file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.wav")])
    if file_path:
        sample_rate, recorded_audio = wav_read(file_path)
        messagebox.showinfo("Success", "Audio file uploaded successfully!")

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
        # Create a new window to display the key
        key_window = tk.Toplevel(window)
        key_window.title("Secret Key")
        key_window.geometry("400x150")

        # Add a label
        tk.Label(key_window, text="🔑 Current Key:", font=("Arial", 12)).pack(pady=10)

        # Add an entry widget to display the key (read-only)
        key_entry = tk.Entry(key_window, width=50, font=("Arial", 10), justify="center")
        key_entry.insert(0, key)
        key_entry.config(state="readonly")  # Make it read-only
        key_entry.pack(pady=10)

        # Add a "Copy" button
        def copy_key():
            window.clipboard_clear()
            window.clipboard_append(key)
            messagebox.showinfo("Success", "Key copied to clipboard!")

        tk.Button(key_window, text="Copy Key", command=copy_key, width=20, height=2).pack(pady=10)

def change_key():
    # Ask the user to input a custom key
    custom_key = simpledialog.askstring("Change Key", "Enter a new key (must be a valid Fernet key):")
    if custom_key:
        if save_custom_key(custom_key.encode()):  # Convert the key to bytes
            messagebox.showinfo("Success", "Custom key saved successfully!")
        else:
            messagebox.showerror("Error", "Invalid key! Please enter a valid Fernet key.")

def generate_new_key():
    new_key = generate_key()
    messagebox.showinfo("Success", "New key generated and saved successfully!")

# Waveform Visualization Functions
def view_all_waveforms():
    if recorded_audio is None:
        messagebox.showwarning("Warning", "Record audio first!")
        return

    plt.figure(figsize=(12, 8))  # Made figure taller for better visibility

    # Plot original waveform
    plt.subplot(3, 1, 1)
    plt.plot(recorded_audio, color='b')
    plt.title("Original Audio Waveform")
    plt.xlabel("Sample")
    plt.ylabel("Amplitude")

    # Plot frequency domain representation (Fourier Transform)
    transformed_audio = np.abs(np.fft.fft(recorded_audio))
    plt.subplot(3, 1, 2)
    plt.plot(transformed_audio, color='orange')
    plt.title("Fourier Transform (Before Encryption)")
    plt.xlabel("Frequency Bin")
    plt.ylabel("Magnitude")

    # Plot encrypted data visualization
    if encrypted_audio is not None:
        # Convert encrypted bytes to numerical array and reshape if needed
        encrypted_data = np.frombuffer(encrypted_audio, dtype=np.uint8)
        # Take a subset of data points to make the plot more manageable
        plot_length = min(len(encrypted_data), 10000)
        plt.subplot(3, 1, 3)
        plt.plot(encrypted_data[:plot_length], color='r', linewidth=0.5)
        plt.title("Encrypted Data Pattern")
        plt.xlabel("Sample Index")
        plt.ylabel("Byte Value")
        # Add grid for better visibility
        plt.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.show()




# GUI Setup
window = tk.Tk()
window.title("Real-Time AES Audio Encryption")
window.geometry("600x680")  # Adjusted window size to accommodate the title

# Center the window on the screen
window.update_idletasks()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
x = (screen_width - window.winfo_width()) // 2
y = (screen_height - window.winfo_height()) // 2
window.geometry(f"+{x}+{y}")

# Create a frame for the title (using pack)
title_frame = tk.Frame(window)
title_frame.pack(pady=(20, 10))

# Add multi-line title labels to the title frame
title_label1 = tk.Label(
    title_frame,
    text="Welcome to",
    font=("Montserrat", 25),
    fg="#222"
)
title_label1.pack(pady=(0, 1))  # Small padding below

title_label2 = tk.Label(
    title_frame,
    text="Audio Encryption & Decryption System",
    font=("Rockwell", 22, "bold"),
    fg="#222"
)
title_label2.pack(pady=(1, 1))  # Small padding below

title_label3 = tk.Label(
    title_frame,
    text="🔒🎤 Secure Your Voice, Protect Your Privacy! \nEncrypt your voice data and decrypt it only when needed 🎤🔒",
    font=("Montserrat", 12),
    fg="#222"
)
title_label3.pack(pady=(1, 20))  # Larger padding below

# Create a frame for the buttons (using grid)
button_frame = tk.Frame(window)
button_frame.pack(pady=(10, 20))

# Use grid for better button arrangement inside the button_frame
# Row 0: Recording
tk.Button(button_frame, text="🎤 Record Audio", command=start_recording, width=20, height=2, bg="#ffdc52", font=("Arial", 10, "bold")).grid(row=0, column=0, padx=10, pady=10)
tk.Button(button_frame, text="📂 Upload Audio", command=upload_audio, width=20, height=2, bg="#ffdc52", font=("Arial", 10, "bold")).grid(row=0, column=1, padx=10, pady=10)

# Row 1: Encryption and Decryption
tk.Button(button_frame, text="🔒 Encrypt Audio", command=encrypt, width=20, height=2, bg="#ffdc52", font=("Arial", 10, "bold")).grid(row=1, column=0, padx=10, pady=10)
tk.Button(button_frame, text="🔓 Decrypt Audio", command=decrypt, width=20, height=2, bg="#ffdc52", font=("Arial", 10, "bold")).grid(row=1, column=1, padx=10, pady=10)

# Row 2: Playback
tk.Button(button_frame, text="▶️ Play Original", command=play_original, width=20, height=2, bg="#ffdc52", font=("Arial", 10, "bold")).grid(row=2, column=0, padx=10, pady=10)
tk.Button(button_frame, text="▶️ Play Decrypted", command=play_decrypted, width=20, height=2, bg="#ffdc52", font=("Arial", 10, "bold")).grid(row=2, column=1, padx=10, pady=10)

# Row 3: Save Files
tk.Button(button_frame, text="💾 Save Encrypted", command=save_encrypted, width=20, height=2, bg="#ffdc52", font=("Arial", 10, "bold")).grid(row=3, column=0, padx=10, pady=10)
tk.Button(button_frame, text="💾 Save Decrypted", command=save_decrypted, width=20, height=2, bg="#ffdc52", font=("Arial", 10, "bold")).grid(row=3, column=1, padx=10, pady=10)

# Row 4: Upload and Decrypt
tk.Button(button_frame, text="📂 Upload & Decrypt", command=upload_and_decrypt, width=20, height=2, bg="#ffdc52", font=("Arial", 10, "bold")).grid(row=4, column=0, padx=10, pady=10)
tk.Button(button_frame, text="▶️ Play Decrypted File", command=play_uploaded_decrypted, width=20, height=2, bg="#ffdc52", font=("Arial", 10, "bold")).grid(row=4, column=1, padx=10, pady=10)

# Row 5: Key Management
tk.Button(button_frame, text="🔑 View Key", command=show_key, width=20, height=2, bg="#ffdc52", font=("Arial", 10, "bold")).grid(row=5, column=0, padx=10, pady=10)
tk.Button(button_frame, text="🔄 Change Key", command=change_key, width=20, height=2, bg="#ffdc52", font=("Arial", 10, "bold")).grid(row=5, column=1, padx=10, pady=10)

# Row 6: Generate New Key
tk.Button(button_frame, text="✨ Generate New Key", command=generate_new_key, width=20, height=2, bg="#ffdc52", font=("Arial", 10, "bold")).grid(row=6, column=0, padx=10, pady=10)
tk.Button(button_frame, text="📊 View Waveforms", command=view_all_waveforms, width=20, height=2, bg="#ffdc52", font=("Arial", 10, "bold")).grid(row=6, column=1, padx=10, pady=10)

# Run the application
window.mainloop()