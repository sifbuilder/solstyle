from unittest.mock import patch, Mock
from unittest import mock
import unittest
import os
import solstyle
from solstyle_regs import WebNetworkActions, AudioRecordActions, AudioSpeechActions, VariableDictionaryActions, VariableListActions, ControlFlowActions, DateTimeActions, NoteManagementActions, SysopsActions, FileActions, AssignmentActions, VoidActions, TextManipulationActions, PdfFileActions
from solstyle import DataActions, ScriptActions, ArgsActions

#   ========================================
#   TestWebNetworkActions   WebNetworkActions
#


class TestWebNetworkActions(unittest.TestCase):

    # get_contents_of_url_post_action function
    #
    def test__get_contents_of_url_post_action(self):

        self.verb = os.environ.get("verb", "False").lower() in ["1", "true", "yes"]

        line = 'Contents_of_URL = Get_contents_of url ({Method: POST, Headers: headers, json: body})'

        result = WebNetworkActions.get_contents_of_url_post_action(
            line, 0, False, verb=self.verb)

        if result is not None:
            code, in_otherwise_block = result
        else:
            code = in_otherwise_block = None

        expected_output = "import requests\nContents_of_URL = requests.post(url, headers=headers, json=body)"

        self.assertEqual(code, expected_output)

    # get_contents_of_url_get_action
    #
    def test__get_contents_of_url_get_action(self):

        self.verb = os.environ.get("verb", "False").lower() in ["1", "true", "yes"]
        """
        This test covers the HTTP GET method and the handling of headers.
        """
        line = '''
Contents_of_URL = Get_contents_of url ({Method: GET, Headers: headers})
'''
        result = WebNetworkActions.get_contents_of_url_get_action(
            line, 0, False, verb=self.verb)

        if result is not None:
            code, in_otherwise_block = result
        else:
            code = in_otherwise_block = None

        expected_output = '''import requests
Contents_of_URL = requests.get(url, headers=headers)
Contents_of_URL = Contents_of_URL.content
'''
        if code is not None:
            self.assertMultiLineEqual(code.strip(), expected_output.strip())
        else:
            self.assertEqual(code, expected_output)  # If code is None, this checks if expected_output is also None.



