import json
import urllib.request
import shutil
import re
import os
import sys
import argparse
import subprocess
import unittest
from pprint import pprint


INDENTATION_AMOUNT = 4  # Number of spaces for each level of indentation
INDENTATION_CHAR = " "
INDENTATION_STRING = INDENTATION_CHAR * INDENTATION_AMOUNT
NEW_LINE = "\n"
CATEGORY_PARSING_MAP = {}

#   ===============================================
#   parse_action_categories
#
#   iterate over all potential parsing actions categories
#
def parse_action_categories():
    import solstyle_regs

    action_categories = [
        solstyle_regs.WebNetworkActions,
        solstyle_regs.AudioRecordActions,
        solstyle_regs.AudioSpeechActions,
        solstyle_regs.VariableDictionaryActions,
        solstyle_regs.VariableListActions,
        solstyle_regs.ControlFlowActions,
        solstyle_regs.DateTimeActions,
        solstyle_regs.NoteManagementActions,
        solstyle_regs.SysopsActions,
        solstyle_regs.FileActions,
        solstyle_regs.AssignmentActions,
        solstyle_regs.VoidActions,
        solstyle_regs.TextManipulationActions,
        solstyle_regs.PdfFileActions,
    ]
    return action_categories

#   ===============================================
#   parse_line
#
#   parse each line of solstyle pseudocode
#
def parse_line(line, indent_level, in_otherwise_block, verb=False):
    indentation = INDENTATION_CHAR * INDENTATION_AMOUNT * indent_level

    for category in parse_action_categories():
        for action_name in vars(category):
            if action_name.startswith("__"):  # ignore Python special methods
                continue
            # Use getattr to get the method
            action = getattr(category, action_name)
            parsed_line = action(
                line, indent_level, in_otherwise_block, verb
            )  # Call the method
            if parsed_line is not None:
                print(f"Parsed line: {parsed_line}") if verb else None
                return parsed_line

    print(f">other") if verb else None
    return indentation + line, in_otherwise_block


