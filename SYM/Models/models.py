#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import re
import requests

def get_raw(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.text

def parse_models(regex, text):
    result = []
    lastModel = ""
    model_regex = re.compile(r'.*\d,\d')
    for item in regex.findall(text):
        if model_regex.match(item):
            result.append([lastModel, item])
        else:
            lastModel = item
    return result

def output(results):
    print('''# This file is generated by model.py
# refer: https://www.theiphonewiki.com/wiki/Models

i386:Simulator
x86_64:Simulator''')
    
    for model in results:
        print('{}:{}'.format(model[1], model[0]))

def main(url):
    text = get_raw(url)
    if not text:
        print("Connect to url failed")
        return

    results = []

ipad = re.compile(r'rowspan.*(iPad[\w \(\)-.]*)')
results += parse_models(ipad, text)

iPhone = re.compile(r'rowspan.*(iPhone[\w \(\)-.]*)')
results += parse_models(iPhone, text)

output(results)

if __name__ == '__main__':
    main('https://www.theiphonewiki.com/w/index.php?title=Models&action=edit')