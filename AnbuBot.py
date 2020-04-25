from discord.ext import commands
from plugins.BotCommands import BotCommands
from plugins.RPSresult import RPSgame
from plugins.mafia import Mafia
import asyncio


class Anbu(commands.Bot):

    """
    Main class
    """

    def __init__(self):

        """
        secret chat - if secret chat is activated/diactivated (true/false)
        secret_chat_messages - list, which contains messages to delete(we using this to delete messages
                               in background loop)
        secret_chat_delete_time - time after which message will be deleted
        bg_task - special loop, which runs in the second thread
        """

        self.secret_chat = False
        self.secret_chat_messages = []
        self.secret_chat_delete_time = 0
        super().__init__(command_prefix=("?", "!"),
                         description="Discord bot from MIPT")
        self.bg_task = self.loop.create_task(self.my_background_task())

    async def on_message(self, message):

        """
        This func is called then someone send a message in the chat

        I only use it to add messages in secret_chat_messages list while secret chat activated
        """

        if message.author == self.user:
            return
        print("QUERY:" + message.content + "::from " + message.author.name)
        if self.secret_chat:
            self.secret_chat_messages.append(message)
        await self.process_commands(message)

    async def on_command_error(self, context, exception):

        """
        This func is called then bot get an exception

        I use it to catch a CommanNotFound exception
        """

        if isinstance(exception, commands.errors.CommandNotFound):
            await context.channel.send("I haven't got such a command. Type '!helpme' to see all commands")

    async def my_background_task(self):

        """
        Background loop which deletes messages from secret_chat_messgaes
        """

        await self.wait_until_ready()
        while not self.is_closed():
            if not self.secret_chat:
                await asyncio.sleep(10)
            else:
                await asyncio.sleep(self.secret_chat_delete_time)
            if len(self.secret_chat_messages) > 0:
                await self.secret_chat_messages[0].channel.delete_messages([self.secret_chat_messages[0]])
                self.secret_chat_messages.pop(0)

    async def on_ready(self):

        """
        This func is called then bot sets up

        by add_cog, I am adding Classes-Cogs to bot(from folder plugins)
        """

        self.add_cog(BotCommands(self))
        self.add_cog(RPSgame(self))
        self.add_cog(Mafia(self))
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')
