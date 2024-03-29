# Multilingual tranlate real-time "Konjac"

Crypto has an AMA (Ask Me Anything) community-building initiative for each of its products.
The creator of the product shares an overview of the product and its progress with the community, followed by a question-and-answer session.
Many of the AMAs are conducted in English, and my inability to speak English well has made me reluctant to actively participate in these AMAs.
It is very sad that the appeal of the product cannot be fully conveyed due to the language barrier, and the event is not very exciting.
I would like to support any Japanese product that aims to break down the language barrier by using the latest AI technology and expand into the global market.
As a first step, we have created a simultaneous interpretation function.

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

![スクリーンショット 2023-06-19 194500](https://github.com/jmoriu/Konjac/assets/136766894/7a7d05b1-4e37-4c11-b0de-b8e2d54d7434)


If you want to translate what you speak, type speaker.you are the listener, type listener.

For languages, use the first two letters of the language. See language.json for details.


# Author
* Jodaiichi Moriuchi
* jmoriuchi8[@]gmail.comm
