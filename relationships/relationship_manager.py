import sqlite3
import os

"""

Relationships:
  ** Who Alan is and who he knows **
  Friends
    Name, pictures, contact info, relationship to another friend
  Alan
    Name, gender, language spoken, personality

Schema:
  Table 1: Faces
    - Name
    - File Path
  Table 2: Contact info
    - Name
    - Phone
    - Address
  Table 3: Alan
"""

sqlite_file = os.path.abspath('relationships/relationships.sqlite')
text_type="TEXT"
table_name = "RELATIONSHIP"

#Connect to DB
conn = sqlite3.connect(sqlite_file)
c = conn.cursor()

def database_exists():
  # Returns true if db is found
  return os.stat(sqlite_file).st_size > 0


def store_relationship(key, image):
  """
    Function to store a relationship.
  """
  query = "INSERT INTO {} (NAME,IMAGE) \
        VALUES ('{}', '{}')".format(table_name, key.lower(), image)
  try:
    c.execute(query)
    conn.commit()
  except Exception,e: print str(e)


def recall_all():
  """
    Function to simply print the whole relationship table.
  """
  c.execute("SELECT * FROM {}".format(table_name))
  print c.fetchall()


def recall_relationship(relationship_name):
  """
    Function to recall a certain relationship by NAME column in the relationship table.
  """
  c.execute("SELECT * FROM {} WHERE NAME = '{}'".format(table_name, relationship_name))
  return c.fetchall()


def init_db():
  """
    The main function creates the table if it run.
    TODO this should be moved to another function.
  """
  # Create SQLite table
  try:
    c.execute("CREATE TABLE {tn} ({t1} UNIQUE, {t2});"\
      .format(tn=table_name, t1="NAME", t2="IMAGE"))
  except Exception,e: print str(e)
  
  #Save
  conn.commit()
  
def close_db():
  conn.close()
  