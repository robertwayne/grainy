#!/usr/bin/python
from gevent import monkey; monkey.patch_socket()
import discord
import asyncio
from Client import client
import CrashReport
import Trackers
import Configuration as ini
import Commands

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
    print('Running...')
    # this needs to be rewritten asynchronously... source of crash
    await client.change_presence(game=discord.Game(name='Use !help for commands'))
    await CrashReport.send_crash_report()
    client.loop.create_task(Trackers.get_npc_health()) and client.loop.create_task(Trackers.get_grain_price())


def main():
    try:
        client.run(ini.BOT_TOKEN)
    except Exception as e:
        CrashReport.save_crash_report(e)
        client.reload_bot()
    finally:
        client.loop.close()


if __name__ == '__main__':
    main()
