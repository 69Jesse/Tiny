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


class BaseTurf:
    ID: int
    DEFAULT_FUNDS_PER_SECOND: int
    GANG: GlobalStat
    HELD_FOR: GlobalStat
    HP: GlobalStat
    MAX_HP: GlobalStat
    FUNDS: GlobalStat
    FUNDS_PER_SECOND: GlobalStat
    HIT_COOLDOWN: GlobalStat
    HEAL_COOLDOWN: GlobalStat
    MEMBERS: GlobalStat


class Turf1(BaseTurf):
    ID = 1
    DEFAULT_FUNDS_PER_SECOND = 3
    GANG = GlobalStat('turf1/gang')
    HELD_FOR = GlobalStat('turf1/held')
    HP = GlobalStat('turf1/hp')
    MAX_HP = GlobalStat('turf1/mhp')
    FUNDS = GlobalStat('turf1/funds')
    FUNDS_PER_SECOND = GlobalStat('turf1/af')
    HIT_COOLDOWN = GlobalStat('turf1/hicd')
    HEAL_COOLDOWN = GlobalStat('turf1/hecd')
    MEMBERS = GlobalStat('turf1/members')

class Turf2(BaseTurf):
    ID = 2
    DEFAULT_FUNDS_PER_SECOND = 2
    GANG = GlobalStat('turf2/gang')
    HELD_FOR = GlobalStat('turf2/held')
    HP = GlobalStat('turf2/hp')
    MAX_HP = GlobalStat('turf2/mhp')
    FUNDS = GlobalStat('turf2/funds')
    FUNDS_PER_SECOND = GlobalStat('turf2/af')
    HIT_COOLDOWN = GlobalStat('turf2/hicd')
    HEAL_COOLDOWN = GlobalStat('turf2/hecd')
    MEMBERS = GlobalStat('turf2/members')

class Turf3(BaseTurf):
    ID = 3
    DEFAULT_FUNDS_PER_SECOND = 1
    GANG = GlobalStat('turf3/gang')
    HELD_FOR = GlobalStat('turf3/held')
    HP = GlobalStat('turf3/hp')
    MAX_HP = GlobalStat('turf3/mhp')
    FUNDS = GlobalStat('turf3/funds')
    FUNDS_PER_SECOND = GlobalStat('turf3/af')
    HIT_COOLDOWN = GlobalStat('turf3/hicd')
    HEAL_COOLDOWN = GlobalStat('turf3/hecd')
    MEMBERS = GlobalStat('turf3/members')


EMPTY_TURF_GANG = 7
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

TIP_COUNTER = GlobalStat('tipc')
TIP_INDEX = GlobalStat('tipm')


PLAYER_ID = PlayerStat('id')
PLAYER_GANG = PlayerStat('gang')
PLAYER_CRED = PlayerStat('cred')
PLAYER_FUNDS = PlayerStat('funds')
PLAYER_PRESTIGE = PlayerStat('prestige')

PLAYER_LAST_GANG = PlayerStat('lastgang')

PLAYER_POWER = PlayerStat('power')
PLAYER_MAX_POWER = PlayerStat('maxpower')

PLAYER_KILLS = PlayerStat('kills')
PLAYER_DEATHS = PlayerStat('deaths')
PLAYER_KILL_STREAK = PlayerStat('killstreak')
PLAYER_HIGHEST_KILL_STREAK = PlayerStat('higheststreak')

PLAYER_CURRENT_LEVEL = PlayerStat('currlvl')
PLAYER_CURRENT_XP = PlayerStat('currxp')
PLAYER_CURRENT_REQUIRED_XP = PlayerStat('creqxp')

PLAYER_GLOBAL_LEVEL = PlayerStat('globallevel')

PLAYER_MINING_SPEED = PlayerStat('minespeed')
PLAYER_FORAGING_SPEED = PlayerStat('foraspeed')

PLAYER_MINING_FORTUNE = PlayerStat('minefortune')
PLAYER_FARMING_FORTUNE = PlayerStat('farmfortune')
PLAYER_FORAGING_FORTUNE = PlayerStat('forafortune')

PLAYER_DAMAGE = PlayerStat('damage')

ADD_EXPERIENCE = PlayerStat('addxp')

DISPLAY_ID = PlayerStat('dp/id')
DISPLAY_TIMER = PlayerStat('dp/timer')
DISPLAY_ARG_1 = PlayerStat('dp/arg1')
DISPLAY_ARG_2 = PlayerStat('dp/arg2')
DISPLAY_ARG_3 = PlayerStat('dp/arg3')

LOCATION_ID = PlayerStat('locationid')
BIG_LOCATION_ID = PlayerStat('blocationid')
BIGGEST_LOCATION_ID = PlayerStat('bblocationid')

PREVIOUS_LOCATION_ID = PlayerStat('plocationid')

PLAYTIME_SECONDS = PlayerStat('playtime')

SEND_TO_SPAWN_COUNTER = PlayerStat('stspawnc')