#   ========================================
#   TestAudioRecordActions  AudioRecordActions
#
class TestAudioRecordActions(unittest.TestCase):

    # record_audio_tap_action function
    #
    @patch('pandas.Timestamp.now')
    def test__record_audio_tap_action(self, mock_now):

        self.verb = os.environ.get("verb", "False").lower() in ["1", "true", "yes"]

        mock_timestamp = Mock()
        mock_timestamp.strftime.return_value = "20230701-000000"
        mock_now.return_value = mock_timestamp
        line = '''
my_audio = Record_audio({"Audio_Quality": "high", "Start_Recording": "On_Tap", "Finish_Recording": "On_Tap"})
'''
        result = AudioRecordActions.record_audio_tap_action(
            line, 0, False, verb=self.verb)

        if result is not None:
            code, in_otherwise_block = result
        else:
            code = in_otherwise_block = None

        expected_output = '''
import sounddevice as sd
import numpy as np
import time
from pynput import mouse
import pandas as pd
import scipy.io.wavfile
sr = 16000  # Sample rate
seconds = 10  # Duration of recording
mouseClicked = False
listener = mouse.Listener(on_click=lambda x, y, button, pressed: exec('global mouseClicked\\nmouseClicked=True' if pressed else 'global mouseClicked\\nmouseClicked=False'))
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
my_audio = f"Files/{timestamp}.wav"
scipy.io.wavfile.write(my_audio, sr, recording)
print('Recording saved to '+ my_audio)
'''
        self.maxDiff = None
        if code is not None:
            self.assertMultiLineEqual(code.strip(), expected_output.strip())
        else:
            self.assertEqual(code, expected_output)  # If code is None, this checks if expected_output is also None.


    # record_audio_time_action function
    #
    def test__record_audio_time_action(self):

        self.verb = os.environ.get("verb", "False").lower() in ["1", "true", "yes"]

        line = '''
Recorded_Audio = Record_audio({"Audio_Quality": "Medium", "Start_Recording": "On_Tap", "Finish_Recording": "After_Time", "Seconds": 5})
'''
        indent_level = 0
        in_otherwise_block = False

        expected_output = '''
import sounddevice as sd
import numpy as np
import time
from pynput import mouse
fs = 44100  # Sample rate
Recorded_Audio = np.array([])
mouseClicked = False
listener = mouse.Listener(on_click=lambda x, y, button, pressed: exec('global mouseClicked\\nmouseClicked=True' if pressed else 'global mouseClicked\\nmouseClicked=False'))
listener.start()
print('Click to start recording')
while not mouseClicked:
    time.sleep(0.1)
print('Recording started')
recording = sd.rec(int(5 * fs), samplerate=fs, channels=2)
sd.wait()
Recorded_Audio = np.append(Recorded_Audio, recording)
print('Recording stopped')
listener.stop()
'''
        result = AudioRecordActions.record_audio_time_action(
            line, indent_level, in_otherwise_block, verb=self.verb)

        if result is not None:
            code, in_otherwise_block = result
        else:
            code = in_otherwise_block = None

        if code is None:
            print(f"Error occurred for input line: {line}")
        self.maxDiff = None  # Display the full diff
        if code is not None:
            self.assertMultiLineEqual(code.strip(), expected_output.strip())
        else:
            self.assertEqual(code, expected_output)  # If code is None, this checks if expected_output is also None.


    # record_audio_immediately_tap_action
    #
    def test__record_audio_immediately_tap_action(self):

        self.verb = os.environ.get("verb", "False").lower() in ["1", "true", "yes"]

        line = 'Recorded_Audio = Record_audio({"Audio_Quality": "Low", "Start_Recording": "Immediately", "Finish_Recording": "On_Tap"})'
        indent_level = 0
        in_otherwise_block = False

        expected_output = '''
import sounddevice as sd
import numpy as np
import time
from pynput import mouse
fs = 44100  # Sample rate
seconds = 10  # Duration of recording
Recorded_Audio = np.array([])
mouseClicked = False
listener = mouse.Listener(on_click=lambda x, y, button, pressed: exec('global mouseClicked\\nmouseClicked=True' if pressed else 'global mouseClicked\\nmouseClicked=False'))
listener.start()
print('Recording started')
while not mouseClicked:
    recording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
    time.sleep(0.1)
    Recorded_Audio = np.append(Recorded_Audio, recording)
print('Recording stopped')
listener.stop()
'''
        result = AudioRecordActions.record_audio_immediately_tap_action(
            line, indent_level, in_otherwise_block, verb=self.verb)

        if result is not None:
            code, in_otherwise_block = result
        else:
            code = in_otherwise_block = None

        self.maxDiff = None  # Display the full diff
        if code is not None:
            self.assertMultiLineEqual(code.strip(), expected_output.strip())
        else:
            self.assertEqual(code, expected_output)  # If code is None, this checks if expected_output is also None.


    # record_audio_immediately_time_action
    #
    def test__record_audio_immediately_time_action(self):

        self.verb = os.environ.get("verb", "False").lower() in ["1", "true", "yes"]

        line = 'Recorded_Audio = Record_audio({"Audio_Quality": "Medium", "Start_Recording": "Immediately", "Finish_Recording": "After_Time", "Seconds": 8})'
        indent_level = 0
        in_otherwise_block = False

        expected_output = '''
import sounddevice as sd
import numpy as np
fs = 44100  # Sample rate
Recorded_Audio = np.array([])
print('Recording started')
recording = sd.rec(int(8 * fs), samplerate=fs, channels=2)
sd.wait()
Recorded_Audio = np.append(Recorded_Audio, recording)
print('Recording stopped')
'''
        result = AudioRecordActions.record_audio_immediately_time_action(
            line, indent_level, in_otherwise_block, verb=self.verb)

        if result is not None:
            code, in_otherwise_block = result
        else:
            code = in_otherwise_block = None

        self.maxDiff = None  # Display the full diff
        if code is not None:
            self.assertMultiLineEqual(code.strip(), expected_output.strip())
        else:
            self.assertEqual(code, expected_output)  # If code is None, this checks if expected_output is also None.



