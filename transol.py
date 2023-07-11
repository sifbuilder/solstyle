# ________DEBUG
Text = 1
import os
debug = os.environ.get('debug', Text)
if isinstance(debug, str):
    if debug.isdigit():
        debug = int(debug)
    elif debug.replace('.', '', 1).isdigit() and debug.count('.') < 2:
        debug = float(debug)
    elif debug.lower() in ['true', 'false']:
        debug = debug.lower() == 'true'

if debug == 1:
    print(f"DEBUG.debug:  {debug}")


# ________DESCRIPTION
Text = "translate inlang outlang or switch"
description = Text
if debug == 1:
    print(f"::  {description}  ::")


# ________CONTROL 
Text = 1
control = Text
if debug == 1:
    print(f"CONTROL.control:  {control}")


# ________CODES 
if control == 1:
    Text = "sk-"
    import os
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
    if isinstance(OPENAI_API_KEY, str):
        if OPENAI_API_KEY.isdigit():
            OPENAI_API_KEY = int(OPENAI_API_KEY)
        elif OPENAI_API_KEY.replace('.', '', 1).isdigit() and OPENAI_API_KEY.count('.') < 2:
            OPENAI_API_KEY = float(OPENAI_API_KEY)
        elif OPENAI_API_KEY.lower() in ['true', 'false']:
            OPENAI_API_KEY = OPENAI_API_KEY.lower() == 'true'

    Text = "gapi-"
    import os
    GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')
    if isinstance(GOOGLE_API_KEY, str):
        if GOOGLE_API_KEY.isdigit():
            GOOGLE_API_KEY = int(GOOGLE_API_KEY)
        elif GOOGLE_API_KEY.replace('.', '', 1).isdigit() and GOOGLE_API_KEY.count('.') < 2:
            GOOGLE_API_KEY = float(GOOGLE_API_KEY)
        elif GOOGLE_API_KEY.lower() in ['true', 'false']:
            GOOGLE_API_KEY = GOOGLE_API_KEY.lower() == 'true'

    Text = "gcse-"
    import os
    GOOGLE_CSE_ID = os.environ.get('GOOGLE_CSE_ID')
    if isinstance(GOOGLE_CSE_ID, str):
        if GOOGLE_CSE_ID.isdigit():
            GOOGLE_CSE_ID = int(GOOGLE_CSE_ID)
        elif GOOGLE_CSE_ID.replace('.', '', 1).isdigit() and GOOGLE_CSE_ID.count('.') < 2:
            GOOGLE_CSE_ID = float(GOOGLE_CSE_ID)
        elif GOOGLE_CSE_ID.lower() in ['true', 'false']:
            GOOGLE_CSE_ID = GOOGLE_CSE_ID.lower() == 'true'


    Text = "__xi_api_key__"
    import os
    XI_API_KEY = os.environ.get('XI_API_KEY')
    if isinstance(XI_API_KEY, str):
        if XI_API_KEY.isdigit():
            XI_API_KEY = int(XI_API_KEY)
        elif XI_API_KEY.replace('.', '', 1).isdigit() and XI_API_KEY.count('.') < 2:
            XI_API_KEY = float(XI_API_KEY)
        elif XI_API_KEY.lower() in ['true', 'false']:
            XI_API_KEY = XI_API_KEY.lower() == 'true'



# ________SWITCH langs switch
Text = 0
import os
switch = os.environ.get('switch', Text)
if isinstance(switch, str):
    if switch.isdigit():
        switch = int(switch)
    elif switch.replace('.', '', 1).isdigit() and switch.count('.') < 2:
        switch = float(switch)
    elif switch.lower() in ['true', 'false']:
        switch = switch.lower() == 'true'

if debug == 1:
    print(f"SWITCH.switch:  {switch}")


# ________LANGS 
if control == 1:

    Text = "Spanish"
    import os
    inlang = os.environ.get('inlang', Text)
    if isinstance(inlang, str):
        if inlang.isdigit():
            inlang = int(inlang)
        elif inlang.replace('.', '', 1).isdigit() and inlang.count('.') < 2:
            inlang = float(inlang)
        elif inlang.lower() in ['true', 'false']:
            inlang = inlang.lower() == 'true'

    Text = "German"
    import os
    outlang = os.environ.get('outlang', Text)
    if isinstance(outlang, str):
        if outlang.isdigit():
            outlang = int(outlang)
        elif outlang.replace('.', '', 1).isdigit() and outlang.count('.') < 2:
            outlang = float(outlang)
        elif outlang.lower() in ['true', 'false']:
            outlang = outlang.lower() == 'true'


    if switch == 1:
        tmpLang = inlang
        inlang = outlang
        outlang = tmpLang
    