PREVIOUS_COORDINATE_X = PlayerStat('pcoordx')
PREVIOUS_COORDINATE_Y = PlayerStat('pcoordy')
PREVIOUS_COORDINATE_Z = PlayerStat('pcoordz')

TELEPORTING_ID = PlayerStat('tpid')
TELEPORTING_TIMER = PlayerStat('tptimer')


SPEED_EFFECT_TIMER = PlayerStat('et/spe')
RESISTANCE_EFFECT_TIMER = PlayerStat('et/res')
REGENERATION_EFFECT_TIMER = PlayerStat('et/reg')
JUMPBOOST_EFFECT_TIMER = PlayerStat('et/jum')
INVISIBILITY_EFFECT_TIMER = PlayerStat('et/inv')


NEW_DESIRED_GANG_ID = PlayerStat('ndgid')


COMBAT_TIMER = PlayerStat('ctimer')


DAILY_RESET_LAST_DAY = PlayerStat('drlastday')

DAILY_FREE_SWITCHES = PlayerStat('dfswitches')


TEAM_ID = TeamStat('id')
leader_id_key = 'leaderid'
leader_is_wearing_crown_key = 'leaderisc'
leader_not_worn_timer_key = 'leadernwt'
TEAM_LEADER_ID = TeamStat(leader_id_key)


class GangSimTeam:
    TEAM: Team
    LEVEL: PlayerStat
    EXPERIENCE: PlayerStat
    REQUIRED_EXPERIENCE: PlayerStat
    ID: int

    @classmethod
    def name(cls) -> str:
        return cls.__name__.removesuffix('Team')


class GangSimGang(GangSimTeam):
    LEADER_ID: TeamStat
    LEADER_IS_WEARING_CROWN: TeamStat
    LEADER_NOT_WORN_TIMER: TeamStat


TEAM_LEADER_ID = TeamStat(leader_id_key)
TEAM_LEADER_IS_WEARING_CROWN = TeamStat(leader_is_wearing_crown_key)
TEAM_LEADER_NOT_WORN_TIMER = TeamStat(leader_not_worn_timer_key)


class Bloods(GangSimGang):
    TEAM = Team('BLOOD')
    LEVEL = PlayerStat('bloodlevel')
    EXPERIENCE = PlayerStat('b/xp')
    REQUIRED_EXPERIENCE = PlayerStat('b/xpr')
    ID = 4
    LEADER_ID = TeamStat(leader_id_key, TEAM)
    LEADER_IS_WEARING_CROWN = TeamStat(leader_is_wearing_crown_key, TEAM)
    LEADER_NOT_WORN_TIMER = TeamStat(leader_not_worn_timer_key, TEAM)


class Crips(GangSimGang):
    TEAM = Team('CRIP')
    LEVEL = PlayerStat('criplevel')
    EXPERIENCE = PlayerStat('c/xp')
    REQUIRED_EXPERIENCE = PlayerStat('c/xpr')
    ID = 9
    LEADER_ID = TeamStat(leader_id_key, TEAM)
    LEADER_IS_WEARING_CROWN = TeamStat(leader_is_wearing_crown_key, TEAM)
    LEADER_NOT_WORN_TIMER = TeamStat(leader_not_worn_timer_key, TEAM)


class Kings(GangSimGang):
    TEAM = Team('KING')
    LEVEL = PlayerStat('kinglevel')
    EXPERIENCE = PlayerStat('k/xp')
    REQUIRED_EXPERIENCE = PlayerStat('k/xpr')
    ID = 6
    LEADER_ID = TeamStat(leader_id_key, TEAM)
    LEADER_IS_WEARING_CROWN = TeamStat(leader_is_wearing_crown_key, TEAM)
    LEADER_NOT_WORN_TIMER = TeamStat(leader_not_worn_timer_key, TEAM)


class Grapes(GangSimGang):
    TEAM = Team('GRAPE')
    LEVEL = PlayerStat('grapelevel')
    EXPERIENCE = PlayerStat('g/xp')
    REQUIRED_EXPERIENCE = PlayerStat('g/xpr')
    ID = 5
    LEADER_ID = TeamStat(leader_id_key, TEAM)
    LEADER_IS_WEARING_CROWN = TeamStat(leader_is_wearing_crown_key, TEAM)
    LEADER_NOT_WORN_TIMER = TeamStat(leader_not_worn_timer_key, TEAM)


class SpawnTeam(GangSimTeam):
    TEAM = Team('SPAWN')
    LEVEL = PlayerStat('spawnlevel')
    EXPERIENCE = PlayerStat('s/xp')
    REQUIRED_EXPERIENCE = PlayerStat('s/xpr')
    ID = EMPTY_TURF_GANG


ALL_TEAMS = (
    Bloods, Crips, Kings, Grapes, SpawnTeam,
)


ALL_GANG_TEAMS: tuple[type[GangSimGang], ...] = (
    Bloods, Crips, Kings, Grapes,
)


IMPORTANT_MESSAGE_PREFIX = '&f[&a!&f] '


def seconds_to_every_4_ticks(seconds: int) -> int:
    return seconds * 5
