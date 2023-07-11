import shutil
import re
import os
import sys
import argparse
import subprocess
import unittest

INDENTATION_AMOUNT = 4  # Number of spaces for each level of indentation
INDENTATION_CHAR = " "
INDENTATION_STRING = INDENTATION_CHAR * INDENTATION_AMOUNT
NEW_LINE = "\n"
CATEGORY_PARSING_MAP = {}

#   ===============================================
#   web_network_actions - WebNetworkActions
#


class WebNetworkActions:
    @staticmethod
    def get_contents_of_url_post_action(
        line, indent_level, in_otherwise_block, verb=False
    ):
        """
        Function to parse and execute 'POST' method for a URL.

        :param line: String to be parsed.
        :param indent_level: Level of indentation for code.
        :param in_otherwise_block: If the line is in otherwise block.
        :return: Tuple (parsed string, in_otherwise_block).
        """
        GET_CONTENTS_OF_URL_POST_REGEX = r"^\s*Contents_of_URL\s*=\s*Get_contents_of\s*url\s*\(\s*\{Method:\s*POST,\s*Headers:\s*(\w+),\s*((?:files|json|data):\s*\w+\s*,?\s*)*\}\s*\)$"
        match = re.match(GET_CONTENTS_OF_URL_POST_REGEX, line)
        if match:
            print(f"GET_CONTENTS_OF_URL_POST_REGEX") if verb else None
            for i, value in enumerate(match.groups(), start=1):
                print(f"\tGroup {i}: {value}") if verb else None
            indentation = INDENTATION_CHAR * INDENTATION_AMOUNT * indent_level
            headers_var = match.group(1)
            body_vars = re.findall(
                r"((?:files|json|data|body)):\s*(\w+)", line)
            parsed_line = f"{indentation}Contents_of_URL = requests.post(url, headers={headers_var}"
            for body_type, body_var in body_vars:
                parsed_line += f", {body_type}={body_var}"
            parsed_line += ")"
            return f"{indentation}import requests\n{parsed_line}", in_otherwise_block
        return None

    @staticmethod
    def get_contents_of_url_get_action(
        line, indent_level, in_otherwise_block, verb=False
    ):
        """
        Function to parse and execute 'GET' method for a URL.

        :param line: String to be parsed.
        :param indent_level: Level of indentation for code.
        :param in_otherwise_block: If the line is in otherwise block.
        :return: Tuple (parsed string, in_otherwise_block).
        """
        GET_CONTENTS_OF_URL_GET_REGEX = r"^\s*Contents_of_URL\s*=\s*Get_contents_of\s*url\s*\(\s*\{Method:\s*GET,\s*Headers:\s*(\w+)\}\s*\)$"
        match = re.match(GET_CONTENTS_OF_URL_GET_REGEX, line)
        if match:
            print(f"GET_CONTENTS_OF_URL_GET_REGEX") if verb else None
            for i, value in enumerate(match.groups(), start=1):
                print(f"\tGroup {i}: {value}") if verb else None
            indentation = INDENTATION_CHAR * INDENTATION_AMOUNT * indent_level
            headers_var = match.group(1)
            code = f"{indentation}import requests\n"
            code += f"{indentation}Contents_of_URL = requests.get(url, headers={headers_var})\n"
            code += f"{indentation}Contents_of_URL = Contents_of_URL.content"
            return code, in_otherwise_block
        return None


#   ===============================================
#   audio_record_actions - AudioRecordActions
#
class AudioRecordActions:
    @staticmethod
    def record_audio_tap_action(line, indent_level, in_otherwise_block, verb=False):
        """
        Converts the 'Record_audio' pseudo code to Python code when 'On_Tap' action is triggered for both starting and stopping the recording.
        """
        RECORD_AUDIO_TAP_REGEX = r"^\s*(\w+)\s*=\s*Record_audio\s*\(\s*\{\s*\"Audio_Quality\":\s*\"(\w+)\",\s*\"Start_Recording\":\s*\"(On_Tap)\",\s*\"Finish_Recording\":\s*\"(On_Tap)\"\s*\}\s*\)\s*$"
        match = re.match(RECORD_AUDIO_TAP_REGEX, line)
        if match:
            print(f"RECORD_AUDIO_TAP_REGEX") if verb else None
            for i, value in enumerate(match.groups(), start=1):
                print(f"\tGroup {i}: {value}") if verb else None
            var_name = match.group(1)
            audio_quality = match.group(2).lower()
            start_recording = match.group(3)
            finish_recording = match.group(4)

            indentation = INDENTATION_CHAR * INDENTATION_AMOUNT * indent_level
            code = ""
            code += f"{indentation}import sounddevice as sd\n"
            code += f"{indentation}import numpy as np\n"
            code += f"{indentation}import time\n"
            code += f"{indentation}from pynput import mouse\n"
            code += f"{indentation}import pandas as pd\n"
            code += f"{indentation}import scipy.io.wavfile\n"
            code += f"{indentation}sr = 16000  # Sample rate\n"
            code += f"{indentation}seconds = 10  # Duration of recording\n"
            code += f"{indentation}mouseClicked = False\n"
            code += f"{indentation}listener = mouse.Listener(on_click=lambda x, y, button, pressed: exec('global mouseClicked\\nmouseClicked=True' if pressed else 'global mouseClicked\\nmouseClicked=False'))\n"
            code += f"{indentation}listener.start()\n"
            code += f"{indentation}print('Click to start recording')\n"
            code += f"{indentation}while not mouseClicked:\n"
            code += f"{indentation}{INDENTATION_STRING * 1}time.sleep(0.1)\n"
            code += f"{indentation}print('Recording started. Click mouse to stop recording')\n"
            code += f"{indentation}recording = sd.rec(int(seconds * sr), samplerate=sr, channels=2)\n"
            code += f"{indentation}while mouseClicked:\n"
            code += f"{indentation}{INDENTATION_STRING * 1}time.sleep(0.1)\n"
            code += f"{indentation}sd.wait()\n"
            code += f"{indentation}print('Recording stopped')\n"
            code += f"{indentation}listener.stop()\n"
            code += f'{indentation}timestamp = pd.Timestamp.now().strftime("%Y%m%d-%H%M%S")\n'
            code += f'{indentation}{var_name} = f"Files/{{timestamp}}.wav"\n'
            code += f"{indentation}scipy.io.wavfile.write({var_name}, sr, recording)\n"
            code += f"{indentation}print('Recording saved to '+ {var_name})\n"

            return code, in_otherwise_block
        return None

    @staticmethod
    def record_audio_time_action(line, indent_level, in_otherwise_block, verb=False):
        """
        Converts the 'Record_audio' pseudo code to Python code when 'On_Tap' action starts and 'After_Time' action stops the recording.
        """
        RECORD_AUDIO_TIME_REGEX = r"^\s*(\w+)\s*=\s*Record_audio\s*\(\s*\{\s*\"Audio_Quality\":\s*\"(\w+)\",\s*\"Start_Recording\":\s*\"(On_Tap)\",\s*\"Finish_Recording\":\s*\"(After_Time)\",\s*\"Seconds\":\s*(\d+)\s*\}\s*\)\s*$"
        match = re.match(RECORD_AUDIO_TIME_REGEX, line)
        if match:
            print(f"RECORD_AUDIO_TIME_REGEX") if verb else None
            for i, value in enumerate(match.groups(), start=1):
                print(f"\tGroup {i}: {value}") if verb else None
            audio_quality = match.group(1).lower()
            start_recording = match.group(2)
            finish_recording = match.group(3)
            seconds = match.group(5)  # Duration of recording
            var_name = match.group(1)

            indentation = INDENTATION_CHAR * INDENTATION_AMOUNT * indent_level
            code = ""
            code += f"{indentation}import sounddevice as sd\n"
            code += f"{indentation}import numpy as np\n"
            code += f"{indentation}import time\n"
            code += f"{indentation}from pynput import mouse\n"
            code += f"{indentation}fs = 44100  # Sample rate\n"
            # Initialize variable before while loop
            code += f"{indentation}{var_name} = np.array([])\n"
            code += f"{indentation}mouseClicked = False\n"
            code += f"{indentation}listener = mouse.Listener(on_click=lambda x, y, button, pressed: exec('global mouseClicked\\nmouseClicked=True' if pressed else 'global mouseClicked\\nmouseClicked=False'))\n"
            code += f"{indentation}listener.start()\n"
            code += f"{indentation}print('Click to start recording')\n"
            # Loop until mouse click
            code += f"{indentation}while not mouseClicked:\n"
            code += f"{indentation}{INDENTATION_STRING * 1}time.sleep(0.1)\n"
            code += f"{indentation}print('Recording started')\n"
            code += f"{indentation}recording = sd.rec(int({seconds} * fs), samplerate=fs, channels=2)\n"
            code += f"{indentation}sd.wait()\n"
            code += f"{indentation}{var_name} = np.append({var_name}, recording)\n"
            code += f"{indentation}print('Recording stopped')\n"
            code += f"{indentation}listener.stop()\n"

            return code, in_otherwise_block
        return None

    @staticmethod
    def record_audio_immediately_tap_action(
        line, indent_level, in_otherwise_block, verb=False
    ):
        """
        Converts the 'Record_audio' pseudo code to Python code when recording starts 'Immediately' and 'On_Tap' action stops the recording.
        """
        RECORD_AUDIO_IMMEDIATELY_TAP_REGEX = r"^\s*(\w+)\s*=\s*Record_audio\s*\(\s*\{\s*\"Audio_Quality\":\s*\"(\w+)\",\s*\"Start_Recording\":\s*\"(Immediately)\",\s*\"Finish_Recording\":\s*\"(On_Tap)\"\s*\}\s*\)\s*$"
        match = re.match(RECORD_AUDIO_IMMEDIATELY_TAP_REGEX, line)
        if match:
            print(f"RECORD_AUDIO_IMMEDIATELY_TAP_REGEX") if verb else None
            for i, value in enumerate(match.groups(), start=1):
                print(f"\tGroup {i}: {value}") if verb else None
            audio_quality = match.group(1).lower()
            start_recording = match.group(2)
            finish_recording = match.group(3)
            var_name = match.group(1)

            indentation = INDENTATION_CHAR * INDENTATION_AMOUNT * indent_level
            code = ""
            code += f"{indentation}import sounddevice as sd\n"
            code += f"{indentation}import numpy as np\n"
            code += f"{indentation}import time\n"
            code += f"{indentation}from pynput import mouse\n"
            code += f"{indentation}fs = 44100  # Sample rate\n"
            code += f"{indentation}seconds = 10  # Duration of recording\n"
            # Initialize variable before while loop
            code += f"{indentation}{var_name} = np.array([])\n"
            code += f"{indentation}mouseClicked = False\n"
            code += f"{indentation}listener = mouse.Listener(on_click=lambda x, y, button, pressed: exec('global mouseClicked\\nmouseClicked=True' if pressed else 'global mouseClicked\\nmouseClicked=False'))\n"
            code += f"{indentation}listener.start()\n"
            code += f"{indentation}print('Recording started')\n"
            # Record while mouse is not clicked
            code += f"{indentation}while not mouseClicked:\n"
            code += f"{indentation}{INDENTATION_STRING * 1}recording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)\n"
            # Sleep for 0.1 seconds
            code += f"{indentation}{INDENTATION_STRING * 1}time.sleep(0.1)\n"
            code += f"{indentation}{INDENTATION_STRING * 1}{var_name} = np.append({var_name}, recording)\n"
            code += f"{indentation}print('Recording stopped')\n"
            code += f"{indentation}listener.stop()\n"

            return code, in_otherwise_block

        return None

    @staticmethod
    def record_audio_immediately_time_action(
        line, indent_level, in_otherwise_block, verb=False
    ):
        """
        Converts the 'Record_audio' pseudo code to Python code when recording starts 'Immediately' and 'After_Time' action stops the recording.
        """
        RECORD_AUDIO_IMMEDIATELY_TIME_REGEX = r"^\s*(\w+)\s*=\s*Record_audio\s*\(\s*\{\s*\"Audio_Quality\":\s*\"(\w+)\",\s*\"Start_Recording\":\s*\"(Immediately)\",\s*\"Finish_Recording\":\s*\"(After_Time)\",\s*\"Seconds\":\s*(\d+)\s*\}\s*\)\s*$"
        match = re.match(RECORD_AUDIO_IMMEDIATELY_TIME_REGEX, line)
        if match:
            print(f"RECORD_AUDIO_IMMEDIATELY_TIME_REGEX") if verb else None
            for i, value in enumerate(match.groups(), start=1):
                print(f"\tGroup {i}: {value}") if verb else None
            audio_quality = match.group(1).lower()
            start_recording = match.group(2)
            finish_recording = match.group(3)
            seconds = match.group(5)  # Duration of recording

            indentation = INDENTATION_CHAR * INDENTATION_AMOUNT * indent_level
            code = ""
            code += f"{indentation}import sounddevice as sd\n"
            code += f"{indentation}import numpy as np\n"
            code += f"{indentation}fs = 44100  # Sample rate\n"
            code += f"{indentation}Recorded_Audio = np.array([])\n"
            code += f"{indentation}print('Recording started')\n"
            code += f"{indentation}recording = sd.rec(int({seconds} * fs), samplerate=fs, channels=2)\n"
            code += f"{indentation}sd.wait()\n"
            code += (
                f"{indentation}Recorded_Audio = np.append(Recorded_Audio, recording)\n"
            )
            code += f"{indentation}print('Recording stopped')\n"

            return code, in_otherwise_block

        return None


