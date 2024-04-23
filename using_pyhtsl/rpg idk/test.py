from pyhtsl import PlayerStat, goto


goto('function', name='Some Function')
for i in range(2000):
    PlayerStat('foo').value = i
