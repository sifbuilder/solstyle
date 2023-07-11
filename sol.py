# ________DEBUG
Text = 1
debug = Text
if debug == 1:
    print(f"DEBUG.debug:  {debug}")


# ________CONTROL 
Text = 1
control = Text
if debug == 1:
    print(f"CONTROL.control:  {control}")


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


# ________DATE

import datetime
Date = datetime.datetime.now()
FormatedDate = Date.strftime('%Y-%m-%d %H:%M:%S')
nowDate = FormatedDate
if debug == 1:
    print(f"DATE.nowDate:  {nowDate}")


# ________CODES

if control == 1:
    Text = "sk-"
    import os
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY', Text)
    if isinstance(OPENAI_API_KEY, str):
        if OPENAI_API_KEY.isdigit():
            OPENAI_API_KEY = int(OPENAI_API_KEY)
        elif OPENAI_API_KEY.replace('.', '', 1).isdigit() and OPENAI_API_KEY.count('.') < 2:
            OPENAI_API_KEY = float(OPENAI_API_KEY)
        elif OPENAI_API_KEY.lower() in ['true', 'false']:
            OPENAI_API_KEY = OPENAI_API_KEY.lower() == 'true'

    Text = "gapi-"
    import os
    GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY', Text)
    if isinstance(GOOGLE_API_KEY, str):
        if GOOGLE_API_KEY.isdigit():
            GOOGLE_API_KEY = int(GOOGLE_API_KEY)
        elif GOOGLE_API_KEY.replace('.', '', 1).isdigit() and GOOGLE_API_KEY.count('.') < 2:
            GOOGLE_API_KEY = float(GOOGLE_API_KEY)
        elif GOOGLE_API_KEY.lower() in ['true', 'false']:
            GOOGLE_API_KEY = GOOGLE_API_KEY.lower() == 'true'

    Text = "gcse-"
    import os
    GOOGLE_CSE_ID = os.environ.get('GOOGLE_CSE_ID', Text)
    if isinstance(GOOGLE_CSE_ID, str):
        if GOOGLE_CSE_ID.isdigit():
            GOOGLE_CSE_ID = int(GOOGLE_CSE_ID)
        elif GOOGLE_CSE_ID.replace('.', '', 1).isdigit() and GOOGLE_CSE_ID.count('.') < 2:
            GOOGLE_CSE_ID = float(GOOGLE_CSE_ID)
        elif GOOGLE_CSE_ID.lower() in ['true', 'false']:
            GOOGLE_CSE_ID = GOOGLE_CSE_ID.lower() == 'true'



# ________QUESTION

Text = "tell me the principles of mathematics"
import os
quest = os.environ.get('quest', Text)
if isinstance(quest, str):
    if quest.isdigit():
        quest = int(quest)
    elif quest.replace('.', '', 1).isdigit() and quest.count('.') < 2:
        quest = float(quest)
    elif quest.lower() in ['true', 'false']:
        quest = quest.lower() == 'true'


Text = 1
qquestion = Text

Text = 0
translateQuestion = Text
if debug == 1:
    print(f"QUESTION.quest:  {quest}")
    print(f"QUESTION.qquestion:  {qquestion}")
    print(f"QUESTION.translateQuestion:  {translateQuestion}")


# ________AUDIO

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


# ________LANGS 

Text = "english"
import os
inlang = os.environ.get('inlang', Text)
if isinstance(inlang, str):
    if inlang.isdigit():
        inlang = int(inlang)
    elif inlang.replace('.', '', 1).isdigit() and inlang.count('.') < 2:
        inlang = float(inlang)
    elif inlang.lower() in ['true', 'false']:
        inlang = inlang.lower() == 'true'

Text = "english"
import os
outlang = os.environ.get('outlang', Text)
if isinstance(outlang, str):
    if outlang.isdigit():
        outlang = int(outlang)
    elif outlang.replace('.', '', 1).isdigit() and outlang.count('.') < 2:
        outlang = float(outlang)
    elif outlang.lower() in ['true', 'false']:
        outlang = outlang.lower() == 'true'


Text = 0
import os
qinlang = os.environ.get('qinlang', Text)
if isinstance(qinlang, str):
    if qinlang.isdigit():
        qinlang = int(qinlang)
    elif qinlang.replace('.', '', 1).isdigit() and qinlang.count('.') < 2:
        qinlang = float(qinlang)
    elif qinlang.lower() in ['true', 'false']:
        qinlang = qinlang.lower() == 'true'


