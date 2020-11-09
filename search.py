"""
Author:     Cody Hawkins
Class:      CS5420
Project:    Assignment 5
File:       search.py
Desc:       DFS search for given directory and file
"""

import os
import sys


def file_search(filename, directory):

    result = []
    for root, dirs, files in os.walk(directory):
        if filename in files:
            result.append(os.path.join(root, filename))
    if len(result) == 0:
        print("Could not find image! Please try a new image!")
        sys.exit(1)

    return result[0]