#   ===============================================
#   audio_speech_actions AudioSpeechActions
#
class AudioSpeechActions:
    @staticmethod
    def dictate_text_tap_action(line, indent_level, in_otherwise_block, verb=False):
        """
        Parses and converts 'Dictate_text' with 'On_Tap' action in pseudo code to Python code.
        """
        DICTATE_TEXT_TAP_REGEX = r"^\s*(\w+)\s*=\s*Dictate_text\s*\(\s*\{\s*\"Language\":\s*\"(\w+)\",\s*\"Stop_Listening\":\s*\"(On_Tap)\"\s*\}\s*\)\s*$"
        match = re.match(DICTATE_TEXT_TAP_REGEX, line)
        if match:
            print(f"DICTATE_TEXT_TAP_REGEX") if verb else None
            for i, value in enumerate(match.groups(), start=1):
                print(f"\tGroup {i}: {value}") if verb else None
            language = match.group(2).lower()
            stop_listening = match.group(3)
            var_name = match.group(1)

            indentation = INDENTATION_CHAR * INDENTATION_AMOUNT * indent_level
            code = ""
            code += f"{indentation}import speech_recognition as sr\n"
            code += f"{indentation}import time\n"
            code += f"{indentation}from pynput import keyboard\n"
            code += f"{indentation}r = sr.Recognizer()\n"
            # Initialize variable before while loop
            code += f'{indentation}{var_name} = ""\n'
            code += f"{indentation}keyPressed = False\n"
            code += f"{indentation}listener = keyboard.Listener(on_press=lambda key: exec('global keyPressed\\nkeyPressed=True'))\n"
            code += f"{indentation}listener.start()\n"
            code += f"{indentation}with sr.Microphone() as source:\n"
            code += f"{indentation}{INDENTATION_STRING * 1}print('Listening... press any key to stop')\n"
            # Loop until key press
            code += f"{indentation}{INDENTATION_STRING * 1}while True:\n"
            code += f"{indentation}{INDENTATION_STRING * 2}audio = r.listen(source, phrase_time_limit=4)\n"
            code += f"{indentation}{INDENTATION_STRING * 2}if keyPressed:\n"
            code += (
                f"{indentation}{INDENTATION_STRING * 3}print('Key pressed, exiting')\n"
            )
            code += f"{indentation}{INDENTATION_STRING * 3}break\n"
            code += f"{indentation}{INDENTATION_STRING * 2}try:\n"
            code += f"{indentation}{INDENTATION_STRING * 3}text = r.recognize_google(audio, language='{language}')\n"
            code += (
                f"{indentation}{INDENTATION_STRING * 3}print(f'You said: {{text}}')\n"
            )
            code += f'{indentation}{INDENTATION_STRING * 3}{var_name} += " " + text\n'
            code += (
                f"{indentation}{INDENTATION_STRING * 2}except sr.UnknownValueError:\n"
            )
            code += f"{indentation}{INDENTATION_STRING * 3}print('Sorry, I did not understand that.')\n"
            code += (
                f"{indentation}{INDENTATION_STRING * 2}except sr.RequestError as e:\n"
            )
            code += f"{indentation}{INDENTATION_STRING * 3}print(f'Could not request results from Google Speech Recognition service: {{e}}')\n"
            code += f"{indentation}print('Your recorded query:', {var_name})\n"
            code += f"{indentation}listener.stop()\n"
            return code, in_otherwise_block
        return None

    @staticmethod
    def dictate_text_short_action(line, indent_level, in_otherwise_block, verb=False):
        """
        Parses and converts 'Dictate_text' with 'After_Short_Pause' action in pseudo code to Python code.
        """
        DICTATE_TEXT_SHORT_REGEX = r"^\s*(\w+)\s*=\s*Dictate_text\s*\(\s*\{\s*\"Language\":\s*\"(\w+)\",\s*\"Stop_Listening\":\s*\"(After_Short_Pause)\"\s*\}\s*\)\s*$"
        match = re.match(DICTATE_TEXT_SHORT_REGEX, line)
        if match:
            print(f"DICTATE_TEXT_SHORT_REGEX") if verb else None
            for i, value in enumerate(match.groups(), start=1):
                print(f"\tGroup {i}: {value}") if verb else None
            language = match.group(2).lower()
            stop_listening = match.group(3)
            var_name = match.group(1)

            indentation = INDENTATION_CHAR * INDENTATION_AMOUNT * indent_level
            code = ""
            code += f"{indentation}import speech_recognition as sr\n"
            code += f"{indentation}r = sr.Recognizer()\n"
            code += f"{indentation}with sr.Microphone() as source:\n"
            # Initialize variable before while loop
            code += f"{indentation}{INDENTATION_STRING * 1}{var_name} = None\n"
            code += f"{indentation}{INDENTATION_STRING * 1}print('Listening...')\n"
            if stop_listening == "After_Short_Pause":
                code += (
                    f"{indentation}{INDENTATION_STRING * 1}audio = r.listen(source)\n"
                )
                code += f"{indentation}{INDENTATION_STRING * 1}try:\n"
                code += f"{indentation}{INDENTATION_STRING * 2}text = r.recognize_google(audio, language='{language}')\n"
                code += f"{indentation}{INDENTATION_STRING * 2}print(f'You said: {{text}}')\n"
                code += f"{indentation}{INDENTATION_STRING * 2}{var_name} = text\n"
                code += f"{indentation}{INDENTATION_STRING * 1}except sr.UnknownValueError:\n"
                code += f"{indentation}{INDENTATION_STRING * 2}print('Sorry, I did not understand that.')\n"
                code += f"{indentation}{INDENTATION_STRING * 2}{var_name} = None\n"
                code += f"{indentation}{INDENTATION_STRING * 1}except sr.RequestError as e:\n"
                code += f"{indentation}{INDENTATION_STRING * 2}print(f'Could not request results from Google Speech Recognition service: {{e}}')\n"
                code += f"{indentation}{INDENTATION_STRING * 2}{var_name} = None\n"
            return code, in_otherwise_block
        return None

    @staticmethod
    def dictate_text_long_action(line, indent_level, in_otherwise_block, verb=False):
        """
        Parses and converts 'Dictate_text' with 'After_Pause' action in pseudo code to Python code.
        """
        DICTATE_TEXT_LONG_REGEX = r"^\s*(\w+)\s*=\s*Dictate_text\s*\(\s*\{\s*\"Language\":\s*\"(\w+)\",\s*\"Stop_Listening\":\s*\"(After_Pause)(?:\",\s*\"Pause\":\s*(\d+))?\s*\}\s*\)\s*$"
        match = re.match(DICTATE_TEXT_LONG_REGEX, line)
        if match:
            print(f"DICTATE_TEXT_LONG_REGEX") if verb else None
            for i, value in enumerate(match.groups(), start=1):
                print(f"\tGroup {i}: {value}") if verb else None
            language = match.group(2).lower()
            stop_listening = match.group(3)
            pause_duration = match.group(4)
            var_name = match.group(1)

            indentation = INDENTATION_CHAR * INDENTATION_AMOUNT * indent_level
            code = ""
            code += f"{indentation}import speech_recognition as sr\n"
            code += f"{indentation}r = sr.Recognizer()\n"
            code += f"{indentation}with sr.Microphone() as source:\n"
            # Initialize variable before while loop
            code += f"{indentation}{INDENTATION_STRING * 1}{var_name} = None\n"
            code += f"{indentation}{INDENTATION_STRING * 1}print('Listening...')\n"
            if stop_listening == "After_Pause":
                # If no pause duration specified, default to 5 seconds
                pause_duration = pause_duration if pause_duration else 5
                code += f"{indentation}{INDENTATION_STRING * 1}audio = r.record(source, duration={pause_duration})\n"
                code += f"{indentation}{INDENTATION_STRING * 1}try:\n"
                code += f"{indentation}{INDENTATION_STRING * 2}text = r.recognize_google(audio, language='{language}')\n"
                code += f"{indentation}{INDENTATION_STRING * 2}print(f'You said: {{text}}')\n"
                code += f"{indentation}{INDENTATION_STRING * 2}{var_name} = text\n"
                code += f"{indentation}{INDENTATION_STRING * 1}except sr.UnknownValueError:\n"
                code += f"{indentation}{INDENTATION_STRING * 2}print('Sorry, I did not understand that.')\n"
                code += f"{indentation}{INDENTATION_STRING * 2}{var_name} = None\n"
                code += f"{indentation}{INDENTATION_STRING * 1}except sr.RequestError as e:\n"
                code += f"{indentation}{INDENTATION_STRING * 2}print(f'Could not request results from Google Speech Recognition service: {{e}}')\n"
                code += f"{indentation}{INDENTATION_STRING * 2}{var_name} = None\n"
            return code, in_otherwise_block
        return None

    @staticmethod
    def speak_action(line, indent_level, in_otherwise_block, verb=False):
        """
        Parses and converts 'Speak' action in pseudo code to Python code.
        """
        SPEAK_REGEX = r'^\s*Speak ("[^"]+"|[^\s]+)(?: \(\{(?:\s*"Wait"\s*:\s*(True|False))?(?:,\s*"Rate"\s*:\s*(\d+(?:\.\d+)?|\w+))?(?:,\s*"Pitch"\s*:\s*(\d+(?:\.\d+)?|\w+))?(?:,\s*"Language"\s*:\s*"(\w+)")?\s*\}\))?\s*$'
        match = re.match(SPEAK_REGEX, line)
        if match:
            print(f"SPEAK_REGEX") if verb else None
            for i, value in enumerate(match.groups(), start=1):
                print(f"\tGroup {i}: {value}") if verb else None
            text = match.group(1)
            wait = match.group(2)  # Wait group
            # rate = float(match.group(3)) if match.group(3) else 1.0  # Rate group
            try:
                rate = float(match.group(3))
            except ValueError:
                rate = match.group(3)  # If not, it's a variable name
            rate = rate if rate else 1.0
            # pitch = float(match.group(4)) if match.group(4) else 1.0  # Pitch group
            try:
                pitch = float(match.group(4))
            except ValueError:
                pitch = match.group(4)  # If not, it's a variable name
            pitch = pitch if pitch else 1.0
            language = (
                match.group(5).lower() if match.group(5) else "english"
            )  # Language group

            indentation = INDENTATION_CHAR * INDENTATION_AMOUNT * indent_level
            code = f"{indentation}import pyttsx3\n"
            code += f"{indentation}engine = pyttsx3.init()\n"
            code += f"{indentation}voices = engine.getProperty('voices')\n"
            code += f"{indentation}voice_id = voices[0].id\n"
            code += f"{indentation}for voice in voices:\n"
            code += (
                f"{indentation}{INDENTATION_STRING * 1}for lang in voice.languages:\n"
            )
            code += f"{indentation}{INDENTATION_STRING * 2}if '{language}' in lang.decode().lower():  # Compare language settings\n"
            code += f"{indentation}{INDENTATION_STRING * 3}voice_id = voice.id\n"
            code += f"{indentation}{INDENTATION_STRING * 3}break\n"
            code += f"{indentation}engine.setProperty('voice', voice_id)\n"
            code += f"{indentation}engine.setProperty('rate', {rate} * 100)  # 1 should be average speed\n"
            code += f"{indentation}engine.setProperty('pitch', {pitch})  # 1 should be average pitch\n"
            code += f"{indentation}engine.say({text})\n"
            # Control execution based on "Wait"
            code += f"{indentation}if {wait}:\n"
            code += f"{indentation}{INDENTATION_STRING * 1}engine.runAndWait()\n"

            return code, in_otherwise_block
        return None

    @staticmethod
    def play_sound_action(line, indent_level, in_otherwise_block, verb=False):
        PLAY_SOUND_REGEX = (
            r"^\s*Play_sound \(\{\"Sound_File\": (\"[\w\s]+\"|\w+)\}\)\s*$")
        match = re.match(PLAY_SOUND_REGEX, line)
        if match:
            print(f"PLAY_SOUND_REGEX") if verb else None
            for i, value in enumerate(match.groups(), start=1):
                print(f"\tGroup {i}: {value}") if verb else None
            sound_file_match = match.group(1)
            is_filename = sound_file_match.startswith(
                '"'
            ) and sound_file_match.endswith('"')
            sound_file = (
                sound_file_match.strip(
                    '"') if is_filename else sound_file_match
            )

            indentation = INDENTATION_CHAR * INDENTATION_AMOUNT * indent_level
            code = f"{indentation}import pygame\n"
            code += f"{indentation}import os\n"
            code += f"{indentation}import tempfile\n"
            code += f"{indentation}pygame.init()\n"
            if is_filename:
                code += f"{indentation}sound_file_path = os.path.join('Files', \"{sound_file}\")\n"
            else:
                code += f"{indentation}sound_file_path = os.path.join('Files', {sound_file})\n"
            code += f"{indentation}if os.path.isfile(sound_file_path):\n"
            code += f"{indentation}{INDENTATION_STRING * 1}sound_path = sound_file_path\n"
            code += f"{indentation}else:\n"
            code += f"{indentation}{INDENTATION_STRING * 1}with tempfile.NamedTemporaryFile(delete=False) as temp_file:\n"
            if is_filename:
                code += (
                    f'{indentation}{INDENTATION_STRING * 2}temp_file.write("{sound_file}".encode())\n'
                )
            else:
                code += f"{indentation}{INDENTATION_STRING * 2}temp_file.write({sound_file}.encode())\n"
            code += f"{indentation}{INDENTATION_STRING * 2}sound_path = temp_file.name\n"
            code += f"{indentation}pygame.mixer.music.load(sound_path)\n"
            code += f"{indentation}pygame.mixer.music.play()\n"
            code += f"{indentation}while pygame.mixer.music.get_busy():\n"
            code += f"{indentation}{INDENTATION_STRING * 1}continue\n"
            code += f"{indentation}pygame.quit()\n"
            code += f"{indentation}if sound_file_path != sound_path:\n"
            code += f"{indentation}{INDENTATION_STRING * 1}os.remove(sound_path)\n"

            return code, in_otherwise_block
        return None


