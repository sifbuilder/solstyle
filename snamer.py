# ________DEBUG________

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


# ________CONTROL________ 

Text = 1
control = Text
if debug == 1:
    print(f"CONTROL.control:  {control}")


# ________CODES________ 

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



# ________MOCK________

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


Text = "this is a mock response" 
mockResponse = Text

if debug == 1:
    print(f"MOCK.mock:  {mock}")
    print(f"MOCK.mockResponse:  {mockResponse}")


# ________USRQUEST________

Text = "how do you name a parser that converts Apple iOS shortcut pseudocode to functional python ?"
usrQuest = Text

Text = 1
askQuest = Text

if debug == 1:
    print(f"USRQUEST.usrQuest:  {usrQuest}")
    print(f"USRQUEST.askQuest:  {askQuest}")


# ________AUDIO________

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


Text = 1
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


# ________LANGS________

Text = "English"
outlang = Text
Text = 0
qoutlang = Text
Text = "Spanish"
inlang = Text
Text = 0
qinlang = Text

if control == 1:
    if qoutlang == 1:
        List = ["English", "Spanish"]
        Choose_Item = input('Choose from ' + str(List) + ':  ')
        outlang = Choose_Item
    
    if qinlang == 1:
        List = ["English", "Spanish"]
        Choose_Item = input('Choose from ' + str(List) + ':  ')
        inlang = Choose_Item
    

if debug == 1:
    print(f"LANGS.inlang:  {inlang}")
    print(f"LANGS.outlang:  {outlang}")


# ________ROLER________ 

Text = "snamer"
roler = Text

if debug == 1:
    print(f"ROLER.roler:  {roler}")


# ________SYSTEM________

Text = "You are a linguistic expert with in-depth knowledge of human psychology. I will present you with the context and purpose of an algorithm and your task is to propose three names that relate to that purpose and will be meaninful to people."
sysPrompt = Text

Dictionary = {"content": sysPrompt, "role": "system"}
sysDict = Dictionary

if debug == 1:
    print(f"SYSTEM_DICT.sysDict  {sysDict}")


# ________PREQUEST________

Text = "Answer in " + outlang
preQuest = Text
if debug == 1:
    print(f"PREQUEST.preQuest:  {preQuest}")


# ________USER________
if debug == 1:
    print(f"User.inaudio:  {inaudio}")
    print(f"User.outaudio:  {outaudio}")


