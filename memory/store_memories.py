import sqlite3
import os


sqlite_file = os.path.abspath('memory/memories.sqlite')
text_type="TEXT"
table_name = "MEMORY"

#Connect to DB
conn = sqlite3.connect(sqlite_file)
c = conn.cursor()


def store_task(key, raw_memory, coded_memory):
  """
    Function to store a task into memory.
    Tasks are learned procedures from the learning module.
  """
  query = "INSERT INTO {} (NAME,RAW,CODE) \
        VALUES ('{}', '{}', '{}')".format(table_name, key.lower(), raw_memory, coded_memory)
  try:
    c.execute(query)
    conn.commit()
  except Exception,e: print str(e)


def recall_all():
  c.execute("SELECT * FROM {}".format(table_name))
  print c.fetchall()


if __name__ == "__main__":

  """
    The main function creates the table if it run.
    TODO this should be moved to another function.
  """

  # Create SQLite table
  c.execute("CREATE TABLE {tn} ({t1} UNIQUE, {t2}, {t3});"\
    .format(tn=table_name, t1="NAME", t2="RAW", t3="CODE"))

  #Save
  conn.commit()
  conn.close()