#   ========================================
#   TestAudioSpeechActions  AudioSpeechActions
#
class TestAudioSpeechActions(unittest.TestCase):

    # dictate_text_tap_action
    #
    def test__dictate_text_tap_action(self):

        self.verb = os.environ.get("verb", "False").lower() in ["1", "true", "yes"]

        line = 'Recorded_Text = Dictate_text({"Language": "English", "Stop_Listening": "On_Tap"})'
        indent_level = 0
        in_otherwise_block = False

        expected_output = '''
import speech_recognition as sr
import time
from pynput import keyboard
r = sr.Recognizer()
Recorded_Text = ""
keyPressed = False
listener = keyboard.Listener(on_press=lambda key: exec('global keyPressed\\nkeyPressed=True'))
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
            Recorded_Text += " " + text
        except sr.UnknownValueError:
            print('Sorry, I did not understand that.')
        except sr.RequestError as e:
            print(f'Could not request results from Google Speech Recognition service: {e}')
print('Your recorded query:', Recorded_Text)
listener.stop()
'''
        result = AudioSpeechActions.dictate_text_tap_action(
            line, indent_level, in_otherwise_block, verb=self.verb)

        if result is not None:
            code, in_otherwise_block = result
        else:
            code = in_otherwise_block = None

        self.maxDiff = None  # Display the full diff
        if code is not None:
            self.assertMultiLineEqual(code.strip(), expected_output.strip())
        else:
            self.assertEqual(code, expected_output)  # If code is None, this checks if expected_output is also None.


    # dictate_text_short_action function
    #
    def test__dictate_text_short_action(self):

        self.verb = os.environ.get("verb", "False").lower() in ["1", "true", "yes"]

        line = 'Recorded_Text = Dictate_text({"Language": "English", "Stop_Listening": "After_Short_Pause"})'
        indent_level = 0
        in_otherwise_block = False

        expected_output = '''
import speech_recognition as sr
r = sr.Recognizer()
with sr.Microphone() as source:
    Recorded_Text = None
    print('Listening...')
    audio = r.listen(source)
    try:
        text = r.recognize_google(audio, language='english')
        print(f'You said: {text}')
        Recorded_Text = text
    except sr.UnknownValueError:
        print('Sorry, I did not understand that.')
        Recorded_Text = None
    except sr.RequestError as e:
        print(f'Could not request results from Google Speech Recognition service: {e}')
        Recorded_Text = None
'''

        result = AudioSpeechActions.dictate_text_short_action(
            line, indent_level, in_otherwise_block, verb=self.verb)

        if result is not None:
            code, in_otherwise_block = result
        else:
            code = in_otherwise_block = None

        self.maxDiff = None  # Display the full diff
        if code is not None:
            self.assertMultiLineEqual(code.strip(), expected_output.strip())
        else:
            self.assertEqual(code, expected_output)  # If code is None, this checks if expected_output is also None.


    # speak_action_with_constants
    #
    def test__speak_action_with_constants(self):

        self.verb = os.environ.get("verb", "False").lower() in ["1", "true", "yes"]

        line = '''
Speak "Hello world" ({ "Wait": True, "Rate": 1.5, "Pitch": 1.2, "Language": "english" })
'''
        indent_level = 0
        in_otherwise_block = False

        expected_output = '''
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
engine.setProperty('rate', 1.5 * 100)  # 1 should be average speed
engine.setProperty('pitch', 1.2)  # 1 should be average pitch
engine.say("Hello world")
if True:
    engine.runAndWait()
'''
        result = AudioSpeechActions.speak_action(
            line, indent_level, in_otherwise_block, verb=self.verb)

        if result is not None:
            code, in_otherwise_block = result
        else:
            code = in_otherwise_block = None

        self.maxDiff = None  # Display the full diff
        if code is not None:
            self.assertMultiLineEqual(code.strip(), expected_output.strip())
        else:
            self.assertEqual(code, expected_output)  # If code is None, this checks if expected_output is also None.


    # speak_action__with_vars
    #
    def test__speak_action__with_vars(self):

        self.verb = os.environ.get("verb", "False").lower() in ["1", "true", "yes"]

        line = '''
Speak "Hello world" ({ "Wait": True, "Rate": rate, "Pitch": pitch, "Language": "english" })
'''
        indent_level = 0
        in_otherwise_block = False

        expected_output = '''
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
engine.say("Hello world")
if True:
    engine.runAndWait()
'''
        result = AudioSpeechActions.speak_action(
            line, indent_level, in_otherwise_block, verb=self.verb)

        if result is not None:
            code, in_otherwise_block = result
        else:
            code = in_otherwise_block = None

        self.maxDiff = None  # Display the full diff
        if code is not None:
            self.assertMultiLineEqual(code.strip(), expected_output.strip())
        else:
            self.assertEqual(code, expected_output)  # If code is None, this checks if expected_output is also None.


    # play_sound_action
    #

    def test__play_sound_action_with_file_name(self):

        self.verb = os.environ.get("verb", "False").lower() in ["1", "true", "yes"]

        line = '''
Play_sound ({"Sound_File": file_name_or_data})
'''
        indent_level = 0
        in_otherwise_block = False

        # This expected_output assumes that 'file_name_or_data' exists in the 'Files' directory
        expected_output = '''
import pygame
import os
import tempfile
pygame.init()
sound_file_path = os.path.join('Files', file_name_or_data)
if os.path.isfile(sound_file_path):
    sound_path = sound_file_path
else:
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(file_name_or_data.encode())
        sound_path = temp_file.name
pygame.mixer.music.load(sound_path)
pygame.mixer.music.play()
while pygame.mixer.music.get_busy():
    continue
pygame.quit()
if sound_file_path != sound_path:
    os.remove(sound_path)
'''
        result = AudioSpeechActions.play_sound_action(
            line, indent_level, in_otherwise_block, verb=self.verb)

        if result is not None:
            code, in_otherwise_block = result
        else:
            code = in_otherwise_block = None

        self.maxDiff = None  # Display the full diff
        if code is not None:
            self.assertMultiLineEqual(code.strip(), expected_output.strip())
        else:
            self.assertEqual(code, expected_output)  # If code is None, this checks if expected_output is also None.



