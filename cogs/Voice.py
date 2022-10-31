import discord
import os
import ffmpeg
from discord.ext import commands
from dotenv import load_dotenv
from discord.ext.audiorec import NativeVoiceClient  # important!
import random
from time import sleep

class Voice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n----")

    @commands.command()
    async def join(self, ctx: commands.Context):
        channel: discord.VoiceChannel = ctx.author.voice.channel
        if ctx.voice_client is not None:
            return await ctx.voice_client.move_to(channel)
        await channel.connect(cls=NativeVoiceClient)

    async def timeCheck(self):
        return(5)


    @commands.command()
    async def rec(self, ctx, name=None):
        ctx.voice_client.record(lambda e: print(f"Error Recording Message. Exceptioxn: {e}"))
        embedVar = discord.Embed(title="Started the Recording!",
                                description="use $stop to stop!", color=0x546e7a)
        message = await ctx.send(embed=embedVar)

        recTime = await self.timeCheck()
        sleep(recTime)

        if not ctx.voice_client.is_recording():
            return
        sMessage = await ctx.send(f'Stopping the Recording')

        wav_bytes = await ctx.voice_client.stop_record()

        if not name:
            name = str(random.randint(000000, 999999))
        with open(f'{name}.mp3', 'wb') as f:
            f.write(wav_bytes)
        await ctx.channel.send(file=discord.File(f.name))
        await message.delete()
        await sMessage.delete()
        await ctx.message.delete()
        await ctx.voice_client.disconnect()

    @commands.command()
    async def stop(ctx: commands.Context):
        if not ctx.voice_client.is_recording():
            return
        await ctx.send(f'Stopping the Recording')

        wav_bytes = await ctx.voice_client.stop_record()

        name = str(random.randint(000000, 999999))
        with open(f'{name}.mp3', 'wb') as f:
            f.write(wav_bytes)
        await ctx.voice_client.disconnect()

    @rec.before_invoke
    async def ensure_voice(self, ctx):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect(cls=NativeVoiceClient)
            else:
                await ctx.send("You are not connected to a voice channel.")
                raise commands.CommandError(
                    "Author not connected to a voice channel.")
        elif ctx.voice_client.is_playing():
            ctx.voice_client.stop()

def setup(bot):
    bot.add_cog(Voice(bot))