if debug == 1:
    print(f"LANGS.inlang:  {inlang}")
    print(f"LANGS.outlang:  {outlang}")


# ________MOCK 
Text = 0
import os
mock = os.environ.get('mock', Text)
if isinstance(mock, str):
    if mock.isdigit():
        mock = int(mock)
    elif mock.replace('.', '', 1).isdigit() and mock.count('.') < 2:
        mock = float(mock)
    elif mock.lower() in ['true', 'false']:
        mock = mock.lower() == 'true'

if debug == 1:
    print(f"MOCK.mock:  {mock}")


# ________QUESTION

Text = "Where is Rachael Tyrell ?"
userQuestion = Text

Text = 1
qquestion = Text

Text = 0
translateQuestion = Text

if debug == 1:
    print(f"QUESTION.userQuestion:  {userQuestion}")
    print(f"QUESTION.qquestion:  {qquestion}")
    print(f"QUESTION.translateQuestion:  {translateQuestion}")


# ________AUDIO

Text = "Rachel"
VOICE_NAME = Text
if debug == 1:
    print(f"XI.VOICE_NAME:  {VOICE_NAME}")


if control == 1:
    Text = 0
    import os
    outaudio = os.environ.get('outaudio', Text)
    if isinstance(outaudio, str):
        if outaudio.isdigit():
            outaudio = int(outaudio)
        elif outaudio.replace('.', '', 1).isdigit() and outaudio.count('.') < 2:
            outaudio = float(outaudio)
        elif outaudio.lower() in ['true', 'false']:
            outaudio = outaudio.lower() == 'true'


    Text = 0
    import os
    inaudio = os.environ.get('inaudio', Text)
    if isinstance(inaudio, str):
        if inaudio.isdigit():
            inaudio = int(inaudio)
        elif inaudio.replace('.', '', 1).isdigit() and inaudio.count('.') < 2:
            inaudio = float(inaudio)
        elif inaudio.lower() in ['true', 'false']:
            inaudio = inaudio.lower() == 'true'


if debug == 1:
    print(f"AUDIO.outaudio:  {outaudio}")
    print(f"AUDIO.inaudio:  {inaudio}")


# ________ELEVEN get voiceid

Text = "21m00Tcm4TlvDq8ikWAM"
XI_VOICE_ID = Text

if not XI_VOICE_ID:

    url = 'https://api.elevenlabs.io/v1/voices'

    Dictionary = {
                "accept": "application/json",
                "xi-api-key": XI_API_KEY
    }
    headers = Dictionary
    import requests
    Contents_of_URL = requests.get(url, headers=headers)
    Contents_of_URL = Contents_of_URL.content

    import json
    Dictionary = json.loads(Contents_of_URL)
    Dictionary_Value = Dictionary['voices']

    for Repeat_Item in Dictionary_Value:
        voice = Repeat_Item
        DICTIONARY_VALUE = voice['name']
        name = DICTIONARY_VALUE
        DICTIONARY_VALUE = voice['voice_id']
        voiceid = DICTIONARY_VALUE
        if name == VOICE_NAME:
            XI_VOICE_ID = voiceid
        


if debug == 1:
    print(f"XI.VOICE_NAME:  {VOICE_NAME}")
    print(f"XI.XI_VOICE_ID:  {XI_VOICE_ID}")


# ________INAUDIO

audioFile = "Recorded_Audio.wav"

if inaudio == 1:
    import sounddevice as sd
    import numpy as np
    import time
    from pynput import mouse
    import pandas as pd
    import scipy.io.wavfile
    sr = 16000  # Sample rate
    seconds = 10  # Duration of recording
    mouseClicked = False
    listener = mouse.Listener(on_click=lambda x, y, button, pressed: exec('global mouseClicked\nmouseClicked=True' if pressed else 'global mouseClicked\nmouseClicked=False'))
    listener.start()
    print('Click to start recording')
    while not mouseClicked:
        time.sleep(0.1)
    print('Recording started. Click mouse to stop recording')
    recording = sd.rec(int(seconds * sr), samplerate=sr, channels=2)
    while mouseClicked:
        time.sleep(0.1)
    sd.wait()
    print('Recording stopped')
    listener.stop()
    timestamp = pd.Timestamp.now().strftime("%Y%m%d-%H%M%S")
    Recorded_Audio = f"Files/{timestamp}.wav"
    scipy.io.wavfile.write(Recorded_Audio, sr, recording)
    print('Recording saved to '+ Recorded_Audio)

    audioFile = Recorded_Audio

    if debug == 1:
        print(f"INAUDIO.audioFile:  {audioFile}")
    



