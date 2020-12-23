import os
import sys
import json
from shutil import copy, rmtree
import random
import pickle

APPLICATION_NAME = "CSS"

DATA_FILE = 'dataFile'
MERKLE_FILE = "merkleFile"

SERVER_ADDR = "http://api.plos.org"
SERVER_URL = "/search?q=title%3ADNA"
# SERVER_ADDR = 'http://192.168.1.10:3000'
# SERVER_URL = "/checkData"

while (True):
    if (os.path.split(os.getcwd())[1] == APPLICATION_NAME):
        ROOT_DIR = os.getcwd()
        break
    elif (os.path.split(os.getcwd())[1] == ""):
        ROOT_DIR = None
        break
    else:
        os.chdir(os.path.split(os.getcwd())[0])

USER_DATA_DIR = os.path.join(ROOT_DIR + "/UserData")
BACK_UP_DIR = os.path.join(ROOT_DIR + "/UserData/BackUpUserData/")
# INPUT_DATA_DIR = os.path.join(ROOT_DIR + "/TestData/")
INPUT_DATA_DIR = os.path.join(ROOT_DIR + "/CssSite/CssSite/storage")
MERKLE_TREE_DIR = os.path.join(ROOT_DIR + "/MerkleTree")

sys.path.insert(1, MERKLE_TREE_DIR)
from MerkleTree import *