#   ===============================================
#   parse_program
#
#   parse the whole solstyle .sol app
#
def parse_program(input_program, cmdargs_dict):
    lines = input_program.split("\n")
    parsed_code = []
    indent_level = 0

    if_symbol = "If"
    otherwise_symbol = "Otherwise"
    endif_symbol = "End_If"
    in_otherwise_block = False

    repeat_symbol = "Repeat"
    end_repeat_symbol = "End_Repeat"
    repeat_block = False

    dictionary_lines = []
    dictionary_symbol = "Dictionary = Dictionary {"
    dictionary_body_block = False
    MULTI_LINE_DICT_START_REGEX = r"^\s*Dictionary\s*=\s*Dictionary\s*\{(?!.*\})\s*$"
    SINGLE_LINE_DICT_ASSIGNMENT_REGEX = (
        r"^\s*(Dictionary\s*=\s*)(Dictionary\s*)(\{.*\})$"
    )

    for line in lines:
        stripped_line = line.strip()

        # Dictioary block
        if (
            dictionary_body_block or re.match(
                MULTI_LINE_DICT_START_REGEX, line)
        ) and not re.match(SINGLE_LINE_DICT_ASSIGNMENT_REGEX, line):
            if not dictionary_body_block:
                # Store the indentation of the first line
                first_line_indentation = line[: len(line) - len(line.lstrip())]
                first_line_indentation = INDENTATION_STRING * indent_level
                # parsed_code.append(line.replace(dictionary_symbol, first_line_indentation + "Dictionary = {") + f"  # Indent Level: {indent_level}")  # Replace the dictionary symbol in the first line and append the indent level
                parsed_code.append(
                    re.sub(
                        r"\s*" + re.escape(dictionary_symbol),
                        first_line_indentation + "Dictionary = {",
                        line,
                    )
                )
                indent_level += 1  # Increment indent level for the opening brace
                dictionary_body_block = True
            elif stripped_line.endswith("}"):
                dictionary_body_block = False
                for dictionary_line in dictionary_lines:
                    # Replace 'null' with 'None' in the line
                    dictionary_line = dictionary_line.replace(
                        ": null", ": None")
                    parsed_line, _ = parse_line(
                        dictionary_line,
                        indent_level,
                        in_otherwise_block,
                        cmdargs_dict["verb"],
                    )
                    parsed_code.append(parsed_line)
                dictionary_lines = []
                indent_level -= 1  # Decrement indent level for the closing brace
                last_line_indentation = (
                    INDENTATION_STRING * indent_level
                )  # Store the indentation of the last line
                # Include the indented closing brace
                parsed_code.append(last_line_indentation + "}")
            elif not stripped_line.startswith(dictionary_symbol):
                parsed_line, _ = parse_line(
                    line, indent_level, in_otherwise_block, cmdargs_dict["verb"]
                )
                parsed_code.append(parsed_line)  # Append the indent level
            continue

        # Repeat block
        elif stripped_line.startswith(repeat_symbol):
            repeat_block = True
            parsed_line, in_otherwise_block = parse_line(
                line, indent_level, in_otherwise_block, cmdargs_dict["verb"]
            )
            parsed_code.append(parsed_line)
            indent_level += 1
        elif stripped_line == end_repeat_symbol:
            repeat_block = False
            indent_level -= 1
            parsed_line, in_otherwise_block = parse_line(
                line, indent_level, in_otherwise_block, cmdargs_dict["verb"]
            )
            # parsed_code.append(parsed_line)

        # Condition_block
        elif stripped_line.startswith(if_symbol):
            parsed_line, in_otherwise_block = parse_line(
                line, indent_level, in_otherwise_block, cmdargs_dict["verb"]
            )
            parsed_code.append(parsed_line)
            indent_level += 1
        elif stripped_line == otherwise_symbol:
            indent_level -= 1
            parsed_line, in_otherwise_block = parse_line(
                line, indent_level, in_otherwise_block, cmdargs_dict["verb"]
            )
            parsed_code.append(parsed_line)
            indent_level += 1
        elif stripped_line == endif_symbol:
            indent_level -= 1
            if in_otherwise_block:
                in_otherwise_block = False
            parsed_line, in_otherwise_block = parse_line(
                line, indent_level, in_otherwise_block, cmdargs_dict["verb"]
            )
            parsed_code.append(parsed_line)

        # Other
        else:
            parsed_line, in_otherwise_block = parse_line(
                line, indent_level, in_otherwise_block, cmdargs_dict["verb"]
            )
            parsed_code.append(parsed_line)

    return "\n".join(parsed_code)


#   ===============================================
#   data
#

class DataActions:
    @staticmethod
    def data_json_from_url(url):
        try:
            with urllib.request.urlopen(url) as response:
                data = response.read()
                return json.loads(data)
        except Exception as e:
            print(f"An error occurred: {e}")

    @staticmethod
    def data_json_from_file(file_path):
        with open(file_path, 'r') as f:
            return json.load(f)

    @staticmethod
    def data_url_to_file(url, file_path):
        with urllib.request.urlopen(url) as response, open(file_path, 'wb') as out_file:
            out_file.write(response.read())


