import streamlit as st
import pyaudio
import wave
from pydub import AudioSegment
from pydub.playback import play

# Function to record audio
def record_audio(filename, duration=5, chunk=1024, format=pyaudio.paInt16, channels=1, rate=44100):
    audio = pyaudio.PyAudio()

    stream = audio.open(format=format, channels=channels,
                        rate=rate, input=True,
                        frames_per_buffer=chunk)

    st.write("Recording...")
    frames = []

    for i in range(0, int(rate / chunk * duration)):
        data = stream.read(chunk)
        frames.append(data)

    st.write("Recording finished.")

    stream.stop_stream()
    stream.close()
    audio.terminate()

    wf = wave.open(filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(audio.get_sample_size(format))
    wf.setframerate(rate)
    wf.writeframes(b''.join(frames))
    wf.close()

# Streamlit UI
st.title("Audio Chatbot")

# Record audio input
st.write("Press the button and start speaking...")
record_button = st.button("Record")

if record_button:
    record_audio("input.wav")

    st.write("Audio recorded!")

# Respond with audio
st.write("Processing...")

# Here you can perform your processing on the recorded audio (e.g., passing it to your chatbot model)

# For demonstration, let's respond with a simple audio message
response_audio = AudioSegment.from_file('output.wav',format='wav')
play(response_audio)

st.write("Response audio played!")
