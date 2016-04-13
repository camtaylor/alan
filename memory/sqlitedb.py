import sqlite3

sqlite_file = 'alan_db.sqlite'
text_type="TEXT"
table_name = "memory"

#Connect to DB
conn = sqlite3.connect(sqlite_file)
c = conn.cursor()


# Create SQLite table
c.execute("CREATE TABLE {tn} ({t1} UNIQUE, {t2}, {t3});"\
  .format(tn=table_name, t1="key", t2="raw", t3="prog"))

#Save
conn.commit()
conn.close()