#   ===============================================
#   script
#
class ScriptActions:
    
    @staticmethod
    def script_param_lookup(argdict, param):
        ret = None
        for key, val in argdict.items():
            try:
                if val["long"] == f"--{param}":
                    ret = key
                    break
                elif val["short"] == f"-{param}":
                    ret = key
                    break
                else:
                    pass
            except Exception:
                pass
        return ret

    
    @staticmethod
    def script_format_parameter_option(option, value):
        param = ""
        if isinstance(value, bool):
            if value:
                param = f" {option}"
            else:
                pass
        elif (isinstance(value, str) or isinstance(value, float) or isinstance(value, int)):
            if isinstance(value, str):
                if " " in value:
                    # Using double quotes around value
                    param = f' {option} "{value}"'
                else:
                    param = f" {option} {value}"
            elif isinstance(value, float) :
                param = f" {option} {value}"
            elif isinstance(value, int):
                param = f" {option} {value}"
        elif value is None:
            # If the value is None, include only the option in the command.
            param = f" {option}"
        
        return param

    
    @staticmethod
    def script_cases_dict(cases_params, argdict, cmdline_args, script_name, debug = False):
        commands = {}
        for case_id, params in cases_params.items():

            if False and not case_id == str(6):
                continue

            command = f"python {script_name}"
            cmd = ["python", script_name]

            # create a copy of case parameters and update it with command line parameters
            case_params = params.copy()
            for param in cmdline_args:
                #if cmdline_args[param] is not None:
                # take positive args
                if cmdline_args[param]:
                    case_params[param] = cmdline_args[param]

            ## Convert short forms to long form using the script_param_lookup function
            new_case_params = {}
            for key, val in case_params.items():
                new_key = ScriptActions.script_param_lookup(argdict, key)
                if new_key is not None:
                    new_case_params[new_key] = val
                else:
                    new_case_params[key] = val

            case_params = new_case_params

            for param, value in case_params.items():
                # Skip 'case' - meta parameter
                if param == 'case':
                    continue

                option_short = argdict.get(param, {}).get("short")
                option_long = argdict.get(param, {}).get("long")

                option = option_short
                if option is None:
                    option = option_long
                    if option is None:
                        option = f"--{param}"

                command += ScriptActions.script_format_parameter_option(option, value)

                if value == True:
                    cmd.append(option)
                elif value == False:
                    pass
                else:
                    cmd.append(option)
                    cmd.append(str(value))

            commands[case_id] = {"command": command, "cmd": cmd, "parameters": case_params}
        return commands


    
    @staticmethod
    def script_test_suite(args, test_file, debug=False):
        test_suite = unittest.defaultTestLoader.discover(".", pattern=test_file)
        print(f"run tests in {test_file}") if debug else None

        # Print the names of all discovered test cases
        test_result = unittest.TextTestRunner().run(test_suite)
        if test_result.errors or test_result.failures:
            print("Unit tests failed. Exiting.")
            sys.exit(1)
        else:
            print("Unit tests passed successfully.")


    
    @staticmethod
    def script_unknown_env(unknown, debug=False):
        # Loop over 'unknown' list in pairs (assuming that it contains '--arg value' pairs)
        for i in range(0, len(unknown), 2):
            arg = unknown[i]
            # remove leading dashes and replace other dashes with underscores for valid env variable
            env_arg = arg.lstrip('-').replace('-', '_')
            value = unknown[i+1]

            # Convert boolean values to 1 or 0
            if value.lower() in ["true", "false"]:
                value = "1" if value.lower() == "true" else "0"

            os.environ[env_arg] = value

            if debug:
                print(f"[script_unknown_env] {env_arg}: {os.environ[env_arg]}")

    @staticmethod
    def script_unknowndict_env(unknown_dict, debug=False):
        # Loop over 'unknown' dictionary
        for arg, value in unknown_dict.items():
            # remove leading dashes and replace other dashes with underscores for valid env variable
            env_arg = arg.lstrip('-').replace('-', '_')

            # Convert boolean values to 1 or 0
            if isinstance(value, bool):
                value = "1" if value else "0"
            elif value.lower() in ["true", "false"]:
                value = "1" if value.lower() == "true" else "0"

            os.environ[env_arg] = value

            if debug:
                print(f"[script_unknown_env] {env_arg}: {os.environ[env_arg]}")

    
    @staticmethod
    def script_case_env(case_params, debug=False):
        for key, value in case_params.items():
            if isinstance(value, bool):
                os.environ[key] = "1" if value else "0"
                print(
                    f"[script_case_env] {key}: {os.environ[key]}") if debug else None
            else:
                os.environ[key] = str(value)
                print(
                    f"[script_case_env] {key}: {os.environ[key]}") if debug else None


    
    @staticmethod
    def script_cmdargs_env(parser, args, debug=False):
        # Get the default values
        defaults = vars(parser.parse_args([]))

        # Compare actual args values against defaults
        for arg, value in vars(args).items():
            # The value of arg is not the default, handle it accordingly
            # if value != defaults.get(arg):
            if value is not None:
                if isinstance(value, bool):
                    os.environ[arg] = "1" if value else "0"
                    print(
                        f"[script_cmdargs_env] {arg}: {os.environ[arg]}") if debug else None
                else:
                    os.environ[arg] = str(value)
                    print(
                        f"[script_cmdargs_env] {arg}: {os.environ[arg]}") if debug else None


    
    @staticmethod
    def script_save_python(code, output_file):
        """This function will save the provided python code to the output_file."""
        with open(output_file, "w") as file:
            file.write(code)


    
    @staticmethod
    def script_run_python(script_path, debug=False):
        """This function will execute a python script with the given script_path."""

        print(f"[script_run_python] run {script_path}") if debug else None

        subprocess.run(["python", script_path], env=os.environ.copy())


    
    @staticmethod
    def script_process_save(cmdargs_dict, input_file, output_file, debug=False):

        print(f"[script_process_save] output_file: {output_file}") if debug else None

        if input_file is None:
            raise ValueError("No file provided")

        if not input_file.endswith(".sol"):
            raise ValueError("The file argument must be of type '.sol'")

        # read the pseudocode
        with open(input_file, "r") as file:
            pseudocode = file.read()

        # convert pseudocode into python code
        python_code = parse_program(pseudocode, cmdargs_dict)

        print(f"[script_process_save] save {output_file}") if debug else None
        ScriptActions.script_save_python(python_code, output_file)


