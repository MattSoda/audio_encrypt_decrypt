import sounddevice as sd
import wave

# Record real-time audio from the microphone
def record_audio(duration=5, sample_rate=44100):
    print("🎤 Recording... Speak Now!")
    audio = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype="int16")
    sd.wait()
    print("✅ Recording complete!")
    return sample_rate, audio

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
