from discord.ext import commands
import pandas as pd


class RPSgame(commands.Cog):

    """
    This Cog adds rock-paper-scissors game
    """

    def __init__(self, client):

        """
        Client - bot Anbu
        rps_data - matrix with players data kind of:
            1st_player's_name   R/P/S
            2nd_player's_name   R/P/S
        """

        self.client = client
        self.rps_data = []

    @commands.command(name='rps')
    async def playrps(self, context, *args):

        """
        This func is called then someone want to play or manage his scores

        players append in rps_data
        Then there is 2 players match begins. It gets result
            and after that write result in RPSscores.csv and return them to the bot
        if arg == 'scores', it will return player scores
        if arg == 'resetscores', it will reset player scores

        scores have a look as:
            wins:draws:losses
        """

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

        """
        This func checks who win
        """

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
        This func write scores in RPSscores.csv
        """

        df = pd.read_csv('RPSscores.csv')
        for i in range(2):
            if not str(self.rps_data[i][0]) in df['Name'].to_dict().values():
                df.loc[len(df.index)] = [str(self.rps_data[i][0]),
                                         0, 0, 0]
        first_player_index = int(df.loc[df['Name'] == str(self.rps_data[0][0])].index[0])
        second_player_index = int(df.loc[df['Name'] == str(self.rps_data[0][0])].index[0])
        if result == 'Draw':
            df.iloc[first_player_index, 2] += 1
            df.iloc[second_player_index, 2] += 1
        if result == 'First':
            df.iloc[first_player_index, 1] += 1
            df.iloc[second_player_index, 3] += 1
        if result == 'Second':
            df.iloc[first_player_index, 3] += 1
            df.iloc[second_player_index, 1] += 1
        df.to_csv('RPSscores.csv', index=False)

    def reset_score(self, player):

        """
        This func set players score to 0;0;0
        """

        player = str(player)
        df = pd.read_csv('RPSscores.csv')
        if not str(player) in df['Name'].to_dict().values():
            df.loc[len(df.index)] = [str(player),
                                     0, 0, 0]
        player_index = int(df.loc[df['Name'] == player].index[0])
        df.iloc[player_index, 1] = 0
        df.iloc[player_index, 2] = 0
        df.iloc[player_index, 3] = 0
        df.to_csv('RPSscores.csv', index=False)

    def get_score(self, player):

        """
         This func get players score
         """

        df = pd.read_csv('RPSscores.csv')
        if not str(player) in df['Name'].to_dict().values():
            df.loc[len(df.index)] = [str(player),
                                     0, 0, 0]
        player_index = int(df.loc[df['Name'] == str(player)].index[0])
        result = 'wins: ' + str(df.iloc[player_index, 1]) + '\n' + \
                 'draws: ' + str(df.iloc[player_index, 2]) + '\n' + \
                 'losses: ' + str(df.iloc[player_index, 3])
        return result
