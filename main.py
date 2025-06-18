import discord
import os
import random
from discord.ext import commands
from discord import app_commands
from discord import FFmpegPCMAudio

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
SERV_ID = os.getenv("SERV_ID")
PREFIX = "ZIZ"
GUILD_ID = discord.Object(id = SERV_ID)

intents = discord.Intents.all()
intents.message_content = True
bot = commands.Bot(command_prefix=PREFIX, intents=intents)

@bot.event
async def on_ready():
    print(f"c {bot.user}")

@bot.command(name="join",help="join un channel")
async def join(ctx):
    if ctx.author.voice == None:
        await ctx.send("ya personne")
        return
    
    channel = ctx.author.voice.channel
    voice_client = await channel.connect()

    await ctx.send(f"salem {channel.name}")

@bot.command(name="leave",help="leave un channel")
async def leave(ctx):
    if ctx.voice_client == None:
        await ctx.send("ya r")
        return
    channel = ctx.author.voice.channel
    await ctx.voice_client.disconnect()
    await ctx.send(f"g leave {channel.name}")

@bot.command(name="audio_test",help="test audio")
async def audio_test(ctx):
    if ctx.author.voice == None:
        await ctx.send("ya r")
        return
    if ctx.voice_client != ctx.author.voice.channel:
        if ctx.voice_client == None:
            await ctx.author.voice.channel.connect()
        else:
            ctx.voice_client.move_to(ctx.author.voice.channel)
    audio_file="./audio/Maroon5-Animals0.mp3"
    ctx.voice_client.play(FFmpegPCMAudio(audio_file))

@bot.command(name="pause",help="pause l'audio")
async def pause(ctx):
    if not ctx.voice_client or not ctx.voice_client.is_playing():
        return await ctx.send("Aucun audio en cours de lecture !")
    
    ctx.voice_client.pause()
    await ctx.send("Lecture en pause")

@bot.command(name="resume",help="continu l'audio")
async def resume(ctx):
    if not ctx.voice_client or not ctx.voice_client.is_paused():
        return await ctx.send("Aucun audio en pause !")
    
    ctx.voice_client.resume()
    await ctx.send("Lecture reprise")

@bot.command(name="stop",help="stop l'audio en cours")
async def stop(ctx):
    if not ctx.voice_client:
        return 
    ctx.voice_client.stop()

### le jeu

LAST=None

def getAudioFile(dif):
    if dif == None:
        dif=random.randint(0,3)
    with open("music.txt","r") as file:
        musics=file.read().splitlines()[:-1]
        file.close()
    music=musics[random.randint(0,len(musics)-1)]
    return [music,dif,f"./audio/{music}{dif}.mp3"]
    

@bot.command(name="game",help="le jeu: \n rajouter apres une difficulté entre 0 et 3 sinon elle sera random\n0 = 5s\n1 = 3s\n2 = 1s\n3 = 0.5s")
async def game(ctx,dif:int=None):
    if ctx.author.voice == None:
        await ctx.send("ya r")
        return
    if ctx.voice_client != ctx.author.voice.channel:
        if ctx.voice_client == None:
            await ctx.author.voice.channel.connect()
        else:
            ctx.voice_client.move_to(ctx.author.voice.channel)
    audio_file=getAudioFile(dif)
    LAST=audio_file[2]
    print(f"{LAST[0]} {LAST[1]}")
    ctx.voice_client.play(FFmpegPCMAudio(audio_file[2]))

@bot.command(name="last")
async def last(ctx):
    if LAST == None:
        return
    ctx.voice_client.play(FFmpegPCMAudio(LAST))
"""
LAST=None

def getAudioFile(dif):
    if dif == None:
        dif=random.randint(0,3)
    with open("music.txt","r") as file:
        musics=file.read().splitlines()[:-1]
        file.close()
    music=musics[random.randint(0,len(musics)-1)]
    return [music,dif,f"./audio/{music}{dif}.mp3"]

CX=None

def play(dif:int=None):
    audio_file=getAudioFile(dif)
    LAST=audio_file[0]
    print(f"{LAST[0]} {LAST[1]}")
    CX.voice_client.play(FFmpegPCMAudio(audio_file[2]))


L=[]

@bot.command(name="game",help="le jeu: \n rajouter apres une difficulté entre 0 et 3 sinon elle sera random\n0 = 5s\n1 = 3s\n2 = 1s\n3 = 0.5s")
async def gameStart(ctx,nb: int=1,dif:int=None):
    L=[]
    CX=ctx
    if ctx.author.voice == None:
        await ctx.send("ya r")
        return
    if ctx.voice_client != ctx.author.voice.channel:
        if ctx.voice_client == None:
            await ctx.author.voice.channel.connect()
        else:
            ctx.voice_client.move_to(ctx.author.voice.channel)
    print(nb)
    for _ in range(nb):
        CACA=False
        audio_file=getAudioFile(dif)
        L.append(audio_file)
    audio_file=L.pop(0)
    LAST=audio_file[0]
    print(f"{LAST[0]} {LAST[1]}")
    ctx.voice_client.play(FFmpegPCMAudio(audio_file[2]))
    
@bot.command()
async def next(ctx):
    if len(L)==None or len(L)==0:
        return
    audio_file=L.pop(0)
    LAST=audio_file[0]
    print(f"{LAST[0]} {LAST[1]}")
    ctx.voice_client.play(FFmpegPCMAudio(audio_file[2]))
"""
bot.run(BOT_TOKEN)