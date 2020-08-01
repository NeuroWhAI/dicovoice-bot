import discord
from discord.ext import commands
from gtts import gTTS

with open("token.txt") as f:
    TOKEN = f.readline()

client = commands.Bot(command_prefix='$')

@client.event
async def on_ready():
    print("Bot online.")
    
@client.event
async def on_voice_state_update(member, before, after):
    """음성 채널에 사람이 입장할 경우 소리 재생."""

    # 봇에 관련된 음성 이벤트는 무시.
    if member.bot:
        return

    # 음성 채널에 입장한 경우.
    if after.channel and before.channel != after.channel:
        # 현재 음성 채널에 해당하는 Voice Client 획득.
        vc = next((vc for vc in client.voice_clients if after.channel == vc.channel), None)
        if vc is None or vc.is_playing():
            return

        vc.play(discord.FFmpegPCMAudio('welcome.mp3'))

@client.command()
async def ping(ctx):
    await ctx.send("pong")

@client.command(pass_context=True)
async def join(ctx):
    """음성 채널에 입장."""
    if ctx.voice_client:
        await ctx.send("이미 음성 채널에 있습니다.")
        return

    if ctx.author.voice:
        channel = ctx.author.voice.channel
        await channel.connect()
    else:
        await ctx.send("음성 채널에 들어간 후 사용해주세요.")

@client.command(pass_context=True)
async def leave(ctx):
    """음성 채널에서 나가기."""
    if ctx.voice_client:
        await ctx.voice_client.disconnect()

@client.command(pass_context=True, name='v')
async def voice(ctx, *, text):
    """TTS 재생하기."""
    if not ctx.voice_client or ctx.voice_client.is_playing():
        return

    tts_file = 'tts.mp3'
    tts = gTTS(text=text, lang='ko')
    tts.save(tts_file)
        
    ctx.voice_client.play(discord.FFmpegPCMAudio(tts_file))

client.run(TOKEN)