#   ===============================================
#   args
#
class ArgsActions:


    @staticmethod    
    def args_defaults_create():
        """Create default parameters"""
        defaults = {}
        return defaults


    @staticmethod
    def args_create_argdict():
        """Create argument dictionary based on defaults"""
        defaults = ArgsActions.args_defaults_create()
        argdict = {
            "file": {
                "short": "-f",
                "long": "--file",
                "type": "str",
                "dest": "file",
                "help": ".sol pseudocode file",
            },
            "run": {
                "short": "-r",
                "long": "--run",
                "action": "store_true",
                "help": "run the .py file related to .sol",
            },
            "test": {
                "short": "-t",
                "long": "--test",
                "action": "store_true",
                "help": "run unit tests",
            },
            "env": {
                "short": "-e",
                "long": "--env",
                "action": "store_true",
                "help": "set cmd and case args to the env to be accessible by the running .py",
            },
            "debug": {
                "short": "-d",
                "long": "--debug", "action": "store_true",
                "help": "set debug value",
            },
            "case": {
                "short": "-c",
                "long": "--case",
                "type": "int",
                "dest": "case",
                "help": "use case as defined in the case dictionary",
            },
            "proc": {
                "short": "-p",
                "long": "--proc",
                "action": "store_true",
                "help": "convert .sol pseudocode and save .py",
            },
            "verb": {
                "short": "-v",
                "long": "--verb",
                "action": "store_true",
                "help": "set verbose value for parsing methods",
            },
            "desc": {
                "long": "--desc",
                "type": "str",
                "dest": "desc",
                "help": "Command description.",
            },        
        }

        return argdict


    @staticmethod
    def args_parse(argdict):
        parser = argparse.ArgumentParser()
        for key, val in argdict.items():
            short_key = val.get("short")
            long_key = val.get("long")
            if "type" in val and isinstance(val["type"], str):
                if val["type"] == "int":
                    val["type"] = int
                elif val["type"] == "str":
                    val["type"] = str
                elif val["type"] == "float":
                    val["type"] = float
                elif val["type"] == "bool":
                    val["type"] = bool
            if short_key is not None and long_key is not None:
                parser.add_argument(
                    short_key,
                    long_key,
                    **{k: v for k, v in val.items() if k not in ["short", "long"]},
                )
            elif short_key is not None:
                parser.add_argument(
                    short_key, **{k: v for k, v in val.items() if k != "short"}
                )
            elif long_key is not None:
                parser.add_argument(
                    long_key, **{k: v for k, v in val.items() if k != "long"}
                )
            else:
                raise ValueError(
                    f"Both 'short' and 'long' options are missing for {key}")
        
        args, unknown = parser.parse_known_args()  # Parse known arguments

        return parser, args, unknown


    @staticmethod
    def args_add_unknown(args, unknown, use_case):
        # Convert the 'args' Namespace to a dictionary
        cmdargs_dict = vars(args)

        # For each unrecognized argument
        for i in range(len(unknown)):
            # If the argument starts with '--', it's a flag or argument
            if unknown[i].startswith('--'):
                # If it's the last item in the list or the next item also starts with '--',
                # it's a standalone flag
                if i == len(unknown) - 1 or unknown[i+1].startswith('--'):
                    # Remove the '--' prefix from the argument name
                    arg = unknown[i].lstrip('--')
                    # Add the flag to the 'args' dictionary with value True (since it's present)
                    cmdargs_dict[arg] = True
                    # Add the flag to the command string
                    use_case['command'] += f" {unknown[i]}"
                # Otherwise, it's an argument followed by its value
                else:
                    # Remove the '--' prefix from the argument name
                    arg = unknown[i].lstrip('--')
                    val = unknown[i+1]
                    # Add the unrecognized argument to the 'args' dictionary
                    cmdargs_dict[arg] = val
                    # Add the unrecognized argument to the command string
                    use_case['command'] += f" {unknown[i]} {val}"

        # Convert the 'args' dictionary back into a Namespace
        args = argparse.Namespace(**cmdargs_dict)
        return args, use_case


    @staticmethod
    def args_add_unknowndict(args, unknown, use_case):
        # Convert the 'args' Namespace to a dictionary
        cmdargs_dict = vars(args)

        # For each unrecognized argument
        for arg, val in unknown.items():
            # Add the unrecognized argument to the 'args' dictionary
            cmdargs_dict[arg] = val

            # Add the unrecognized argument to the command string
            # If val is a boolean and is True, we only add the argument name
            # If val is a boolean and is False, we don't add anything
            # For other types of val, we add both the argument name and its value
            if isinstance(val, bool):
                if val:
                    use_case['command'] += f" --{arg}"
            else:
                use_case['command'] += f" --{arg} {val}"

        # Convert the 'args' dictionary back into a Namespace
        args = argparse.Namespace(**cmdargs_dict)
        return args, use_case


    @staticmethod
    def args_get_arg(cmdargs_dict, case_dict, param):
        param_value = None
        if param in cmdargs_dict and cmdargs_dict[param] is not None:
            param_value = cmdargs_dict[param]
        elif param in case_dict and case_dict[param] is not None:
            param_value = case_dict[param]

        return param_value