#   ========================================
#   TestVariableDictionaryActions   VariableDictionaryActions
#
class TestVariableDictionaryActions(unittest.TestCase):

    # get_text_action
    #
    def test__get_text_action(self):

        self.verb = os.environ.get("verb", "False").lower() in ["1", "true", "yes"]

        line = 'my_variable = Get_text_from Dictionary_Value'
        indent_level = 1
        in_otherwise_block = False

        expected_output = "    my_variable = str(Dictionary_Value)"
        expected_in_otherwise_block = False

        result = VariableDictionaryActions.get_text_action(
            line, indent_level, in_otherwise_block, verb=self.verb)

        if result is not None:
            code, in_otherwise_block = result
        else:
            code = in_otherwise_block = None

        self.assertEqual(code, expected_output)
        self.assertEqual(in_otherwise_block, expected_in_otherwise_block)

    # ask_for_text_action_case1
    #
    def test__ask_for_text_action_case1(self):

        self.verb = os.environ.get("verb", "False").lower() in ["1", "true", "yes"]

        line = 'Provided_Input = Ask_for_Text with "Como puedo ayudarte ? ... " ({"Default": ""})'

        expected_output = '''
try:
    Provided_Input = input('Como puedo ayudarte ? ...  (Default: ): ')
    if Provided_Input == '':
        Provided_Input = ""
except Exception:
    Provided_Input = ""
'''
        result = VariableDictionaryActions.ask_for_text_action(
            line, 0, False, verb=self.verb)

        if result is not None:
            code, in_otherwise_block = result
        else:
            code = in_otherwise_block = None

        self.maxDiff = None  # Display the full diff
        if code is not None:
            self.assertMultiLineEqual(code.strip(), expected_output.strip())
        else:
            self.assertEqual(code, expected_output)  # If code is None, this checks if expected_output is also None.


    # ask_for_text_action_case2
    #
    def test__ask_for_text_action_case2(self):

        self.verb = os.environ.get("verb", "False").lower() in ["1", "true", "yes"]

        line = 'Provided_Input = Ask_for_Text with "Como puedo ayudarte ? ... " ({"Default": "John"})'

        expected_output = '''
try:
    if isinstance("John", str) and "John".startswith('"') and "John".endswith('"'):
        "John" = "John"[1:-1]
    Provided_Input = input('Como puedo ayudarte ? ...  (Default: ' + str("John") + '): ')
    if Provided_Input == '':
        Provided_Input = "John"
except Exception:
    Provided_Input = "John"
'''
        result = VariableDictionaryActions.ask_for_text_action(
            line, 0, False, verb=self.verb)

        if result is not None:
            code, in_otherwise_block = result
        else:
            code = in_otherwise_block = None

        self.maxDiff = None  # Display the full diff
        if code is not None:
            self.assertMultiLineEqual(code.strip(), expected_output.strip())
        else:
            self.assertEqual(code, expected_output)  # If code is None, this checks if expected_output is also None.


    # ask_for_text_action_case3
    #
    def test__ask_for_text_action_case3(self):

        self.verb = os.environ.get("verb", "False").lower() in ["1", "true", "yes"]

        line = 'Provided_Input = Ask_for_Text with "Como puedo ayudarte ?" ({"Default": userQuery})'

        expected_output = '''
try:
    if isinstance(userQuery, str) and userQuery.startswith('"') and userQuery.endswith('"'):
        userQuery = userQuery[1:-1]
    Provided_Input = input('Como puedo ayudarte ? (Default: ' + str(userQuery) + '): ')
    if Provided_Input == '':
        Provided_Input = userQuery
except Exception:
    Provided_Input = userQuery
'''
        result = VariableDictionaryActions.ask_for_text_action(
            line, 0, False, verb=self.verb)

        if result is not None:
            code, in_otherwise_block = result
        else:
            code = in_otherwise_block = None

        self.maxDiff = None  # Display the full diff

        if code is not None:
            self.assertMultiLineEqual(code.strip(), expected_output.strip())
        else:
            self.assertEqual(code, expected_output)  # If code is None, this checks if expected_output is also None.


    # multi_line_dict_start_action
    #
    def test__multi_line_dict_start_action(self):

        self.verb = os.environ.get("verb", "False").lower() in ["1", "true", "yes"]

        line = 'Dictionary = Dictionary {'
        indent_level = 1
        in_otherwise_block = False

        expected_output = '    Dictionary = {'
        expected_in_otherwise_block = False

        result = VariableDictionaryActions.multi_line_dict_start_action(
            line, indent_level, in_otherwise_block, verb=self.verb)

        if result is not None:
            code, in_otherwise_block = result
        else:
            code = in_otherwise_block = None

        self.assertEqual(code, expected_output)
        self.assertEqual(in_otherwise_block, expected_in_otherwise_block)

    # single_line_dict_assignment_action
    #
    def test__single_line_dict_assignment_action(self):

        self.verb = os.environ.get("verb", "False").lower() in ["1", "true", "yes"]

        line = 'Dictionary = Dictionary { "key": "value" }'
        indent_level = 1
        in_otherwise_block = False

        expected_output = '    Dictionary = { "key": "value" }'
        expected_in_otherwise_block = False

        result = VariableDictionaryActions.single_line_dict_assignment_action(
            line, indent_level, in_otherwise_block, verb=self.verb)

        if result is not None:
            code, in_otherwise_block = result
        else:
            code = in_otherwise_block = None

        self.assertEqual(code, expected_output)
        self.assertEqual(in_otherwise_block, expected_in_otherwise_block)

    # get_dict_from_text_action
    #
    def test__get_dict_from_text_action(self):

        self.verb = os.environ.get("verb", "False").lower() in ["1", "true", "yes"]

        line = 'Dictionary = Get_dictionary_from my_text'
        indent_level = 1
        in_otherwise_block = False

        expected_output = '''
    import json
    Dictionary = json.loads(my_text)
'''
        expected_in_otherwise_block = False

        result = VariableDictionaryActions.get_dict_from_text_action(
            line, indent_level, in_otherwise_block, verb=self.verb)

        if result is not None:
            code, in_otherwise_block = result
        else:
            code = in_otherwise_block = None

        if code is not None:
            self.assertEqual(code.strip(), expected_output.strip())
        else:
            self.assertEqual(code, expected_output)  # if code is None, compare it directly

        self.assertEqual(in_otherwise_block, expected_in_otherwise_block)


    # json_assignment_action
    #
    def test__json_assignment_action(self):

        self.verb = os.environ.get("verb", "False").lower() in ["1", "true", "yes"]

        line = 'my_variable = { "key": "value" }'
        indent_level = 1
        in_otherwise_block = False

        expected_output = '    my_variable = { "key": "value" }'
        expected_in_otherwise_block = False

        result = VariableDictionaryActions.json_assignment_action(
            line, indent_level, in_otherwise_block, verb=self.verb)

        if result is not None:
            code, in_otherwise_block = result
        else:
            code = in_otherwise_block = None

        self.assertEqual(code, expected_output)
        self.assertEqual(in_otherwise_block, expected_in_otherwise_block)

    # dict_value_for_key_action
    #
    def test__dict_value_for_key_action(self):

        self.verb = os.environ.get("verb", "False").lower() in ["1", "true", "yes"]

        line = 'my_variable = Get_Dict_Value_for my_key in my_dict'
        indent_level = 1
        in_otherwise_block = False

        expected_output = "    my_variable = my_dict['my_key']"
        expected_in_otherwise_block = False

        result = VariableDictionaryActions.dict_value_for_key_action(
            line, indent_level, in_otherwise_block, verb=self.verb)

        if result is not None:
            code, in_otherwise_block = result
        else:
            code = in_otherwise_block = None

        self.assertEqual(code, expected_output)
        self.assertEqual(in_otherwise_block, expected_in_otherwise_block)


