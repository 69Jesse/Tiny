from pyhtsl import GlobalStat, PlayerStat, Team, TeamStat


LAST_UNIX = GlobalStat('lastunix')

LATEST_COOKIES = GlobalStat('latestcookies')
COOKIE_GOAL = GlobalStat('cookiegoal')
COOKIES_NEEDED = GlobalStat('cookiesneeded')

TIME_TEMP = GlobalStat('time/temp')
TIME_DAY = GlobalStat('time/day')
TIME_HOUR = GlobalStat('time/hour')
TIME_MINUTES = GlobalStat('time/minutes')
TIME_COLOR = GlobalStat('time/color')

TURF_1_GANG = GlobalStat('turf1/gang')
TURF_1_HELD_FOR = GlobalStat('turf1/held')
TURF_1_HP = GlobalStat('turf1/hp')
TURF_1_MAX_HP = GlobalStat('turf1/mhp')
TURF_1_FUNDS = GlobalStat('turf1/funds')
TURF_1_FUNDS_PER_SECOND = GlobalStat('turf1/af')

TURF_2_GANG = GlobalStat('turf2/gang')
TURF_2_HELD_FOR = GlobalStat('turf2/held')
TURF_2_HP = GlobalStat('turf2/hp')
TURF_2_MAX_HP = GlobalStat('turf2/mhp')
TURF_2_FUNDS = GlobalStat('turf2/funds')
TURF_2_FUNDS_PER_SECOND = GlobalStat('turf2/af')

TURF_3_GANG = GlobalStat('turf3/gang')
TURF_3_HELD_FOR = GlobalStat('turf3/held')
TURF_3_HP = GlobalStat('turf3/hp')
TURF_3_MAX_HP = GlobalStat('turf3/mhp')
TURF_3_FUNDS = GlobalStat('turf3/funds')
TURF_3_FUNDS_PER_SECOND = GlobalStat('turf3/af')


CRED = PlayerStat('credibility')
FUNDS = PlayerStat('funds')

POWER = PlayerStat('power')
MAX_POWER = PlayerStat('maxpower')

MINING_SPEED = PlayerStat('minespeed')
FORAGING_SPEED = PlayerStat('foraspeed')

MINING_FORTUNE = PlayerStat('minefortune')
FARMING_FORTUNE = PlayerStat('farmfortune')
FORAGING_FORTUNE = PlayerStat('forafortune')

DAMAGE = PlayerStat('damage')

DISPLAY_ID = PlayerStat('displayid')
DISPLAY_TIMER = PlayerStat('displaytimer')
DISPLAY_ARG_1 = PlayerStat('displayarg1')
DISPLAY_ARG_2 = PlayerStat('displayarg2')
DISPLAY_ARG_3 = PlayerStat('displayarg3')

LOCATION_ID = PlayerStat('locationid')
BIG_LOCATION_ID = PlayerStat('blocationid')
BIGGEST_LOCATION_ID = PlayerStat('bblocationid')

LAST_LOCATION_ID = PlayerStat('llocationid')


TEAM_ID = TeamStat('id')


class GangSimTeam:
    TEAM: Team
    LEVEL: PlayerStat
    EXPERIENCE: PlayerStat
    REQUIRED_EXPERIENCE: PlayerStat
    ID: int


class Bloods(GangSimTeam):
    TEAM = Team('BLOOD')
    LEVEL = PlayerStat('blood lvl')
    EXPERIENCE = PlayerStat('b/xp')
    REQUIRED_EXPERIENCE = PlayerStat('b/xpr')
    ID = 4


class Crips(GangSimTeam):
    TEAM = Team('CRIP')
    LEVEL = PlayerStat('crip lvl')
    EXPERIENCE = PlayerStat('c/xp')
    REQUIRED_EXPERIENCE = PlayerStat('c/xpr')
    ID = 9


class Kings(GangSimTeam):
    TEAM = Team('KING')
    LEVEL = PlayerStat('king lvl')
    EXPERIENCE = PlayerStat('k/xp')
    REQUIRED_EXPERIENCE = PlayerStat('k/xpr')
    ID = 6


class Grapes(GangSimTeam):
    TEAM = Team('GRAPE')
    LEVEL = PlayerStat('grape lvl')
    EXPERIENCE = PlayerStat('g/xp')
    REQUIRED_EXPERIENCE = PlayerStat('g/xpr')
    ID = 5


class Guards(GangSimTeam):
    TEAM = Team('GUARD')
    LEVEL = PlayerStat('guard lvl')
    EXPERIENCE = PlayerStat('u/xp')
    REQUIRED_EXPERIENCE = PlayerStat('u/xpr')
    ID = 3


class SpawnTeam(GangSimTeam):
    TEAM = Team('SPAWN')
    LEVEL = PlayerStat('spawn lvl')
    EXPERIENCE = PlayerStat('s/xp')
    REQUIRED_EXPERIENCE = PlayerStat('s/xpr')
    ID = 7