#   ===============================================
#   variable_dictionary_actions VariableDictionaryActions
#
class VariableDictionaryActions:
    @staticmethod
    def get_text_action(line, indent_level, in_otherwise_block, verb=False):
        """
        Converts 'Get_text_from' pseudo code to Python code.
        """
        GET_TEXT_REGEX = r"^\s*(\w+)\s*=\s*Get_text_from (\w+)\s*$"
        match = re.match(GET_TEXT_REGEX, line)
        if match:
            print(f"GET_TEXT_REGEX") if verb else None
            for i, value in enumerate(match.groups(), start=1):
                print(f"\tGroup {i}: {value}") if verb else None
            indentation = INDENTATION_CHAR * INDENTATION_AMOUNT * indent_level
            variable_name = match.group(1)  # Text
            target = match.group(2)  # Dictionary_Value
            parsed_line = f"{variable_name} = str({target})"
            return f"{indentation}{parsed_line}", in_otherwise_block
        return None

    @staticmethod
    def ask_for_text_action(line, indent_level, in_otherwise_block, verb=False):
        ASK_FOR_TEXT_REGEX = r'^\s*(?:(\w+)\s*=\s*)?Ask_for_Text\s*with\s*"([^"]*)"\s*\(\{"Default":\s*(".*?"|\w*)\}\)\s*$'
        match = re.match(ASK_FOR_TEXT_REGEX, line)
        if match:
            print(f"ASK_FOR_TEXT_REGEX") if verb else None
            for i, value in enumerate(match.groups(), start=1):
                print(f"\tGroup {i}: {value}") if verb else None
            indentation = INDENTATION_CHAR * INDENTATION_AMOUNT * indent_level
            var_name = match.group(1) or "text_input"
            prompt = match.group(2)
            default = match.group(3)

            code = f"\n{indentation}try:\n"
            if default == '""':
                code += f"{indentation}{INDENTATION_STRING * 1}{var_name} = input('{prompt} (Default: ): ')\n"
            else:
                code += f"{indentation}{INDENTATION_STRING * 1}if isinstance({default}, str) and {default}.startswith('\"') and {default}.endswith('\"'):\n"
                code += f"{indentation}{INDENTATION_STRING * 2}{default} = {default}[1:-1]\n"
                code += f"{indentation}{INDENTATION_STRING * 1}{var_name} = input('{prompt} (Default: ' + str({default}) + '): ')\n"

            code += f"{indentation}{INDENTATION_STRING * 1}if {var_name} == '':\n"
            code += f"{indentation}{INDENTATION_STRING * 2}{var_name} = {default}\n"
            code += f"{indentation}except Exception:\n"
            code += f"{indentation}{INDENTATION_STRING * 1}{var_name} = {default}\n"

            return code, in_otherwise_block

        return None

    @staticmethod
    def ask_for_number_action(line, indent_level, in_otherwise_block, verb=False):
        ASK_FOR_NUMBER_REGEX = r'^\s*(?:(\w+)\s*=\s*)?Ask_for_Number\s*with\s*"([^"]*)"\s*\(\{"Default":\s*(".*?"|\w*)\}\)\s*$'
        match = re.match(ASK_FOR_NUMBER_REGEX, line)
        if match:
            print(f"ASK_FOR_NUMBER_REGEX") if verb else None
            for i, value in enumerate(match.groups(), start=1):
                print(f"\tGroup {i}: {value}") if verb else None
            indentation = INDENTATION_CHAR * INDENTATION_AMOUNT * indent_level
            var_name = match.group(1) or "number_input"
            prompt = match.group(2)
            default = match.group(3)

            code = f"\n{indentation}try:\n"
            if default == '""':
                code += f"{indentation}{INDENTATION_STRING * 1}{var_name} = input('{prompt} (Default: ): ')\n"
            else:
                code += f"{indentation}{INDENTATION_STRING * 1}if isinstance({default}, str) and {default}.startswith('\"') and {default}.endswith('\"'):\n"
                code += f"{indentation}{INDENTATION_STRING * 2}{default} = {default}[1:-1]\n"
                code += f"{indentation}{INDENTATION_STRING * 1}{var_name} = input('{prompt} (Default: ' + str({default}) + '): ')\n"

            code += f"{indentation}{INDENTATION_STRING * 1}if {var_name} == '':\n"
            code += f"{indentation}{INDENTATION_STRING * 2}{var_name} = {default}\n"
            code += f"{indentation}{INDENTATION_STRING * 1}else:\n"
            code += (
                f"{indentation}{INDENTATION_STRING * 2}{var_name} = float({var_name})\n"
            )
            code += f"{indentation}except Exception:\n"
            code += f"{indentation}{INDENTATION_STRING * 1}{var_name} = {default}\n"

            return code, in_otherwise_block

        return None

    @staticmethod
    def multi_line_dict_start_action(line, indent_level, in_otherwise_block, verb=False):
        """
        Converts the start of 'Dictionary' pseudo code to Python code when the dictionary is defined over multiple lines.
        """
        MULTI_LINE_DICT_START_REGEX = (
            r"^\s*Dictionary\s*=\s*Dictionary\s*\{(?!.*\})\s*$")
        match = re.match(MULTI_LINE_DICT_START_REGEX, line)
        if match:
            print(f"MULTI_LINE_DICT_START_REGEX") if verb else None
            for i, value in enumerate(match.groups(), start=1):
                print(f"\tGroup {i}: {value}") if verb else None
            indentation = INDENTATION_CHAR * INDENTATION_AMOUNT * indent_level
            return indentation + "Dictionary = {", in_otherwise_block
        return None

    @staticmethod
    def single_line_dict_assignment_action(line, indent_level, in_otherwise_block, verb=False):
        """
        Converts 'Dictionary' pseudo code to Python code when the dictionary is defined in a single line.
        """
        SINGLE_LINE_DICT_ASSIGNMENT_REGEX = (
            r"^\s*(Dictionary\s*=\s*)(Dictionary\s*)(\{.*\})\s*$")
        match = re.match(SINGLE_LINE_DICT_ASSIGNMENT_REGEX, line)
        if match:
            print(f"SINGLE_LINE_DICT_ASSIGNMENT_REGEX") if verb else None
            for i, value in enumerate(match.groups(), start=1):
                print(f"\tGroup {i}: {value}") if verb else None
            indentation = INDENTATION_CHAR * INDENTATION_AMOUNT * indent_level
            parsed_line = re.sub(
                SINGLE_LINE_DICT_ASSIGNMENT_REGEX, r"Dictionary = \3", line
            )
            # Add quotes around keys of the dictionary only if they're not already quoted
            parsed_line = re.sub(
                r'({\s*|\s*,\s*)(\b[^":]+\b)(\s*:)', r'\1"\2"\3', parsed_line
            )
            return indentation + parsed_line, in_otherwise_block
        return None

    @staticmethod
    def get_dict_from_text_action(line, indent_level, in_otherwise_block, verb=False):
        """
        Converts 'Get_dictionary_from' pseudo code to Python code.
        """
        GET_DICT_FROM_TEXT_REGEX = r"^\s*(Dictionary)\s*=\s*Get_dictionary_from (\w+)"
        match = re.match(GET_DICT_FROM_TEXT_REGEX, line)
        if match:
            print(f"GET_DICT_FROM_TEXT_REGEX") if verb else None
            for i, value in enumerate(match.groups(), start=1):
                print(f"\tGroup {i}: {value}") if verb else None
            indentation = INDENTATION_CHAR * INDENTATION_AMOUNT * indent_level
            variable_name = match.group(1)
            text_variable = match.group(2)
            parsed_line = f"{indentation}{variable_name} = json.loads({text_variable})"
            return f"{indentation}import json\n{parsed_line}", in_otherwise_block
        return None

    @staticmethod
    def json_assignment_action(line, indent_level, in_otherwise_block, verb=False):
        """
        Converts JSON assignment pseudo code to Python code.
        """
        JSON_ASSIGNMENT_REGEX = r"^\s*(\w+)\s*=\s*\{(.*)\}"
        match = re.match(JSON_ASSIGNMENT_REGEX, line)
        if match:
            print(f"JSON_ASSIGNMENT_REGEX") if verb else None
            for i, value in enumerate(match.groups(), start=1):
                print(f"\tGroup {i}: {value}") if verb else None
            indentation = INDENTATION_CHAR * INDENTATION_AMOUNT * indent_level
            return (
                indentation + re.sub(JSON_ASSIGNMENT_REGEX,
                                     r"\1 = {\2}", line),
                in_otherwise_block,
            )
        return None

    @staticmethod
    def dict_value_for_key_action(line, indent_level, in_otherwise_block, verb=False):
        """
        Converts 'Get_Dict_Value_for' pseudo code to Python code.
        """
        DICT_VALUE_FOR_KEY_REGEX = (
            r"^\s*(\w+)\s*= Get_Dict_Value_for ([\w\.]+) in (\w+)")
        match = re.match(DICT_VALUE_FOR_KEY_REGEX, line)
        if match:
            print(f"DICT_VALUE_FOR_KEY_REGEX") if verb else None
            for i, value in enumerate(match.groups(), start=1):
                print(f"\tGroup {i}: {value}") if verb else None
            indentation = INDENTATION_CHAR * INDENTATION_AMOUNT * indent_level
            variable_name = match.group(1)
            keys = match.group(2).split(".")
            dict_name = match.group(3)
            keys_access = ""
            for key in keys:
                if key.isdigit():
                    # Subtract 1 because Python list indexes start at 0
                    keys_access += f"[{int(key) - 1}]"
                else:
                    keys_access += f"['{key}']"
            if dict_name == "Contents_of_URL":
                dict_name += ".json()"
            return (
                f"{indentation}{variable_name} = {dict_name}{keys_access}",
                in_otherwise_block,
            )
        return None