Text = 0
import os
qoutlang = os.environ.get('qoutlang', Text)
if isinstance(qoutlang, str):
    if qoutlang.isdigit():
        qoutlang = int(qoutlang)
    elif qoutlang.replace('.', '', 1).isdigit() and qoutlang.count('.') < 2:
        qoutlang = float(qoutlang)
    elif qoutlang.lower() in ['true', 'false']:
        qoutlang = qoutlang.lower() == 'true'


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


# ________ROLER 

Text = "You are an empathetic and inspiring conversationalist, creating meaningful connections through your attentive listening and genuine understanding"
sysPrompt = Text

Text = ""
withRole = Text

Text = "Chater"
import os
roler = os.environ.get('roler', Text)
if isinstance(roler, str):
    if roler.isdigit():
        roler = int(roler)
    elif roler.replace('.', '', 1).isdigit() and roler.count('.') < 2:
        roler = float(roler)
    elif roler.lower() in ['true', 'false']:
        roler = roler.lower() == 'true'


Text = 0
import os
qrole = os.environ.get('qrole', Text)
if isinstance(qrole, str):
    if qrole.isdigit():
        qrole = int(qrole)
    elif qrole.replace('.', '', 1).isdigit() and qrole.count('.') < 2:
        qrole = float(qrole)
    elif qrole.lower() in ['true', 'false']:
        qrole = qrole.lower() == 'true'


if qrole == 1:
    List = []
    sysPromptsList = List

    import os
    folder_path = "Notes/Prompts"
    os.makedirs(folder_path, exist_ok=True)
    Note_files = os.listdir(folder_path)
    Note_files = sorted([os.path.join(folder_path, file) for file in Note_files], key=os.path.getctime, reverse=True)
    Notes = []
    for file in Note_files:
        with open(file, 'r') as f:
            Notes.append(f.read())
    for Repeat_Item_1 in Notes:
        import json
        Dictionary = json.loads(Repeat_Item_1)
        for Repeat_Item_2 in Dictionary:
            Dictionary_Value = Repeat_Item_2['role']
            Text = str(Dictionary_Value)

            sysPromptsList.append(Text)


    Choose_Item = input('Choose from ' + str(sysPromptsList) + ':  ')
    roler = Choose_Item

if debug == 1:
    print(f"ROLER.roler:  {roler}")


# ________AGAIN 

if control == 1:
    import os
    folder_path = "Notes/Ontime"
    os.makedirs(folder_path, exist_ok=True)
    Note_files = os.listdir(folder_path)
    Note_files = sorted([os.path.join(folder_path, file) for file in Note_files], key=os.path.getctime, reverse=True)
    Notes = []
    for file in Note_files:
        with open(file, 'r') as f:
            Notes.append(f.read())
    if debug == 1:
        print(f"AGAIN.Notes:  {Notes}")
    
    
    if not Notes:
        roler = roler
    else:
        Item_from_List = Notes[0]
        lastNote = Item_from_List
        Split_Text = lastNote.split("\n")
        Item_from_List = Split_Text[0]
        lastRole = Item_from_List
        Item_from_List = Split_Text[1]
        lastDate = Item_from_List
        import datetime
        Time_Between_Dates = (datetime.datetime.strptime(nowDate, '%Y-%m-%d %H:%M:%S') - datetime.datetime.strptime(lastDate, '%Y-%m-%d %H:%M:%S')).total_seconds()
        diffDate = Time_Between_Dates

        if debug == 1:
            print(f"AGAIN.nowDate:  {nowDate}")
            print(f"AGAIN.lastDate:  {lastDate}")
            print(f"AGAIN.lastRole:  {lastRole}")
            print(f"AGAIN.diffDate:  {diffDate}")
        

        if diffDate:
            if diffDate < 90:
                roler = lastRole
            
        
    

if debug == 1:
    print(f"AGAIN.roler:  {roler}")


# ________USER