#   ===============================================
#   main
#
#   Parsing arguments
#   Running tests if necessary
#   Loading cases
#   Processing cases
#   Running the script
#
def main():

    # Create a dictionary with all possible command-line arguments
    knownargs_dict = ArgsActions.args_create_argdict()

    # Parse the command-line arguments.
    # 'args' contains recognized arguments, 'unknown_list' contains unrecognized arguments

    parser, args, unknown_list = ArgsActions.args_parse(knownargs_dict)
    # debug in args
    debug = args.debug

    unknown_dict = dict(zip(unknown_list[::2], unknown_list[1::2]))
    if debug:
        print(f"\n[main] unknown_dict:")
        pprint(unknown_dict)

    cmdargs_dict = vars(args)
    if debug:
        print(f"\n[main] cmdargs_dict:")
        pprint(cmdargs_dict)


    # If the 'test' argument was provided, run the test suite
    if args.test:
        import os
        script_file = os.path.basename(__file__)
        script_name = os.path.splitext(script_file)[0]
        test_file = f"{script_name}_test.py"

        try:
            ScriptActions.script_test_suite(args, test_file, debug)
        except Exception as e:
            print(f"{test_file} NOT found")

    # Case refers to predefined sets of arguments and their values
    case = args.case

    import os
    script_file = os.path.basename(__file__)
    script_name = os.path.splitext(script_file)[0]
    cases_path = f"{script_name}_cases.json"

    # Check if file exists in the local directory
    if os.path.isfile(cases_path):
        case_params = DataActions.data_json_from_file(cases_path)
    else:
        # Fetch from URL as a fallback
        case_params = DataActions.data_json_from_url(cases_path)

    # Build a dictionary of use_cases based on the case parameters, recognized arguments, and command line arguments
    script_name = os.path.basename(sys.argv[0])
    use_cases = ScriptActions.script_cases_dict(case_params, knownargs_dict, cmdargs_dict, script_name, debug)

    case_dict = {}

    # If the case number is 0, just print the available use cases and their parameters

    if case == 0:
        for number, use_case in use_cases.items():
            print(f"\n[main][case {number}]  {use_case['command']}") if debug else None
            print(f"\n[main][case {number}]  {use_case['cmd']}") if debug else None
            pprint(use_case["parameters"]) if debug else None
    # If the case number is in the use cases, replace the command-line arguments with the use case parameters
    elif str(case) in use_cases:

        # case is str from json file
        case = str(case)

        use_case = use_cases[case]
        if debug:
            print(f"\n[main] use_case:")
            pprint(use_case)


        case_dict = use_case["parameters"]
        if debug:
            print(f"\n[main] case_dict:")
            pprint(case_dict)


        # add debug from case
        debug = debug or case_dict.get('debug')

        # If the 'env' argument was provided, set environment variables based on the use case parameters and unrecognized arguments
        if args.env:
            ScriptActions.script_case_env(case_dict, debug)
            # ScriptActions.script_unknown_env(unknown_list, debug)
            ScriptActions.script_unknowndict_env(unknown_dict, debug)
            ScriptActions.script_cmdargs_env(parser, args, debug)

        # Add the unrecognized arguments to the 'args' namespace and the command string
        args, use_case = ArgsActions.args_add_unknown(args, unknown_list, use_case)

        # Replace command-line arguments with the use case parameters
        for key, value in use_case["parameters"].items():
            setattr(args, key, value)

        # If debug mode is on, print the final command and use case parameters
        if debug:
            print(f"\n[case {case}] command:\n") if debug else None
            print(f"\t{use_case['command']}\n") if debug else None

    # If the case number is not in the use cases and not 0, just set environment variables based on unrecognized arguments
    else:
        if args.env:
            # ScriptActions.script_unknown_env(unknown_list, debug)
            ScriptActions.script_unknowndict_env(unknown_dict, debug)
            ScriptActions.script_cmdargs_env(parser, args, debug)

    # If the 'file' argument was provided, or if the case number is in the use cases, convert the 'sol' script to Python and/or run the Python script
    if args.file or case in use_cases:
        print(f"[main] cmdargs_dict: {cmdargs_dict}") if debug else None
        print(f"[main] case_dict: {case_dict}") if debug else None
        # If 'proc' argument is provided, convert 'sol' script to Python
        if cmdargs_dict.get("proc"):

            file = ArgsActions.args_get_arg(cmdargs_dict, case_dict, "file")
            if file is None:
                raise ValueError("The 'file' argument must be provided either directly or as part of a use case.")
            
            output_file = f"{file.rsplit('.', 1)[0]}.py"

            print(
                f"[main] file/outfile: {file} / {output_file}") if debug else None

            ScriptActions.script_process_save(cmdargs_dict, file, output_file, debug)

        # If 'run' argument is provided, run the Python script
        if ArgsActions.args_get_arg(cmdargs_dict, case_dict, "run"):
            file = ArgsActions.args_get_arg(cmdargs_dict, case_dict, "file")

            if file is None:
                raise ValueError("The 'file' argument must be provided either directly or as part of a use case.")

            output_file = f"{file.rsplit('.', 1)[0]}.py"

            print(f"[main] to run file: {output_file}") if debug else None

            ScriptActions.script_run_python(output_file, debug)
        else:
            print(f"\nwill not run") if debug else None

    else:
        if not args.test:
            print(f"\n\tno file.sol or case.id") if debug else None



if __name__ == "__main__":
    main()
