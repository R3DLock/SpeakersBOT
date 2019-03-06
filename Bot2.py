import os
import asyncio

import youtube_dl

import discord
from discord.ext import commands


startup_extensions = ("Music")
bot = commands.Bot(description='Music Bot By R3DLock#0002', command_prefix='s!')
bot.remove_command('help')

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)



@bot.event
async def on_ready():
    await bot.change_presence(activity = discord.Game (name="s!help | BY R3DLOCK"))


@bot.command()
async def help(ctx):
    embed=discord.Embed(
        title='-Liste des commandes-',
        colour=discord.Colour.purple()
        )

    embed.set_footer(text='SpeakersBOT v.1.0')
    embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/332845778290868224/551475719734296576/1emojie_hauyt_parleur.png')
    embed.set_author(name='SpeakersBOT', icon_url='https://cdn.discordapp.com/attachments/332845778290868224/551475719734296576/1emojie_hauyt_parleur.png')
    embed.add_field(name='```join```', value='*Rejoins un salon*')
    embed.add_field(name='```leave```', value='*Quitte le salon')
    embed.add_field(name='```\Coming Soon/```', value='[...]')
    embed.add_field(name='```\Coming Soon/```', value='[...]')



    await ctx.send(embed=embed)
    await ctx.message.delete()

@bot.command(name='join')
async def _connect(ctx: commands.Context, *, channel: discord.VoiceChannel = None):
    if channel is None:
        try:
            channel = ctx.author.voice.channel
        except Exception:
            return await ctx.send("Vous n'êtes pas connecté sur un salon vocale !")

    vocal = ctx.voice_client

    if vocal:
        if vocal.channel.id == channel.id:
            return
        await vocal.move_to(channel)
    else:
        await channel.connect()

    await ctx.send('je suis connecter sur **{0}** !'.format(channel))


@bot.command(name='leave')
async def _leave(ctx: commands.Context, *, channel: discord.VoiceChannel = None):
    guild = ctx.message.guild
    vocal = ctx.voice_client
    channel = vocal.channel
    if not vocal or not vocal.is_connected():
        return await ctx.send('Je suis connecter nul part !')
    await vocal.disconnect()

    await ctx.send('je suis déconnecté de **{0}** !'.format(channel))

@bot.command(name='play')
async def _play(ctx, url) :
    loop = asyncio.get_event_loop()
    data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=False))
    ctx.voice_client.play(cls(discord.FFmpegPCMAudio(ytdl.prepare_filename(data), '-vn'), data=data), after=lambda e: print('Player error: %s' % e) if e else None)

    await ctx.send('Je lance : {}'.format(query))



bot.run('TOKEN')
