import sounddevice as sd
import wave
import numpy as np
import threading
import queue

# Record real-time audio from the microphone
def record_audio(callback=None):
    # Create a queue to store audio chunks
    audio_queue = queue.Queue()
    # Flag to control recording
    recording = True

    def audio_callback(indata, frames, time, status):
        if status:
            print(status)
        if recording:
            audio_queue.put(indata.copy())

    # Create an input stream
    stream = sd.InputStream(samplerate=44100, channels=1, dtype='int16', callback=audio_callback)
    
    def stop_recording():
        nonlocal recording
        recording = False
        stream.stop()
        stream.close()
        
        # Combine all audio chunks
        audio_chunks = []
        while not audio_queue.empty():
            audio_chunks.append(audio_queue.get())
        
        if audio_chunks:
            complete_audio = np.concatenate(audio_chunks)
            if callback:
                callback(44100, complete_audio)
    
    print("🎤 Recording... Speak Now!")
    stream.start()
    return stop_recording

# Save audio to a WAV file
def save_audio(file_path, sample_rate, data):
    with wave.open(file_path, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(data.tobytes())

# Play audio
def play_audio(data, sample_rate):
    sd.play(data, samplerate=sample_rate)
    sd.wait()
