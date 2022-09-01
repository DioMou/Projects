import happybase as hb

connection = hb.Connection()
connection.open()
power_table=connection.table('powers')
# DON'T CHANGE THE PRINT FORMAT, WHICH IS THE OUTPUT
# OR YOU WON'T RECEIVE POINTS FROM THE GRADER
row1=power_table.row('row1'.encode())

hero = row1["personal:hero".encode()]
power = row1["personal:power".encode()]
name = row1["professional:name".encode()]
xp = row1["professional:xp".encode()]
color = row1["custom:color".encode()]
print('hero: {}, power: {}, name: {}, xp: {}, color: {}'.format(hero, power, name, xp, color))

row19=power_table.row('row19'.encode())
hero = row19["personal:hero".encode()]
color = row19["custom:color".encode()]
print('hero: {}, color: {}'.format(hero, color))

row1_partial=power_table.row('row1'.encode())
hero = row1["personal:hero".encode()]
name = row1["professional:name".encode()]
color = row1["custom:color".encode()]
print('hero: {}, name: {}, color: {}'.format(hero, name, color))