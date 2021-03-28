"""
MIT License

Copyright (c) 2018 くろねこまいける

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

Source: https://github.com/kuronekomichael/dartcop/

Modified 2021 by Hans to write to output_checkstyle.xml file
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import xml.etree.ElementTree as ET
import subprocess

VERSION = '0.0.1'

def perror(*args):
  sys.stderr.write(*args)
  sys.stderr.write('\n')

def output2xml(strings):
  # 行単位にパースして辞書形式にする
  dicts = [read_line(line) for line in strings.split('\n') if line != '']

  # 同ファイル名毎にリスト化
  files = {}
  for dic in dicts:
    if dic['file'] not in files:
      files[dic['file']] = []
    files[dic['file']].append(dic)

  # XMLのツリーに変換
  root = ET.Element('checkstyle')
  root.attrib['version'] = '8.0'

  for file in files.keys():
      file_element = ET.SubElement(root, 'file', attrib={'name':file})
      for dic in files[file]:
        file_element.append(line2element(dic))

  return root

def read_line(line):
  result = dict(zip(['severity', 'type', 'source', 'file', 'line', 'column', 'message_type', 'message'], line.split('|')))
  result['severity'] = result['severity'].lower()
  return result

def line2element(dic):
  """
  <error line='15' column='50' severity='info' message='Avoid using braces in interpolation when not needed.' source='unnecessary_brace_in_string_interps'/>
  """
  attributes = {k: v for k, v in dic.items() if k in ['line', 'column', 'severity', 'message', 'source']}
  element = ET.Element('error', attrib=attributes)
  return element

# Help
def show_help():
  perror('Usage: dartcop [options...] <directory or list of files>')
  perror('       dartcop --version')
  perror('')
  perror('dartcop')
  perror('Homepage: https://github.com/kuronekomichael/dartcop')
  perror('Simple `dartanalyzer` wrapper convert to checkstyle format')
  exit(255)

def main(argv):
  if len(argv) == 0:
    return False

  if argv[0] == '-V' or argv[0] == '--version':
    print('dartcop v' + VERSION)
    exit(0)

  if argv[0] == 'help':
    show_help()
    exit(0)

  try:
    subprocess.check_output(['which', 'dartanalyzer'], stderr=subprocess.STDOUT)
  except subprocess.CalledProcessError as cpe:
    perror('ERROR!!')
    perror('dartanalyzer not found. Install Dart SDK and add it to PATH.')
    exit(1)

  if any([v == '--format=human' for v in argv]):
    perror('ERROR!!')
    perror('Cannot set --format=human.')
    exit(1)

  try:
    ret = subprocess.check_output(['dartanalyzer', '--format=machine'] + argv, stderr=subprocess.STDOUT)
  except subprocess.CalledProcessError as cpe:
    ret = cpe.output

  checkstyle = output2xml(ret.decode('utf-8'))

  checkStyleFile = ET.ElementTree(checkstyle)
  checkStyleFile.write('output_checkstyle.xml')

  exit(0)

if __name__ == '__main__':
  main(sys.argv[1:])
