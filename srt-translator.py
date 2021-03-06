import os
import sys
import time
import argparse
import re
from tqdm import tqdm
from colorama import Fore, Back, Style 
from google.cloud import translate

'''
  * @desc load input file function 
  * @param string file_path - input file path and name
  * @param string split_on - split each line with. Default: "\n"
  * @return list
''' 
def load_file(file_path, split_on='\n'):
    # function takes the text file path, read it, split it on passed split_on (default is \n [newline])
    # and returns the list acquired

    # open the file in read mode, encoding utf-8
    fp = open(file_path, "r")
    # read the data from the file
    _data = fp.read()
    # close the file
    fp.close()
    # split the data over split_on
    _data = _data.split(split_on)
    # return the list acquired above
    return _data


'''
  * @desc split sentence into chunks
  * @param string s - Sentence to split
  * @param integer n - number of desired chunks
  * @return list of chunks
''' 
def chunks(s, n):
    mylist = list()
    _work_list = list()
    words = s.split()
    _word_count = len(words) // n
    _word_modulo = len(words) % n

    z = 0
    for i in range(0, n):
        for j in range(z, len(words)):
            _work_list.append(words[j])
            if len(_work_list) == _word_count:
                if _word_modulo > 0:
                    _work_list.append(words[j+1])
                    _word_modulo -= 1
                break

        mylist.append(" ".join(_work_list))
        z = len(" ".join(mylist).split())
        _work_list.clear()

    return mylist

'''
  * @desc translate a text with GCP Translate API
  * @param string text - Text to translate
  * @param integer project_id - GCP project ID where API is enable
  * @param integer source_language - Source language of file
  * @param integer target_language - Target language
  * @return list with translated sentences
''' 
def translate_text(text="YOUR_TEXT_TO_TRANSLATE", project_id="YOUR_PROJECT_ID",source_language="en-US",target_language="fr"):

    client = translate.TranslationServiceClient()
    location = "global"
    parent = f"projects/{project_id}/locations/{location}"

    # Detail on supported types can be found here:
    # https://cloud.google.com/translate/docs/supported-formats
    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "mime_type": "text/plain",  # mime types: text/plain, text/html
            "source_language_code": source_language,
            "target_language_code": target_language,
        }
    )

    # Display the translation for each input text provided
    for translation in response.translations:
        return translation.translated_text


##### Main #####
if __name__ == '__main__':

    # Script Parser and arguments management
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--project_id", help="GCP Project ID", type=str)
    parser.add_argument("-s", "--source_language", help="Set source language. Default: en-US", type=str, default="en-US")
    parser.add_argument("-t", "--target_language", help="Set target language. Default: fr", type=str, default="fr")
    parser.add_argument("ifile", help="Specify SRT file you want to translate", type=str)

    args = parser.parse_args()
    project_id = ""

    # The script needs the GCP project ID parameter
    # Neither with project_id parameter or with TRANSLATE_PROJECT_ID environment variable
    if not args.project_id and not os.getenv('TRANSLATE_PROJECT_ID'):
        parser.print_help()
        print("\n" + Fore.GREEN + "project_id " + Fore.RESET + "parameter is required. Please set it or set TRANSLATE_PROJECT_ID env variable.\n")
        sys.exit(2)
    elif args.project_id:
        project_id = args.project_id
    else:
        project_id = os.getenv('TRANSLATE_PROJECT_ID')

    # work variables
    _len = _i = 0
    _sentence = list()
    _work_list = list()
    to_split = list()
    translated = list()

    # Read each line of input file
    for d in tqdm(load_file(args.ifile), desc="Processing SRT file", colour="blue"):
        # do something if the line contains letters
        # else just append the line into _work_list list
        if d and re.match('[a-zA-Z-]+',d):
            # add fake line in the _work_list to replace it with (chunked) translated sentence.
            _work_list.append("my_line" + str(_i))
            _sentence.append(d)
            _i += 1

            if not d.endswith(".") and not d.endswith("?") and not d.endswith('"') and not d.endswith('!'):
                # continue the loop if it is not the end of the sentence 
                continue
            else:
                # Translate the sentence
                _len = len(_sentence)
                _translated = translate_text(" ".join(_sentence), project_id, args.source_language, args.target_language)

                # If there is more than one item (parts of sentence) in the _sentence list.
                # Replace fake lines with good translated (chunked) sentence.
                if _len > 1: 
                    _to_split = chunks(_translated, _len)
                    for index, value in enumerate(_to_split):
                        for i, v in enumerate(_work_list):
                            if v == "my_line" + str(index):
                                _work_list[i] = value
                else:
                    for i, v in enumerate(_work_list):
                        if v == "my_line0":
                            _work_list[i] = _translated
                    
                # Merge_work_list list with (final) translated list.
                # Clear temporary lists and vars
                translated += _work_list
                _work_list.clear()
                _sentence.clear()
                _i = 0
        else:
            _work_list.append(d)

    # get filename without extension
    ofile = args.ifile.split(".")
    ofile.pop()
    ofile = ".".join(ofile)

    # write translated subtitle file to an translated ouput file
    output = open(ofile + "-translated.srt", 'w')
    output.write('\n'.join(translated))
    output.close

    # Ending message
    print(Fore.BLUE + "\nDone.")
    print("Output File: " + ofile + "-translated.srt\n" + Fore.RESET)