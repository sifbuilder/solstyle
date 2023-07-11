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



# ________CODES________

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