userQuery = quest
if qquestion == 1:
    if roler == "Again":
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
                engine.setProperty('rate', 1.0 * 100)  # 1 should be average speed
                engine.setProperty('pitch', 1.0)  # 1 should be average pitch
                engine.say("Dime")
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
                engine.setProperty('rate', 1.0 * 100)  # 1 should be average speed
                engine.setProperty('pitch', 1.0)  # 1 should be average pitch
                engine.say("Tell me")
                if True:
                    engine.runAndWait()

            
        else:
            if outlang == "Spanish":

                try:
                    Provided_Input = input('Dime (Default: ): ')
                    if Provided_Input == '':
                        Provided_Input = ""
                except Exception:
                    Provided_Input = ""

            else:

                try:
                    Provided_Input = input('Tell me (Default: ): ')
                    if Provided_Input == '':
                        Provided_Input = ""
                except Exception:
                    Provided_Input = ""

            
            userQuery = Provided_Input
        
        if inaudio == 1:
            if outlang == "Spanish":
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

            
            userQuery = Result
        else:
            if outlang == "Spanish":

                try:
                    if isinstance(userQuery, str) and userQuery.startswith('"') and userQuery.endswith('"'):
                        userQuery = userQuery[1:-1]
                    Provided_Input = input('Como puedo ayudarte ? (Default: ' + str(userQuery) + '): ')
                    if Provided_Input == '':
                        Provided_Input = userQuery
                except Exception:
                    Provided_Input = userQuery

            else:

                try:
                    if isinstance(userQuery, str) and userQuery.startswith('"') and userQuery.endswith('"'):
                        userQuery = userQuery[1:-1]
                    Provided_Input = input('What can I do for you? (Default: ' + str(userQuery) + '): ')
                    if Provided_Input == '':
                        Provided_Input = userQuery
                except Exception:
                    Provided_Input = userQuery

            
            userQuery = Provided_Input
        
    else:
        if outaudio == 1:
            Text = 2
            import os
            rate = os.environ.get('rate', Text)
            if isinstance(rate, str):
                if rate.isdigit():
                    rate = int(rate)
                elif rate.replace('.', '', 1).isdigit() and rate.count('.') < 2:
                    rate = float(rate)
                elif rate.lower() in ['true', 'false']:
                    rate = rate.lower() == 'true'

            Text = 1.0
            import os
            pitch = os.environ.get('pitch', Text)
            if isinstance(pitch, str):
                if pitch.isdigit():
                    pitch = int(pitch)
                elif pitch.replace('.', '', 1).isdigit() and pitch.count('.') < 2:
                    pitch = float(pitch)
                elif pitch.lower() in ['true', 'false']:
                    pitch = pitch.lower() == 'true'


            if debug == 1:
                print(f"USER.outaudio:  {outaudio}")
                print(f"USER.rate:  {rate}")
                print(f"USER.pitch:  {pitch}")
            

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
                engine.setProperty('rate', rate * 100)  # 1 should be average speed
                engine.setProperty('pitch', pitch)  # 1 should be average pitch
                engine.say("Como puedo ayudarte ? ... ")
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
                engine.setProperty('rate', rate * 100)  # 1 should be average speed
                engine.setProperty('pitch', pitch)  # 1 should be average pitch
                engine.say("What can I do for you? ... ")
                if True:
                    engine.runAndWait()

            
            if inaudio == 1:
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

                    userQuery = Result
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

                    userQuery = Result
                
            else:
                if outlang == "Spanish":

                    try:
                        if isinstance(userQuery, str) and userQuery.startswith('"') and userQuery.endswith('"'):
                            userQuery = userQuery[1:-1]
                        Provided_Input = input('Como puedo ayudarte ? (Default: ' + str(userQuery) + '): ')
                        if Provided_Input == '':
                            Provided_Input = userQuery
                    except Exception:
                        Provided_Input = userQuery

                    userQuery = Provided_Input
                else:

                    try:
                        if isinstance(userQuery, str) and userQuery.startswith('"') and userQuery.endswith('"'):
                            userQuery = userQuery[1:-1]
                        Provided_Input = input('What can I do for you? (Default: ' + str(userQuery) + '): ')
                        if Provided_Input == '':
                            Provided_Input = userQuery
                    except Exception:
                        Provided_Input = userQuery

                    userQuery = Provided_Input
                
            
        else:
            if inaudio == 1:
                if outlang == "Spanish":
                    print(f"Como puedo ayudarte ? ... ")
                else:
                    print(f"What can I do for you? ... ")
                
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

                    userQuery = Result
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

                    userQuery = Result
                
            else:
                if outlang == "Spanish":

                    try:
                        if isinstance(userQuery, str) and userQuery.startswith('"') and userQuery.endswith('"'):
                            userQuery = userQuery[1:-1]
                        Provided_Input = input('Como puedo ayudarte ? ...  (Default: ' + str(userQuery) + '): ')
                        if Provided_Input == '':
                            Provided_Input = userQuery
                    except Exception:
                        Provided_Input = userQuery

                    userQuery = Provided_Input
                else:

                    try:
                        if isinstance(userQuery, str) and userQuery.startswith('"') and userQuery.endswith('"'):
                            userQuery = userQuery[1:-1]
                        Provided_Input = input('What can I do for you? ...  (Default: ' + str(userQuery) + '): ')
                        if Provided_Input == '':
                            Provided_Input = userQuery
                    except Exception:
                        Provided_Input = userQuery

                    userQuery = Provided_Input
                
            
        
    

