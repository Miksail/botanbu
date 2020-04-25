from discord.ext import commands
from plugins.decandfunc import is_master
from discord import *
import random


class Mafia(commands.Cog):
    """
    status: 0 - waiting for register game / 1 - waiting for players to join /2 - ?? / 3 - morning /
    4 - night

    Role for game
    mafia/don/peace/doctor/police
    1    /2  /3    /4     /5
    """

    role_map = {1: "mafia", 2: "don", 3: "peace", 4: "doctor", 5: "police"}

    def __init__(self, client):
        self.roles = [1, 1, 2, 4, 5]
        self.status = 0
        self.player_list = []
        self.player_number = 0
        self.main_message = None
        self.client = client
        self.game_master = None
        self.alive_list = []
        self.to_kill = -1

        self.night_kill = False
        self.night_police_check = False
        self.night_don_check = False
        self.night_heal = False
        self.don_is_dead = False
        self.police_is_dead = False
        self.doc_is_dead = False
        self.to_check_police = -1
        self.to_heal = -1

    @is_master()
    @commands.command(name='regmafia')
    async def mafia(self, context, *args):
        if self.status != 0:
            await context.channel.send('Game already registered')
            return
        if len(args) != 1:
            await context.channel.send('Wrong format')
            return
        if args[0].isnumeric():
            self.player_number = int(args[0])
            while len(self.roles) < self.player_number:
                self.roles.append(3)
            self.status = 1
            print("STATUS UPD: " + str(0) + " -> " + str(1))
            self.game_master = context.author
            await context.channel.send("Game master " + self.game_master.name + " started registration for game")
            self.main_message = await context.channel.send("Players(" +
                                                     str(len(self.player_list)) + "/" + str(self.player_number) +
                                                     ")\n" + str([user.name for user in self.player_list]))
        else:
            await context.channel.send('Wrong format')
            return

    @commands.command(name="joinmafia")
    async def join(self, context):
        if self.status != 1:
            await context.channel.send('Game not registered or in process already')
            return
        if self.player_number <= len(self.player_list):
            await context.channel.send('Game already filled')
            return
        if context.author not in [player.author_handle for player in self.player_list]:
            self.player_list.append(Player(context.author))
            await self.main_message.edit(content="Players(" + str(len(self.player_list)) + "/" + str(self.player_number) +
                                   ")\n" + str([user.author_handle.name for user in self.player_list]))

    @is_master()
    @commands.command(name="startmafia")
    async def startmafia(self, context, *args):
        if self.player_number < len(self.player_list):
            await context.channel.send('Too few players')
            return
        self.give_roles()
        await self.send_roles()
        self.status = 3
        print("STATUS UPD: " + str(1) + " -> " + str(3));
        self.alive_list = self.player_list.copy()
        data_for_master = ""
        for player in self.alive_list:
            data_for_master += (player.author_handle.name + " - " + Mafia.role_map[player.role] + "\n")
        await self.send_to_master(data_for_master)

    @is_master()
    @commands.command(name="refreshmafia")
    async def refreshmafia(self, context, *args):
        if True:
            self.status = 0
            self.player_list = []
            self.player_number = 0
            self.main_message = None
            self.roles = [1, 1, 2, 4, 5]
            print("STATUS UPD: ?" + " -> " + str(0))

    @is_master()
    @commands.command(name="startnight")
    async def start_night(self, context):
        if self.status == 3:
            print("STATUS UPD: " + str(3) + " -> " + str(4))
            self.status = 4
            self.night_kill = False
            self.night_police_check = False
            self.night_don_check = False
            self.night_heal = False
            await self.show_who_alive()

    async def show_who_alive(self):
        alive_modified = str([player.author_handle.name for player in self.alive_list])
        await self.send_to_master(alive_modified)
        for player in self.alive_list:
            if player.role != 3 and player.status:
                await player.author_handle.send(alive_modified)
            if player.role == 1 or player.role == 2:
                await player.author_handle.send("type !kill 'number'")
            if player.role == 4:
                await player.author_handle.send("type !heal 'number'")
            if player.role == 5:
                await player.author_handle.send("type !check 'number'")
            if player.role == 2:
                await player.author_handle.send("type !iskom 'number'")

    @commands.command(name="kill")
    async def kill_someone(self, context, *args):
        if len(args) != 1:
            return
        if int(args[0]) >= len(self.alive_list):
            return
        if self.status == 4 and (not self.night_kill) and self.is_maf(context.author):
            await self.send_to_master("mafia want to kill " + args[0])
            self.night_kill = True
            self.to_kill = int(args[0])
            await context.author.send("Ok bro")

    @commands.command(name="check")
    async def check_someone(self, context, *args):
        if len(args) != 1:
            return
        if int(args[0]) >= len(self.alive_list):
            return
        if self.status == 4 and (not self.night_police_check) and self.is_kom(context.author):
            await self.send_to_master("policmen check " + args[0])
            self.night_police_check = True
            if self.is_maf(self.alive_list[len(args)]):
                await context.author.send("HE IS MAF")
            else:
                await context.author.send("HE IS NOT MAF")

    @commands.command(name="heal")
    async def heal_someone(self, context, *args):
        if len(args) != 1:
            return
        if int(args[0]) >= len(self.alive_list):
            return
        if self.status == 4 and (not self.night_heal) and self.is_doc(context.author):
            await self.send_to_master("doctor heal " + args[0])
            self.night_heal = True
            self.to_heal = int(args[0])
            await context.author.send("Ok bro")

    @commands.command(name="iskom")
    async def heal_someone(self, context, *args):
        if len(args) != 1:
            return
        if int(args[0]) >= len(self.alive_list):
            return
        if self.status == 4 and (not self.night_don_check) and self.is_don(context.author):
            await self.send_to_master("don checked " + args[0])
            self.night_don_check = True
            self.to_check_police = int(args[0])
            await context.author.send("Ok bro")

    @is_master()
    @commands.command(name="stopnight")
    async def stop_night(self, context):
        print(str(self.night_don_check) + str(self.don_is_dead) + str(self.night_police_check)
              + str(self.police_is_dead) + str(self.night_kill) + str(self.night_heal) + str(self.doc_is_dead))
        if (self.night_don_check or self.don_is_dead) and (self.night_police_check or self.police_is_dead) \
                and self.night_kill and (self.night_heal or self.doc_is_dead):
            if not self.don_is_dead:
                for player in self.alive_list:
                    if player.role == 2:
                        if self.is_kom(self.alive_list[self.to_check_police]):
                            await player.author_handle.send("ОН КОМ, ХУЯРЬ ЕГО")
                        else:
                            await player.author_handle.send("ОН НЕ КОМ")
            if self.to_kill != self.to_kill:
                if self.is_kom(self.alive_list[self.to_kill]):
                    self.police_is_dead = True
                if self.is_doc(self.alive_list[self.to_kill]):
                    self.doc_is_dead = True
                if self.is_don(self.alive_list[self.to_kill]):
                    self.don_is_dead = True
                self.alive_list.pop(self.to_kill)
            self.status = 3
            print("STATUS UPD: " + str(4) + " -> " + str(3))
        else:
            return

    @is_master()
    @commands.command(name="showalive")
    async def show_alive(self, context):
        if self.status < 3:
            return
        await context.channel.send(str([player.author_handle.name for player in self.alive_list]))

    def give_roles(self):
        for player in self.player_list:
            player.role = self.roles.pop(random.randrange(self.player_number))
            self.player_number -= 1

    async def send_roles(self):
        for player in self.player_list:
            await player.author_handle.send("Ты хуй, но ты и " + Mafia.role_map[player.role])

    def is_maf(self, author):
        for player in self.alive_list:
            if author == player.author_handle:
                return (player.role == 1 or player.role == 2) and player.status
        return False

    def is_kom(self, author):
        for player in self.alive_list:
            if author == player.author_handle:
                return player.role == 5 and player.status
        return False

    def is_don(self, author):
        for player in self.alive_list:
            if author == player.author_handle:
                return player.role == 2 and player.status
        return False

    def is_doc(self, author):
        for player in self.alive_list:
            if author == player.author_handle:
                return player.role == 4 and player.status
        return False

    async def send_to_master(self, s):
        await self.game_master.send(s)

    @commands.command()
    async def get_ved(self, context, *args):
        print("IAMHERE")
        print(str(context.channel.guild.roles))
        for role in context.author.guild.roles:
            if role.name == "ведущий":
                print("YA ETO SEDALLALSD")
                await context.author.add_roles(role)


class Player:

    """
    player - author of message 'joinmafia'

    status: true - live; false - dead
    """

    def __init__(self, player_in):
        self.role = None
        self.author_handle = player_in
        self.status = True
