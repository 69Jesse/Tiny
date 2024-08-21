from pyhtsl import TeamPlayers, Team, chat


t = Team('BLOOD')
chat(f'some team players: {t.stat('id')} {t.players()}')