# ________WHISPER get transliteration
scribed_text = " "

if inaudio == 1:
    url = f"https://api.openai.com/v1/audio/transcriptions"
    method = POST

    Dictionary = {
                "accept": "application/json",
                "Authorization": f"Bearer {OPENAI_API_KEY}"
    }
    headers = Dictionary

    Dictionary = {
                'file': open(audioFile, 'rb')
    }
    files = Dictionary

    Dictionary = {
                'model': 'whisper-1'
    }
    data = Dictionary

    import requests
    Contents_of_URL = requests.post(url, headers=headers, files=files, data=data)
    scribed_headers = Contents_of_URL.headers
    import json
    Dictionary = json.loads(Contents_of_URL)
    Dictionary_Value = Dictionary['text']
    scribed_text = Dictionary_Value

    if debug == 1:
        print(f"WHISPER.Contents_of_URL:  {Contents_of_URL}")
        print(f"WHISPER.content headers:  {scribed_headers}")
    


if debug == 1:
    print(f"WHISPER.scribed_text:  {scribed_text}")


# ________ELEVEN speak scribed

if inaudio == 1:
    userQuestion = scribed_text


XI_TEXT = userQuestion
XI_FILE = ""

if debug == 1:
    print(f"XI.XI_TEXT:  {XI_TEXT}")


if outaudio == 1:

    JSON = {
            "text": XI_TEXT,
            "model_id": "eleven_multilingual_v1",
            "voice_settings": {
                "stability": 0.8,
                "similarity_boost": 0.9
            }
        }
    XI_DATA = JSON
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{XI_VOICE_ID}"

    # Create headers and body dictionaries
    Dictionary = {
                "Accept": "application/json",
                "xi-api-key": XI_API_KEY
    }
    headers = Dictionary

    Dictionary = {
                "text": XI_TEXT,
                "model_id": "eleven_multilingual_v1"
    }
    data = Dictionary

    import requests
    Contents_of_URL = requests.post(url, headers=headers, json=data)
    headers = Contents_of_URL.headers
    content = Contents_of_URL.content


    if debug == 1:
        print(f"ELEVEN.Contents_of_URL:  {Contents_of_URL}")
        print(f"ELEVEN.content headers:  {headers}")
    


    # audio Saved_File eg: Files/20230702-155534
    # save content
    os.makedirs('Files', exist_ok=True)
    import pandas as pd
    timestamp = pd.Timestamp.now().strftime("%Y%m%d-%H%M%S")
    Saved_File = f"Files/{timestamp}"
    with open(Saved_File, 'wb') as file: file.write(content)

    print(f"ELEVEN.Saved_File: {Saved_File}")


    # soundFileName: audio file name
    Text = "XIQ.mp3"
    soundFileName = Text

    if debug == 1:
        print(f"ELEVEN.soundFileName: {soundFileName}")
    

    # copy Saved_File to soundFileName, ie. Files/20230702-155534 to Files/XIQ.mp3
    import shutil
    folder = os.path.dirname(Saved_File)
    dst_path = os.path.join(folder, soundFileName)
    Renamed_Item = dst_path
    with open(Renamed_Item, 'wb') as dst, open(Saved_File, 'rb') as src:
        shutil.copyfileobj(src, dst)


    soundFilePath = Renamed_Item

    if debug == 1:
        print(f"ELEVEN.soundFileName: {soundFileName}")
        print(f"ELEVEN.Renamed_Item: {Renamed_Item}")
        print(f"ELEVEN.soundFilePath: {soundFilePath}")
    
   
    import pygame
    import os
    import tempfile
    pygame.init()
    sound_file_path = os.path.join('Files', soundFileName)
    if os.path.isfile(sound_file_path):
        sound_path = sound_file_path
    else:
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(soundFileName.encode())
            sound_path = temp_file.name
    pygame.mixer.music.load(sound_path)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        continue
    pygame.quit()
    if sound_file_path != sound_path:
        os.remove(sound_path)



if debug == 1:
    print(f"ELEVEN.XIQ_FILE:  {XI_FILE}")


# ________OPENAI translate

userQuery = userQuestion
if debug == 1:
    print(f"OPENAI.userQuery:  {userQuery}")


