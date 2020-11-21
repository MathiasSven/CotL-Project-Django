from os import path
from shutil import copy

folder = path.dirname(path.realpath(__file__))

copy(f"{folder}/config.ini.sample", f"{folder}/config.ini")