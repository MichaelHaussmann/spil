# -*- coding: utf-8 -*-

name = 'spil'

version = '0.1.2'

requires = [
    "Fileseq",
    "future",
    "logzero",
    "typing_extensions"
]

description = "https://github.com/MichaelHaussmann/spil"
authors = ['Michael Haussmann']


def commands():
    env.PYTHONPATH.append('{root}')


is_pure_python = True
