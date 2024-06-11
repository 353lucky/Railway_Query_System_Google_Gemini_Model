from dotenv import load_dotenv
load_dotenv() ## load all the environemnt variables

import streamlit as st
import os
import sqlite3
import streamlit as st
import pyaudio
import wave
import speech_recognition as sr
from pydub import AudioSegment
from pydub.playback import play
from gtts import gTTS
import os
import google.generativeai as genai
## Configure Genai Key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

## Function To Load Google Gemini Model and provide queries as response

def get_gemini_response(question,prompt):
    model=genai.GenerativeModel('gemini-pro')
    response=model.generate_content([prompt[0],question])
    return response.text

## Fucntion To retrieve query from the database

def read_sql_query(sql,db):
    conn=sqlite3.connect(db)
    cur=conn.cursor()
    cur.execute(sql)
    rows=cur.fetchall()
    conn.commit()
    conn.close()
    for row in rows:
        print(row)
    return rows

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
    
    ## Define Your Prompt
    result = []

    prompt=[
        """
        You are an expert in converting English questions to SQL query!
        The SQL database has the name train_information and has the following columns - train_name, source_station, destination_station, current_location, ticket_price, departure_time, arrival_time 
        also the sql code should not have ``` in beginning or end and sql word in output
        """
    ]

    ## Streamlit App

    st.set_page_config(page_title="I can Retrieve Any SQL query")
    st.header("App To Retrieve SQL Data")

    st.write("Press the button and start speaking...")
    record_button = st.button("Record")

    if record_button:
        record_audio("input.wav")
        st.write("Audio recorded!")
    # st.write("Processing...")
    input_text = audio_to_text("input.wav")
    st.write("Your Audio input:", input_text)

    question = input_text

    # question=st.text_input("Input: ",key="input")



    submit=st.button("Ask the question")

    # if submit is clicked
    if submit:
        response=get_gemini_response(question,prompt)
        print(response)
        response=read_sql_query(response,"train_information.db")
        print(response)
        for row in response:
            result.append(row[0])

    if submit:
        st.subheader("The Bot Response is:")
        for row in result:
            response_text = row
            st.write(response_text)

    # Convert text to audio
    if submit:
        response_audio_file = "output.wav"
        print(result)
        response_text = " ".join(result)
        print("response_text",response_text)
        try:
            text_to_audio(response_text, response_audio_file)
            st.success("Text converted to audio successfully!")
            st.audio(response_audio_file, format='audio/mp3', start_time=0)
            # response_audio = AudioSegment.from_file("output.wav")
            # play(response_audio)

            # st.write("Response audio played!")
        except:
            st.write("Sorry it is out of context question")
            text_to_audio("Sorry it is out of context question", response_audio_file)
            st.success("Text converted to audio successfully!")
            st.audio(response_audio_file, format='audio/mp3', start_time=0)

            # response_audio = AudioSegment.from_file("output.wav")
            # play(response_audio)

            # st.write("Response audio played!")
    

if __name__ == "__main__":
    main()






