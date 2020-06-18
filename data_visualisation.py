import mysql.connector as sqlcon
import pandas as pd

conn = sqlcon.connect(user = 'root', password = 'aybs1196', host = '127.0.0.1', database = 'py_vis')
query = 'SELECT * FROM plcmnt_stats'
cursor = conn.cursor()
cursor.execute(query)
plcmnt_records = cursor.fetchall()
plcmnt_records = pd.DataFrame(plcmnt_records)
colnames = list([i[0] for i in cursor.description])
plcmnt_records.columns = colnames
print(plcmnt_records)
cursor.close()
