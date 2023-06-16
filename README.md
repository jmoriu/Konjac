# Multilingual AMA platform "Konjac"

AMA "Ask Me Anything" events are often held by product creators.
The creator of a product or other person is invited to explain the product and answer questions in order to promote awareness of the product.
Some of them reward participants with NFTs as a token of participation or for asking good questions.
By creating a single platform for these events, we aim to transcend language barriers and spread the word about truly good projects.

# Features
1.multilingual support
The language corresponding to the speaker and the language after translation are different.

 Language corresponding to the speaker(faster-whisper)

 Afrikaans, Arabic, Armenian, Azerbaijani, Belarusian, Bosnian, Bulgarian, Catalan, Chinese, Croatian, Czech, 
 Danish, Dutch, English, Estonian, Finnish, French, Galician, German, Greek, Hebrew, Hindi, Hungarian, Icelandic, 
 Indonesian, Italian, Japanese, Kannada, Kazakh, Korean, Latvian, Lithuanian, Macedonian, Malay, Marathi, Maori, 
 Nepali, Norwegian, Persian, Polish, Portuguese, Romanian, Russian, Serbian, Slovak, Slovenian, Spanish, Swahili, 
 Swedish, Tagalog, Tamil, Thai, Turkish, Ukrainian, Urdu, Vietnamese, and Welsh.

 Corresponding language for translation(Google Cloud Text-to-Speech)
 
 Afrikaans, Arabic, Basque, Bengali, Bulgarian, Catalan, Chinese, Czech, Danish, Dutch (Belgium), Dutch (Netherlands), 
 English (Australia), English (India), English (United Kingdom), English (USA), Filipino, Finnish, French (Canada), 
 French (France), Galician, German, Greek, Gujarati, Hebrew, Hindi, Hungarian, Icelandic, Indonesian, Italian, 
 Japanese, Kannada, Korean, Latvian, Lithuanian, Malay, Malayalam, Mandarin, Marathi, Norwegian, Polish, Portuguese, 
 Portuguese, Punjabi, Romanian, Russian, Serbian, Slovak, Spanish (Spain), Spanish (USA), Swedish, Tamil, Telugu, Thai, 
 Turkish, Ukrainian, Vietnamese
2.Speak/Listen in any language in real time.
 1.faster-whisper(Speech to Text)
 2.Chatgpt API(Translate text to any language)
 3.Google Cloud Text-to-Speech(Text to Speech)

# Requirement
 
* faster-whisper
* google-cloud-texttospeech
* openai

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
