from flask import Flask, request, jsonify
from flask_cors import CORS
import os, sys
from invokes import invoke_http

app = Flask(__name__)
CORS(app)

'''
this complex service has two functions
1) get all available food
2) get all available nearby food
    - for user
    - for guest
3) get all 
'''