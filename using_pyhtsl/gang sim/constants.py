from pyhtsl import GlobalStat, PlayerStat, Team, TeamStat


TOTAL_PLAYERS_JOINED = GlobalStat('playersjoined')
LAST_UNIX = GlobalStat('lastunix')

LATEST_COOKIES = GlobalStat('latestcookies')
COOKIE_GOAL = GlobalStat('cookiegoal')
COOKIES_NEEDED = GlobalStat('cookiesneeded')

TIME_TEMP = GlobalStat('time/temp')
TIME_DAY = GlobalStat('time/day')
TIME_HOUR = GlobalStat('time/hour')
TIME_MINUTES = GlobalStat('time/minutes')
TIME_COLOR = GlobalStat('time/color')

TURF_1_ID = 1
TURF_1_GANG = GlobalStat('turf1/gang')
TURF_1_HELD_FOR = GlobalStat('turf1/held')
TURF_1_HP = GlobalStat('turf1/hp')
TURF_1_MAX_HP = GlobalStat('turf1/mhp')
TURF_1_FUNDS = GlobalStat('turf1/funds')
TURF_1_FUNDS_PER_SECOND = GlobalStat('turf1/af')
TURF_1_HIT_COOLDOWN = GlobalStat('turf1/hco')

TURF_2_ID = 2
TURF_2_GANG = GlobalStat('turf2/gang')
TURF_2_HELD_FOR = GlobalStat('turf2/held')
TURF_2_HP = GlobalStat('turf2/hp')
TURF_2_MAX_HP = GlobalStat('turf2/mhp')
TURF_2_FUNDS = GlobalStat('turf2/funds')
TURF_2_FUNDS_PER_SECOND = GlobalStat('turf2/af')
TURF_2_HIT_COOLDOWN = GlobalStat('turf2/hco')

TURF_3_ID = 3
TURF_3_GANG = GlobalStat('turf3/gang')
TURF_3_HELD_FOR = GlobalStat('turf3/held')
TURF_3_HP = GlobalStat('turf3/hp')
TURF_3_MAX_HP = GlobalStat('turf3/mhp')
TURF_3_FUNDS = GlobalStat('turf3/funds')
TURF_3_FUNDS_PER_SECOND = GlobalStat('turf3/af')
TURF_3_HIT_COOLDOWN = GlobalStat('turf3/hco')

EMPTY_TURF_ID = 7
TURF_DEFAULT_MAX_HP = 100
TURF_HP_PER_PRESTIGE = 10

LATEST_DEATH_TIME = GlobalStat('ld/time')
LATEST_DEATH_PLAYER_ID = GlobalStat('ld/pid')
LATEST_DEATH_GANG = GlobalStat('ld/gang')
LATEST_DEATH_WAS_LEADER = GlobalStat('ld/wasl')
LATEST_DEATH_FUNDS = GlobalStat('ld/funds')
LATEST_DEATH_CRED = GlobalStat('ld/cred')

GLOBAL_DISPLAY_ARG_1 = GlobalStat('dp/arg1')
GLOBAL_DISPLAY_ARG_2 = GlobalStat('dp/arg2')
GLOBAL_DISPLAY_ARG_3 = GlobalStat('dp/arg3')
GLOBAL_DISPLAY_ARG_4 = GlobalStat('dp/arg4')
GLOBAL_DISPLAY_ARG_5 = GlobalStat('dp/arg5')
GLOBAL_DISPLAY_ARG_6 = GlobalStat('dp/arg6')

PAYOUT_GANG = GlobalStat('po/gang')
PAYOUT_WHOLE = GlobalStat('po/whole')
PAYOUT_REST = GlobalStat('po/rest')


PLAYER_ID = PlayerStat('id')
PLAYER_GANG = PlayerStat('gang')
PLAYER_CRED = PlayerStat('cred')
PLAYER_FUNDS = PlayerStat('funds')

PLAYER_POWER = PlayerStat('power')
PLAYER_MAX_POWER = PlayerStat('maxpower')

PLAYER_MINING_SPEED = PlayerStat('minespeed')
PLAYER_FORAGING_SPEED = PlayerStat('foraspeed')

PLAYER_MINING_FORTUNE = PlayerStat('minefortune')
PLAYER_FARMING_FORTUNE = PlayerStat('farmfortune')
PLAYER_FORAGING_FORTUNE = PlayerStat('forafortune')

PLAYER_DAMAGE = PlayerStat('damage')

DISPLAY_ID = PlayerStat('dp/id')
DISPLAY_TIMER = PlayerStat('dp/timer')
DISPLAY_ARG_1 = PlayerStat('dp/arg1')
DISPLAY_ARG_2 = PlayerStat('dp/arg2')
DISPLAY_ARG_3 = PlayerStat('dp/arg3')

LOCATION_ID = PlayerStat('locationid')
BIG_LOCATION_ID = PlayerStat('blocationid')
BIGGEST_LOCATION_ID = PlayerStat('bblocationid')

PREVIOUS_LOCATION_ID = PlayerStat('plocationid')


TEAM_ID = TeamStat('id')
TEAM_LEADER_ID = TeamStat('leaderid')


TURF_FUNDS_PER_SECOND_MAPPING: dict[int, int] = {
    TURF_1_ID: 3,
    TURF_2_ID: 2,
    TURF_3_ID: 1,
}


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


SPAWN = (-0.5, 46, -40.5)
SPAWN_WITH_ROTATION = (-0.5, 46, -40.5, -180, 0)
IMPORTANT_MESSAGE_PREFIX = '&f[&a!&f] '
