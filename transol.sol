# ________DEBUG
Text = 1
Set_variable debug from_environ with_default Text
If debug is 1
    Show "DEBUG.debug: " debug
End_If

# ________DESCRIPTION
Text = "translate inlang outlang or switch"
Set_variable description to Text
If debug is 1
    Show ":: " description " ::" 
End_If

# ________CONTROL 
Text = 1
Set_variable control to Text
If debug is 1
    Show "CONTROL.control: " control
End_If

# ________CODES 
If control is 1
    Text = "sk-"
    Set_variable OPENAI_API_KEY from_environ
    Text = "gapi-"
    Set_variable GOOGLE_API_KEY from_environ
    Text = "gcse-"
    Set_variable GOOGLE_CSE_ID from_environ

    Text = "__xi_api_key__"
    Set_variable XI_API_KEY from_environ
End_If

# ________SWITCH langs switch
Text = 0
Set_variable switch from_environ with_default Text
If debug is 1
    Show "SWITCH.switch: " switch
End_If

# ________LANGS 
If control is 1

    Text = "Spanish"
    Set_variable inlang from_environ with_default Text
    Text = "German"
    Set_variable outlang from_environ with_default Text

    If switch is 1
        Set_variable tmpLang to inlang
        Set_variable inlang to outlang
        Set_variable outlang to tmpLang
    End_If
End_If
If debug is 1
    Show "LANGS.inlang: " inlang
    Show "LANGS.outlang: " outlang
End_If

# ________MOCK 
Text = 0
Set_variable mock from_environ with_default Text
If debug is 1
    Show "MOCK.mock: " mock
End_If

# ________QUESTION

Text = "Where is Rachael Tyrell ?"
Set_variable userQuestion to Text

Text = 1
Set_variable qquestion to Text

Text = 0
Set_variable translateQuestion to Text  

If debug is 1
    Show "QUESTION.userQuestion: " userQuestion
    Show "QUESTION.qquestion: " qquestion
    Show "QUESTION.translateQuestion: " translateQuestion
End_If

# ________AUDIO

Text = "Rachel"
Set_variable VOICE_NAME to Text
If debug is 1
    Show "XI.VOICE_NAME: " VOICE_NAME
End_If

If control is 1
    Text = 0
    Set_variable outaudio from_environ with_default Text

    Text = 0
    Set_variable inaudio from_environ with_default Text
End_If
If debug is 1
    Show "AUDIO.outaudio: " outaudio
    Show "AUDIO.inaudio: " inaudio
End_If

# ________ELEVEN get voiceid

Text = "21m00Tcm4TlvDq8ikWAM"
Set_variable XI_VOICE_ID to Text

If XI_VOICE_ID does_not_have_any_value

    Set_variable url to "https://api.elevenlabs.io/v1/voices"

    Dictionary = Dictionary {
        "accept": "application/json",
        "xi-api-key": XI_API_KEY
    }
    Set_variable headers to Dictionary
    Contents_of_URL = Get_contents_of url ({Method: GET, Headers: headers})

    Dictionary = Get_dictionary_from Contents_of_URL
    Dictionary_Value = Get_Dict_Value_for voices in Dictionary

    Repeat_with_each Repeat_Item in Dictionary_Value
        Set_variable voice to Repeat_Item
        DICTIONARY_VALUE = Get_Dict_Value_for name in voice
        Set_variable name to DICTIONARY_VALUE
        DICTIONARY_VALUE = Get_Dict_Value_for voice_id in voice
        Set_variable voiceid to DICTIONARY_VALUE
        If name is VOICE_NAME
            XI_VOICE_ID = voiceid
        End_If
    End_Repeat

End_If
If debug is 1
    Show "XI.VOICE_NAME: " VOICE_NAME
    Show "XI.XI_VOICE_ID: " XI_VOICE_ID
End_If

# ________INAUDIO

Set_variable audioFile to "Recorded_Audio.wav"

