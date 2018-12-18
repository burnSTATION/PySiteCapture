from PySiteCapture.modules import wp_login

import asyncio
import argparse
import json
from pyppeteer import launch
from time import strftime

project_descr = """
PySiteCapture is used to take multiple screenshots of a website and its elements, 
and then compare them against one another.
"""

"""Argument management"""
# Create a class instance of ArgumentParser
parser = argparse.ArgumentParser(description=project_descr)

# Generate arguments for the argparser
parser.add_argument('-i', type=str, default='test_list.json', help='The input json.')
parser.add_argument('-w', type=int, default=4, help='The number of workers to spawn and use')
parser.add_argument('--width', type=int, default=1920, help='Used to override the width of the viewport.')
parser.add_argument('--height', type=int, default=1080, help='Used to override the height of the viewport.')
parser.add_argument('--max', type=int, default=5, help='Maximum percentage of allowed image difference')
parser.add_argument('-u', type=str, help='User account for logging into sites and retrieving an auth token')
parser.add_argument('-pw', type=str, help='User password for logging into sites and retrieving an auth token')
parser.add_argument('--nologin', type=bool, default=False, help='Used when sites do not require a login for page SS')

# Parse the arguments passed in the command line and assign them to an iterable object named "args".
args = parser.parse_args()

# PySiteCapture vars
viewport = {'width': args.width, 'height': args.height}
user = {'login': args.u, 'pass': args.pw}
max_workers = args.w
suffix = '_orig'
job_list = json.load(open(args.i))
workers = 0
tasks = []


# Worker class. These are spawned and each navigate pages to complete the jobs in job_list
class Worker:
    def __init__(self, w_id, w_container):
        self.id = w_id
        self.page = w_container
        self.name = 'Worker {}: '.format(str(self.id))
        self.job = None
        tasks.append(asyncio.ensure_future(self.get_job()))

    def log(self, message):
        print('[{}]'.format(strftime("%H:%M:%S")) + ' ' + self.name + message)

    async def get_job(self):
        self.job = job_list.pop(0)
        await self.start_job()

    async def start_job(self):
        self.log('Starting job "{}" on {}'.format(self.job['name'], self.job['url']))
        await self.page.goto(self.job['url'])
        element = await self.page.querySelector(self.job['selector'])
        element_bounding = await element.boundingBox()

        # Buffer all lazily loaded content
        viewport_height = self.page.viewport['height']
        scroll = 0
        while scroll + viewport_height < element_bounding['height']:
            await self.page.evaluate('_viewportHeight= > {window.scrollBy(0, _viewportHeight);}', viewport_height)
            await self.page.waitFor(20)
            scroll = scroll + viewport_height
        await self.page.waitFor(100)

        # Take screenshot
        await self.page.screenshot(path='screenshots/{}{}.png'.format(self.job['name'], suffix), clip=element_bounding)
        self.log('Finished job "{}" on {}'.format(self.job['name'], self.job['url']))

        # Check if no more jobs are to be done, else get a new job.
        if len(job_list) == 0:
            print(self.name + 'Shutting down')
            global workers
            workers -= 1
            if workers == 0:
                print('INFO: All jobs complete.')
                loop.stop()
        else:
            await self.get_job()


# Starts Chromium browser, spawns workers, gets auth tokens. General setup
async def setup():
    # user_auth = await wp_login.get_auth_token(job_list[0]['url'], user)
    browser = await launch({
        'args': ['--no-sandbox']
    })
    print('[{}]'.format(strftime("%H:%M:%S")) + ' INFO: Spawning {} workers'.format(max_workers))
    for _ in range(0, max_workers):
        page = await browser.newPage()
        await page.setJavaScriptEnabled(False)
        await page.setViewport(viewport)
        global workers
        workers += 1
        worker = Worker(workers, page)


loop = asyncio.get_event_loop()
loop.run_until_complete(setup())

# Run all screenshot jobs
loop.run_forever()

# Do image comparison
