#!/usr/bin/python
from gevent import monkey; monkey.patch_socket()
import Configuration as ini
import discord
import asyncio
from Client import client
import CrashReport
from Commands import reload_bot
import Trackers
import logging


logging.basicConfig(level=logging.DEBUG, filename='./temp/crash.log')


@client.event
async def on_member_join(member):
    # rewrite this to use config file and role ID's
    role_new = discord.utils.get(member.server.roles, name="Fresh Faces / Outsiders")
    role_hide = discord.utils.get(member.server.roles, name="Frank’s Little Beauties")
    try:
        await client.add_roles(member, role_new)
    finally:
        await client.add_roles(member, role_hide)


@client.event
@asyncio.coroutine
async def on_ready():
    print('Logged in as ' + client.user.name + ' (' + client.user.id + ')')
    print('-----------------------------------------')
    print('Tracking all sorts of shit...')
    # this needs to be rewritten asynchronously... source of crash
    await CrashReport.send_crash_report()
    client.loop.create_task(Trackers.run_trackers())


def main():
    try:
        client.run(ini.BOT_TOKEN)
    except Exception as e:
        logging.exception(e)
        reload_bot()
    finally:
        client.loop.close()


if __name__ == '__main__':
    main()
