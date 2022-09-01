import happybase as hb

connection = hb.Connection()
connection.open()


connection.create_table(
    'powers',
    {'personal': dict(max_versions=25),
     'professional': dict(max_versions=25),
     'custom': dict(max_versions=25),  # use defaults
    }
)
connection.create_table(
    'food',
    {'nutrition': dict(max_versions=25),
     'taste': dict(max_versions=25)
    }
)

#table = connection.table('powers')