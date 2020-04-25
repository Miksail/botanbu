from discord.ext import commands
from plugins import decandfunc


class BotCommands(commands.Cog):

    """
    Class-Cog with typical commands
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def secretchat(self, context, *args):

        """
        This func is used to activate/deactivate secret_chat mode
        """

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

        """
        This func is used to get weather in the city

        arg - city's name
        """

        await context.channel.send(decandfunc.get_weather_broadcast(arg))

    @commands.command()
    async def news(self, context, arg: str):

        """
        This func is used to get random news from the region

        arg - region (ru/us/gb etc.)
        """

        await context.channel.send(decandfunc.get_news(arg))

    @commands.command()
    async def helpme(self, context, *args):

        """
        This func is used to display bot commands
        """

        await context.channel.send(decandfunc.get_helpme(*args))

    @commands.command(pass_context=True)
    async def joind(self, context):

        """
        This func is used to join voice channel by bot

        'IN DEVELOPMENT'
        """

        if context.author.voice is not None:
            channel = context.author.voice.channel
            await channel.connect()

    @commands.command()
    @decandfunc.is_administrator()
    async def delete_bot_messages(self, context):

        """
        This func is used tO delete bot messages from the chat
        """

        def is_bot(m):
            return m.author == self.bot.user
        deleted = await context.channel.purge(limit=50, check=is_bot)
        await context.channel.send('Deleted {} message(s)'.format(len(deleted)))

    @commands.command()
    @decandfunc.is_administrator()
    async def delete_all_messages(self, context, *args):

        """
        This func is used to delete last 'args[0]' messages from the chat
        """

        def is_true(m):
            return True
        try:
            await context.channel.purge(limit=int(args[0]), check=is_true)
        except ValueError or IndexError:
            pass
