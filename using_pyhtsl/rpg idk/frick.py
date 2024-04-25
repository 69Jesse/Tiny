from pyhtsl import PlayerStat, IfAnd, goto


goto('function', 'Some Function')
with IfAnd():
    for i in range(1, 51):
        PlayerStat('foo').value = i
for i in range(1, 51):
    PlayerStat('bar').value = i
