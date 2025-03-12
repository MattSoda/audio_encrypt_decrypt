import tkinter as tk
from tkinter import ttk, messagebox, filedialog, simpledialog
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
stop_recording_func = None
  
def recording_callback(sr, audio):
    global sample_rate, recorded_audio
    sample_rate = sr
    recorded_audio = audio
    messagebox.showinfo("Success", "Recording complete! You can now encrypt the audio.")

def start_recording():
    global stop_recording_func
    record_button = button_frame.grid_slaves(row=0, column=0)[0]
    
    if record_button["text"] == "🎤 Record Audio":
        # Start recording
        stop_recording_func = record_audio(callback=recording_callback)
        record_button.config(text="⏹️ Stop Recording", style="Stop.TButton")
        style.configure("Stop.TButton", background="#ff5252")
    else:
        # Stop recording
        if stop_recording_func:
            stop_recording_func()
            stop_recording_func = None
        record_button.config(text="🎤 Record Audio", style="TButton")

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
def show_waveform():
    if recorded_audio is None:
        messagebox.showwarning("Warning", "No recorded audio to visualize.")
        return
    
    plt.figure(figsize=(10, 5))
    plt.plot(recorded_audio, color='#2196F3', linewidth=0.5)
    plt.title("Audio Waveform")
    plt.xlabel("Time")
    plt.ylabel("Amplitude")
    plt.grid(True, alpha=0.3)
    
    # Center the window on screen
    mngr = plt.get_current_fig_manager()
    if hasattr(mngr, 'window'):
        window_width = 800
        window_height = 400
        screen_width = mngr.window.winfo_screenwidth()
        screen_height = mngr.window.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        mngr.window.geometry(f"{window_width}x{window_height}+{x}+{y}")
        mngr.window.title("Simple Audio Waveform")
    
    plt.show()

