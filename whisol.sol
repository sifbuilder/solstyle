# ________DEBUG________
Text = 1
Set_variable debug from_environ with_default Text
If debug is 1
    Show "DEBUG.debug: " debug
End_If

# ________DESCRIPTION________
Text = "translate inlang to outlang eg: \n python sol.py -t -r -e -m whisol.sol"
Set_variable description to Text
If debug is 1
    Show "DESCRIPTION: " description
End_If

# ________CONTROL ________
Text = 1
Set_variable control to Text
If debug is 1
    Show "CONTROL.control: " control
End_If

# ________CODES________

Text = "sk-"
Set_variable OPENAI_API_KEY from_environ
Text = "gapi-"
Set_variable GOOGLE_API_KEY from_environ
Text = "gcse-"
Set_variable GOOGLE_CSE_ID from_environ
Text = "__xi_api_key__"
Set_variable XI_API_KEY from_environ

# ________LANGS________

Text = "spanish"
Set_variable inlang from_environ with_default Text

Text = "german"
Set_variable outlang from_environ with_default Text

If debug is 1
    Show "LANGS.inlang: " inlang
    Show "LANGS.outlang: " outlang
End_If

# ________MOCK________

Text = 0
Set_variable mock from_environ with_default Text

Text = "this is a mock response" 
Set_variable mockResponse to Text

If debug is 1
    Show "MOCK.mock: " mock
    Show "MOCK.mockResponse: " mockResponse
End_If

# ________QUESTION________

Text = "Where is Rachael Tyrell ?"
Set_variable defaultQuestion to Text

# if questionOnMic, ask user for question on mic
Text = 1
Set_variable questionOnMic to Text

If debug is 1
    Show "QUESTION.defaultQuestion: " defaultQuestion
    Show "QUESTION.questionOnMic: " questionOnMic
End_If

# ________ELEVEN ________

Text = ""
Set_variable XI_VOICE_ID to Text

# voice name
Text = "Rachel"
Set_variable XI_VOICE_NAME to Text

# get XI_VOICE_ID from XI_VOICE_NAME
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
    If name is XI_VOICE_NAME
        XI_VOICE_ID = voiceid
    End_If
End_Repeat

If debug is 1
    Show "ELEVEN.XI_VOICE_NAME: " XI_VOICE_NAME
    Show "ELEVEN.XI_VOICE_ID: " XI_VOICE_ID
End_If

# ________RECORD________

# if questionOnMic, get audioFile with recorded user question

If questionOnMic is 1
    Recorded_Audio = Record_audio ({"Audio_Quality": "Normal", "Start_Recording": "On_Tap", "Finish_Recording": "On_Tap"})
    Set_variable audioFile to Recorded_Audio
End_If

If debug is 1
    Show "RECORD.audioFile: " audioFile
End_If

# ________WHISPER get transliteration________

# initialize scribedText with defaultQuestion
Set_variable scribedText to defaultQuestion

# if recorded question, transliterate voice from audioFile
If questionOnMic is 1

    Set_variable url to f"https://api.openai.com/v1/audio/transcriptions"

    Dictionary = Dictionary {
        "accept": "application/x-wav",
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
    Set_variable scribed_contents to Contents_of_URL.content

    Dictionary = Get_dictionary_from scribed_contents
    Dictionary_Value = Get_Dict_Value_for text in Dictionary
    Set_variable scribedText to Dictionary_Value

    If debug is 1
        Show "WHISPER.Contents_of_URL: " Contents_of_URL
        Show "WHISPER.content headers: " scribed_headers
        Show "WHISPER.content scribedText: " scribedText
    End_If 

End_If

If debug is 1
    Show "WHISPER.scribedText: " scribedText
End_If


# ________OPENAI respond________

# initialize userQuery with scribedText
Set_variable userQuery to scribedText

If debug is 1
    Show "OPENAI.userQuery: " userQuery
End_If

Text = "You are a highly qualified multilingual conversational agent "
Dictionary = Dictionary {"content": Text, "role": "system"}
Set_variable sysDict to Dictionary

Text = "Translate " + userQuery + " into " + outlang + " and respond in :" + outlang
Set_variable userPrompt to Text

If debug is 1
    Show "OPENAI.userPrompt: " userPrompt
End_If 

Dictionary = Dictionary {"content": userPrompt, "role": "user"}
Set_variable usrDict to Dictionary

Text = {
    "model": "gpt-3.5-turbo",
    "messages": [sysDict, usrDict],
    "stop": None,
    "max_tokens": 500,
    "n": 1,
    "top_p": 0.8,
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

If mock is 1

    # if mock, set response with mockResponse
    Set_variable response to mockResponse

Otherwise
    Contents_of_URL = Get_contents_of url ({Method: POST, Headers: headers, json: data})

    If debug is 1
        Show "REQUEST.Contents_of_URL: " Contents_of_URL
    End_If

    Dictionary_Value = Get_Dict_Value_for choices.1.message.content in Contents_of_URL
    Set_variable response to Dictionary_Value

End_If 

If debug is 1
    Show "OPENAI.response: " response
End_If
 
# ________ELEVEN speak scribed________

# initializa XI_TEXT with openai response
Set_variable XI_TEXT to response
If debug is 1
    Show "ELEVEN.XI_TEXT: " XI_TEXT
End_If 

# if we have found a voice id from the voice name
If XI_VOICE_ID has_any_value

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
    Show "ELEVEN.Contents_of_URL: " Contents_of_URL

    # the resulting audio code is in content
    content = Contents_of_URL.content

    # audio Saved_File eg: Files/20230702-155534
    Saved_File = Save_File content {"Ask Where To Save": False, "Overwrite If File Exists": True}
    Show "ELEVEN.Saved_File:" Saved_File

    # soundFile: audio file name
    Text = "XI.mp3"
    Set_variable soundFile to Text
    If debug is 1
        Show "ELEVEN.soundFile:" soundFile
    End_If     

    # copy Saved_File to soundFile, ie. Files/20230702-155534 to Files/XI.mp3
    Renamed_Item = Set_name_of Saved_File to soundFile
    If debug is 1
        Show "ELEVEN.Renamed_Item:" Renamed_Item
    End_If

    Set_variable soundFilePath to Renamed_Item
    Show "ELEVEN.soundFilePath:" soundFilePath    

    Play_sound ({"Sound_File": soundFile})

Otherwise
    Show XI_VOICE_NAME " is not recognized as a XI voice"
End_If

