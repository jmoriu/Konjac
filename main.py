# base code https://github.com/davabase/whisper_real_time/blob/master/transcribe_demo.py

import io
import os
import speech_recognition as sr
import tempfile
from faster_whisper import WhisperModel
from tempfile import NamedTemporaryFile
from datetime import datetime, timedelta
from queue import Queue
from time import sleep
import openai
import google.cloud.texttospeech as tts
import simpleaudio
import soundcard as sc
import threading
import numpy as np
import yaml
import json

# load language json
lang_json = open('languages.json', 'r')
languages = json.load(lang_json)

with open('config.yaml') as file:
    config = yaml.safe_load(file)

# load whisper model
whisper_model = config['whisper_model']
audio_model= WhisperModel(whisper_model, device='cuda', compute_type='float16')

# set config variables
SAMPLE_RATE = config['SAMPLE_RATE']
INTERVAL = config['INTERVAL']
BUFFER_SIZE = config['BUFFER_SIZE']
openai.organization = config['OrganizationID']
openai.api_key = config['OpenAIapikey']
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'secret-key.json'
q = Queue()
original_text = Queue()
translated_text = Queue()
b = np.ones(100) / 100
translate_Flag = True
from_lang = 'en'
to_lang = 'ja'
transcription = ['']
translated_list = ['']

# translate text to any language
def translate_text():
    to_language = languages['languages'][to_lang]
    print(to_language)
    while True:
        if translate_Flag == True:
            text = original_text.get()
            if text != "":
                completion = openai.ChatCompletion.create(
                        model = 'gpt-3.5-turbo',
                        messages  = [
                                    {'role': 'system', 'content': f'You are an excellent translator and very good at translating from English to {to_language}.'},
                                    {'role': 'user', 'content': f'Writing speculation other than the content when translating constitutes spreading rumors and can lead to litigation issues. Never write about anything other than the given text.Please use a polite tone of voice when translating.'},
                                    {'role': 'user', 'content': f'Translate the following sentences English to {to_language} :{text}. Please answer only with your translation.'}
                                    ] , 
                        max_tokens  = 1000,
                        n           = 1,
                        stop        = None,
                        temperature = 0,
                )   
                response = completion.choices[0].message.content
                print(response)
                translated_text.put(response)
        else:
            text = original_text.get()
            translated_text.put(text)            

# text to speech
def text_to_speech():
    to_language = languages['speech_Language'][to_lang]
    while True:
        text = translated_text.get()
        if text != "":
            # Using Google Cloud Text-to-Speech API
            client = tts.TextToSpeechClient()
            synthesis_input = tts.SynthesisInput(text=text)

            # voice param
            voiceparam = tts.VoiceSelectionParams(
                language_code=to_language, ssml_gender=tts.SsmlVoiceGender.FEMALE, name=to_language+'-Standard-A'
                )

            # encode to LINEAR16
            audio_config = tts.AudioConfig(
                audio_encoding=tts.AudioEncoding.LINEAR16, speaking_rate=1.3,
                )

            response = client.synthesize_speech(
                input=synthesis_input, voice=voiceparam, audio_config=audio_config
                )

            # play audio
            with tempfile.TemporaryDirectory() as tmp:
                with open(f'{tmp}/output.wav', 'wb') as f:
                    f.write(response.audio_content)
                    wav_obj = simpleaudio.WaveObject.from_wave_file(f'{tmp}/output.wav')
                    play_obj = wav_obj.play()
                    play_obj.wait_done()