If inaudio is 1
    Recorded_Audio = Record_audio ({"Audio_Quality": "Normal", "Start_Recording": "On_Tap", "Finish_Recording": "On_Tap"})
    Set_variable audioFile to Recorded_Audio

    If debug is 1
        Show "INAUDIO.audioFile: " audioFile
    End_If

End_If

# ________WHISPER get transliteration
Set_variable scribed_text to " "

If inaudio is 1
    Set_variable url to f"https://api.openai.com/v1/audio/transcriptions"
    Set_variable method to POST

    Dictionary = Dictionary {
        "accept": "application/json",
        "Authorization": f"Bearer {OPENAI_API_KEY}"
    }
    Set_variable headers to Dictionary

    Dictionary = Dictionary {
        'file': open(audioFile, 'rb')
    }
    Set_variable files to Dictionary

    Dictionary = Dictionary {
        'model': 'whisper-1'
    }
    Set_variable data to Dictionary

    Contents_of_URL = Get_contents_of url ({Method: POST, Headers: headers, files: files, data: data})
    Set_variable scribed_headers to Contents_of_URL.headers
    Dictionary = Get_dictionary_from Contents_of_URL.content
    Dictionary_Value = Get_Dict_Value_for text in Dictionary
    Set_variable scribed_text to Dictionary_Value

    If debug is 1
        Show "WHISPER.Contents_of_URL: " Contents_of_URL
        Show "WHISPER.content headers: " scribed_headers
    End_If 

End_If
If debug is 1
    Show "WHISPER.scribed_text: " scribed_text
End_If

# ________ELEVEN speak scribed

If inaudio is 1
    Set_variable userQuestion to scribed_text
End_If

Set_variable XI_TEXT to userQuestion
Set_variable XI_FILE to ""

If debug is 1
    Show "XI.XI_TEXT: " XI_TEXT
End_If

If outaudio is 1

    JSON = {
        "text": XI_TEXT,
        "model_id": "eleven_multilingual_v1",
        "voice_settings": {
            "stability": 0.8,
            "similarity_boost": 0.9
        }
    }
    Set_variable XI_DATA to JSON
    Set_variable url to f"https://api.elevenlabs.io/v1/text-to-speech/{XI_VOICE_ID}"

    # Create headers and body dictionaries
    Dictionary = Dictionary {
        "Accept": "application/json",
        "xi-api-key": XI_API_KEY
    }
    Set_variable headers to Dictionary

    Dictionary = Dictionary {
        "text": XI_TEXT,
        "model_id": "eleven_multilingual_v1"
    }
    Set_variable data to Dictionary

    Contents_of_URL = Get_contents_of url ({Method: POST, Headers: headers, json: data})
    headers = Contents_of_URL.headers
    content = Contents_of_URL.content


    If debug is 1
        Show "ELEVEN.Contents_of_URL: " Contents_of_URL
        Show "ELEVEN.content headers: " headers
    End_If 


    # audio Saved_File eg: Files/20230702-155534
    # save content
    Saved_File = Save_File content {"Ask Where To Save": False, "Overwrite If File Exists": True}
    Show "ELEVEN.Saved_File:" Saved_File


    # soundFileName: audio file name
    Text = "XIQ.mp3"
    Set_variable soundFileName to Text

    If debug is 1
        Show "ELEVEN.soundFileName:" soundFileName
    End_If     

    # copy Saved_File to soundFileName, ie. Files/20230702-155534 to Files/XIQ.mp3
    Renamed_Item = Set_name_of Saved_File to soundFileName

    Set_variable soundFilePath to Renamed_Item

    If debug is 1
        Show "ELEVEN.soundFileName:" soundFileName
        Show "ELEVEN.Renamed_Item:" Renamed_Item
        Show "ELEVEN.soundFilePath:" soundFilePath
    End_If 
   
    Play_sound ({"Sound_File": soundFileName})

End_If
If debug is 1
    Show "ELEVEN.XIQ_FILE: " XI_FILE
End_If 

# ________OPENAI translate

