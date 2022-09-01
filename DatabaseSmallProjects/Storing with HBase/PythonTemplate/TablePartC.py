import happybase as hb
import csv
#reference:https://gist.github.com/narulkargunjan/ab8d3b4905cb131e7613cd790b5e298d
connection = hb.Connection()
connection.open()
csv_path="./input.csv"
ufile=open(csv_path)
reader = csv.DictReader(ufile, fieldnames=['row_num','hero','power','name','xp','color'])
power_table=connection.table('powers')

i=0
for row in reader:
    #print(row)
    power_table.put(row["row_num"],{"personal:hero":row['hero'],"personal:power":row['power'],"professional:name":row['name'],\
    "professional:xp":row['xp'],"custom:color":row['color']})
#for key, data in power_table.scan():
#    print(key, data)