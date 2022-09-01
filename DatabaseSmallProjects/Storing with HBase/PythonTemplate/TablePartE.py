import happybase as hb

connection = hb.Connection()
connection.open()
power_table=connection.table('powers')
# DON'T CHANGE THE PRINT FORMAT, WHICH IS THE OUTPUT
# OR YOU WON'T RECEIVE POINTS FROM THE GRADER

for key, data in power_table.scan(include_timestamp=True):
    print('Found: {}, {}'.format(key, data))

