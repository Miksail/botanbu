from discord.ext import commands
from plugins import decandfunc


class BotCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def secretchat(self, context, *args):
        """This func is used to activate/deactivate secret_chat mode"""
        if len(args) == 1:
            try:
                self.bot.secret_chat_delete_time = int(args[0])
            except ValueError:
                self.bot.secret_chat_delete_time = 0
        else:
            self.bot.secret_chat_delete_time = 0
        await context.channel.delete_messages([context.message])
        self.bot.secret_chat = not self.bot.secret_chat

    @commands.command()
    async def weather(self, context, arg: str):
        await context.channel.send(decandfunc.get_weather_broadcast(arg))

    @commands.command()
    async def news(self, context, arg: str):
        await context.channel.send(decandfunc.get_news(arg))

    @commands.command()
    async def helpme(self, context, *args):
        await context.channel.send(decandfunc.get_helpme(*args))

    @commands.command(pass_context=True)
    async def joind(self, context):
        if context.author.voice is not None:
            channel = context.author.voice.channel
            await channel.connect()

    @commands.command()
    @decandfunc.is_administrator()
    async def delete_bot_messages(self, context):
        def is_bot(m):
            return m.author == self.bot.user
        deleted = await context.channel.purge(limit=50, check=is_bot)
        await context.channel.send('Deleted {} message(s)'.format(len(deleted)))

    @commands.command()
    @decandfunc.is_administrator()
    async def delete_all_messages(self, context, *args):
        def is_true(m):
            return True
        try:
            await context.channel.purge(limit=int(args[0]), check=is_true)
        except ValueError or IndexError:
            pass

