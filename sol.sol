# ________DEBUG
Text = 1
Set_variable debug to Text
If debug is 1
    Show "DEBUG.debug: " debug
End_If 

# ________CONTROL 
Text = 1
Set_variable control to Text
If debug is 1
    Show "CONTROL.control: " control
End_If

# ________MOCK 
Text = 0
Set_variable mock from_environ with_default Text
If debug is 1
    Show "MOCK.mock: " mock
End_If

# ________DATE

Date = Current_Date
FormatedDate = Format_Date
Set_variable nowDate to FormatedDate
If debug is 1
    Show "DATE.nowDate: " nowDate
End_If

# ________CODES

If control is 1
    Text = "sk-"
    Set_variable OPENAI_API_KEY from_environ with_default Text
    Text = "gapi-"
    Set_variable GOOGLE_API_KEY from_environ with_default Text
    Text = "gcse-"
    Set_variable GOOGLE_CSE_ID from_environ with_default Text
End_If

# ________QUESTION

Text = "tell me the principles of mathematics"
Set_variable quest from_environ with_default Text

Text = 1
Set_variable qquestion to Text

Text = 0
Set_variable translateQuestion to Text  
If debug is 1
    Show "QUESTION.quest: " quest
    Show "QUESTION.qquestion: " qquestion
    Show "QUESTION.translateQuestion: " translateQuestion
End_If

# ________AUDIO

Text = 0
Set_variable outaudio from_environ with_default Text

Text = 0
Set_variable inaudio from_environ with_default Text

If debug is 1
    Show "AUDIO.outaudio: " outaudio
    Show "AUDIO.inaudio: " inaudio
End_If

# ________LANGS 

Text = "english"
Set_variable inlang from_environ with_default Text
Text = "english"
Set_variable outlang from_environ with_default Text

Text = 0
Set_variable qinlang from_environ with_default Text

Text = 0
Set_variable qoutlang from_environ with_default Text

If control is 1
    If qoutlang is 1
        List = List["English", "Spanish"]
        Choose_Item = Choose_from List
        Set_variable outlang to Choose_Item
    End_If
    If qinlang is 1
        List = List["English", "Spanish"]
        Choose_Item = Choose_from List
        Set_variable inlang to Choose_Item
    End_If
End_If

If debug is 1
    Show "LANGS.inlang: " inlang
    Show "LANGS.outlang: " outlang
End_If

# ________ROLER 

Text = "You are an empathetic and inspiring conversationalist, creating meaningful connections through your attentive listening and genuine understanding"
Set_variable sysPrompt to Text

Text = ""
Set_variable withRole to Text

Text = "Chater"
Set_variable roler from_environ with_default Text

Text = 0
Set_variable qrole from_environ with_default Text

If qrole is 1
    List = List[]
    Set_variable sysPromptsList to List

    Notes = Find_Notes where Folder is Prompts
    Repeat_with_each Repeat_Item_1 in Notes
        Dictionary = Get_dictionary_from Repeat_Item_1
        Repeat_with_each Repeat_Item_2 in Dictionary
            Dictionary_Value = Get_Dict_Value_for role in Repeat_Item_2
            Text = Get_text_from Dictionary_Value

            Add Text to sysPromptsList

        End_Repeat
    End_Repeat

    Choose_Item = Choose_from sysPromptsList
    Set_variable roler to Choose_Item
End_If
If debug is 1
    Show "ROLER.roler: " roler
End_If

# ________AGAIN 