def view_all_waveforms():
    if recorded_audio is None:
        messagebox.showwarning("Warning", "Record audio first!")
        return

    # Create a new figure with a specific size and DPI for better resolution
    plt.figure(figsize=(10, 8), dpi=100)
    
    # Calculate number of subplots needed
    num_plots = 3 if encrypted_audio is None else 4
    
    # Plot original waveform
    plt.subplot(num_plots, 1, 1)
    plt.plot(recorded_audio, color='#2196F3', linewidth=0.5)
    plt.title("Original Audio Waveform")
    plt.xlabel("Sample")
    plt.ylabel("Amplitude")
    plt.grid(True, alpha=0.3)

    # Plot frequency domain representation (Fourier Transform)
    transformed_audio = np.abs(np.fft.fft(recorded_audio))
    plt.subplot(num_plots, 1, 2)
    plt.plot(transformed_audio[:len(transformed_audio)//2], color='#FF9800', linewidth=0.5)
    plt.title("Frequency Spectrum (Before Encryption)")
    plt.xlabel("Frequency Bin")
    plt.ylabel("Magnitude")
    plt.grid(True, alpha=0.3)

    # Plot encrypted data visualization
    if encrypted_audio is not None:
        # Convert encrypted bytes to numerical array
        encrypted_data = np.frombuffer(encrypted_audio, dtype=np.uint8)
        # Take a subset of data points to make the plot more manageable
        plot_length = min(len(encrypted_data), 10000)
        plt.subplot(num_plots, 1, 3)
        plt.plot(encrypted_data[:plot_length], color='#F44336', linewidth=0.5)
        plt.title("Encrypted Data Pattern")
        plt.xlabel("Sample Index")
        plt.ylabel("Byte Value")
        plt.grid(True, alpha=0.3)

        # Plot decrypted audio waveform if available
        if decrypted_audio is not None:
            plt.subplot(num_plots, 1, 4)
            plt.plot(decrypted_audio, color='#4CAF50', linewidth=0.5)
            plt.title("Decrypted Audio Waveform")
            plt.xlabel("Sample")
            plt.ylabel("Amplitude")
            plt.grid(True, alpha=0.3)

    plt.tight_layout(pad=2.0)
    
    # Center the window on screen
    mngr = plt.get_current_fig_manager()
    if hasattr(mngr, 'window'):
        window_width = 1000  # Width in pixels
        window_height = 800  # Height in pixels
        screen_width = mngr.window.winfo_screenwidth()
        screen_height = mngr.window.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        mngr.window.geometry(f"{window_width}x{window_height}+{x}+{y}")
        mngr.window.title("Audio Waveform Analysis")

    plt.show()

# Main Window Setup
window = tk.Tk()
window.title("Audio Encryption and Decryption")
window.geometry("700x750")  
window.configure(bg="#222831")  # Dark theme background

# Apply a style for ttk widgets
style = ttk.Style()
style.configure("TButton", font=("Arial", 11), padding=10, background="#76ABAE", foreground="black")
style.configure("TLabel", font=("Arial", 12), background="#222831", foreground="white")
style.configure("Stop.TButton", background="#ff5252")

# Title Frame
title_frame = tk.Frame(window, bg="#222831")
title_frame.pack(pady=(20, 10))

title_label = tk.Label(
    title_frame, text="EchoCrypt",
    font=("Rockwell", 30, "bold"), fg="white", bg="#222831"
)
title_label.pack()

subtitle_label = tk.Label(
    title_frame, text="🔒🎤 Secure Your Voice, Protect Your Privacy!!!🎤🔒", 
    font=("Arial", 12), fg="#76ABAE", bg="#222831"
)
subtitle_label.pack(pady=(5, 15))

# Button Frame
button_frame = tk.Frame(window, bg="#222831")
button_frame.pack(pady=10)

# Row 1: Record and Upload
ttk.Button(button_frame, text="🎤 Record Audio", command=start_recording, width=25).grid(row=0, column=0, padx=15, pady=10)
ttk.Button(button_frame, text="📂 Upload Audio", command=upload_audio, width=25).grid(row=0, column=1, padx=15, pady=10)

# Row 2: Encryption and Decryption
ttk.Button(button_frame, text="🔒 Encrypt Audio", command=encrypt, width=25).grid(row=1, column=0, padx=15, pady=10)
ttk.Button(button_frame, text="🔓 Decrypt Audio", command=decrypt, width=25).grid(row=1, column=1, padx=15, pady=10)

# Row 3: Play Buttons
ttk.Button(button_frame, text="▶️ Play Original", command=play_original, width=25).grid(row=2, column=0, padx=15, pady=10)
ttk.Button(button_frame, text="▶️ Play Decrypted", command=play_decrypted, width=25).grid(row=2, column=1, padx=15, pady=10)

# Row 4: Save Buttons
ttk.Button(button_frame, text="💾 Save Encrypted", command=save_encrypted, width=25).grid(row=3, column=0, padx=15, pady=10)
ttk.Button(button_frame, text="💾 Save Decrypted", command=save_decrypted, width=25).grid(row=3, column=1, padx=15, pady=10)

# Key Management Section
key_frame = tk.Frame(window, bg="#222831")
key_frame.pack(pady=15)

ttk.Button(key_frame, text="🔑 Show Encryption Key", command=show_key, width=30).pack(pady=5)
ttk.Button(key_frame, text="🔄 Change Key", command=change_key, width=30).pack(pady=5)
ttk.Button(key_frame, text="🔧 Generate New Key", command=generate_new_key, width=30).pack(pady=5)

# Waveform Visualization Frame
waveform_frame = tk.Frame(window, bg="#222831")
waveform_frame.pack(pady=15)

# Simple waveform button
ttk.Button(
    waveform_frame,
    text="📊 View Simple Waveform",
    command=show_waveform,
    width=30
).pack(pady=5)

# All waveforms button (including encrypted and decrypted)
ttk.Button(
    waveform_frame,
    text="📈 View All Waveforms",
    command=view_all_waveforms,
    width=30
).pack(pady=5)

# Run the Tkinter event loop
window.mainloop()
