from discord.ext import commands 
from discord.ext.commands import Context
import discord
import requests
import os
import aiohttp
import json
from yt_dlp import YoutubeDL


api_token = os.getenv('API_TOKEN')
#-http_persistent 0

class Genaral(commands.Cog):
    
    def __init__(self, bot): 
        self.bot = bot
        self.ytdlOptions = {'format': 'bestaudio','noplaylist':'True'}
        self.FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5 ',
                               'options': '-vn'}
        self.musicQueue = []
        self.voiceClient = None
        self.isPlaying = False
        self.isPaused = False


    @commands.hybrid_command()
    async def hello(self, ctx: Context): 
        await ctx.send('Hello!')
        
    def search(self,song): 
      print('songgg',song)
      with YoutubeDL(self.ytdlOptions) as ytdl :
        try:
          info = ytdl.extract_info(f'ytsearch:{song}',download=False)['entries'][0] 
        except Exception as e:
          print(e = f"{type(e).__name__}: {e}")
          return False
      return { 'source' : info['url'], 'title' : info['title'],'original_url' : info['original_url']}
    
    async def process_song(self, ctx: Context,song):
      self.voiceClient = await ctx.author.voice.channel.connect()
      try:
        await self.voiceClient.play(discord.FFmpegPCMAudio(song, **self.FFMPEG_OPTIONS))
      except Exception as e:
        return False
    
    
          
    @commands.hybrid_command()
    async def play(self, ctx: Context, song):
      if(ctx.author.voice is not None):
        if self.isPaused == True: 
          self.voiceClient.resume()
          self.isPaused = False
        
        songName = self.search(song)
        
        if(type(songName) == type(True)):
          await ctx.send('Could not download the song. Something went wrong')
        else : 
          await ctx.send('Song added to queue')
          self.musicQueue.append({'song':songName['title'],'channel':ctx.author.voice.channel})
          
          if(not self.isPlaying):
            await self.process_song(ctx,songName['source'])
      else:
        await ctx.send('You must be connected to a voice channel')   
      
    @commands.hybrid_command()
    async def queue(self, ctx: Context):
      msg = ''
      for song in self.queue:
        msg = msg + song['title'] + '\n'  
      await ctx.send(msg)
      
    @commands.hybrid_command()
    async def test(self, ctx: Context,song):
      self.search(song)
    
    @commands.hybrid_command()
    async def pause(self, ctx: Context):
      self.voiceClient.pause()
      self.isPaused = True
    
    @commands.hybrid_command()
    async def resume(self, ctx: Context):
      self.voiceClient.resume()
      self.isPaused = False
      

async def setup(bot) -> None:
    await bot.add_cog(Genaral(bot))