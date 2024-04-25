from pyhtsl import PlayerStat, goto, IfAnd


goto('function', name='Some Function')
with IfAnd():
    for i in range(11):
        PlayerStat('foo').value = i
PlayerStat('bar').value += 1