#   ========================================
#   TestAssignmentActions   AssignmentActions
#
class TestAssignmentActions(unittest.TestCase):

    # set_url_action
    #
    def test__set_url__action(self):

        self.verb = os.environ.get("verb", "False").lower() in ["1", "true", "yes"]

        """
        This test ensures that the URL variable is correctly set to the provided value.
        """
        line = 'Set_variable url to "http://example.com"'
        result = AssignmentActions.set_url_action(
            line, 0, False, verb=self.verb)

        if result is not None:
            code, in_otherwise_block = result
        else:
            code = in_otherwise_block = None

        expected_output = "url = 'http://example.com'"
        self.assertEqual(code, expected_output)

    # sysvar_assignment_action
    #
    def test__sysvar_assignment__action_with_var(self):

        self.verb = os.environ.get("verb", "False").lower() in ["1", "true", "yes"]

        line = 'sys_var = value'
        result = AssignmentActions.sysvar_assignment_action(
            line, 0, False, verb=self.verb)

        if result is not None:
            code, in_otherwise_block = result
        else:
            code = in_otherwise_block = None

        expected_output = 'sys_var = value'
        self.assertEqual(code, expected_output)

    # sysvar_assignment_action_with_texts
    #
    def test__sysvar_assignment__action_with_texts(self):

        self.verb = os.environ.get("verb", "False").lower() in ["1", "true", "yes"]

        line = 'Text = "this is a mock response to question " + usrQuest'
        result = AssignmentActions.sysvar_assignment_action(
            line, 0, False, verb=self.verb)

        if result is not None:
            code, in_otherwise_block = result
        else:
            code = in_otherwise_block = None

        expected_output = 'Text = "this is a mock response to question " + usrQuest'
        self.assertEqual(code, expected_output)

    # variable_assignment_to_action
    #
    def test__set_variable__action(self):

        self.verb = os.environ.get("verb", "False").lower() in ["1", "true", "yes"]

        line = 'Set_variable Text to "Hello, world!"'
        result = AssignmentActions.variable_assignment_to_action(
            line, 0, False, verb=self.verb)

        if result is not None:
            code, in_otherwise_block = result
        else:
            code = in_otherwise_block = None

        expected_output = 'Text = "Hello, world!"'
        self.assertEqual(code, expected_output)

    # variable_assignment_from_env_action_with_default_numeric
    #
    def test__variable_assignment_from_env_action_with_default_numeric(self):

        self.verb = os.environ.get("verb", "False").lower() in ["1", "true", "yes"]

        """
        Test the variable_assignment_from_env_action function with default numeric.
        """
        line = 'Set_variable Text from_environ with_default 1'
        result = AssignmentActions.variable_assignment_from_env_action(
            line, 0, False, verb=self.verb)

        if result is not None:
            code, in_otherwise_block = result
        else:
            code = in_otherwise_block = None

        expected_output = '''
import os
Text = os.environ.get('Text', 1)
if isinstance(Text, str):
    if Text.isdigit():
        Text = int(Text)
    elif Text.replace('.', '', 1).isdigit() and Text.count('.') < 2:
        Text = float(Text)
    elif Text.lower() in ['true', 'false']:
        Text = Text.lower() == 'true'
'''
        if code is not None:
            self.assertMultiLineEqual(code.strip(), expected_output.strip())
        else:
            self.assertEqual(code, expected_output)


    # variable_assignment_from_env_action_with_default_string
    #
    def test__variable_assignment_from_env_action_with_default_string(self):

        self.verb = os.environ.get("verb", "False").lower() in ["1", "true", "yes"]

        """
        Test the variable_assignment_from_env_action function with default string.
        """
        line = 'Set_variable Text from_environ with_default "default value"'
        result = AssignmentActions.variable_assignment_from_env_action(
            line, 0, False, verb=self.verb)

        if result is not None:
            code, in_otherwise_block = result
        else:
            code = in_otherwise_block = None

        expected_output = '''
import os
Text = os.environ.get('Text', "default value")
if isinstance(Text, str):
    if Text.isdigit():
        Text = int(Text)
    elif Text.replace('.', '', 1).isdigit() and Text.count('.') < 2:
        Text = float(Text)
    elif Text.lower() in ['true', 'false']:
        Text = Text.lower() == 'true'
'''
        if code is not None:
            self.assertMultiLineEqual(code.strip(), expected_output.strip())
        else:
            self.assertEqual(code, expected_output)


    # variable_assignment_from_env_no_default_action
    #
    def test__variable_assignment_from_env_no_default_action(self):

        self.verb = os.environ.get("verb", "False").lower() in ["1", "true", "yes"]

        """
        Test the variable_assignment_from_env_no_default_action function.
        """
        line = 'Set_variable Text from_environ'
        result = AssignmentActions.variable_assignment_from_env_no_default_action(
            line, 0, False, verb=self.verb)

        if result is not None:
            code, in_otherwise_block = result
        else:
            code = in_otherwise_block = None

        expected_output = '''
import os
Text = os.environ.get('Text')
if isinstance(Text, str):
    if Text.isdigit():
        Text = int(Text)
    elif Text.replace('.', '', 1).isdigit() and Text.count('.') < 2:
        Text = float(Text)
    elif Text.lower() in ['true', 'false']:
        Text = Text.lower() == 'true'
'''
        if code is not None:
            self.assertMultiLineEqual(code.strip(), expected_output.strip())
        else:
            self.assertEqual(code, expected_output)

    def test_variable_assignment_from_env_no_default_float(self):

        self.verb = os.environ.get("verb", "False").lower() in ["1", "true", "yes"]

        """
        Test the variable_assignment_from_env_no_default_action function for float.
        """
        line = 'Set_variable FloatText from_environ'
        with patch.dict('os.environ', {'FloatText': '1.23'}):
            result = AssignmentActions.variable_assignment_from_env_no_default_action(
                line, 0, False, verb=self.verb)

            if result is not None:
                code, in_otherwise_block = result
            else:
                code = in_otherwise_block = None

            expected_output = '''
import os
FloatText = os.environ.get('FloatText')
if isinstance(FloatText, str):
    if FloatText.isdigit():
        FloatText = int(FloatText)
    elif FloatText.replace('.', '', 1).isdigit() and FloatText.count('.') < 2:
        FloatText = float(FloatText)
    elif FloatText.lower() in ['true', 'false']:
        FloatText = FloatText.lower() == 'true'
'''

            if code is not None:
                self.assertMultiLineEqual(code.strip(), expected_output.strip())
            else:
                self.assertEqual(code, expected_output)


    def test_variable_assignment_from_env_no_default_bool(self):

        self.verb = os.environ.get("verb", "False").lower() in ["1", "true", "yes"]

        """
        Test the variable_assignment_from_env_no_default_action function for boolean.
        """
        line = 'Set_variable BoolText from_environ'
        with patch.dict('os.environ', {'BoolText': 'true'}):
            result = AssignmentActions.variable_assignment_from_env_no_default_action(
                line, 0, False, verb=self.verb)

            if result is not None:
                code, in_otherwise_block = result
            else:
                code = in_otherwise_block = None

            expected_output = '''
import os
BoolText = os.environ.get('BoolText')
if isinstance(BoolText, str):
    if BoolText.isdigit():
        BoolText = int(BoolText)
    elif BoolText.replace('.', '', 1).isdigit() and BoolText.count('.') < 2:
        BoolText = float(BoolText)
    elif BoolText.lower() in ['true', 'false']:
        BoolText = BoolText.lower() == 'true'
'''

            if code is not None:
                self.assertMultiLineEqual(code.strip(), expected_output.strip())
            else:
                self.assertEqual(code, expected_output)


    def test_variable_assignment_from_env_no_default_str(self):

        self.verb = os.environ.get("verb", "False").lower() in ["1", "true", "yes"]

        """
        Test the variable_assignment_from_env_no_default_action function for non-numeric string.
        """
        line = 'Set_variable StrText from_environ'
        with patch.dict('os.environ', {'StrText': 'test'}):
            result = AssignmentActions.variable_assignment_from_env_no_default_action(
                line, 0, False, verb=self.verb)

            if result is not None:
                code, in_otherwise_block = result
            else:
                code = in_otherwise_block = None

            expected_output = '''
import os
StrText = os.environ.get('StrText')
if isinstance(StrText, str):
    if StrText.isdigit():
        StrText = int(StrText)
    elif StrText.replace('.', '', 1).isdigit() and StrText.count('.') < 2:
        StrText = float(StrText)
    elif StrText.lower() in ['true', 'false']:
        StrText = StrText.lower() == 'true'
'''

            if code is not None:
                self.assertMultiLineEqual(code.strip(), expected_output.strip())
            else:
                self.assertEqual(code, expected_output)

