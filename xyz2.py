import streamlit as st
import pyaudio
import wave
import speech_recognition as sr
from pydub import AudioSegment
from pydub.playback import play
from gtts import gTTS
import os
import asyncio
    # db = SQLDatabase.from_uri("sqlite:///train_information.db")

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

# Function to convert audio to text
def audio_to_text(audio_file):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio_data = recognizer.record(source)
        text = recognizer.recognize_google(audio_data)
    return text

# Function to convert text to audio
def text_to_audio(text, filename):
    tts = gTTS(text)
    tts.save(filename)


def main():

    # Streamlit UI
    st.title("Audio Chatbot")

    # Record audio input
    st.write("Press the button and start speaking...")
    record_button = st.button("Record")

    if record_button:
        record_audio("input.wav")
        st.write("Audio recorded!")

    # Convert audio to text
    st.write("Processing...")

    input_text = audio_to_text("input.wav")
    st.write("You said:", input_text)

    # Here you can perform your processing on the input text (e.g., passing it to your chatbot model)

    # For demonstration, let's respond with a simple text message
    response_text = "This is a response to your input."
    st.write("Bot:", response_text)

    # Convert text to audio
    response_audio_file = "output.wav"
    text_to_audio(response_text, response_audio_file)
    st.success("Text converted to audio successfully!")
    st.audio(response_audio_file, format='audio/mp3', start_time=0)

    response_audio = AudioSegment.from_file("output.wav")
    play(response_audio)

    st.write("Response audio played!")

if __name__ == "__main__":
    main()