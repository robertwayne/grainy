from discord.ext import commands
from chatbot.client import bot
import discord
import sys
import os
import random
from chatbot.trackers import *
from databot.omnispider import *
# from config.configuration import update_grain_threshold


@bot.event
async def on_message(message):
    # prevent the bot from replying to itself
    if message.author == bot.user:
        return

    # recognizes decorated functions as commands
    await bot.process_commands(message)


async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return

    errors = {commands.CheckFailure: 'You do not have permission to run this command.',
              commands.NoPrivateMessage: 'You cannot use commands outside the server.'}

    for type, text in errors.items():
        if isinstance(error, type):
            return await bot.say(errors[type])


# restarts the entire bot script
async def reload_bot():
    python = sys.executable
    await asyncio.sleep(1)
    os.execl(python, python, *sys.argv)


@bot.command(pass_context=True, no_pm=True)
@commands.has_role('{}'.format(ini.ELEVATED_ROLE_NAME))
async def restart():
    await bot.say('Restarting now!')
    print('Restarting...')
    await reload_bot()


@bot.command(pass_context=True, no_pm=True)
async def help():
    em = discord.Embed(title='OmniBot Help',
                       color=0x783e8e,
                       url='https://omnidb.io/#')
    # em.add_field(name='!stash', value='Displays items in the safehouse stash.', inline=False)
    em.add_field(name='!item "item name" or id',
                 value='Displays the stats of an in-game item. Use quotes "" for multiple words.',
                 inline=False)
    em.add_field(name='!vehicle "name" or id',
                 value='Displays the stats of an in-game vehicle.',
                 inline=False)
    em.add_field(name='!land',
                 value='Displays general land ownership statistics.',
                 inline=False)
    em.add_field(name='!restart',
                 value='Allows an elevated user to restart me.',
                 inline=False)

    await bot.say(embed=em)


# noinspection PyShadowingNames
@bot.command(pass_context=True, no_pm=True)
async def land():
    # noinspection PyShadowingNames
    land = await db_get_land_stats()
    em = discord.Embed(title='Land Stats',
                       color=0x783e8e)
    em.add_field(name='Unowned: ',
                 value=str(land.get('unowned')))
    em.add_field(name='Owned (Farms): ',
                 value=str(land['owned_farm']))
    em.add_field(name='Owned (Buildings): ',
                 value=str(land['owned_building']))
    em.set_footer(text='Total Owned: ' + str(land['total_owned']) + ' | Total:' + str(land['total']) + ' | Last updated: ' + str(land['timestamp']))

    await bot.say(embed=em)


@bot.command(pass_context=True, no_pm=True, aliases=['inum', 'i'])
async def item(ctx, x):
    # noinspection PyShadowingNames
    try:
        item = await db_get_item_stats_from_name(x)
        if item is None:
            item = await db_get_item_stats(x)
    except TypeError as e:
        print(e)
    finally:
        if item:
            em = discord.Embed(title=item['Name'] + ' [' + str(item['id']) + ']' + ' | ' + item['Type'],
                               url='https://www.zapoco.com/item/{}'.format(item['id']),
                               color=0x783e8e)
            em.set_footer(text='Value: ' + str(item['Value']) + ' | Circulation: ' + str(item['Circulation']))
            for stat in item:
                if stat == 'Name':
                    pass
                elif stat == 'Value':
                    pass
                elif stat == 'Type':
                    pass
                elif stat == 'Circulation':
                    pass
                elif stat == 'Purchasable':
                    pass
                elif item[stat] is None or item[stat] == '0.0':
                    pass
                elif stat == 'id':
                    pass
                elif stat == 'Cooldown':
                    em.add_field(name='{}'.format(stat),
                                 value='{}'.format(str(int(item[stat])) + 'm (' + str(int((50 / item[stat]))) + 'x at once before OD)'),
                                 inline=False)
                elif stat:
                    em.add_field(name='{}'.format(stat),
                                 value=str(int(item[stat])),
                                 inline=False)
            await bot.say(embed=em)
        else:
            await bot.say('Item name not found.')


