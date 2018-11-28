import asyncio
import argparse
from .modules import wp_login
from pyppeteer import launch

project_descr = """
PySiteCapture is used to take multiple screenshots of a website and its elements, 
and then compare them against one another.
"""

"""Argument management"""
## Create a class instance of ArgumentParser
parser = argparse.ArgumentParser(description=project_descr)

## Generate arguments for the argparser
parser.add_argument('-i', type=str, default='test_list.json', help='The input json.')
parser.add_argument('-b', type=int, default=10, help='The size of the batches to be processed.')
parser.add_argument('--width', type=int, default=1920, help='Used to override the width of the viewport.')
parser.add_argument('--height', type=int, default=1080, help='Used to override the height of the viewport.')
parser.add_argument('--max', type=int, default=5, help='Maximum percentage of allowed image difference')

## Parse the arguments passed in the command line and assign them to an iterable object named "args".
args = parser.parse_args()


"""General setup"""
## Puppeteer setup
browser = await launch()

## PySiteCapture setup
viewport = {
    'width': args.width,
    'height': args.height,
}
element_list = []
workers = args.b


"""Main entry point of script"""
async def main():
    index_url = data[0]
    auth_cookie = wp_login.get_auth_cookie(index_url)
    workers = argparse.
    for worker in range(1, len(workers)):
        pass

# Generate a task in the main event loop to execute the main function
asyncio.get_event_loop().run_until_complete(main())

