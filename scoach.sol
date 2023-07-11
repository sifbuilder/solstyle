Comment ________DEBUG
Text = 1
Set_variable debug from_environ with_default Text
If debug is 1
    Show "DEBUG.debug: " debug
End_If 

Comment ________CONTROL 
Text = 1
Set_variable control to Text
If debug is 1
    Show "CONTROL.control: " control
End_If

Comment ________MOCK 
Text = 1
Set_variable mock from_environ with_default Text
If debug is 1
    Show "MOCK.mock: " mock
End_If

Comment ________CODES 
If control is 1
    Text = "sk-"
    Set_variable OPENAI_API_KEY from_environ
End_If

Comment ________USRQUEST
If debug is 1
    Show "________USRQUEST"
End_If

Text = "I'm applying for the position of Head of the Information Systems at the United Nations. My motivation stems from recognizing the vital role that information systems play in supporting the UN's global initiatives and operations. With my extensive experience and expertise in managing complex information systems, I am confident in my ability to lead and optimize the architecture and operations of the unit, ensuring seamless and efficient information flow for the organization's critical work."

Set_variable usrQuest to Text

Text = 1
Set_variable askQuest to Text  

If debug is 1
    Show "USRQUEST.usrQuest: " usrQuest
    Show "USRQUEST.askQuest: " askQuest
End_If

Comment ________AUDIO
If debug is 1
    Show "________AUDIO"
End_If

Text = 0
Set_variable outaudio from_environ with_default Text

Text = 1
Set_variable inaudio from_environ with_default Text

If debug is 1
    Show "AUDIO.outaudio: " outaudio
    Show "AUDIO.inaudio: " inaudio
End_If

Comment ________LANGS 
If debug is 1
    Show "________LANGS"
End_If 
Text = "English"
Set_variable outlang to Text
Text = 0
Set_variable qoutlang to Text
Text = "Spanish"
Set_variable inlang to Text
Text = 0
Set_variable qinlang to Text

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

Comment ________ROLER 
If debug is 1
    Show "________ROLER"
End_If
Text = "scoach"
Set_variable roler to Text

If debug is 1
    Show "ROLER.roler: " roler
End_If

Comment ________SYSTEM
If debug is 1
    Show "________SYSTEM"
End_If

Text = "You an HR Manager with extensive expertise in human psychology, your task is to evaluate responses from candidates applying for different management positions. The responses you will evalaute pertain to key dimensions such as Motivation, Personal Qualities, Specific skills and experience, Management skills, Activity management, People management, Interpersonal management, and Personal management. The candidate's response should reveal attributes such as people-centric approach, leadership, communication, information sharing, and operational excellence."

Set_variable sysPrompt to Text

Dictionary = Dictionary {content: sysPrompt, role: "system"}
Set_variable sysDict to Dictionary

If debug is 1
    Show "SYSTEM_DICT.sysDict " sysDict
End_If

Comment ________PREQUEST
If debug is 1
    Show "________PREQUEST"
End_If
Text = "Answer in " + outlang
Set_variable preQuest to Text
If debug is 1
    Show "PREQUEST.preQuest: " preQuest"
End_If

Comment ________USER
If debug is 1
    Show "________USER"
    Show "USER.usrQuest: " usrQuest
End_If
If askQuest is 1
    Comment will ask with audio
    If inaudio is 1
        If outlang is "Spanish"
            Speak "como puedo ayudarte ? ... " ({"Wait": True, "Rate": 2.0, "Pitch": 1.5, "Language": "Spanish"})
        Otherwise
            Speak "how can I help you ? ... " ({"Wait": True, "Rate": 2.0, "Pitch": 1.5, "Language": "English"})
        End_If
        If outaudio is 1
            If debug is 1
                Show "USER.using outaudio"
            End_If         
            If inlang is "Spanish"
                Result = Dictate_text ({"Language": "Spanish", "Stop_Listening": "On_Tap"})
                Set_variable usrQuest to Result
            Otherwise
                Result = Dictate_text ({"Language": "English", "Stop_Listening": "On_Tap"})
                Set_variable usrQuest to Result
            End_If
        Otherwise
            If debug is 1
                Show "USER.using inText"
            End_If           
            If outlang is "Spanish"
                Provided_Input = Ask_for_Text with "como puedo ayudarte ?" ({"Default": usrQuest})
                Set_variable usrQuest to Provided_Input
            Otherwise
                Provided_Input = Ask_for_Text with "how can I help you ?" ({"Default": usrQuest})
                Set_variable usrQuest to Provided_Input
            End_If
        End_If
    Otherwise
        Comment will ask with text
         If outaudio is 1
             If outlang is "Spanish"
                 Show "como puedo ayudarte ? ... "
             Otherwise
                 Show "how can I help you ? ... "
             End_If
             If inlang is "Spanish"
                 Dictated_text = Dictate_text ({"Language": "Spanish", "Stop_Listening": "On_Tap"})
                 Set_variable usrQuest to Dictated_text
             Otherwise
                 Dictated_text = Dictate_text ({"Language": "English", "Stop_Listening": "On_Tap"})
                 Set_variable usrQuest to Dictated_text
             End_If
         Otherwise
             If outlang is "Spanish"
                 Provided_Input = Ask_for_Text with "como puedo ayudarte ? ... " ({"Default": usrQuest})
                 Set_variable usrQuest to Provided_Input
             Otherwise
                 Provided_Input = Ask_for_Text with "how can I help you ? ... " ({"Default": usrQuest})
                 Set_variable usrQuest to Provided_Input
             End_If
         End_If
    End_If