#   ========================================
#   TestFileActions FileActions
#
class TestFileActions(unittest.TestCase):

    # save_file_action
    #
    def test__save_file_action(self):

        self.verb = os.environ.get("verb", "False").lower() in ["1", "true", "yes"]

        line = 'my_file = Save_File my_variable {}'
        expected_output = '''
os.makedirs('Files', exist_ok=True)
import pandas as pd
timestamp = pd.Timestamp.now().strftime("%Y%m%d-%H%M%S")
my_file = f"Files/{timestamp}"
with open(my_file, 'wb') as file: file.write(my_variable)
'''
        result = FileActions.save_file_action(
            line, 0, False, verb=self.verb)

        if result is not None:
            code, in_otherwise_block = result
        else:
            code = in_otherwise_block = None

        if code is not None:
            self.assertMultiLineEqual(code.strip(), expected_output.strip())
        else:
            self.assertEqual(code, expected_output)


    # set_name_action
    #

    def test__set_name_action(self):

        self.verb = os.environ.get("verb", "False").lower() in ["1", "true", "yes"]

        """
        This test ensures that the item name is correctly set to the provided value.
        """
        line = 'Renamed_Item = Set_name_of Saved_File to soundFile'
        result = FileActions.set_name_action(
            line, 0, False, verb=self.verb)

        if result is not None:
            code, in_otherwise_block = result
        else:
            code = in_otherwise_block = None

        # Assuming Saved_File is a valid file path
        src_dir = os.path.dirname('Saved_File')

        expected_output = f'''
import shutil
folder = os.path.dirname(Saved_File)
dst_path = os.path.join(folder, soundFile)
Renamed_Item = dst_path
with open(Renamed_Item, 'wb') as dst, open(Saved_File, 'rb') as src:
    shutil.copyfileobj(src, dst)
'''
        if code is not None:
            self.assertMultiLineEqual(code.strip(), expected_output.strip())
        else:
            self.assertEqual(code, expected_output)

