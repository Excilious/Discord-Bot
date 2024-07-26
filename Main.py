#]--Imports--[#
import discord
from discord.ext import commands,tasks
import os
import youtube_dl
import time as t
import requests
from urllib.request import urlopen
import requests as req
import datetime

youtube_dl.utils.bug_reports_message = lambda: ' '

ytdl_format_options = {
    'format': 'bestaudio/best',
    'restrictfilenames':True,
    'noplaylist':True,
    'nocheckcertificate':True,
    'ignoreerrors':False,
    'logtostderr':False,
    'quitet':True,
    'no_warnings':True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'
}

ffmpeg_options = {
    'options':'-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = ""

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]
        filename = data['title'] if stream else ytdl.prepare_filename(data)
        return filename


MySession = {
    "Users":{
        "Default0":{
            "Image":"000",
            "Name":"DEFAULT",
            "Points":0,
            "Rank":"NIL",
            "IsBlacklisted":False
            }
        },
}

client = commands.Bot(command_prefix = "-")
Commands = [{"LogIn":"Timetable"}]

@client.command(name="Radio_On",help="Enables Vortex to join different voice channels")
async def Radio_On(ctx):
    if not ctx.message.author.voice:
        await ctx.send("{} needs to be in a voice channel to access Radio!".format(ctx.message.author.name))
        return
    else:
        channel = ctx.message.author.voice.channel
    await channel.connect()

@client.command(name="Radio_Off",help="Prompts Vortex to leave the current active voice channel")
async def Radio_Off(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_connected():
        await voice_client.disconnect()
    else:
        await ctx.send("Vortex is currently not in an active voice channel.")


@client.command(name="Play",help="Play any reqested url.")
async def Play(ctx,url):
    server = ctx.message.guild
    voice_channel = server.voice_client
    async with ctx.typing():
        filename = await YTDLSource.from_url(url, loop=client.loop)
        voice_channel.play(discord.FFmpegPCMAudio(executable="ffmpeg.exe", source=filename))
    await ctx.send("**Currently Playing: **{}".format(filename))
    #try:
        #server = ctx.message.guild
        #voice_channel = server.voice_client
        #async with ctx.typing():
            #filename = await YTDLSource.from_url(url, loop=bot.loop)
            #voice_channel.play(discord.FFmpegPCMAudio(executable="ffmpeg.exe",source=filename))
        #await ctx.send("**Currently Playing: **{}".format(filename))
    #except:
        #await ctx.send("Vortex is currently not in an active voice channel.")


@client.command(name="Pause", help="Pauses any current song.")
async def Pause(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_playing():
        await voice.client.pause()
    else:
        await ctx.send("Vortex is currently not playing any songs.")


@client.command(name="Resume",help="Resumes any current song.")
async def Resume(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_paused():
        await voice_client.resume()
    else:
        await ctx.send("Vortex is currently not playing any songs.")


@client.command(name="Stop",help="Stops and removes the current song")
async def Stop(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_playing():
        await voice_client.stop()
    else:
        await ctx.send("Vortex is currently not playing any songs.")








SearchHistory = []
def googleSearch(query):
    with requests.session() as c:
        url = 'https://www.google.co.uk'
        query = {'q': query}
        urllink = requests.get(url, params=query)
        print("Link: ",urllink.url)
        SearchHistory.append(urllink.url)
        
#--Timetable--#
@client.command()
async def GoogleSearch(ctx):
    SearchHistory.clear()
    await ctx.send("Enter Search:")
    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel
    msg = await client.wait_for("message", check=check)
    if msg.content.lower() != "":
        googleSearch(msg.content.lower())
        await ctx.send(SearchHistory[0])


@client.command()
async def Menu(ctx):
    global Commands
    index = 0
    embedVar = discord.Embed(color=0x2f3136)
    embedVar.timestamp = datetime.datetime.now()
    for dic in Commands:
        for val,cal in dic.items():
            print(f'{val} is {cal}')
            embedVar.add_field(name=val, value=cal, inline=False)
            embedVar.set_author(name = ctx.author.name,icon_url=ctx.author.avatar_url)
            embedVar.set_footer(text="Home")
    await ctx.send(embed=embedVar)

    
#--Bot Token--#
client.run('[ENTER DISCORD KEY HERE]')
