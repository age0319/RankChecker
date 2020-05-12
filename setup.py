"""
This is a setup.py script generated by py2applet

Usage:
    python setup.py py2app
"""

from setuptools import setup

APP = ['gui.py']
DATA_FILES = ['ranking.pkl']
# OPTIONS = {}

OPTIONS = {'argv_emulation': True,
           'iconfile': '/Users/agematsuharunobu/PycharmProjects/google-search/icon/Jamespeng-Movie-Ranking.icns',
           'plist': {
               'PyRuntimeLocations': [
                '@executable_path/../Frameworks/libpython3.7m.dylib',
                '/opt/anaconda3/lib/libpython3.7m.dylib'
               ]
           }}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
