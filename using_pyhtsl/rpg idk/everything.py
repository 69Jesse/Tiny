from pyhtsl import Team, GlobalStat


class Teams:
    __slots__ = ()
    combat = Team('Combat')
    mining = Team('Mining')
    farming = Team('Farming')
    fishing = Team('Fishing')


class GlobalStats:
    __slots__ = ()
    latest_cookies = GlobalStat('latest_cookies')
    cookie_goal = GlobalStat('cookie_goal')
    cookies_needed = GlobalStat('cookies_needed')
