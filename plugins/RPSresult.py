from discord.ext import commands


class RPSgame(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.rps_data = []

    @commands.command(name='rps')
    async def playrps(self, context, *args):
        """play Rock - Paper - Scissors"""
        if len(self.rps_data) < 2 and len(args) == 1:
            if args[0].upper() in ["R", "P", "S", "||R||", "||P||", "||S||"]:
                await context.channel.delete_messages([context.message])
                self.rps_data.append((context.author, args[0]))
            else:
                if args[0].upper() == "RESETSCORES":
                    self.reset_score(context.author)
                elif args[0].upper() == "SCORES":
                    await context.channel.send(self.get_score(context.author))
                else:
                    await context.channel.send('Wrong format')
        if len(self.rps_data) == 2:
            result = self.get_result()
            if result == "Draw":
                await context.channel.send("It's a Draw!"
                                           " for {} and {}".format(self.rps_data[0][0].display_name,
                                                                   self.rps_data[1][0].display_name))
            elif result == "First":
                await context.channel.send(self.rps_data[0][0].display_name + " won!")
            else:
                await context.channel.send(self.rps_data[1][0].display_name + " won!")
            self.rps_data.clear()

    def get_result(self):
        x = self.rps_data[0][1].upper()
        y = self.rps_data[1][1].upper()
        if x[0] == '|':
            x = x[2:3]
        if y[0] == '|':
            y = y[2:3]
        if x == y:
            self.write_scores("Draw")
            return "Draw"
        elif (x == 'R' and y == 'S') or (x == 'S' and y == 'P') or (x == 'P' and y == 'R'):
            self.write_scores("First")
            return "First"
        else:
            self.write_scores("Second")
            return "Second"

    def write_scores(self, result):
        """
        Scores - 'wins;draws;loses'
        """
        players_scores_list = {}
        with open('RPSscores.txt', 'r') as f:
            lines = f.read().split('\n')
            if lines[len(lines) - 1] == '':
                lines.pop()
            for i in lines:
                players_scores_list[i.split('::')[0]] = i.split('::')[1]
        f.close()
        if result == 'Draw':
            if str(self.rps_data[0][0]) not in players_scores_list.keys():
                players_scores_list[str(self.rps_data[0][0])] = "0;1;0"
            else:
                scores = players_scores_list[str(self.rps_data[0][0])].split(';')
                scores[1] = str(int(scores[1]) + 1)
                players_scores_list[str(self.rps_data[0][0])] = str("{};{};{}".format(scores[0],
                                                                                      scores[1],
                                                                                      scores[2]))
            if str(self.rps_data[1][0]) not in players_scores_list.keys():
                players_scores_list[str(self.rps_data[1][0])] = "0;1;0"
            else:
                scores = players_scores_list[str(self.rps_data[1][0])].split(';')
                scores[1] = str(int(scores[1]) + 1)
                players_scores_list[str(self.rps_data[1][0])] = str("{};{};{}".format(scores[0],
                                                                                      scores[1],
                                                                                      scores[2]))

        if result == 'First':
            if str(self.rps_data[0][0]) not in players_scores_list.keys():
                players_scores_list[str(self.rps_data[0][0])] = "1;0;0"
            else:
                scores = players_scores_list[str(self.rps_data[0][0])].split(';')
                scores[0] = str(int(scores[0]) + 1)
                players_scores_list[str(self.rps_data[0][0])] = str("{};{};{}".format(scores[0],
                                                                                      scores[1],
                                                                                      scores[2]))
            if str(self.rps_data[1][0]) not in players_scores_list.keys():
                players_scores_list[str(self.rps_data[1][0])] = "0;0;1"
            else:
                scores = players_scores_list[str(self.rps_data[1][0])].split(';')
                scores[2] = str(int(scores[2]) + 1)
                players_scores_list[str(self.rps_data[1][0])] = str("{};{};{}".format(scores[0],
                                                                                      scores[1],
                                                                                      scores[2]))

        if result == 'Second':
            if str(self.rps_data[0][0]) not in players_scores_list.keys():
                players_scores_list[str(self.rps_data[0][0])] = "0;0;1"
            else:
                scores = players_scores_list[str(self.rps_data[0][0])].split(';')
                scores[2] = str(int(scores[2]) + 1)
                players_scores_list[str(self.rps_data[0][0])] = str("{};{};{}".format(scores[0],
                                                                                      scores[1],
                                                                                      scores[2]))
            if str(self.rps_data[1][0]) not in players_scores_list.keys():
                players_scores_list[str(self.rps_data[1][0])] = "1;0;0"
            else:
                scores = players_scores_list[str(self.rps_data[1][0])].split(';')
                scores[0] = str(int(scores[0]) + 1)
                players_scores_list[str(self.rps_data[1][0])] = str("{};{};{}".format(scores[0],
                                                                                      scores[1],
                                                                                      scores[2]))

        with open('RPSscores.txt', 'w') as f:
            for i in players_scores_list.keys():
                f.write(i + "::" + players_scores_list[i])
                f.write('\n')
        f.close()

    def reset_score(self, player):
        """ Set players score to 0;0;0"""
        players_scores_list = {}
        with open('RPSscores.txt', 'r') as f:
            lines = f.read().split('\n')
            if lines[len(lines) - 1] == '':
                lines.pop()
            for i in lines:
                players_scores_list[i.split('::')[0]] = i.split('::')[1]
        f.close()
        player = str(player)
        if player in players_scores_list.keys():
            players_scores_list[player] = "0;0;0"
        with open('RPSscores.txt', 'w') as f:
            for i in players_scores_list.keys():
                f.write(i + "::" + players_scores_list[i])
                f.write('\n')
        f.close()

    def get_score(self, player):
        """ get players score"""
        players_scores_list = {}
        with open('RPSscores.txt', 'r') as f:
            lines = f.read().split('\n')
            if lines[len(lines) - 1] == '':
                lines.pop()
            for i in lines:
                players_scores_list[i.split('::')[0]] = i.split('::')[1]
        f.close()
        player = str(player)
        result = '0:0:0'
        if player in players_scores_list.keys():
            result = players_scores_list[player]
        with open('RPSscores.txt', 'w') as f:
            for i in players_scores_list.keys():
                f.write(i + "::" + players_scores_list[i])
                f.write('\n')
        f.close()
        return result