#   ===============================================
#   variable_list_actions VariableListActions
#
class VariableListActions:
    @staticmethod
    def add_to_list_action(line, indent_level, in_otherwise_block, verb=False):
        """
        Converts 'Add to list' pseudo code to Python code.
        """
        ADD_TO_LIST_REGEX = r'^\s*Add\s+(?:"([^"]*)"|([^\"]+))\s+to\s+(\w+)\s*$'
        match = re.match(ADD_TO_LIST_REGEX, line)
        if match:
            print(f"ADD_TO_LIST_REGEX") if verb else None
            for i, value in enumerate(match.groups(), start=1):
                print(f"\tGroup {i}: {value}") if verb else None
            indentation = INDENTATION_CHAR * INDENTATION_AMOUNT * indent_level
            line = re.sub(
                ADD_TO_LIST_REGEX,
                lambda match: (
                    f'{indentation}{match.group(3)}.append("{match.group(1)}")'
                    if match.group(1)
                    else f"{indentation}{match.group(3)}.append({match.group(2).strip()})"
                ),
                line,
            )
            in_otherwise_block = True  # Assuming this to be the switch
            return line, in_otherwise_block
        return None

    @staticmethod
    def combine_list_custom_action(line, indent_level, in_otherwise_block, verb=False):
        """
        Converts 'Combine with Custom' pseudo code to Python code.
        """
        COMBINE_LIST_CUSTOM_REGEX = (
            r"^\s*(\w+)\s*=\s*Combine (\w+) with Custom\s*\"(.*?)\"")
        match = re.match(COMBINE_LIST_CUSTOM_REGEX, line)
        if match:
            print(f"COMBINE_LIST_CUSTOM_REGEX") if verb else None
            for i, value in enumerate(match.groups(), start=1):
                print(f"\tGroup {i}: {value}") if verb else None
            indentation = INDENTATION_CHAR * INDENTATION_AMOUNT * indent_level
            variable_name, list_name, delimiter = match.groups()  # re-use the match object
            code = f"{indentation}if len({list_name}) > 0 and isinstance({list_name}[0], dict):\n"
            code += f"{indentation}{INDENTATION_STRING}import json\n"
            code += f"{indentation}{INDENTATION_STRING}{variable_name} = '{delimiter}'.join(json.dumps(item) for item in {list_name})\n"
            code += f"{indentation}else:\n"
            code += f"{indentation}{INDENTATION_STRING}{variable_name} = '{delimiter}'.join({list_name})\n"
            return code, in_otherwise_block
        return None

    @staticmethod
    def combine_list_nl_action(line, indent_level, in_otherwise_block, verb=False):
        """
        Converts 'Combine with New_Lines' pseudo code to Python code.
        """
        COMBINE_LIST_NL_REGEX = r"^\s*(\w+)\s*=\s*Combine (\w+) with New_Lines\s*$"
        match = re.match(COMBINE_LIST_NL_REGEX, line)
        if match:
            print(f"COMBINE_LIST_NL_REGEX") if verb else None
            for i, value in enumerate(match.groups(), start=1):
                print(f"\tGroup {i}: {value}") if verb else None
            indentation = INDENTATION_CHAR * INDENTATION_AMOUNT * indent_level
            variable_name, list_name = re.match(
                COMBINE_LIST_NL_REGEX, line).groups()
            return (
                f"{indentation}{variable_name} = '\\n'.join({list_name})",
                in_otherwise_block,
            )
        return None

    @staticmethod
    def list_assignment_action(line, indent_level, in_otherwise_block, verb=False):
        """
        Converts 'List' pseudo code to Python code.
        """
        LIST_ASSIGNMENT_REGEX = r"^\s*(List\s*=\s*)(List\s*)(\[.*?\])"
        match = re.match(LIST_ASSIGNMENT_REGEX, line)
        if match:
            print(f"LIST_ASSIGNMENT_REGEX") if verb else None
            for i, value in enumerate(match.groups(), start=1):
                print(f"\tGroup {i}: {value}") if verb else None
            indentation = INDENTATION_CHAR * INDENTATION_AMOUNT * indent_level
            return (
                indentation + re.sub(LIST_ASSIGNMENT_REGEX,
                                     r"List = \3", line),
                in_otherwise_block,
            )
        return None

    @staticmethod
    def choose_from_list_action(line, indent_level, in_otherwise_block, verb=False):
        """
        Converts 'Choose_from' pseudo code to Python code.
        """
        CHOOSE_FROM_LIST_REGEX = r"^\s*(\w+)\s*=\s*Choose_from\s+(\w+)"
        match = re.match(CHOOSE_FROM_LIST_REGEX, line)
        if match:
            print(f"CHOOSE_FROM_LIST_REGEX") if verb else None
            for i, value in enumerate(match.groups(), start=1):
                print(f"\tGroup {i}: {value}") if verb else None
            indentation = INDENTATION_CHAR * INDENTATION_AMOUNT * indent_level
            variable_name = match.group(1)
            placeholder = match.group(2)
            return (
                f"{indentation}{variable_name} = input('Choose from ' + str({placeholder}) + ':  ')",
                in_otherwise_block,
            )
        return None

    @staticmethod
    def split_text_action(line, indent_level, in_otherwise_block, verb=False):
        """
        Converts 'Split by' pseudo code to Python code.
        """
        SPLIT_TEXT_REGEX = r"^\s*(\w+\s*=\s*)Split\s+(\w+)\s+by\s+(\w+)"
        match = re.match(SPLIT_TEXT_REGEX, line)
        if match:
            print(f"SPLIT_TEXT_REGEX") if verb else None
            for i, value in enumerate(match.groups(), start=1):
                print(f"\tGroup {i}: {value}") if verb else None
            indentation = INDENTATION_CHAR * INDENTATION_AMOUNT * indent_level
            variable_name = match.group(1)  # Split_text
            split_target = match.group(2)  # Notes
            delimiter = match.group(3)  # New_Lines
            if delimiter == "New_Lines":
                delimiter = "\\n"
            parsed_line = f'{variable_name}{split_target}.split("{delimiter}")'
            return f"{indentation}{parsed_line}", in_otherwise_block
        return None

    @staticmethod
    def item_from_list_action(line, indent_level, in_otherwise_block, verb=False):
        """
        Converts 'Get Items_in_Range from' pseudo code to Python code.
        """
        ITEM_FROM_LIST_REGEX = (
            r"^\s*(\w+)\s*=\s*Get Items_in_Range (\d+)(?:\s*to\s*(\d+)?\s*)?from (\w+)")
        match = re.match(ITEM_FROM_LIST_REGEX, line)
        if match:
            print(f"ITEM_FROM_LIST_REGEX") if verb else None
            for i, value in enumerate(match.groups(), start=1):
                print(f"\tGroup {i}: {value}") if verb else None
            indentation = INDENTATION_CHAR * INDENTATION_AMOUNT * indent_level
            range_start = match.group(2)
            range_end = (
                match.group(3)
                if match.group(3) and match.group(3).strip() != ""
                else None
            )
            if (
                range_start is not None
                and range_end is not None
                and range_start == range_end
            ):
                new_line = f"{match.group(1)} = {match.group(4)}[{range_start}]"
            elif range_end:
                new_line = (
                    f"{match.group(1)} = {match.group(4)}[{range_start}:{range_end}]"
                )
            else:
                new_line = f"{match.group(1)} = {match.group(4)}[{range_start}:]"
            return indentation + new_line, in_otherwise_block
        return None

    @staticmethod
    def item_first_from_list_action(line, indent_level, in_otherwise_block, verb=False):
        """
        Converts 'Get First_Item from' pseudo code to Python code.
        """
        ITEM_FIRST_FROM_LIST_REGEX = r"^\s*(\w+)\s*=\s*Get First_Item from\s(\w+)"
        match = re.match(ITEM_FIRST_FROM_LIST_REGEX, line)
        if match:
            print(f"ITEM_FIRST_FROM_LIST_REGEX") if verb else None
            for i, value in enumerate(match.groups(), start=1):
                print(f"\tGroup {i}: {value}") if verb else None
            indentation = INDENTATION_CHAR * INDENTATION_AMOUNT * indent_level
            new_line = f"{match.group(1)} = {match.group(2)}[0]"
            return indentation + new_line, in_otherwise_block
        return None

    @staticmethod
    def item_last_from_list_action(line, indent_level, in_otherwise_block, verb=False):
        """
        Converts 'Get Last_Item from' pseudo code to Python code.
        """
        ITEM_LAST_FROM_LIST_REGEX = r"^\s*(\w+)\s*=\s*Get Last_Item from\s(\w+)"
        match = re.match(ITEM_LAST_FROM_LIST_REGEX, line)
        if match:
            print(f"ITEM_LAST_FROM_LIST_REGEX") if verb else None
            for i, value in enumerate(match.groups(), start=1):
                print(f"\tGroup {i}: {value}") if verb else None
            indentation = INDENTATION_CHAR * INDENTATION_AMOUNT * indent_level
            new_line = f"{match.group(1)} = {match.group(2)}[-1]"
            return indentation + new_line, in_otherwise_block
        return None

    @staticmethod
    def item_index_from_list_action(line, indent_level, in_otherwise_block, verb=False):
        """
        Converts 'Get Item_at_Index from' pseudo code to Python code.
        """
        ITEM_INDEX_FROM_LIST_REGEX = (
            r"^\s*(\w+)\s*=\s*Get Item_at_Index\s(\d+)\sfrom\s(\w+)")
        match = re.match(ITEM_INDEX_FROM_LIST_REGEX, line)
        if match:
            print(f"ITEM_INDEX_FROM_LIST_REGEX") if verb else None
            for i, value in enumerate(match.groups(), start=1):
                print(f"\tGroup {i}: {value}") if verb else None
            indentation = INDENTATION_CHAR * INDENTATION_AMOUNT * indent_level
            new_line = f"{match.group(1)} = {match.group(3)}[{int(match.group(2))-1}]"
            return indentation + new_line, in_otherwise_block
        return None