#   ========================================
#   TestScriptActions ScriptActions
#
class TestScriptActions(unittest.TestCase):

    @mock.patch("subprocess.run")
    def test_script_run_python(self, mock_run):
        # Run the script_run_python function
        ScriptActions.script_run_python("test.py", False)  # Change this to ScriptActions.script_run_python if needed
        # Check that subprocess.run was called with the expected arguments
        mock_run.assert_called_once_with(["python", "test.py"], env=os.environ.copy())


    def test_script_cases_dict(self):
        argdict = ArgsActions.args_create_argdict()

        # Define some example cases and cmdline_args
        cases = {
            "1": {"file": "test1.sol", "run": True},
            "2": {"file": "test2.sol", "run": False, "desc": "test case 2"}
        }
        cmdline_args = {"file": "testing.sol", "run": False, "proc": True}

        script_name = "myscript.py"
        # get use_cass dict
        use_cases = ScriptActions.script_cases_dict(cases, argdict, cmdline_args, script_name)

        # Check the commands for case 1
        self.assertIn("1", use_cases)
        self.assertIn("python myscript.py -f testing.sol -r", use_cases["1"]["command"])

        ## Check the commands for case 2
        self.assertIn("2", use_cases)
        self.assertIn("python myscript.py -f testing.sol --desc \"test case 2\" -p", use_cases["2"]["command"])


    def test_script_cases_dict_1(self):
        argdict = ArgsActions.args_create_argdict()

        # Define some example cases and cmdline_args
        cases = {
            "1": {"file": "test1.sol", "run": True},
            "2": {"file": "test2.sol", "run": False, "desc": "test case 2"}
        }
        cmdline_args = {"file": "testing.sol", "run": False, "proc": True}

        script_name = "myscript.py"
        # get use_cass dict
        use_cases = ScriptActions.script_cases_dict(cases, argdict, cmdline_args, script_name)

        # Check the commands for case 1
        self.assertIn("1", use_cases)
        self.assertIn("python myscript.py -f testing.sol -r", use_cases["1"]["command"])


    def test_script_cases_dict_2(self):
        argdict = ArgsActions.args_create_argdict()

        # Define some example cases and cmdline_args
        cases = {
            "1": {"file": "test1.sol", "run": True},
            "2": {"file": "test2.sol", "run": False, "desc": "test case 2"}
        }
        cmdline_args = {"file": "testing.sol", "run": False, "proc": True}

        script_name = "solstyle.py"
        # get use_cass dict
        use_cases = ScriptActions.script_cases_dict(cases, argdict, cmdline_args, script_name)

        ## Check the commands for case 2
        self.assertIn("2", use_cases)
        self.assertIn(f"python {script_name} -f testing.sol --desc \"test case 2\" -p", use_cases["2"]["command"])

    def test_script_cases_dict_6(self):
        argdict = ArgsActions.args_create_argdict()

        # Define some example cases and cmdline_args
        cases = {
            "6": {"d": True, "f": "testing.sol", "desc": "testing case", "mock": 0, "inlang": "english", "outlang": "spanish", "inaudio": 0, "outaudio": 0, "openaimodel": "gpt-3.5-turbo", "openaitemp": 0.5, "openaitokens": 100},
        }
        cmdline_args = {"file": "testing.sol", "run": False, "proc": True}

        script_name = "solstyle.py"

        # get use_case dict
        use_cases = ScriptActions.script_cases_dict(cases, argdict, cmdline_args, script_name)

        # Check the commands for case
        self.assertIn("6", use_cases)
        self.assertIn(f'python {script_name} -d -f testing.sol --desc "testing case" --mock 0 --inlang english --outlang spanish --inaudio 0 --outaudio 0 --openaimodel gpt-3.5-turbo --openaitemp 0.5 --openaitokens 100 -p', use_cases["6"]["command"])


    def test_script_cases_dict_7(self):
        argdict = ArgsActions.args_create_argdict()

        # Define some example cases and cmdline_args
        cases = {
            "7": { "d": True, "e": True, "r": True, "mock": 1, "file": "sol.sol" },
        }
        cmdline_args = {"run": False, "proc": True, "c": 7}

        script_name = "solstyle.py"

        # get use_case dict
        use_cases = ScriptActions.script_cases_dict(cases, argdict, cmdline_args, script_name)

        # Check the commands for case
        self.assertIn("7", use_cases)
        self.assertIn(f'python {script_name} -d -e -r --mock 1 -f sol.sol', use_cases["7"]["command"])


    def test_script_cases_dict_9(self):
        argdict = ArgsActions.args_create_argdict()

        # Define some example cases and cmdline_args
        cases = {
            "9": { "debug": True, "mock": 1, "inlang": "spanish", "outlang": "english", "rate": 2.0, "openaimodel": "gpt-3.5-turbo", "openaitemp": 0.5, "openaitokens": 100, "file": "sol.sol"},
        }
        cmdline_args = {"file": "testing.sol", "run": False, "proc": True}

        script_name = "solstyle.py"

        # get use_case dict
        use_cases = ScriptActions.script_cases_dict(cases, argdict, cmdline_args, script_name)

        # Check the commands for case
        self.assertIn("9", use_cases)
        self.assertIn(f'python {script_name} -d --mock 1 --inlang spanish --outlang english --rate 2.0 --openaimodel gpt-3.5-turbo --openaitemp 0.5 --openaitokens 100 -f testing.sol', use_cases["9"]["command"])