if askQuest == 1:
    # will ask with audio
    if outaudio == 1:
        if outlang == "Spanish":
            import pyttsx3
            engine = pyttsx3.init()
            voices = engine.getProperty('voices')
            voice_id = voices[0].id
            for voice in voices:
                for lang in voice.languages:
                    if 'spanish' in lang.decode().lower():  # Compare language settings
                        voice_id = voice.id
                        break
            engine.setProperty('voice', voice_id)
            engine.setProperty('rate', 2.0 * 100)  # 1 should be average speed
            engine.setProperty('pitch', 1.0)  # 1 should be average pitch
            engine.say("como puedo ayudarte ? ... ")
            if True:
                engine.runAndWait()

        else:
            import pyttsx3
            engine = pyttsx3.init()
            voices = engine.getProperty('voices')
            voice_id = voices[0].id
            for voice in voices:
                for lang in voice.languages:
                    if 'english' in lang.decode().lower():  # Compare language settings
                        voice_id = voice.id
                        break
            engine.setProperty('voice', voice_id)
            engine.setProperty('rate', 2.0 * 100)  # 1 should be average speed
            engine.setProperty('pitch', 1.0)  # 1 should be average pitch
            engine.say("how can I help you ? ... ")
            if True:
                engine.runAndWait()

        
        if inaudio == 1:
            if debug == 1:
                print(f"USER.using inaudio")
            
            if inlang == "Spanish":
                import speech_recognition as sr
                import time
                from pynput import keyboard
                r = sr.Recognizer()
                Result = ""
                keyPressed = False
                listener = keyboard.Listener(on_press=lambda key: exec('global keyPressed\nkeyPressed=True'))
                listener.start()
                with sr.Microphone() as source:
                    print('Listening... press any key to stop')
                    while True:
                        audio = r.listen(source, phrase_time_limit=4)
                        if keyPressed:
                            print('Key pressed, exiting')
                            break
                        try:
                            text = r.recognize_google(audio, language='spanish')
                            print(f'You said: {text}')
                            Result += " " + text
                        except sr.UnknownValueError:
                            print('Sorry, I did not understand that.')
                        except sr.RequestError as e:
                            print(f'Could not request results from Google Speech Recognition service: {e}')
                print('Your recorded query:', Result)
                listener.stop()

                usrQuest = Result
            else:
                import speech_recognition as sr
                import time
                from pynput import keyboard
                r = sr.Recognizer()
                Result = ""
                keyPressed = False
                listener = keyboard.Listener(on_press=lambda key: exec('global keyPressed\nkeyPressed=True'))
                listener.start()
                with sr.Microphone() as source:
                    print('Listening... press any key to stop')
                    while True:
                        audio = r.listen(source, phrase_time_limit=4)
                        if keyPressed:
                            print('Key pressed, exiting')
                            break
                        try:
                            text = r.recognize_google(audio, language='english')
                            print(f'You said: {text}')
                            Result += " " + text
                        except sr.UnknownValueError:
                            print('Sorry, I did not understand that.')
                        except sr.RequestError as e:
                            print(f'Could not request results from Google Speech Recognition service: {e}')
                print('Your recorded query:', Result)
                listener.stop()

                usrQuest = Result
            
        else:
            if debug == 1:
                print(f"USER.using inText")
            
            if outlang == "Spanish":

                try:
                    if isinstance(usrQuest, str) and usrQuest.startswith('"') and usrQuest.endswith('"'):
                        usrQuest = usrQuest[1:-1]
                    Provided_Input = input('como puedo ayudarte ? (Default: ' + str(usrQuest) + '): ')
                    if Provided_Input == '':
                        Provided_Input = usrQuest
                except Exception:
                    Provided_Input = usrQuest

                usrQuest = Provided_Input
            else:

                try:
                    if isinstance(usrQuest, str) and usrQuest.startswith('"') and usrQuest.endswith('"'):
                        usrQuest = usrQuest[1:-1]
                    Provided_Input = input('how can I help you ? (Default: ' + str(usrQuest) + '): ')
                    if Provided_Input == '':
                        Provided_Input = usrQuest
                except Exception:
                    Provided_Input = usrQuest

                usrQuest = Provided_Input
            
        
    else:
        # will ask with text
        if inaudio == 1:
            if outlang == "Spanish":
                print(f"como puedo ayudarte ? ... ")
            else:
                print(f"how can I help you ? ... ")
            
            if inlang == "Spanish":
                import speech_recognition as sr
                import time
                from pynput import keyboard
                r = sr.Recognizer()
                Dictated_text = ""
                keyPressed = False
                listener = keyboard.Listener(on_press=lambda key: exec('global keyPressed\nkeyPressed=True'))
                listener.start()
                with sr.Microphone() as source:
                    print('Listening... press any key to stop')
                    while True:
                        audio = r.listen(source, phrase_time_limit=4)
                        if keyPressed:
                            print('Key pressed, exiting')
                            break
                        try:
                            text = r.recognize_google(audio, language='spanish')
                            print(f'You said: {text}')
                            Dictated_text += " " + text
                        except sr.UnknownValueError:
                            print('Sorry, I did not understand that.')
                        except sr.RequestError as e:
                            print(f'Could not request results from Google Speech Recognition service: {e}')
                print('Your recorded query:', Dictated_text)
                listener.stop()

                usrQuest = Dictated_text
            else:
                import speech_recognition as sr
                import time
                from pynput import keyboard
                r = sr.Recognizer()
                Dictated_text = ""
                keyPressed = False
                listener = keyboard.Listener(on_press=lambda key: exec('global keyPressed\nkeyPressed=True'))
                listener.start()
                with sr.Microphone() as source:
                    print('Listening... press any key to stop')
                    while True:
                        audio = r.listen(source, phrase_time_limit=4)
                        if keyPressed:
                            print('Key pressed, exiting')
                            break
                        try:
                            text = r.recognize_google(audio, language='english')
                            print(f'You said: {text}')
                            Dictated_text += " " + text
                        except sr.UnknownValueError:
                            print('Sorry, I did not understand that.')
                        except sr.RequestError as e:
                            print(f'Could not request results from Google Speech Recognition service: {e}')
                print('Your recorded query:', Dictated_text)
                listener.stop()

                usrQuest = Dictated_text
            
        else:
            if outlang == "Spanish":

                try:
                    if isinstance(usrQuest, str) and usrQuest.startswith('"') and usrQuest.endswith('"'):
                        usrQuest = usrQuest[1:-1]
                    Provided_Input = input('como puedo ayudarte ? ...  (Default: ' + str(usrQuest) + '): ')
                    if Provided_Input == '':
                        Provided_Input = usrQuest
                except Exception:
                    Provided_Input = usrQuest

                usrQuest = Provided_Input
            else:

                try:
                    if isinstance(usrQuest, str) and usrQuest.startswith('"') and usrQuest.endswith('"'):
                        usrQuest = usrQuest[1:-1]
                    Provided_Input = input('how can I help you ? ...  (Default: ' + str(usrQuest) + '): ')
                    if Provided_Input == '':
                        Provided_Input = usrQuest
                except Exception:
                    Provided_Input = usrQuest

                usrQuest = Provided_Input
            
        
    


if debug == 1:
    print(f"USER_QUERY.usrQuest:  {usrQuest}")


Dictionary = {"content": "", "role": "user"}
usrDict = Dictionary

if control == 1:
    if usrQuest:
        List = [preQuest, usrQuest]
        Combined_Text = '\n'.join(List)
        question = Combined_Text
        Dictionary = {"content": question, "role": "user"}
        usrDict = Dictionary
    

if debug == 1:
    print(f"USER.usrDict:  {usrDict}")


# ________REQUEST________ 

