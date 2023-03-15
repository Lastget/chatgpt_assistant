import gradio as gr
import openai 
import config 
import subprocess 
import os 

openai.api_key = os.environ.get('OPEN_API_KEY')
# openai.api_key = config.OPEN_API_KEY

messages = [
    {"role": "system", "content": "You are a therapist. Respond as if you were a rapper Jay-Z"},

] 

def transcribe(audio):
    global messages  
    
    print(audio)
    audio_file = open(audio, "rb")
    transcript = openai.Audio.transcribe("whisper-1", audio_file)
    print(transcript)
    
    messages.append({"role": "user", "content": transcript['text']},)
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages= messages
    )

    system_message = response['choices'][0]['message']['content'] 
    
    subprocess.call(["say", system_message])
    
    messages.append( {"role": "assistant", "content": system_message})
    
    chat_transcript = ""
    for message in messages:
        if message['role'] != 'system':
            chat_transcript += message['role'] + ": " + message['content'] + "\n\n"

    return chat_transcript


ui = gr.Interface(fn=transcribe, inputs=gr.Audio(source="microphone", type="filepath"), outputs="text")

ui.launch()
