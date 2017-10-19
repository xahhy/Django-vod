import json
from pathlib import Path
import zipfile
import os

file_zip = zipfile.ZipFile('video_pack.zip','r')
for file in file_zip.namelist():
    file_zip.extract(file, r'.')
file_zip.close()