End_If
If debug is 1
    Show "USER_QUERY.usrQuest: " usrQuest 
End_If

Comment ________USRDICT
If debug is 1
    Show "________USRDICT"
End_If

Dictionary = Dictionary {"content": "", "role": "user"}
Set_variable usrDict to Dictionary

If control is 1
    If usrQuest has_any_value
        List = List[preQuest, usrQuest]
        Combined_Text = Combine List with New_Lines
        Set_variable question to Combined_Text
        Dictionary = Dictionary {"content": question, "role": "user"}
        Set_variable usrDict to Dictionary
    End_If
End_If
If debug is 1
    Show "USRDICT.usrDict: " usrDict"
End_If

Comment ________REQUEST 
If debug is 1
    Show "________REQUEST"
End_If
Text = "this is a mock response to question " + usrQuest
Set_variable assistantResponse to Text
If control is 1
    Text = {
        "model": "gpt-3.5-turbo",
        "messages": [sysDict, usrDict],
        "stop": None,
        "max_tokens": 1000,
        "n": 1,
        "top_p": 0.9,
        "temperature": 0.75
    }
    Set_variable body to Text
    Set_variable Method to "POST"
    Dictionary = Dictionary {
        "Authorization": "Bearer " + OPENAI_API_KEY,
        "Content-Type": "application/json"
    }
    Set_variable headers to Dictionary  
    Set_variable url to "https://api.openai.com/v1/chat/completions"

    Set_variable Response to "this is a mock response"
    
    If mock is 0
        Contents_of_URL = Get_contents_of url ({Method: POST, Headers: headers, json: body})

        If debug is 1
            Show "REQUEST.Contents_of_URL: " Contents_of_URL
        End_If

        Response = Get_Dict_Value_for choices.1.message.content in Contents_of_URL

        Set_variable assistantResponse to Response
    End_If

    
End_If
If debug is 1
    Show "REQUEST.assistantResponse: " assistantResponse"
End_If

Comment ________RESPONSE 
If debug is 1
    Show "________RESPONSE"
End_If
If control is 1
    If outlang is "Spanish"
        If inaudio is 0
            Show assistantResponse
        Otherwise
            Speak assistantResponse ({"Wait": True, "Rate": 2.0, "Pitch": 1.5, "Language": "Spanish"})    
        End_If    
    Otherwise
        If inaudio is 0
            Show assistantResponse
        Otherwise
            Speak assistantResponse ({"Wait": True, "Rate": 2.0, "Pitch": 1.5, "Language": "English"})    
        End_If
    End_If
End_If

Comment ________NOTES 
If debug is 1
    Show "________NOTES"
End_If
If control is 1
    Dictionary = Dictionary {"role": "assistant", "content": assistantResponse}
    Set_variable responseDict to Dictionary
    List = List[usrDict, responseDict]
    Combined_Text = Combine List with Custom ","
    Text = "[" + Combined_Text + "]"    
    Set_variable newMessages to Text
    Create_note_with newMessages in Messages
    If debug is 1
        Show "SAVE_NOTES.List: " List
    End_If

    List = List[roler, Response]
    Combined_Text = Combine List with New_Lines
    Create_note_with Combined_Text in Responses
    If debug is 1
        Show "SAVE_NOTES.Combined_Text: " Combined_Text
    End_If

End_If

