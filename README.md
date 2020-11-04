# SRT Translator - Translate a subtible file (SRT) with Google Cloud Translate API 
## Overview:

This script allow you to translate a Serie or Movie subtible file from a language to another with the Google Cloud Translate API.

[Tqdm](https://pypi.python.org/pypi/tqdm) is used to display the progress of the translation job.

Before attempting this aware of the following:
- [6000 request per minute per project limit for the Translate API](https://cloud.google.com/translate/quotas)
- [6000000 characters per minute per project quota for the Translate API](https://cloud.google.com/translate/quotas)
- [First 500000 characters is Free and 20$ per million charasters after](https://cloud.google.com/translate/pricing)

This project is strongly inspired by [mkahn5/translate-book](https://github.com/mkahn5/translate-book) project.

## Requirements:

- Python3
- Google Cloud Translate pip package
- A GCP Environment with billing and Translate API activated
- Google Cloud Platform SDK (https://cloud.google.com/sdk/install)
- Google Cloud Platform SDK initialization and Auth (https://cloud.google.com/sdk/docs/initializing and https://cloud.google.com/sdk/gcloud/reference/auth/application-default)
- Only works with plain/text subtible file

## Configure your environment:

Install python3 in your system if not already installed.  
`brew install python3` - for MacOS  
`sudo apt install python3` - for Debian/Ubuntu  

Install python's packages requirements.  
`pip3 install -r requirements.txt --user`  

Install The Google Cloud Platform SDK (see above) and Auth.  
After SDK is installed, do the following actions and follow interactive instructions:  
`gcloud init`  
`gcloud auth login`  
`gcloud auth application-default login`  

**WARNING**: If you have python errors with gcloud commands, you must set an environment variable to use Python2 with Google SDK:  
`export CLOUDSDK_PYTHON=python2.7` (adjust the 2.x version according to your Python2 version).  


## Usage
```
usage: python3 srt-translator.py [-h] [-p PROJECT_ID] [-s SOURCE_LANGUAGE] [-t TARGET_LANGUAGE] ifile

positional arguments:
  ifile                 Specify SRT file you want to translate

optional arguments:
  -h, --help            show this help message and exit
  -p PROJECT_ID, --project_id PROJECT_ID
                        GCP Project ID
  -s SOURCE_LANGUAGE, --source_language SOURCE_LANGUAGE
                        Set source language. Default: en-US
  -t TARGET_LANGUAGE, --target_language TARGET_LANGUAGE
                        Set target language. Default: fr
```

**Information**: You must provide your GCP project ID. You have two ways to set it: with `-p`/`--project_id` parameter or with `TRANSLATE_PROJECT_ID` environment variable.  

Example: 
```
$ python3 srt-translator.py -p my_gcp_project_id my_serie.S01E01.translate_me.srt
Processing SRT file::  39%|███████████████████████████████████▊                     | 1053/2731 [01:28<02:51,  9.79it/s]
```

The output file will be `my_serie.S01E01.translate_me-translated.srt` in your current directory.  

## Supported Languages

See: https://cloud.google.com/translate/docs/languages   