#   ===============================================
#   control_flow_actions    ControlFlowActions
#
class ControlFlowActions:
    @staticmethod
    def condition_less_than_action(line, indent_level, in_otherwise_block, verb=False):
        """
        Converts 'If <variable> is_less_than <value>' pseudo code to Python code for a less than condition.
        """
        CONDITION_LESS_THAN_REGEX = r"^\s*(If\s*)(\w+)( is_less_than )(\w+)(.*)"
        match = re.match(CONDITION_LESS_THAN_REGEX, line)
        if match:
            print(f"CONDITION_LESS_THAN_REGEX") if verb else None
            for i, value in enumerate(match.groups(), start=1):
                print(f"\tGroup {i}: {value}") if verb else None
            indentation = INDENTATION_CHAR * INDENTATION_AMOUNT * indent_level
            return (
                indentation + re.sub(CONDITION_LESS_THAN_REGEX,
                                     r"if \2 < \4:", line),
                in_otherwise_block,
            )
        return None

    @staticmethod
    def condition_greater_than_action(
        line, indent_level, in_otherwise_block, verb=False
    ):
        """
        Converts 'If <variable> is_greater_than <value>' pseudo code to Python code for a greater than condition.
        """
        CONDITION_GREATER_THAN_REGEX = r"^\s*(If\s*)(\w+)( is_greater_than )(\w+)(.*)"
        match = re.match(CONDITION_GREATER_THAN_REGEX, line)
        if match:
            print(f"CONDITION_GREATER_THAN_REGEX") if verb else None
            for i, value in enumerate(match.groups(), start=1):
                print(f"\tGroup {i}: {value}") if verb else None
            indentation = INDENTATION_CHAR * INDENTATION_AMOUNT * indent_level
            return (
                indentation
                + re.sub(CONDITION_GREATER_THAN_REGEX, r"if \2 > \4:", line),
                in_otherwise_block,
            )
        return None

    @staticmethod
    def condition_not_has_value_action(
        line, indent_level, in_otherwise_block, verb=False
    ):
        """
        Converts 'If <variable> does_not_have_any_value' pseudo code to Python code for a not has value condition.
        """
        CONDITION_NOT_HAS_VALUE_REGEX = r"^\s*(If\s*)(\w+)( does_not_have_any_value)"
        match = re.match(CONDITION_NOT_HAS_VALUE_REGEX, line)
        if match:
            print(f"CONDITION_NOT_HAS_VALUE_REGEX") if verb else None
            for i, value in enumerate(match.groups(), start=1):
                print(f"\tGroup {i}: {value}") if verb else None
            indentation = INDENTATION_CHAR * INDENTATION_AMOUNT * indent_level
            return (
                indentation
                + re.sub(CONDITION_NOT_HAS_VALUE_REGEX, r"if not \2:", line),
                in_otherwise_block,
            )
        return None

    @staticmethod
    def condition_has_value_action(line, indent_level, in_otherwise_block, verb=False):
        """
        Converts 'If <variable> has_any_value' pseudo code to Python code for a has value condition.
        """
        CONDITION_HAS_VALUE_REGEX = r"^\s*(If\s*)(\w+)( has_any_value)"
        match = re.match(CONDITION_HAS_VALUE_REGEX, line)
        if match:
            print(f"CONDITION_HAS_VALUE_REGEX") if verb else None
            for i, value in enumerate(match.groups(), start=1):
                print(f"\tGroup {i}: {value}") if verb else None
            indentation = INDENTATION_CHAR * INDENTATION_AMOUNT * indent_level
            return (
                indentation +
                re.sub(CONDITION_HAS_VALUE_REGEX, r"if \2:", line),
                in_otherwise_block,
            )
        return None

    @staticmethod
    def condition_not_equals_action(line, indent_level, in_otherwise_block, verb=False):
        """
        Converts 'If <variable> is_not <value>' pseudo code to Python code for a not equals condition.
        """
        CONDITION_NOT_EQUALS_REGEX = r"^\s*(If\s*)(\w+)(\s*is_not\s*)(.*)"
        match = re.match(CONDITION_NOT_EQUALS_REGEX, line)
        if match:
            print(f"CONDITION_NOT_EQUALS_REGEX") if verb else None
            for i, value in enumerate(match.groups(), start=1):
                print(f"\tGroup {i}: {value}") if verb else None
            indentation = INDENTATION_CHAR * INDENTATION_AMOUNT * indent_level
            return (
                indentation +
                re.sub(CONDITION_NOT_EQUALS_REGEX, r"if \2 != \4:", line),
                in_otherwise_block,
            )
        return None

    @staticmethod
    def condition_action(line, indent_level, in_otherwise_block, verb=False):
        """
        Converts 'If <variable> is <value>' pseudo code to Python code for an equals condition.
        """
        CONDITION_REGEX = r"^\s*(If\s*)(\w+)(\s*is\s*)(.*)"
        match = re.match(CONDITION_REGEX, line)
        if match:
            print(f"CONDITION_REGEX") if verb else None
            for i, value in enumerate(match.groups(), start=1):
                print(f"\tGroup {i}: {value}") if verb else None
            indentation = INDENTATION_CHAR * INDENTATION_AMOUNT * indent_level
            return (
                indentation + re.sub(CONDITION_REGEX, r"if \2 == \4:", line),
                in_otherwise_block,
            )
        return None

    @staticmethod
    def otherwise_action(line, indent_level, in_otherwise_block, verb=False):
        """
        Converts 'Otherwise' pseudo code to Python code for the else statement.
        """
        OTHERWISE_REGEX = r"^\s*Otherwise\s*$"
        match = re.match(OTHERWISE_REGEX, line)
        if match:
            print(f"OTHERWISE_REGEX") if verb else None
            for i, value in enumerate(match.groups(), start=1):
                print(f"\tGroup {i}: {value}") if verb else None
            indentation = INDENTATION_CHAR * INDENTATION_AMOUNT * indent_level
            return indentation + "else:", True
        return None

    @staticmethod
    def end_if_action(line, indent_level, in_otherwise_block, verb=False):
        """
        Converts 'End_If' pseudo code to Python code for the end of an if statement.
        """
        END_IF_REGEX = r"^\s*End_If\s*$"
        match = re.match(END_IF_REGEX, line)
        if match:
            print(f"END_IF_REGEX") if verb else None
            for i, value in enumerate(match.groups(), start=1):
                print(f"\tGroup {i}: {value}") if verb else None
            indentation = INDENTATION_CHAR * INDENTATION_AMOUNT * indent_level
            return indentation, in_otherwise_block
        return None

    @staticmethod
    def repeat_action(line, indent_level, in_otherwise_block, verb=False):
        """
        Converts 'Repeat_with_each <item> in <list>' pseudo code to Python code for a loop.
        """
        REPEAT_REGEX = r"^\s*Repeat_with_each (\w+)\s+in\s+(\w+)"
        match = re.match(REPEAT_REGEX, line)
        if match:
            print(f"REPEAT_REGEX") if verb else None
            for i, value in enumerate(match.groups(), start=1):
                print(f"\tGroup {i}: {value}") if verb else None
            indentation = INDENTATION_CHAR * INDENTATION_AMOUNT * indent_level
            return (
                indentation + re.sub(REPEAT_REGEX, r"for \1 in \2:", line),
                in_otherwise_block,
            )
        return None

    @staticmethod
    def end_repeat_action(line, indent_level, in_otherwise_block, verb=False):
        """
        Converts 'End_Repeat' pseudo code to Python code for the end of a loop.
        """
        END_REPEAT_REGEX = r"^\s*End_Repeat"
        match = re.match(END_REPEAT_REGEX, line)
        if match:
            print(f"END_REPEAT_REGEX") if verb else None
            for i, value in enumerate(match.groups(), start=1):
                print(f"\tGroup {i}: {value}") if verb else None
            indentation = INDENTATION_CHAR * INDENTATION_AMOUNT * indent_level
            return indentation + line, in_otherwise_block
        return None