@bot.command(pass_context=True, no_pm=True, aliases=['v'])
async def vehicle(ctx, x):
    # noinspection PyShadowingNames
    try:
        vehicle = await db_get_vehicle_stats_from_name(x)
        if vehicle is None:
            vehicle = await db_get_vehicle_stats(x)
    except TypeError as e:
        print(e)
    finally:
        if vehicle:
            em = discord.Embed(title=vehicle['Name'] + ' | Vehicle',
                               url='https://www.zapoco.com/vehicle/{}'.format(x),
                               color=0x783e8e)
            for stat in vehicle:
                if stat == 'Name':
                    pass
                elif vehicle[stat] is None:
                    pass
                elif stat == 'id':
                    pass
                elif stat:
                    em.add_field(name='{}'.format(stat),
                                 value=vehicle[stat],
                                 inline=False)
            await bot.say(embed=em)
        else:
            await bot.say('Vehicle not found.')


@bot.command(pass_context=True, no_pm=True)
async def tier():
    msg = '*tier is a shining star and we love her*'
    print(msg)
    await bot.say(msg)


@bot.command(pass_context=True, no_pm=True)
async def hug():
    msg = '*hugs everyone* You are all awesome!'
    print(msg)
    await bot.say(msg)


@bot.command(pass_context=True, no_pm=True)
async def thunder():
    msg = 'https://cdn.discordapp.com/attachments/445926098816073738/461366338129100800/unknown.png'
    print(msg)
    await bot.say(msg)


@bot.command(pass_context=True, no_pm=True)
async def sightings():
    msg = 'https://cdn.discordapp.com/attachments/445926098816073738/466411177476620288/image.png'
    print(msg)
    await bot.say(msg)


@bot.command(pass_context=True, no_pm=True)
async def tom():
    msg = ['For real though, F Tom...', 'F Tom...', 'F Tom!', 'Fuck Hillto- er, I mean F Tom!', 'Yeah, F Tom!']
    r_msg = random.choice(msg)
    print(r_msg)
    await bot.say(r_msg)


# @bot.command(pass_context=True)
# @commands.has_any_role('The Brains', 'The Looks', 'Headmistress Lestrange', 'The Wildcard')
# async def admin_alter_grain(ctx, x, y):
#     await update_grain_threshold(x, y)
#     await bot.say('New grain thresholds set.')


#####################################
#         DATABASE COMMANDS         #
#####################################

@bot.command(pass_context=True, no_pm=True)
@commands.has_role('{}'.format(ini.ADMIN_ROLE_NAME))
async def db_force_update_table(ctx, x):
    if x == 'items':
        await db_update_item_table()
        await bot.say('Successfully updated OmniDB.Items')
    elif x == 'land':
        await db_update_land_table()
        await bot.say('Successfully updated OmniDB.Land')
    elif x == 'vehicles':
        await db_update_vehicle_table()
        await bot.say('Successfully updated OmniDB.Vehicles')
    else:
        await bot.say('Invalid parameter.')


@bot.command(pass_context=True, no_pm=True)
@commands.has_role('{}'.format(ini.ADMIN_ROLE_NAME))
async def db_force_write_new_table(ctx, x):
    if x == 'items':
        await db_write_item_table()
        await bot.say('Successfully added OmniDB.Items')
    elif x == 'land':
        await db_update_land_table()
        await bot.say('Successfully updated OmniDB.Land')
    elif x == 'vehicles':
        await db_write_vehicle_table()
        await bot.say('Successfully added OmniDB.Vehicles')
    else:
        await bot.say('Invalid parameter.')


@bot.command(pass_context=True, no_pm=True)
@commands.has_role('{}'.format(ini.ADMIN_ROLE_NAME))
async def db_search_index():
    sql = "ALTER TABLE `vehicles` ADD FULLTEXT(Name)"
    db.execute(sql)
    conn.commit()
    await bot.say('Added search index table for Omni.Vehicles')
