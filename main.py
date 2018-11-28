import asyncio
import argparse
import config
import wp_login
from pyppeteer import launch
from time import sleep

# Argument parsing
parser = argparse.ArgumentParser(description = "")

# Puppeteer setup
browser = await launch()

# PySiteCapture setup
element_list = []


async def main():
    index_url = urls
    auth_cookie = wp_login.get_auth_cookie(index_url)
    workers = argparse.
    for worker in total workers
        pass

# Generate a task in the main event loop to execute the main function
asyncio.get_event_loop().run_until_complete(main())