If control is 1
    Notes = Find_Notes where Folder is Ontime ({"Sort by" : "Creation Date", Order: "Latest First"})
    If debug is 1
        Show "AGAIN.Notes: " Notes
    End_If
    
    If Notes does_not_have_any_value
        Set_variable roler to roler
    Otherwise
        Item_from_List = Get First_Item from Notes
        Set_variable lastNote to Item_from_List
        Split_Text = Split lastNote by New_Lines
        Item_from_List = Get First_Item from Split_Text
        Set_variable lastRole to Item_from_List
        Item_from_List = Get Item_at_Index 2 from Split_Text
        Set_variable lastDate to Item_from_List       
        Time_Between_Dates = Get_time_between lastDate and nowDate in Seconds
        Set_variable diffDate to Time_Between_Dates

        If debug is 1
            Show "AGAIN.nowDate: " nowDate
            Show "AGAIN.lastDate: " lastDate
            Show "AGAIN.lastRole: " lastRole
            Show "AGAIN.diffDate: " diffDate
        End_If

        If diffDate has_any_value
            If diffDate is_less_than 90
                Set_variable roler to lastRole
            End_If
        End_If
    End_If
End_If
If debug is 1
    Show "AGAIN.roler: " roler
End_If

# ________USER

Set_variable userQuery to quest
If qquestion is 1
    If roler is "Again"
        If outaudio is 1
            If outlang is "Spanish"
                Speak "Dime" ({"Wait": True, "Rate": 1,  "Pitch": 1,  "Language": "Spanish"})
            Otherwise
                Speak "Tell me" ({"Wait": True, "Rate": 1,  "Pitch": 1,  "Language": "English"})
            End_If
        Otherwise
            If outlang is "Spanish"
                Provided_Input = Ask_for_Text with "Dime" ({"Default": ""})
            Otherwise
                Provided_Input = Ask_for_Text with "Tell me" ({"Default": ""})
            End_If
            Set_variable userQuery to Provided_Input
        End_If        
        If inaudio is 1
            If outlang is "Spanish"
                Result = Dictate_text ({"Language": "Spanish", "Stop_Listening": "On_Tap"})
            Otherwise
                Result = Dictate_text ({"Language": "English", "Stop_Listening": "On_Tap"})
            End_If
            Set_variable userQuery to Result
        Otherwise
            If outlang is "Spanish"
                Provided_Input = Ask_for_Text with "Como puedo ayudarte ?" ({"Default": userQuery})
            Otherwise
                Provided_Input = Ask_for_Text with "What can I do for you?" ({"Default": userQuery})
            End_If
            Set_variable userQuery to Provided_Input
        End_If
    Otherwise
        If outaudio is 1
            Text = 2
            Set_variable rate from_environ with_default Text
            Text = 1.0
            Set_variable pitch from_environ with_default Text  

            If debug is 1
                Show "USER.outaudio: " outaudio 
                Show "USER.rate: " rate 
                Show "USER.pitch: " pitch 
            End_If

            If outlang is "Spanish"
                Speak "Como puedo ayudarte ? ... " ({"Wait": True, "Rate": rate,  "Pitch": pitch,  "Language": "Spanish"})
            Otherwise
                Speak "What can I do for you? ... " ({"Wait": True, "Rate": rate,  "Pitch": pitch,  "Language": "English"})
            End_If
            If inaudio is 1
                If inlang is "Spanish"
                    Result = Dictate_text ({"Language": "Spanish", "Stop_Listening": "On_Tap"})
                    Set_variable userQuery to Result
                Otherwise
                    Result = Dictate_text ({"Language": "English", "Stop_Listening": "On_Tap"})
                    Set_variable userQuery to Result
                End_If
            Otherwise
                If outlang is "Spanish"
                    Provided_Input = Ask_for_Text with "Como puedo ayudarte ?" ({"Default": userQuery})
                    Set_variable userQuery to Provided_Input
                Otherwise
                    Provided_Input = Ask_for_Text with "What can I do for you?" ({"Default": userQuery})
                    Set_variable userQuery to Provided_Input
                End_If
            End_If
        Otherwise
            If inaudio is 1
                If outlang is "Spanish"
                    Show "Como puedo ayudarte ? ... "
                Otherwise
                    Show "What can I do for you? ... "
                End_If            
                If inlang is "Spanish"
                    Result = Dictate_text ({"Language": "Spanish", "Stop_Listening": "On_Tap"})
                    Set_variable userQuery to Result
                Otherwise
                    Result = Dictate_text ({"Language": "English", "Stop_Listening": "On_Tap"})
                    Set_variable userQuery to Result
                End_If
            Otherwise
                If outlang is "Spanish"
                    Provided_Input = Ask_for_Text with "Como puedo ayudarte ? ... " ({"Default": userQuery})
                    Set_variable userQuery to Provided_Input
                Otherwise
                    Provided_Input = Ask_for_Text with "What can I do for you? ... " ({"Default": userQuery})
                    Set_variable userQuery to Provided_Input
                End_If
            End_If
        End_If
    End_If