if control == 1:

    Text = "You are a highly qualified translator from any language into "
    Dictionary = {"content": Text, "role": "system"}
    transUserDict = Dictionary
    Text = "Translate into " + outlang + " the following text:  " + userQuery

    if debug == 1:
        print(f"OPENAI.question:  {Text}")
    

    Dictionary = {"content": Text, "role": "user"}
    transSysDict = Dictionary

    Text = {
            "model": "gpt-3.5-turbo",
            "messages": [transUserDict, transSysDict],
            "stop": None,
            "max_tokens": 1000,
            "n": 1,
            "top_p": 1,
            "temperature": 0.9
        }
    data = Text

    if debug == 1:
        print(f"OPENAI.data  {data}")
    

    Dictionary = {
                "Authorization": f"Bearer {OPENAI_API_KEY}",
                "Content-Type": "application/json"
    }
    headers = Dictionary
    url = 'https://api.openai.com/v1/chat/completions'

    Response = "this is a mock response"
    if mock == 0:
        import requests
        Contents_of_URL = requests.post(url, headers=headers, json=data)

        if debug == 1:
            print(f"REQUEST.Contents_of_URL:  {Contents_of_URL}")
        

        Response = Contents_of_URL.json()['choices'][0]['message']['content']
    

    sysResponse = Response
 

if debug == 1:
    print(f"OPENAI.sysResponse:  {sysResponse}")

 
# ________ELEVEN speak scribed
XI_TEXT = sysResponse

if outaudio == 1:
    print(f"XI.XI_TEXT:  {XI_TEXT}")

    TEXT = {
            "text": XI_TEXT,
            "model_id": "eleven_multilingual_v1",
            "voice_settings": {
                "stability": 0.4,
                "similarity_boost": 1.0
            }
        }
    XI_DATA = TEXT
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{XI_VOICE_ID}"

    # Create headers and body dictionaries
    Dictionary = {
                "Accept": "application/json",
                "xi-api-key": XI_API_KEY
    }
    headers = Dictionary

    Dictionary = {
                "text": XI_TEXT,
                "model_id": "eleven_multilingual_v1"
    }
    data = Dictionary

    import requests
    Contents_of_URL = requests.post(url, headers=headers, json=data)
    headers = Contents_of_URL.headers
    content = Contents_of_URL.content

    if debug == 1:
        print(f"ELEVEN.Contents_of_URL:  {Contents_of_URL}")
        print(f"ELEVEN.content headers:  {headers}")
    


    # Renamed_Item = Set_name_of content to XIR.mp3
    # Show "ELEVEN.file: " Renamed_Item
    # Save Renamed_Item (content, {"Ask Where To Save": False, "Overwrite # If File Exists": True})
    # Set_variable XI_RESPONSE to Renamed_Item


    # audio Saved_File eg: Files/20230702-155534
    # save content
    os.makedirs('Files', exist_ok=True)
    import pandas as pd
    timestamp = pd.Timestamp.now().strftime("%Y%m%d-%H%M%S")
    Saved_File = f"Files/{timestamp}"
    with open(Saved_File, 'wb') as file: file.write(content)

    print(f"ELEVEN.Saved_File: {Saved_File}")

    # soundFile: audio file name
    Text = "XIR.mp3"
    soundFile = Text
    if debug == 1:
        print(f"ELEVEN.soundFile: {soundFile}")
    

    # copy Saved_File to soundFile, ie. Files/20230702-155534 to Files/XIR.mp3
    import shutil
    folder = os.path.dirname(Saved_File)
    dst_path = os.path.join(folder, soundFile)
    Renamed_Item = dst_path
    with open(Renamed_Item, 'wb') as dst, open(Saved_File, 'rb') as src:
        shutil.copyfileobj(src, dst)


    if debug == 1:
        print(f"ELEVEN.Renamed_Item: {Renamed_Item}")
    

    soundFilePath = Renamed_Item
    print(f"ELEVEN.soundFilePath: {soundFilePath}")

    if outaudio == 1:
        import pygame
        import os
        import tempfile
        pygame.init()
        sound_file_path = os.path.join('Files', soundFile)
        if os.path.isfile(sound_file_path):
            sound_path = sound_file_path
        else:
            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                temp_file.write(soundFile.encode())
                sound_path = temp_file.name
        pygame.mixer.music.load(sound_path)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            continue
        pygame.quit()
        if sound_file_path != sound_path:
            os.remove(sound_path)

    else:
        print(f"{XI_TEXT}")
    