Text = 200
import os
openaitokens = os.environ.get('openaitokens', Text)
if isinstance(openaitokens, str):
    if openaitokens.isdigit():
        openaitokens = int(openaitokens)
    elif openaitokens.replace('.', '', 1).isdigit() and openaitokens.count('.') < 2:
        openaitokens = float(openaitokens)
    elif openaitokens.lower() in ['true', 'false']:
        openaitokens = openaitokens.lower() == 'true'


Text = "gpt-3.5-turbo"
import os
openaimodel = os.environ.get('openaimodel', Text)
if isinstance(openaimodel, str):
    if openaimodel.isdigit():
        openaimodel = int(openaimodel)
    elif openaimodel.replace('.', '', 1).isdigit() and openaimodel.count('.') < 2:
        openaimodel = float(openaimodel)
    elif openaimodel.lower() in ['true', 'false']:
        openaimodel = openaimodel.lower() == 'true'


Text = 0.8
import os
openaitemp = os.environ.get('openaitemp', Text)
if isinstance(openaitemp, str):
    if openaitemp.isdigit():
        openaitemp = int(openaitemp)
    elif openaitemp.replace('.', '', 1).isdigit() and openaitemp.count('.') < 2:
        openaitemp = float(openaitemp)
    elif openaitemp.lower() in ['true', 'false']:
        openaitemp = openaitemp.lower() == 'true'


if debug == 1:
    print(f"REQUEST.openaitemp  {openaitemp}")


assistantResponse = mockResponse

if control == 1:
    Text = {
            "model": openaimodel,
            "messages": [sysDict, usrDict],
            "stop": None,
            "max_tokens": openaitokens,
            "n": 1,
            "top_p": 0.9,
            "temperature": openaitemp
        }
    body = Text
    Method = "POST"
    Dictionary = {
                "Authorization": "Bearer " + OPENAI_API_KEY,
                "Content-Type": "application/json"
    }
    headers = Dictionary
    url = 'https://api.openai.com/v1/chat/completions'
    

    if mock == 0:
        import requests
        Contents_of_URL = requests.post(url, headers=headers, json=body)

        if debug == 1:
            print(f"REQUEST.Contents_of_URL:  {Contents_of_URL}")
        

        Response = Contents_of_URL.json()['choices'][0]['message']['content']

        assistantResponse = Response
    

if debug == 1:
    print(f"REQUEST.assistantResponse:  {assistantResponse}")


# ________RESPONSE________ 

if control == 1:
    if outlang == "Spanish":
        if inaudio == 0:
            print(f"{assistantResponse}")
        else:
            import pyttsx3
            engine = pyttsx3.init()
            voices = engine.getProperty('voices')
            voice_id = voices[0].id
            for voice in voices:
                for lang in voice.languages:
                    if 'spanish' in lang.decode().lower():  # Compare language settings
                        voice_id = voice.id
                        break
            engine.setProperty('voice', voice_id)
            engine.setProperty('rate', 2.0 * 100)  # 1 should be average speed
            engine.setProperty('pitch', 1.5)  # 1 should be average pitch
            engine.say(assistantResponse)
            if True:
                engine.runAndWait()

        
    else:
        if inaudio == 0:
            print(f"{assistantResponse}")
        else:
            import pyttsx3
            engine = pyttsx3.init()
            voices = engine.getProperty('voices')
            voice_id = voices[0].id
            for voice in voices:
                for lang in voice.languages:
                    if 'english' in lang.decode().lower():  # Compare language settings
                        voice_id = voice.id
                        break
            engine.setProperty('voice', voice_id)
            engine.setProperty('rate', 2.0 * 100)  # 1 should be average speed
            engine.setProperty('pitch', 1.5)  # 1 should be average pitch
            engine.say(assistantResponse)
            if True:
                engine.runAndWait()

        
    


# ________NOTES________ 

if control == 1:
    Dictionary = {"role": "assistant", "content": assistantResponse}
    responseDict = Dictionary
    List = [usrDict, responseDict]
    if len(List) > 0 and isinstance(List[0], dict):
        import json
        Combined_Text = ','.join(json.dumps(item) for item in List)
    else:
        Combined_Text = ','.join(List)

    Text = "[" + Combined_Text + "]"    
    newMessages = Text
    import os
    import re
    dir_path = os.path.join('Notes', 'Messages')
    os.makedirs(dir_path, exist_ok=True)
    valid_filename = re.sub('[^\w\-_\. ]', '_', newMessages.split('\n')[0][:80])
    with open(os.path.join(dir_path, valid_filename + '.txt'), 'w') as file:
        file.write(newMessages)
    if debug == 1:
        print(f"SAVE_NOTES.List:  {List}")
    

    List = [roler, assistantResponse]
    Combined_Text = '\n'.join(List)
    import os
    import re
    dir_path = os.path.join('Notes', 'Responses')
    os.makedirs(dir_path, exist_ok=True)
    valid_filename = re.sub('[^\w\-_\. ]', '_', Combined_Text.split('\n')[0][:80])
    with open(os.path.join(dir_path, valid_filename + '.txt'), 'w') as file:
        file.write(Combined_Text)
    if debug == 1:
        print(f"SAVE_NOTES.Combined_Text:  {Combined_Text}")
    



