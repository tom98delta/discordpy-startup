from discord.ext import commands
import os
import traceback
bot = commands.Bot(command_prefix='/')
token = os.environ['DISCORD_BOT_TOKEN']
@bot.event
async def on_command_error(ctx, error):
    orig_error = getattr(error, "original", error)
    error_msg = ''.join(traceback.TracebackException.from_exception(orig_error).format())
    await ctx.send(error_msg)
@bot.command()
async def ping(ctx):
    await ctx.send('pong')


@bot.command()
async def neko(ctx):
    await ctx.send('にゃ～ん')
    
@bot.command() 
async def join(ctx):
    """Botをボイスチャンネルに入室させます。"""
    voice_state = ctx.author.voice

    if (not voice_state) or (not voice_state.channel):
        #もし送信者がどこのチャンネルにも入っていないなら
        await ctx.send("先にボイスチャンネルに入っている必要があります。")
        return

    channel = voice_state.channel #送信者のチャンネル

    await channel.connect() #VoiceChannel.connect()を使用
@bot.command()
async def leave(ctx):
    """Botをボイスチャンネルから切断します。"""
    voice_client = ctx.message.guild.voice_client

    if not voice_client:
        await ctx.send("Botはこのサーバーのボイスチャンネルに参加していません。")
        return

    await voice_client.disconnect()
    await ctx.send("ボイスチャンネルから切断しました。")
    
@bot.command()
async def play(ctx):
    if ctx.author.voice is None:
        await ctx.send("いずれかのボイスチャンネルに接続してください")
        return
    else:
        await ctx.author.voice.channel.connect()
        voice_client = ctx.message.guild.voice_client
        if not voice_client:
            await ctx.send("ボイスチャンネルの接続に失敗しました")
            return
        if ctx.message.attachments:
            await ctx.send("添付された曲を再生します")
            await ctx.message.attachments[0].save("tmp.mp3")
            music = "tmp.mp3"
            ffmpeg_audio_source = discord.FFmpegPCMAudio(music)
            voice_client.play(ffmpeg_audio_source)
            return
        else:
            await ctx.send("ファイルを添付してください")

    
bot.run(token)