#   ===============================================
#   date_time_actions   DateTimeActions
#
class DateTimeActions:
    @staticmethod
    def current_date_action(line, indent_level, in_otherwise_block, verb=False):
        """
        Converts 'Current_Date' pseudo code to Python code.
        """
        CURRENT_DATE_REGEX = r"^\s*(\w+)\s*=\s*Current_Date"
        match = re.match(CURRENT_DATE_REGEX, line)
        if match:
            print(f"CURRENT_DATE_REGEX") if verb else None
            for i, value in enumerate(match.groups(), start=1):
                print(f"\tGroup {i}: {value}") if verb else None
            indentation = INDENTATION_CHAR * INDENTATION_AMOUNT * indent_level
            return (
                indentation
                + "import datetime\n"
                + indentation
                + "Date = datetime.datetime.now()",
                in_otherwise_block,
            )
        return None

    @staticmethod
    def format_date_action(line, indent_level, in_otherwise_block, verb=False):
        """
        Converts 'Format_Date' pseudo code to Python code.
        """
        FORMAT_DATE_REGEX = r"^\s*(FormatedDate\s*=\s*Format_Date)"
        match = re.match(FORMAT_DATE_REGEX, line)
        if match:
            print(f"FORMAT_DATE_REGEX") if verb else None
            for i, value in enumerate(match.groups(), start=1):
                print(f"\tGroup {i}: {value}") if verb else None
            indentation = INDENTATION_CHAR * INDENTATION_AMOUNT * indent_level
            return (
                indentation +
                "FormatedDate = Date.strftime('%Y-%m-%d %H:%M:%S')",
                in_otherwise_block,
            )
        return None

    @staticmethod
    def current_date_assignment_action(
        line, indent_level, in_otherwise_block, verb=False
    ):
        """
        Converts 'Current Date' pseudo code to Python code.
        """
        CURRENT_DATE_ASSIGNMENT_REGEX = r"^\s*(\w+)\s*=\s*Current Date"
        match = re.match(CURRENT_DATE_ASSIGNMENT_REGEX, line)
        if match:
            print(f"CURRENT_DATE_ASSIGNMENT_REGEX") if verb else None
            for i, value in enumerate(match.groups(), start=1):
                print(f"\tGroup {i}: {value}") if verb else None
            indentation = INDENTATION_CHAR * INDENTATION_AMOUNT * indent_level
            return (
                indentation
                + f"{indentation}import datetime\nDate = datetime.datetime.now()",
                in_otherwise_block,
            )
        return None

    @staticmethod
    def formatted_date_assignment_action(
        line, indent_level, in_otherwise_block, verb=False
    ):
        """
        Converts 'Format Date' pseudo code to Python code.
        """
        FORMATTED_DATE_ASSIGNMENT_REGEX = r"^\s*(\w+)\s*=\s*Format Date\s*\(\s*\{Date:\s*(\w+),\s*Format:\s*\"(\w+)\"\}\s*\)$"
        match = re.match(FORMATTED_DATE_ASSIGNMENT_REGEX, line)
        if match:
            print(f"FORMATTED_DATE_ASSIGNMENT_REGEX") if verb else None
            for i, value in enumerate(match.groups(), start=1):
                print(f"\tGroup {i}: {value}") if verb else None
            indentation = INDENTATION_CHAR * INDENTATION_AMOUNT * indent_level
            return (
                indentation +
                f"FormatedDate = Date.strftime('%Y-%m-%d %H:%M:%S')",
                in_otherwise_block,
            )
        return None

    @staticmethod
    def time_difference_action(line, indent_level, in_otherwise_block, verb=False):
        """
        Converts 'Get_time_between' pseudo code to Python code.
        """
        TIME_DIFFERENCE_REGEX = (
            r"^\s*(\w+)\s*=\s*Get_time_between (\w+) and (\w+) in\s*Seconds$")
        match = re.match(TIME_DIFFERENCE_REGEX, line)
        if match:
            print(f"TIME_DIFFERENCE_REGEX") if verb else None
            for i, value in enumerate(match.groups(), start=1):
                print(f"\tGroup {i}: {value}") if verb else None
            indentation = INDENTATION_CHAR * INDENTATION_AMOUNT * indent_level
            return (
                indentation
                + "import datetime\n"
                + indentation
                + "Time_Between_Dates = (datetime.datetime.strptime(nowDate, '%Y-%m-%d %H:%M:%S') - datetime.datetime.strptime(lastDate, '%Y-%m-%d %H:%M:%S')).total_seconds()",
                in_otherwise_block,
            )
        return None


#   ===============================================
#   note_management_actions NoteManagementActions
#
class NoteManagementActions:
    @staticmethod
    def find_notes_action(line, indent_level, in_otherwise_block, verb=False):
        """
        Converts 'Find_Notes' pseudo code to Python code.
        """
        FIND_NOTES_REGEX = (
            r"^\s*(\w+)\s*=\s*Find_Notes\s*where\s*Folder is\s*(\w+)\s*.*$")
        match = re.match(FIND_NOTES_REGEX, line)
        if match:
            print(f"FIND_NOTES_REGEX") if verb else None
            for i, value in enumerate(match.groups(), start=1):
                print(f"\tGroup {i}: {value}") if verb else None
            indentation = INDENTATION_CHAR * INDENTATION_AMOUNT * indent_level
            folder_name = match.group(2)
            return (
                indentation
                + "import os\n"
                + f'{indentation}folder_path = "Notes/{folder_name}"\n'
                + indentation
                + "os.makedirs(folder_path, exist_ok=True)\n"
                + indentation
                + "Note_files = os.listdir(folder_path)\n"
                + indentation
                + "Note_files = sorted([os.path.join(folder_path, file) for file in Note_files], key=os.path.getctime, reverse=True)\n"
                + indentation
                + "Notes = []\n"
                + indentation
                + "for file in Note_files:\n"
                + indentation
                + INDENTATION_STRING
                + "with open(file, 'r') as f:\n"
                + indentation
                + INDENTATION_STRING * 2
                + "Notes.append(f.read())",
                in_otherwise_block,
            )
        return None

    @staticmethod
    def create_note_action(line, indent_level, in_otherwise_block, verb=False):
        """
        Converts 'Create_note_with' pseudo code to Python code.
        """
        CREATE_NOTE_REGEX = r"^\s*Create_note_with\s*(\w+)\s*in\s*(\w+)\s*$"
        match = re.match(CREATE_NOTE_REGEX, line)
        if match:
            print(f"CREATE_NOTE_REGEX") if verb else None
            for i, value in enumerate(match.groups(), start=1):
                print(f"\tGroup {i}: {value}") if verb else None
            indentation = INDENTATION_CHAR * INDENTATION_AMOUNT * indent_level
            return (
                re.sub(
                    CREATE_NOTE_REGEX,
                    lambda match: (
                        f"{indentation}import os\n"
                        f"{indentation}import re\n"
                        # include 'Notes' in the directory path
                        f"{indentation}dir_path = os.path.join('Notes', '{match.group(2)}')\n"
                        f"{indentation}os.makedirs(dir_path, exist_ok=True)\n"
                        f"{indentation}valid_filename = re.sub('[^\\w\\-_\\. ]', '_', {match.group(1)}.split('\\n')[0][:80])\n"
                        f"{indentation}with open(os.path.join(dir_path, valid_filename + '.txt'), 'w') as file:\n"
                        f"{indentation}{INDENTATION_STRING}file.write({match.group(1)})"
                    ),
                    line,
                ),
                in_otherwise_block,
            )
        return None