#   ========================================
#   TestRuntActions RuntActions
#
import subprocess
from subprocess import Popen, PIPE
class TestRuntActions(unittest.TestCase):


    def test_subprocess_cmd(self):
        argdict = ArgsActions.args_create_argdict()

        # Define some example cases and cmdline_args
        cases = {
            "1": {"file": "test1.sol", "run": True},
        }
        cmdline_args = {"file": "testing.sol", "run": False, "proc": True}

        script_name = "solstyle.py"

        # get use_case dict
        use_cases = ScriptActions.script_cases_dict(cases, argdict, cmdline_args, script_name)

        cmd = use_cases['1']['cmd']

        completed_process = subprocess.run(cmd)

        self.assertEqual(completed_process.returncode, 0)


    def test_popen_cmd(self):
        argdict = ArgsActions.args_create_argdict()

        # Define some example cases and cmdline_args
        cases = {
            "1": {"outaudio": 0, "outlang": "spanish",  "openaimodel": "gpt-3.5-turbo", "openaitemp": 0.5, "openaitokens": 100, "quest": "what is the fundamental theorem of algebra", "file": "testing.sol", "desc": "sol testing"}
        }
        cmdline_args = { "mock": 1, "t": False,  "d": True, "p": True,  "r": True}

        script_name = "solstyle.py"

        use_cases = ScriptActions.script_cases_dict(cases, argdict, cmdline_args, script_name)

        cmd = use_cases['1']['cmd']
        process = Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE)

        # Send the simulated user input (followed by a newline)
        if process.stdin:
            process.stdin.write(b'input\n')
            process.stdin.flush()

        # Make sure to call communicate() at the end
        stdout, stderr = process.communicate()

        self.assertEqual(process.returncode, 0)



#   ========================================
#   
#
if __name__ == "__main__":
    unittest.main(verbosity=2)
