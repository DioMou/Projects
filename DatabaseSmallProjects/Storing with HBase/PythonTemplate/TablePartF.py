import happybase as hb

connection = hb.Connection()
connection.open()
power_table=connection.table('powers')
# DON'T CHANGE THE PRINT FORMAT, WHICH IS THE OUTPUT
# OR YOU WON'T RECEIVE POINTS FROM THE GRADER
i=0
for key1, data1 in power_table.scan():
    for key2, data2 in power_table.scan():
        if data1["custom:color".encode()]==data2["custom:color".encode()]and \
            data1["professional:name".encode()]!=data2["professional:name".encode()]:
            hero = data1["personal:hero".encode()]
            power = data1["personal:power".encode()]
            name = data1["professional:name".encode()]
            xp = data1["professional:xp".encode()]
            color = data1["custom:color".encode()]
            name2 = data2["professional:name".encode()]
            power2 = data2["personal:power".encode()]
            print('{}, {}, {}, {}, {}'.format(name, power, name2, power2, color))
            #print('{}, {}, {}, {}, {}'.format(hero, power, name, xp, color))
            #print('hero: {}, power: {}, name: {}, xp: {}, color: {}'.format(hero, power, name, xp, color))
            i+=1

# color = ???
# name = ???
# power = ???

# color1 = ???
# name1 = ???
# power1 = ???

#print('{}, {}, {}, {}, {}'.format(name, power, name1, power1, color))


