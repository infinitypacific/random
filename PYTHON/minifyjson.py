import sys
import os
import json
import pathlib

def minifyJson(file):
    try:
        with open(file, 'r', encoding='utf-8') as inFile:
            data = json.load(inFile)
    except json.JSONDecodeError:
        print('[ERROR]: Invalid JSON in '+file, file=sys.stderr)
        return
    with open(file, 'w', encoding='utf-8') as outFile:
        json.dump(data, outFile, separators=(',', ':'))
        print('[INFO]: Successfully minified '+str(file))

def minifyJsonFilesInDirectory(directory):
    for file in pathlib.Path(directory).rglob('*.json'):
        minifyJson(file)
    print('[INFO]: Completed minifying directory: '+directory)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python minifyjson.py <file/directory>')
        sys.exit(1)
    if os.path.isfile(sys.argv[1]) and sys.argv[1].lower().endswith('.json'):
        minifyJson(sys.argv[1])
    elif os.path.isdir(sys.argv[1]):
        minifyJsonFilesInDirectory(sys.argv[1])
    else:
        print('[ERROR]: Invalid file/directory: '+sys.argv[1], file=sys.stderr)
        sys.exit(1)