End_If
If debug is 1
    Show "USER.userQuery: " userQuery 
End_If

# ________SYSTEM 

If control is 1
    Notes = Find_Notes where Folder is Prompts
    Repeat_with_each Repeat_Item_1 in Notes
        Dictionary = Get_dictionary_from Repeat_Item_1
        Repeat_with_each Repeat_Item_2 in Dictionary
            Dictionary_Value = Get_Dict_Value_for role in Repeat_Item_2
            Text = Get_text_from Dictionary_Value
            If Text is roler
                Dictionary_Value = Get_Dict_Value_for prompt in Repeat_Item_2
                Set_variable sysPrompt to Dictionary_Value
            End_If
        End_Repeat
    End_Repeat
End_If
If debug is 1
    Show "SYSTEM.sysPrompt: " sysPrompt"
End_If

Dictionary = Dictionary {content: "", role: "system"}
Set_variable sysDict to Dictionary
If control is 1
    If sysPrompt does_not_have_any_value
        If roler is "Again"
            Notes = Find_Notes where Folder is Systems
            Set_variable sysPrompt to Notes
        Otherwise
            Text = "Your are ChatGPT"
            Set_variable sysPrompt to Text
        End_If
    End_If

    Dictionary = Dictionary {content: sysPrompt, role: "system"}
    Set_variable sysDict to Dictionary
End_If
If debug is 1
    Show "SYSTEM.sysPrompt " sysPrompt
End_If

# ________TRANSLATE

