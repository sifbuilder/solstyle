# ________DEBUG________
Text = 1
Set_variable debug from_environ with_default Text
If debug is 1
    Show "DEBUG.debug: " debug
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


# ________MOCK________

Text = 0
Set_variable mock from_environ with_default Text

Text = "this is a mock response" 
Set_variable mockResponse to Text

If debug is 1
    Show "MOCK.mock: " mock
    Show "MOCK.mockResponse: " mockResponse
End_If