Set_variable userQuery to userQuestion
If debug is 1
    Show "OPENAI.userQuery: " userQuery
End_If 

If control is 1

    Text = "You are a highly qualified translator from any language into "
    Dictionary = Dictionary {"content": Text, "role": "system"}
    Set_variable transUserDict to Dictionary
    Text = "Translate into " + outlang + " the following text:  " + userQuery

    If debug is 1
        Show "OPENAI.question: " Text
    End_If 

    Dictionary = Dictionary {"content": Text, "role": "user"}
    Set_variable transSysDict to Dictionary

    Text = {
        "model": "gpt-3.5-turbo",
        "messages": [transUserDict, transSysDict],
        "stop": None,
        "max_tokens": 1000,
        "n": 1,
        "top_p": 1,
        "temperature": 0.9
    }
    Set_variable data to Text

    If debug is 1
        Show "OPENAI.data " data
    End_If 

    Dictionary = Dictionary {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }
    Set_variable headers to Dictionary  
    Set_variable url to "https://api.openai.com/v1/chat/completions"

    Set_variable Response to "this is a mock response"   
    If mock is 0
        Contents_of_URL = Get_contents_of url ({Method: POST, Headers: headers, json: data})

        If debug is 1
            Show "REQUEST.Contents_of_URL: " Contents_of_URL
        End_If

        Response = Get_Dict_Value_for choices.1.message.content in Contents_of_URL
    End_If 

    Set_variable sysResponse to Response
 
End_If 
If debug is 1
    Show "OPENAI.sysResponse: " sysResponse
End_If
 
# ________ELEVEN speak scribed
Set_variable XI_TEXT to sysResponse

If outaudio is 1
    Show "XI.XI_TEXT: " XI_TEXT

    TEXT = {
        "text": XI_TEXT,
        "model_id": "eleven_multilingual_v1",
        "voice_settings": {
            "stability": 0.4,
            "similarity_boost": 1.0
        }
    }
    Set_variable XI_DATA to TEXT
    Set_variable url to f"https://api.elevenlabs.io/v1/text-to-speech/{XI_VOICE_ID}"

    # Create headers and body dictionaries
    Dictionary = Dictionary {
        "Accept": "application/json",
        "xi-api-key": XI_API_KEY
    }
    Set_variable headers to Dictionary

    Dictionary = Dictionary {
        "text": XI_TEXT,
        "model_id": "eleven_multilingual_v1"
    }
    Set_variable data to Dictionary

    Contents_of_URL = Get_contents_of url ({Method: POST, Headers: headers, json: data})
    headers = Contents_of_URL.headers
    content = Contents_of_URL.content

    If debug is 1
        Show "ELEVEN.Contents_of_URL: " Contents_of_URL
        Show "ELEVEN.content headers: " headers
    End_If 


    # Renamed_Item = Set_name_of content to XIR.mp3
    # Show "ELEVEN.file: " Renamed_Item
    # Save Renamed_Item (content, {"Ask Where To Save": False, "Overwrite # If File Exists": True})
    # Set_variable XI_RESPONSE to Renamed_Item


    # audio Saved_File eg: Files/20230702-155534
    # save content
    Saved_File = Save_File content {"Ask Where To Save": False, "Overwrite If File Exists": True}
    Show "ELEVEN.Saved_File:" Saved_File

    # soundFile: audio file name
    Text = "XIR.mp3"
    Set_variable soundFile to Text
    If debug is 1
        Show "ELEVEN.soundFile:" soundFile
    End_If     

    # copy Saved_File to soundFile, ie. Files/20230702-155534 to Files/XIR.mp3
    Renamed_Item = Set_name_of Saved_File to soundFile

    If debug is 1
        Show "ELEVEN.Renamed_Item:" Renamed_Item
    End_If

    Set_variable soundFilePath to Renamed_Item
    Show "ELEVEN.soundFilePath:" soundFilePath 

    If outaudio is 1
        Play_sound ({"Sound_File": soundFile})
    Otherwise
        Show XI_TEXT
    End_If

End_If