if debug == 1:
    print(f"USER.userQuery:  {userQuery}")


# ________SYSTEM 

if control == 1:
    import os
    folder_path = "Notes/Prompts"
    os.makedirs(folder_path, exist_ok=True)
    Note_files = os.listdir(folder_path)
    Note_files = sorted([os.path.join(folder_path, file) for file in Note_files], key=os.path.getctime, reverse=True)
    Notes = []
    for file in Note_files:
        with open(file, 'r') as f:
            Notes.append(f.read())
    for Repeat_Item_1 in Notes:
        import json
        Dictionary = json.loads(Repeat_Item_1)
        for Repeat_Item_2 in Dictionary:
            Dictionary_Value = Repeat_Item_2['role']
            Text = str(Dictionary_Value)
            if Text == roler:
                Dictionary_Value = Repeat_Item_2['prompt']
                sysPrompt = Dictionary_Value
            

if debug == 1:
    print(f"SYSTEM.sysPrompt:  {sysPrompt}")


Dictionary = {"content": "", "role": "system"}
sysDict = Dictionary
if control == 1:
    if not sysPrompt:
        if roler == "Again":
            import os
            folder_path = "Notes/Systems"
            os.makedirs(folder_path, exist_ok=True)
            Note_files = os.listdir(folder_path)
            Note_files = sorted([os.path.join(folder_path, file) for file in Note_files], key=os.path.getctime, reverse=True)
            Notes = []
            for file in Note_files:
                with open(file, 'r') as f:
                    Notes.append(f.read())
            sysPrompt = Notes
        else:
            Text = "Your are ChatGPT"
            sysPrompt = Text
        
    

    Dictionary = {"content": sysPrompt, "role": "system"}
    sysDict = Dictionary

if debug == 1:
    print(f"SYSTEM.sysPrompt  {sysPrompt}")


# ________TRANSLATE

