from PySiteCapture.modules import wp_login
from PySiteCapture.modules import Worker

import asyncio
import argparse
import json
from pyppeteer import launch
from math import ceil
from time import sleep

project_descr = """
PySiteCapture is used to take multiple screenshots of a website and its elements, 
and then compare them against one another.
"""

"""Argument management"""
# Create a class instance of ArgumentParser
parser = argparse.ArgumentParser(description=project_descr)

# Generate arguments for the argparser
parser.add_argument('-i', type=str, default='test_list.json', help='The input json.')
parser.add_argument('-w', type=int, default=1, help='The number of workers to spawn and use')
parser.add_argument('--width', type=int, default=1920, help='Used to override the width of the viewport.')
parser.add_argument('--height', type=int, default=1080, help='Used to override the height of the viewport.')
parser.add_argument('--max', type=int, default=5, help='Maximum percentage of allowed image difference')
parser.add_argument('-u', type=str, help='User account for logging into sites and retrieving an auth token')
parser.add_argument('-pw', type=str, help='User password for logging into sites and retrieving an auth token')

# Parse the arguments passed in the command line and assign them to an iterable object named "args".
args = parser.parse_args()

# PySiteCapture setup
viewport = {'width': args.width, 'height': args.height}
user = {'login': args.u, 'pass': args.pw}
workers = args.w
suffix = '_original'
tests = json.load(open(args.i))

active_workers = []


async def main(urls):
    #auth_cookie = await wp_login.get_auth_token(urls[0]['url'], user)
    browser = await launch()
    batch_count = ceil(len(urls) / workers)
    print('INFO: Started new job on {} to be completed in {} batches.'.format(urls[0]['url'], batch_count))
    job = 0
    job_queue = len(urls)
    while job_queue > 0:
        for worker in range(0, workers):
            sleep(10)
            print('INFO: Starting job {} of {}'.format(job + 1, batch_count))
        job += 1
        job_queue -= 1


async def spawn_worker(workerID, job):
    for worker in range(0, workers):
        sleep(10)

# Debug vars
"""tests = [
    {
        "url": "http://hamk.aurorads.pro",
        "name": "header",
        "selector": "header"
    },
    {
        "url": "http://hamk.aurorads.pro",
        "name": "footer",
        "selector": "footer"
    },
]"""


# Generate a task in the main event loop to execute the main function
asyncio.get_event_loop().run_until_complete(main(tests))
