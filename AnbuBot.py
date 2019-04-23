from discord.ext import commands
from plugins.BotCommands import BotCommands
from plugins.RPSresult import RPSgame
import asyncio


class Anbu(commands.Bot):
    def __init__(self):
        self.secret_chat = False
        self.secret_chat_messages = []
        self.secret_chat_delete_time = 0
        super().__init__(command_prefix=("?", "!"),
                         description="Discord bot from MIPT")
        self.bg_task = self.loop.create_task(self.my_background_task())

    async def on_message(self, message):
        """This func read all messages in chat"""
        if message.author == self.user:
            return
        if self.secret_chat:
            self.secret_chat_messages.append(message)
        await self.process_commands(message)

    async def on_command_error(self, context, exception):
        if isinstance(exception, commands.errors.CommandNotFound):
            await context.channel.send("I haven't got such a command. Type '!helpme' to see all commands")

    async def my_background_task(self):
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
        self.add_cog(BotCommands(self))
        self.add_cog(RPSgame(self))
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')