def speak_to_translated_voice():
    print('speak_to_translated_voice')
    # The last time a recording was retrieved from the queue.
    phrase_time = None
    # Current raw audio bytes.
    last_sample = bytes()
    # Thread safe Queue for passing data from the threaded recording callback.
    data_queue = Queue()
    # We use SpeechRecognizer to record our audio because it has a nice feature where it can detect when speech ends.
    recorder = sr.Recognizer()
    recorder.energy_threshold = 1000
    # Definitely do this, dynamic energy compensation lowers the energy threshold dramatically to a point where the SpeechRecognizer never stops recording.
    recorder.dynamic_energy_threshold = False
    
    source = sr.Microphone(sample_rate=SAMPLE_RATE)

    record_timeout = INTERVAL # How real-time the recording is in seconds.
    phrase_timeout = 3        # How much empty space between recordings before we consider it a new line in the transcription.

    temp_file = NamedTemporaryFile().name
    text = ''

    with source:
        recorder.adjust_for_ambient_noise(source)

    th_translatetext = threading.Thread(target=translate_text, daemon=True)
    th_translatetext.start()
    th_speechtext = threading.Thread(target=text_to_speech, daemon=True)
    th_speechtext.start()

    def record_callback(_, audio: sr.AudioData) -> None:
        '''
        Threaded callback function to receive audio data when recordings finish.
        audio: An AudioData containing the recorded bytes.
        '''
        # Grab the raw bytes and push it into the thread-safe queue.
        data = audio.get_raw_data()
        data_queue.put(data)

    # Create a background thread that will pass us raw audio bytes.
    # We could do this manually, but SpeechRecognizer provides a nice helper.
    recorder.listen_in_background(source, record_callback, phrase_time_limit=record_timeout)

    while True:
        try:
            now = datetime.utcnow()
            # Pull raw recorded audio from the queue.
            if not data_queue.empty():
                phrase_complete = False
                # If enough time has passed between recordings, consider the phrase complete.
                # Clear the current working audio buffer to start over with the new data.
                if phrase_time and now - phrase_time > timedelta(seconds=phrase_timeout):
                    last_sample = bytes()
                    phrase_complete = True
                # This is the last time we received new audio data from the queue.
                phrase_time = now

                # Concatenate our current audio data with the latest audio data.
                while not data_queue.empty():
                    data = data_queue.get()
                    last_sample += data

                # Use AudioData to convert the raw data to wav data.
                audio_data = sr.AudioData(last_sample, source.SAMPLE_RATE, source.SAMPLE_WIDTH)
                wav_data = io.BytesIO(audio_data.get_wav_data())

                # Write wav data to the temporary file as bytes.
                with open(temp_file, 'w+b') as f:
                    f.write(wav_data.read())

                # Read the transcription. task='translate'
                results, _ = audio_model.transcribe(temp_file, language=from_lang, task='translate', vad_filter=True, without_timestamps=True, )
                for result in results:
                    text =  text + result.text

                if phrase_complete:
                    transcription.append(text)
                else:
                    transcription[-1] = text

                original_text.put(text)
                text = ''

                # Clear the console to reprint the updated transcription.
                os.system('cls' if os.name == 'nt' else 'clear')
                for line in transcription:
                    print(line)

                # Flush stdout.
                print('', end='', flush=True)

                # Infinite loops are bad for processors, must sleep.
                sleep(0.25)
        except KeyboardInterrupt:
            break

    print('\n\nTranscription:')
    for line in transcription:
        print(line)

def recognize():
    text = ''
    while True:
        audio = q.get()
        if (audio ** 2).max() > 0.001:
            # decode the audio
            results, _ = audio_model.transcribe(audio, language=from_lang, task='translate', vad_filter=True, without_timestamps=True, )
            for result in results:
                text =  text + result.text

            if text != '':
                original_text.put(text)
                transcription.append(text)
                print(text)
                text = ''

def listen_to_translated_voice():
    th_recognize = threading.Thread(target=recognize, daemon=True)
    th_translatetext = threading.Thread(target=translate_text, daemon=True)
    th_speechtext = threading.Thread(target=text_to_speech, daemon=True)
    th_recognize.start()
    th_translatetext.start()
    th_speechtext.start()

    while True:
        with sc.get_microphone(id=str(sc.default_speaker().name), include_loopback=True).recorder(samplerate=SAMPLE_RATE, channels=1) as mic:
            audio = np.empty(SAMPLE_RATE * INTERVAL + BUFFER_SIZE, dtype=np.float32)
            n = 0
            while True:
                while n < SAMPLE_RATE * INTERVAL:
                    data = mic.record(BUFFER_SIZE)
                    audio[n:n+len(data)] = data.reshape(-1)
                    n += len(data)

                m = n * 4 // 5
                vol = np.convolve(audio[m:n] ** 2, b, 'same')
                m += vol.argmin()
                q.put(audio[:m])

                audio_prev = audio
                audio = np.empty(SAMPLE_RATE * INTERVAL + BUFFER_SIZE, dtype=np.float32)
                audio[:n-m] = audio_prev[m:n]
                n = n-m

def main():
    global to_lang, from_lang, translate_Flag

    translate_task = input('Speaker or Listener?: ')
    from_lang = input('from language: ')
    to_lang = input('to language : ')

    if to_lang == 'en':
        translate_Flag = False

    if translate_task == 'Speaker':
        speak_to_translated_voice()
    elif translate_task == 'Listener':
        listen_to_translated_voice()
    else:
        print('Please enter the correct task!')
        main()

if __name__ == '__main__':
    main()