#   ===============================================
#   sysops_actions  SysopsActions
#
class SysopsActions:
    @staticmethod
    def wait_action(line, indent_level, in_otherwise_block, verb=False):
        """
        Converts 'Wait' pseudo code to Python code.
        """
        WAIT_REGEX = r"^\s*Wait\s+(\d+)\s+second[s]*\s*$"
        match = re.match(WAIT_REGEX, line)
        if match:
            print(f"WAIT_REGEX") if verb else None
            for i, value in enumerate(match.groups(), start=1):
                print(f"\tGroup {i}: {value}") if verb else None
            indentation = INDENTATION_CHAR * INDENTATION_AMOUNT * indent_level
            wait_time = match.group(1)
            return (
                f"{indentation}import time\n{indentation}time.sleep({wait_time})",
                in_otherwise_block,
            )
        return None

    @staticmethod
    def show_action(line, indent_level, in_otherwise_block, verb=False):
        """
        Converts 'Show' pseudo code to Python code.
        """
        SHOW_REGEX = r"^\s*Show\s+(.*)$"
        match = re.match(SHOW_REGEX, line)
        if match:
            print(f"SHOW_REGEX") if verb else None
            for i, value in enumerate(match.groups(), start=1):
                print(f"\tGroup {i}: {value}") if verb else None
            indentation = INDENTATION_CHAR * INDENTATION_AMOUNT * indent_level
            regex = r'"([^"]+)"|\b(\w+)\b'
            matches = re.findall(regex, line)
            formatted_parts = []
            first_match = True
            for quoted_part, variable_part in matches:
                if first_match:
                    first_match = False
                    continue
                if quoted_part:
                    formatted_parts.append(quoted_part)
                else:
                    formatted_parts.append(f"{{{variable_part}}}")
            print_line = f'print(f"{" ".join(formatted_parts)}")'
            return indentation + print_line, in_otherwise_block
        return None

    @staticmethod
    def stop_action(line, indent_level, in_otherwise_block, verb=False):
        """
        Converts 'Stop_this_shortcut' pseudo code to Python code.
        """
        STOP_REGEX = r"^\s*Stop_this_shortcut\s*$"
        match = re.match(STOP_REGEX, line)
        if match:
            print(f"STOP_REGEX") if verb else None
            for i, value in enumerate(match.groups(), start=1):
                print(f"\tGroup {i}: {value}") if verb else None
            indentation = INDENTATION_CHAR * INDENTATION_AMOUNT * indent_level
            print(f">stop_regex") if verb else None
            return (
                f"{indentation}import sys\n{indentation}sys.exit()",
                in_otherwise_block,
            )
        return None


#   ===============================================
#   file_actions    FileActions
#
class FileActions:
    @staticmethod
    def create_file_action(line, indent_level, in_otherwise_block, verb=False):
        """
        Converts 'Create_file' pseudo code to Python code.
        """
        CREATE_FILE_REGEX = r"^\s*Create_file\s*(\w+)$"
        match = re.match(CREATE_FILE_REGEX, line)
        if match:
            print(f"CREATE_FILE_REGEX") if verb else None
            for i, value in enumerate(match.groups(), start=1):
                print(f"\tGroup {i}: {value}") if verb else None
            indentation = INDENTATION_CHAR * INDENTATION_AMOUNT * indent_level
            print(f">create_file_regex") if verb else None
            return (
                indentation
                + re.sub(
                    CREATE_FILE_REGEX, r"with open('\1', 'w') as file: pass", line
                ),
                in_otherwise_block,
            )
        return None

    @staticmethod
    def read_file_action(line, indent_level, in_otherwise_block, verb=False):
        """
        Converts 'Read_file' pseudo code to Python code.
        """
        READ_FILE_REGEX = r"^\s*Read_file\s*(\w+)\s*to\s*(\w+)$"
        match = re.match(READ_FILE_REGEX, line)
        if match:
            print(f"READ_FILE_REGEX") if verb else None
            for i, value in enumerate(match.groups(), start=1):
                print(f"\tGroup {i}: {value}") if verb else None
            indentation = INDENTATION_CHAR * INDENTATION_AMOUNT * indent_level
            print(f">read_file_regex") if verb else None
            return (
                indentation
                + re.sub(
                    READ_FILE_REGEX,
                    r"with open('\1', 'r') as file: \2 = file.read()",
                    line,
                ),
                in_otherwise_block,
            )
        return None

    @staticmethod
    def save_file_action(line, indent_level, in_otherwise_block, verb=False):
        """
        Converts 'Save_File' pseudo code to Python code.
        """
        SAVE_STATEMENT_REGEX = r"^\s*(\w+)\s*=\s*Save_File (\w+)\s*\{.*\}\s*$"
        match = re.match(SAVE_STATEMENT_REGEX, line)
        if match:
            print(f"SAVE_STATEMENT_REGEX") if verb else None
            for i, value in enumerate(match.groups(), start=1):
                print(f"\tGroup {i}: {value}") if verb else None
            tgt = match.group(1)
            src = match.group(2)
            indentation = INDENTATION_CHAR * INDENTATION_AMOUNT * indent_level
            code = f"{indentation}os.makedirs('Files', exist_ok=True)\n"
            code += f"{indentation}import pandas as pd\n"
            code += f'{indentation}timestamp = pd.Timestamp.now().strftime("%Y%m%d-%H%M%S")\n'
            code += f'{indentation}{tgt} = f"Files/{{timestamp}}"\n'
            code += f"{indentation}with open({tgt}, 'wb') as file: file.write({src})\n"
            return code, in_otherwise_block
        return None

    @staticmethod
    def set_name_action(line, indent_level, in_otherwise_block, verb=False):
        """
        Converts 'Set_name_of' pseudo code to Python code.
        """
        SET_NAME_REGEX = r"^\s*(\w+)\s*=\s*Set_name_of (\w+) to (\w+)\s*$"
        match = re.match(SET_NAME_REGEX, line)
        if match:
            print(f"SET_NAME_REGEX") if verb else None
            for i, value in enumerate(match.groups(), start=1):
                print(f"\tGroup {i}: {value}") if verb else None
            tgt_path = match.group(1)
            src_path = match.group(2)
            dst_file = match.group(3)
            indentation = INDENTATION_CHAR * INDENTATION_AMOUNT * indent_level
            code = ""
            code += f"{indentation}import shutil\n"
            code += f"{indentation}folder = os.path.dirname({src_path})\n"
            code += f"{indentation}dst_path = os.path.join(folder, {dst_file})\n"
            code += f"{indentation}{tgt_path} = dst_path\n"
            code += f"{indentation}with open({tgt_path}, 'wb') as dst, open({src_path}, 'rb') as src:\n"
            code += f"{indentation}{INDENTATION_STRING}shutil.copyfileobj(src, dst)\n"

            return code, in_otherwise_block
        return None


#   ===============================================
#   assignment_actions - AssignmentActions
#
class AssignmentActions:
    @staticmethod
    def set_url_action(line, indent_level, in_otherwise_block, verb=False):
        SET_URL_REGEX = r"^\s*Set_variable url to \"(.*)\"\s*$"
        match = re.match(SET_URL_REGEX, line.strip())
        if match:
            print(f"SET_URL_REGEX") if verb else None
            for i, value in enumerate(match.groups(), start=1):
                print(f"\tGroup {i}: {value}") if verb else None
            indentation = INDENTATION_CHAR * INDENTATION_AMOUNT * indent_level
            return (
                indentation + re.sub(SET_URL_REGEX, r"url = '\1'", line.strip()), in_otherwise_block,
            )
        return None

    @staticmethod
    def sysvar_assignment_action(line, indent_level, in_otherwise_block, verb=False):
        SYSVAR_ASSIGNMENT_REGEX = r"^\s*(\w+\s*=\s*)(.*)"
        match = re.match(SYSVAR_ASSIGNMENT_REGEX, line)
        if match:
            print(f"SYSVAR_ASSIGNMENT_REGEX") if verb else None
            for i, value in enumerate(match.groups(), start=1):
                print(f"\tGroup {i}: {value}") if verb else None
            indentation = INDENTATION_CHAR * INDENTATION_AMOUNT * indent_level
            return (
                indentation + re.sub(SYSVAR_ASSIGNMENT_REGEX, r"\1\2", line),
                in_otherwise_block,
            )
        return None

    @staticmethod
    def variable_assignment_to_action(
        line, indent_level, in_otherwise_block, verb=False
    ):
        VARIABLE_ASSIGNMENT_TO_REGEX = r"^\s*Set_variable\s*(\S+)\s*\sto\s\s*(.*?)\s*$"
        match = re.match(VARIABLE_ASSIGNMENT_TO_REGEX, line)
        if match:
            print(f"VARIABLE_ASSIGNMENT_TO_REGEX") if verb else None
            for i, value in enumerate(match.groups(), start=1):
                print(f"\tGroup {i}: {value}") if verb else None
            indentation = INDENTATION_CHAR * INDENTATION_AMOUNT * indent_level
            variable_name = match.group(1).replace(" ", "")  # control
            value = match.group(2)  # Text
            parsed_line = f"{variable_name} = {value}"
            return f"{indentation}{parsed_line}", in_otherwise_block
        return None

    @staticmethod
    def variable_assignment_from_env_action(
        line, indent_level, in_otherwise_block, verb=False
    ):
        """
        Set_variable inlang from_environ with_default Text
        """
        VARIABLE_ASSIGNMENT_FROM_ENV_REGEX = (
            r"^\s*Set_variable\s*(\w+)\s*from_environ\s*with_default\s*(.*?)\s*$")
        match = re.match(VARIABLE_ASSIGNMENT_FROM_ENV_REGEX, line)
        if match:
            print(f"VARIABLE_ASSIGNMENT_FROM_ENV_REGEX") if verb else None
            for i, value in enumerate(match.groups(), start=1):
                print(f"\tGroup {i}: {value}") if verb else None
            indentation = INDENTATION_CHAR * INDENTATION_AMOUNT * indent_level
            variable_name = match.group(1)
            default_value = match.group(2)

            code = ""
            code += f"{indentation}import os\n"
            code += f"{indentation}{variable_name} = os.environ.get('{variable_name}', {default_value})\n"
            code += f"{indentation}if isinstance({variable_name}, str):\n"
            code += f"{indentation}{INDENTATION_STRING * 1}if {variable_name}.isdigit():\n"
            code += f"{indentation}{INDENTATION_STRING * 2}{variable_name} = int({variable_name})\n"
            code += f"{indentation}{INDENTATION_STRING * 1}elif {variable_name}.replace('.', '', 1).isdigit() and {variable_name}.count('.') < 2:\n"
            code += f"{indentation}{INDENTATION_STRING * 2}{variable_name} = float({variable_name})\n"
            code += (
                f"{indentation}{INDENTATION_STRING * 1}elif {variable_name}.lower() in ['true', 'false']:\n"
            )
            code += f"{indentation}{INDENTATION_STRING * 2}{variable_name} = {variable_name}.lower() == 'true'\n"

            return code, in_otherwise_block
        return None

    @staticmethod
    def variable_assignment_from_env_no_default_action(
        line, indent_level, in_otherwise_block, verb=False
    ):
        """
        Set_variable var from_environ
        """
        VARIABLE_ASSIGNMENT_FROM_ENV_NO_DEFAULT_REGEX = (
            r"^\s*Set_variable\s*(\w+)\s*from_environ\s*$")
        match = re.match(VARIABLE_ASSIGNMENT_FROM_ENV_NO_DEFAULT_REGEX, line)
        if match:
            print(f"VARIABLE_ASSIGNMENT_FROM_ENV_NO_DEFAULT_REGEX") if verb else None
            for i, value in enumerate(match.groups(), start=1):
                print(f"\tGroup {i}: {value}") if verb else None
            indentation = INDENTATION_CHAR * INDENTATION_AMOUNT * indent_level
            variable_name = match.group(1)

            code = ""
            code += f"{indentation}import os\n"
            code += (
                f"{indentation}{variable_name} = os.environ.get('{variable_name}')\n"
            )
            code += f"{indentation}if isinstance({variable_name}, str):\n"
            code += f"{indentation}{INDENTATION_STRING * 1}if {variable_name}.isdigit():\n"
            code += f"{indentation}{INDENTATION_STRING * 2}{variable_name} = int({variable_name})\n"
            code += f"{indentation}{INDENTATION_STRING * 1}elif {variable_name}.replace('.', '', 1).isdigit() and {variable_name}.count('.') < 2:\n"
            code += f"{indentation}{INDENTATION_STRING * 2}{variable_name} = float({variable_name})\n"
            code += (
                f"{indentation}{INDENTATION_STRING * 1}elif {variable_name}.lower() in ['true', 'false']:\n"
            )
            code += f"{indentation}{INDENTATION_STRING * 2}{variable_name} = {variable_name}.lower() == 'true'\n"

            return code, in_otherwise_block
        return None


