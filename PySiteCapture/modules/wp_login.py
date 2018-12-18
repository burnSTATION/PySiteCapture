import asyncio
from pyppeteer import launch

"""
Description:
    Sub module of PySiteCapture used to log into WordPress sites, and provide a cookie used for auth to the site.
    
Usage:
    Import the module, call get_auth_cookie()
    The function returns a future of page.cookies()
"""


async def get_auth_token(url, user):
    browser = await launch()
    page = await browser.newPage()
    nav_future = asyncio.ensure_future(page.waitForNavigation())
    print('INFO: Getting auth cookie for {} at {}...'.format(user['login'], url))
    await page.goto(url + '/wp-login.php')
    await page.waitFor('#user_login')
    await page.type('#user_login', user['login'])
    await page.type('#user_pass', user['pass'])
    await page.click('#wp-submit')
    await nav_future
    await page.waitFor('#wpcontent')
    all_cookies = await page.cookies()
    for cookie in all_cookies:
        if cookie['name'][:20] == 'wordpress_logged_in_':
            await browser.close()
            return cookie
