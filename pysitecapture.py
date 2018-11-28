import asyncio
import argparse
import json
from modules import wp_login
from pyppeteer import launch


project_descr = """
PySiteCapture is used to take multiple screenshots of a website and its elements, 
and then compare them against one another.
"""

"""Argument management"""
# Create a class instance of ArgumentParser
parser = argparse.ArgumentParser(description=project_descr)

# Generate arguments for the argparser
parser.add_argument('-i', type=str, default='test_list.json', help='The input json.')
parser.add_argument('-b', type=int, default=10, help='The size of the batches to be processed.')
parser.add_argument('--width', type=int, default=1920, help='Used to override the width of the viewport.')
parser.add_argument('--height', type=int, default=1080, help='Used to override the height of the viewport.')
parser.add_argument('--max', type=int, default=5, help='Maximum percentage of allowed image difference')
parser.add_argument('-u', type=str, help='User account for logging into sites and retrieving an auth token')
parser.add_argument('-pw', type=str, help='User password for logging into sites and retrieving an auth token')

# Parse the arguments passed in the command line and assign them to an iterable object named "args".
args = parser.parse_args()

# PySiteCapture setup
viewport = {
    'width': args.width,
    'height': args.height,
}

user = {
    'login': args.u,
    'pass': args.pw,
}

element_list = []
workers = args.b


async def main():
    auth_cookie = await wp_login.get_auth_token(index_url, user)
    print(auth_cookie)

# Debug vars
index_url = 'http://hamk.aurorads.pro'
user = {'login':'jesse.frederick@aurorads.fi', 'pass':'18014EEFAd'}

# Generate a task in the main event loop to execute the main function
asyncio.get_event_loop().run_until_complete(main())