If outlang is_not inlang

    Text = "You are a highly qualified translator from any language into "
    Dictionary = Dictionary {"content": Text, "role": "system"}
    Set_variable transUser to Dictionary
    Text = "Translate into " + outlang +  " the following text:" + userQuery

    Dictionary = Dictionary {"content": Text, "role": "user"}
    Set_variable transSystem to Dictionary

    Text = {
        "model": "gpt-3.5-turbo",
        "messages": [ transUser, transSystem ],
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
    If debug is 1
        Show "TRANSLATE.headers " headers
    End_If 

    Set_variable url to "https://api.openai.com/v1/chat/completions"

    Set_variable Response to "this is a mock response"   
    If mock is 0
        Contents_of_URL = Get_contents_of url ({Method: POST, Headers: headers, json: data})

        If debug is 1
            Show "TRANSLATE.Contents_of_URL: " Contents_of_URL
        End_If

        Response = Get_Dict_Value_for choices.1.message.content in Contents_of_URL
    End_If 

    Set_variable transQuestion to Response
    Set_variable userQuery to transQuestion  
End_If
If debug is 1
    Show "TRANSLATE.userQuery: " userQuery"
End_If

# ________PREQUEST

Text = "Answer in " + outlang
Set_variable preQuest to Text
If debug is 1
    Show "FOREDICT.preQuest: " preQuest
End_If

# ________FOREDICT

Text = ""
Set_variable foreAnswer to Text

Dictionary = Dictionary {"content": "", "role": "assistant"}
Set_variable foreDict to Dictionary

If roler is withRole
    Notes = Find_Notes where Folder is Responses ({"Sort by": "Creation Date", Order: "Latest First", Limit: 1})
    Item_from_List = Get First_Item from Notes
    Split_Text = Split Item_from_List by New_Lines
    Item_from_List = Get Items_in_Range 1 to 1 from Split_Text
    Set_variable foreAnswer to Item_from_List

    Dictionary = Dictionary {"content": foreAnswer, "role": "assistant"}
    Set_variable foreDict to Dictionary   
End_If
If debug is 1
    Show "FOREDICT.foreAnswer: " foreAnswer
End_If

# ________QUESTIONDICT

Dictionary = Dictionary {"content": "", "role": "user"}
Set_variable questionDict to Dictionary

If control is 1
    If userQuery has_any_value
        List = List[preQuest, userQuery]
        Combined_Text = Combine List with New_Lines
        Set_variable question to Combined_Text
        Dictionary = Dictionary {"content": question, "role": "user"}
        Set_variable questionDict to Dictionary
    End_If
End_If
If debug is 1
    Show "QUESTIONDICT.questionDict: " questionDict
End_If


# ________REQUEST 

Text = 200
Set_variable openaitokens from_environ with_default Text

Text = "gpt-3.5-turbo"
Set_variable openaimodel from_environ with_default Text

Text = 0.8
Set_variable openaitemp from_environ with_default Text

If debug is 1
    Show "REQUEST.openaitemp " openaitemp
End_If 

If control is 1
    Text = {
        "model": openaimodel,
        "messages": [ sysDict, foreDict, questionDict ],
        "stop": None,
        "max_tokens": openaitokens,
        "n": 1,
        "top_p": 1,
        "temperature": openaitemp
    }

    If debug is 1
        Show "REQUEST.Text " Text
    End_If 


    Set_variable data to Text
 
    If debug is 1
        Show "REQUEST.data " data
    End_If 

    Dictionary = Dictionary {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }
    Set_variable headers to Dictionary  
    If debug is 1
        Show "REQUEST.headers " headers
    End_If 


    Set_variable url to "https://api.openai.com/v1/chat/completions"

    Set_variable Response to "this is a mock response"
    If mock is 0
        Contents_of_URL = Get_contents_of url ({Method: POST, Headers: headers, json: data})

        If debug is 1
            Show "REQUEST.Contents_of_URL: " Contents_of_URL
        End_If 

        Response = Get_Dict_Value_for choices.1.message.content in Contents_of_URL

        If debug is 1
            Show "REQUEST.Response: " Response
        End_If 


    End_If
    Set_variable assistantResponse to Response

End_If
If debug is 1
    Show "REQUEST.assistantResponse: " assistantResponse
End_If

# ________RESPONSE 

If control is 1
    If outlang is "Spanish"
        If outaudio is 0
            Show assistantResponse
        Otherwise    

            Text = 2
            Set_variable rate from_environ with_default Text
            Text = 1.0
            Set_variable pitch from_environ with_default Text  

            Speak assistantResponse ({"Wait": True, "Rate": rate, "Pitch": pitch, "Language": "Spanish"})
        End_If    
    Otherwise
        If outaudio is 0
            Show assistantResponse
        Otherwise

            Text = 2
            Set_variable rate from_environ with_default Text
            Text = 1.0
            Set_variable pitch from_environ with_default Text  

            Speak assistantResponse ({"Wait": True, "Rate": rate, "Pitch": pitch, "Language": "English"})
        End_If
    End_If
End_If

# ________NOTES 

If control is 1
    Dictionary = Dictionary {"role": "assistant", "content": assistantResponse}
    Set_variable responseDict to Dictionary
    List = List[questionDict, responseDict]
    Combined_Text = Combine List with Custom ","
    Text = "[" + Combined_Text + "]"    
    Set_variable newMessages to Text
    Create_note_with newMessages in Messages
    If debug is 1
        Show "NOTES.List: " List
    End_If

    Combined_Text = Combine sysDict with New_Lines
    Set_variable systemNote to Combined_Text
    If debug is 1
        Show "NOTES.systemNote: " systemNote
    End_If

    List = List[roler, Response]
    Combined_Text = Combine List with New_Lines
    Create_note_with Combined_Text in Responses
    If debug is 1
        Show "NOTES.Combined_Text: " Combined_Text
    End_If

    List = List[roler, nowDate]
    Combined_Text = Combine List with New_Lines
    Create_note_with Combined_Text in Ontime
    If debug is 1
        Show "NOTES.Combined_Text: " Combined_Text
    End_If

End_If


