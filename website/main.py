# Copyright © William Adams 2023, licensed under Mozilla Public License Version 2.0

from quart import Quart, render_template, abort, request
from quart_rate_limiter import RateLimiter, rate_limit  
import aiofiles
from datetime import timedelta


app = Quart(__name__)

@app.route('/')
async def index():
    return await render_template('index.html')

@rate_limit(1, timedelta(minutes=1))
@rate_limit(3, timedelta(hours=1))
@rate_limit(5, timedelta(days=1))
@app.route('/actions/mailing_list', methods=['POST'])
async def mailing_list():
    email = (await request.form)['email']
    if not email:
        return abort(400)
    async with aiofiles.open('../email/mailing_list.txt', 'r') as f:
        emails = await f.readlines()
    if email+'\n' in emails:
        return 'Already in mailing list'
    else:
        async with aiofiles.open('../email/mailing_list.txt', 'a') as f:
            await f.write(f'{email}\n')
        return 'Done'


app.run(port='9999')