if outlang != inlang:

    Text = "You are a highly qualified translator from any language into "
    Dictionary = {"content": Text, "role": "system"}
    transUser = Dictionary
    Text = "Translate into " + outlang +  " the following text:" + userQuery

    Dictionary = {"content": Text, "role": "user"}
    transSystem = Dictionary

    Text = {
            "model": "gpt-3.5-turbo",
            "messages": [ transUser, transSystem ],
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
    if debug == 1:
        print(f"TRANSLATE.headers  {headers}")
    

    url = 'https://api.openai.com/v1/chat/completions'

    Response = "this is a mock response"
    if mock == 0:
        import requests
        Contents_of_URL = requests.post(url, headers=headers, json=data)

        if debug == 1:
            print(f"TRANSLATE.Contents_of_URL:  {Contents_of_URL}")
        

        Response = Contents_of_URL.json()['choices'][0]['message']['content']
    

    transQuestion = Response
    userQuery = transQuestion

if debug == 1:
    print(f"TRANSLATE.userQuery:  {userQuery}")


# ________PREQUEST

Text = "Answer in " + outlang
preQuest = Text
if debug == 1:
    print(f"FOREDICT.preQuest:  {preQuest}")


# ________FOREDICT

Text = ""
foreAnswer = Text

Dictionary = {"content": "", "role": "assistant"}
foreDict = Dictionary

if roler == withRole:
    import os
    folder_path = "Notes/Responses"
    os.makedirs(folder_path, exist_ok=True)
    Note_files = os.listdir(folder_path)
    Note_files = sorted([os.path.join(folder_path, file) for file in Note_files], key=os.path.getctime, reverse=True)
    Notes = []
    for file in Note_files:
        with open(file, 'r') as f:
            Notes.append(f.read())
    Item_from_List = Notes[0]
    Split_Text = Item_from_List.split("\n")
    Item_from_List = Split_Text[1]
    foreAnswer = Item_from_List

    Dictionary = {"content": foreAnswer, "role": "assistant"}
    foreDict = Dictionary

if debug == 1:
    print(f"FOREDICT.foreAnswer:  {foreAnswer}")


# ________QUESTIONDICT

Dictionary = {"content": "", "role": "user"}
questionDict = Dictionary

if control == 1:
    if userQuery:
        List = [preQuest, userQuery]
        Combined_Text = '\n'.join(List)
        question = Combined_Text
        Dictionary = {"content": question, "role": "user"}
        questionDict = Dictionary
    

if debug == 1:
    print(f"QUESTIONDICT.questionDict:  {questionDict}")



# ________REQUEST 

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


if control == 1:
    Text = {
            "model": openaimodel,
            "messages": [ sysDict, foreDict, questionDict ],
            "stop": None,
            "max_tokens": openaitokens,
            "n": 1,
            "top_p": 1,
            "temperature": openaitemp
        }

    if debug == 1:
        print(f"REQUEST.Text  {Text}")
    


    data = Text
 
    if debug == 1:
        print(f"REQUEST.data  {data}")
    

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

        if debug == 1:
            print(f"REQUEST.Response:  {Response}")
        


    
    assistantResponse = Response


if debug == 1:
    print(f"REQUEST.assistantResponse:  {assistantResponse}")


# ________RESPONSE 

if control == 1:
    if outlang == "Spanish":
        if outaudio == 0:
            print(f"{assistantResponse}")
        else:

            Text = 2
            import os
            rate = os.environ.get('rate', Text)
            if isinstance(rate, str):
                if rate.isdigit():
                    rate = int(rate)
                elif rate.replace('.', '', 1).isdigit() and rate.count('.') < 2:
                    rate = float(rate)
                elif rate.lower() in ['true', 'false']:
                    rate = rate.lower() == 'true'

            Text = 1.0
            import os
            pitch = os.environ.get('pitch', Text)
            if isinstance(pitch, str):
                if pitch.isdigit():
                    pitch = int(pitch)
                elif pitch.replace('.', '', 1).isdigit() and pitch.count('.') < 2:
                    pitch = float(pitch)
                elif pitch.lower() in ['true', 'false']:
                    pitch = pitch.lower() == 'true'


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
            engine.setProperty('rate', rate * 100)  # 1 should be average speed
            engine.setProperty('pitch', pitch)  # 1 should be average pitch
            engine.say(assistantResponse)
            if True:
                engine.runAndWait()

        
    else:
        if outaudio == 0:
            print(f"{assistantResponse}")
        else:

            Text = 2
            import os
            rate = os.environ.get('rate', Text)
            if isinstance(rate, str):
                if rate.isdigit():
                    rate = int(rate)
                elif rate.replace('.', '', 1).isdigit() and rate.count('.') < 2:
                    rate = float(rate)
                elif rate.lower() in ['true', 'false']:
                    rate = rate.lower() == 'true'

            Text = 1.0
            import os
            pitch = os.environ.get('pitch', Text)
            if isinstance(pitch, str):
                if pitch.isdigit():
                    pitch = int(pitch)
                elif pitch.replace('.', '', 1).isdigit() and pitch.count('.') < 2:
                    pitch = float(pitch)
                elif pitch.lower() in ['true', 'false']:
                    pitch = pitch.lower() == 'true'


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
            engine.setProperty('rate', rate * 100)  # 1 should be average speed
            engine.setProperty('pitch', pitch)  # 1 should be average pitch
            engine.say(assistantResponse)
            if True:
                engine.runAndWait()

        
    


# ________NOTES 

if control == 1:
    Dictionary = {"role": "assistant", "content": assistantResponse}
    responseDict = Dictionary
    List = [questionDict, responseDict]
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
        print(f"NOTES.List:  {List}")
    

    Combined_Text = '\n'.join(sysDict)
    systemNote = Combined_Text
    if debug == 1:
        print(f"NOTES.systemNote:  {systemNote}")
    

    List = [roler, Response]
    Combined_Text = '\n'.join(List)
    import os
    import re
    dir_path = os.path.join('Notes', 'Responses')
    os.makedirs(dir_path, exist_ok=True)
    valid_filename = re.sub('[^\w\-_\. ]', '_', Combined_Text.split('\n')[0][:80])
    with open(os.path.join(dir_path, valid_filename + '.txt'), 'w') as file:
        file.write(Combined_Text)
    if debug == 1:
        print(f"NOTES.Combined_Text:  {Combined_Text}")
    

    List = [roler, nowDate]
    Combined_Text = '\n'.join(List)
    import os
    import re
    dir_path = os.path.join('Notes', 'Ontime')
    os.makedirs(dir_path, exist_ok=True)
    valid_filename = re.sub('[^\w\-_\. ]', '_', Combined_Text.split('\n')[0][:80])
    with open(os.path.join(dir_path, valid_filename + '.txt'), 'w') as file:
        file.write(Combined_Text)
    if debug == 1:
        print(f"NOTES.Combined_Text:  {Combined_Text}")
    




