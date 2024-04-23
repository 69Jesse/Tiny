from pyhtsl import PlayerStat, goto, IfAnd, chat


goto('function', name='Some Function')
for i in range(2000):
    with IfAnd():
        chat('yo')