#   ===============================================
#   void_actions    VoidActions
#
class VoidActions:
    @staticmethod
    def pycomment_action(line, indent_level, in_otherwise_block, verb=False):
        """
        Leaves Python comments unchanged.
        """
        PYCOMMENT_REGEX = r"^\s*#.*$"
        match = re.match(PYCOMMENT_REGEX, line)
        if match:
            print(f"PYCOMMENT_REGEX") if verb else None
            for i, value in enumerate(match.groups(), start=1):
                print(f"\tGroup {i}: {value}") if verb else None
            return line, in_otherwise_block
        return None

    @staticmethod
    def comment_action(line, indent_level, in_otherwise_block, verb=False):
        """
        Converts 'Comment' pseudo code to Python comments.
        """
        COMMENT_REGEX = r"^\s*Comment(.*)$"
        match = re.match(COMMENT_REGEX, line)
        if match:
            print(f"COMMENT_REGEX") if verb else None
            for i, value in enumerate(match.groups(), start=1):
                print(f"\tGroup {i}: {value}") if verb else None
            indentation = INDENTATION_CHAR * INDENTATION_AMOUNT * indent_level
            comment_text = match.group(1)  # Extract the comment text
            return indentation + "#" + comment_text, in_otherwise_block
        return None

    @staticmethod
    def empty_line_action(line, indent_level, in_otherwise_block, verb=False):
        """
        Leaves empty lines unchanged.
        """
        EMPTY_LINE_REGEX = r"^\s*$"
        match = re.match(EMPTY_LINE_REGEX, line)
        if match:
            print(f"EMPTY_LINE_REGEX") if verb else None
            for i, value in enumerate(match.groups(), start=1):
                print(f"\tGroup {i}: {value}") if verb else None
            return line, in_otherwise_block
        return None


#   ===============================================
#   text_manipulation_actions
#
class TextManipulationActions:
    @staticmethod
    def change_case_action(line, indent_level, in_otherwise_block, verb=False):
        """
        Converts 'Change_case_of' pseudo code to Python code for changing the case of a string.
        """
        CHANGE_CASE_REGEX = r"^\s*Change_case_of\s*(\w+)\s*to\s*(lower|upper)$"
        match = re.match(CHANGE_CASE_REGEX, line)
        if match:
            print(f"CHANGE_CASE_REGEX") if verb else None
            for i, value in enumerate(match.groups(), start=1):
                print(f"\tGroup {i}: {value}") if verb else None
            indentation = INDENTATION_CHAR * INDENTATION_AMOUNT * indent_level

            code = ""
            code += (
                f"{indentation}{match.group(1)} = {match.group(1)}.{match.group(2)}()\n"
            )

            return code, in_otherwise_block
        return None


#   ===============================================
#   pdf_file_actions    PdfFileActions
#
class PdfFileActions:
    @staticmethod
    def merge_pdfs_action(line, indent_level, in_otherwise_block, verb=False):
        """
        Converts 'Merge_PDFs' pseudo code to Python code for merging PDF files.
        """
        MERGE_PDFS_REGEX = r"^\s*Merge_PDFs\s*List\s*\(\s*(\w+)\s*\)\s*to\s*(\w+)$"
        match = re.match(MERGE_PDFS_REGEX, line)
        if match:
            print(f"MERGE_PDFS_REGEX") if verb else None
            for i, value in enumerate(match.groups(), start=1):
                print(f"\tGroup {i}: {value}") if verb else None
            indentation = INDENTATION_CHAR * INDENTATION_AMOUNT * indent_level
            return (
                indentation
                + re.sub(
                    MERGE_PDFS_REGEX,
                    r"from PyPDF2 import PdfFileMerger\n\2 = PdfFileMerger()\nfor pdf in \1:\n{indentation}\t\2.append(pdf)\n\2.write('\2.pdf')\n\2.close()",
                    line,
                ),
                in_otherwise_block,
            )
        return None

    @staticmethod
    def split_pdf_action(line, indent_level, in_otherwise_block, verb=False):
        """
        Converts 'Split_PDF' pseudo code to Python code for splitting a PDF file.
        """
        SPLIT_PDF_REGEX = r"^\s*Split_PDF\s*(\w+)\s*to\s*(\w+)$"
        match = re.match(SPLIT_PDF_REGEX, line)
        if match:
            print(f"SPLIT_PDF_REGEX") if verb else None
            for i, value in enumerate(match.groups(), start=1):
                print(f"\tGroup {i}: {value}") if verb else None
            indentation = INDENTATION_CHAR * INDENTATION_AMOUNT * indent_level
            return (
                indentation
                + re.sub(
                    SPLIT_PDF_REGEX,
                    r"from PyPDF2 import PdfFileReader\npdf = PdfFileReader(open('\1', 'rb'))\nfor i in range(pdf.getNumPages()):\n{indentation}\tpdf_writer = PdfFileWriter()\n{indentation}\tpdf_writer.addPage(pdf.getPage(i))\n{indentation}\toutput_filename = '\2_{}.pdf'.format(i)\n{indentation}\twith open(output_filename, 'wb') as out:\n{indentation}\t\tpdf_writer.write(out)",
                    line,
                ),
                in_otherwise_block,
            )
        return None

    @staticmethod
    def read_pdf_action(line, indent_level, in_otherwise_block, verb=False):
        """
        Converts 'Read_PDF' pseudo code to Python code for reading text from a PDF file.
        """
        READ_PDF_REGEX = r"^\s*Read_PDF\s*(\w+)\s*to\s*(\w+)$"
        match = re.match(READ_PDF_REGEX, line)
        if match:
            print(f"READ_PDF_REGEX") if verb else None
            for i, value in enumerate(match.groups(), start=1):
                print(f"\tGroup {i}: {value}") if verb else None
            indentation = INDENTATION_CHAR * INDENTATION_AMOUNT * indent_level
            return (
                indentation
                + re.sub(
                    READ_PDF_REGEX,
                    r"from PyPDF2 import PdfFileReader\nwith open('\1', 'rb') as file:\n{indentation}\tpdf = PdfFileReader(file)\n{indentation}\t\2 = ''\n{indentation}\tfor page in range(pdf.getNumPages()):\n{indentation}\t\t\2 += pdf.getPage(page).extractText()",
                    line,
                ),
                in_otherwise_block,
            )
        return None

    @staticmethod
    def create_pdf_action(line, indent_level, in_otherwise_block, verb=False):
        """
        Converts 'Create_PDF' pseudo code to Python code for creating a PDF file from a list of text.
        """
        CREATE_PDF_REGEX = (
            r"^\s*Create_PDF\s*from\s*List\s*\(\s*(\w+)\s*\)\s*to\s*(\w+)$")
        match = re.match(CREATE_PDF_REGEX, line)
        if match:
            print(f"CREATE_PDF_REGEX") if verb else None
            for i, value in enumerate(match.groups(), start=1):
                print(f"\tGroup {i}: {value}") if verb else None
            indentation = INDENTATION_CHAR * INDENTATION_AMOUNT * indent_level
            return (
                indentation
                + re.sub(
                    CREATE_PDF_REGEX,
                    r"from fpdf import FPDF\npdf = FPDF()\nfor text in \1:\n{indentation}\tpdf.add_page()\n{indentation}\tpdf.set_font('Arial', size=12)\n{indentation}\tpdf.multi_cell(0, 10, text)\npdf.output('\2.pdf')",
                    line,
                ),
                in_otherwise_block,
            )
        return None
