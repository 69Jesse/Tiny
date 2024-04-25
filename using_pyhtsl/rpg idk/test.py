from pyhtsl import *  # You can import everything you need individually if you want

experience = PlayerStat('experience')
reward = PlayerStat('reward')
multiplier = PlayerStat('multiplier')
global_multiplier = GlobalStat('multiplier')

experience += reward * multiplier * global_multiplier
chat(f'&eYour EXP has been updated to &a{experience}&e!')

level = PlayerStat('level')
EXP_TO_LEVEL_UP = 100  # Python variable, ! not ! a stat

with IfAnd(experience >= EXP_TO_LEVEL_UP):
    experience -= EXP_TO_LEVEL_UP
    level += 1
    chat(f'&eYou leveled up to &dLevel {level}&e!')
with Else:
    chat(f'&eOnly &a{EXP_TO_LEVEL_UP - experience} EXP&e left to level up!')