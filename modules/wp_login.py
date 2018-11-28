import asyncio
from pyppeteer import launch

"""
Description:
    Sub module of PySiteCapture used to log into WordPress sites, and provide a cookie used for auth to the site.
    
Usage:
    Import the module, call get_auth_cookie()
    The function returns a future of page.cookies()
"""


async def get_auth_cookie(url):
    browser = await launch()
    page = await browser.newPage()
    nav_future = asyncio.ensure_future(page.waitForNavigation())

    await page.goto(url)
    await page.waitFor('#user_login')
    await page.waitFor(3000)
    await page.type('#user_login', config.auth['user'])
    await page.type('#user_pass', config.auth['pass'])
    await page.click('#wp-submit')
    await nav_future
    return page.cookies()
