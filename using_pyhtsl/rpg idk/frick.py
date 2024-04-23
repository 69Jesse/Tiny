from pyhtsl import PlayerStat, goto, IfAnd


goto('function', 'Test')
for _ in range(20):
    with IfAnd():
        pass
for i in range(1, 101):
    PlayerStat('foo').value = i
