from pyhtsl import Team, TeamStat


TEAM_ID = TeamStat('id')


class BloodsTeam:
    __slots__ = ()
    TEAM = Team('BLOOD')
    ID = 4


class CripsTeam:
    __slots__ = ()
    TEAM = Team('CRIP')
    ID = 9


class KingsTeam:
    __slots__ = ()
    TEAM = Team('KING')
    ID = 6


class BlacksTeam:
    __slots__ = ()
    TEAM = Team('BLACK')
    ID = 8
