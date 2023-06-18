# Multilingual AMA platform "Konjac"

AMA "Ask Me Anything" events are often held by product creators.
The creator of a product or other person is invited to explain the product and answer questions in order to promote awareness of the product.
Some of them reward participants with NFTs as a token of participation or for asking good questions.
By creating a single platform for these events, we aim to transcend language barriers and spread the word about truly good projects.

# Features
1.multilingual support
The language corresponding to the speaker and the language after translation are different.

english, chinese, german, spanish, russian, korean, french, japanese, portuguese, turkish, polish, 
catalan, dutch, arabic, swedish, italian, indonesian, hindi, finnish, vietnamese, hebrew, ukrainian, 
greek, malay, czech, romanian, danish, hungarian, tamil, norwegian, thai, bulgarian, lithuanian, 
malayalam, slovak, telugu, latvian, bengali, serbian, estonian, basque, icelandic, galician, marathi, 
punjabi, afrikaans, gujarati

2.Speak/Listen in any language in real time.
 1.faster-whisper(Speech to Text)
 2.Chatgpt API(Translate text to any language)
 3.Google Cloud Text-to-Speech(Text to Speech)

# Requirement
 
* faster-whisper
* google-cloud-texttospeech
* openai
* speech_recognition
* soundcard
* threading

 You need to set up the authentication information by referring to the following URL.
 https://cloud.google.com/docs/authentication/application-default-credentials?hl=ja

# Installation
 
```bash
pip install -r requirements.txt
```

# Usage
```bash
python main.py
```

# Author
* Jodaiichi Moriuchi
* jmoriuchi8[@]gmail.comm
