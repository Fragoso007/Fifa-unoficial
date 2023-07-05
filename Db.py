import mysql.connector
from mysql.connector import errorcode

print("Conecting...")
try:
      conn = mysql.connector.connect(
            host='127.0.0.1',
            user='root',
            password='1994Fragoso'
      )
except mysql.connector.Error as err:
      if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print('There is something wrong with the username or password')
      else:
            print(err)

cursor = conn.cursor()

cursor.execute("DROP DATABASE IF EXISTS `Read`;")

cursor.execute("CREATE DATABASE `Read`;")

cursor.execute("USE `Read`;")

# creating tables
TABLES = {}
TABLES['players'] = ('''
      CREATE TABLE `players` (
      `id` int(11) NOT NULL AUTO_INCREMENT,
      `name` varchar(50) NOT NULL,
      `nationality` varchar(40) NOT NULL,
      `team` varchar(50) NOT NULL,
      `tshirt` varchar(3) NOT NULL,
      PRIMARY KEY (`id`)
      ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;''')

TABLES['Users'] = ('''
      CREATE TABLE `users` (
      `name` varchar(50) NOT NULL,
      `nickname` varchar(20) NOT NULL,
      `password` varchar(100) NOT NULL,
      PRIMARY KEY (`nickname`)
      ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;''')

for table_name in TABLES:
      table_sql = TABLES[table_name]
      try:
            print('Creating table {}:'.format(table_name), end=' ')
            cursor.execute(table_sql)
      except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                  print('Already exists')
            else:
                  print(err.msg)
      else:
            print('OK')

# inserting users
user_sql = 'INSERT INTO users (name, nickname, password) VALUES (%s, %s, %s)'
user = [
      ("Alvis Haal", "Alvis", "2023"),
      ("Camila Ferreira", "Mila", "paozinho"),
      ("Antonio Fragoso", "Fragoso", "1994")
]
cursor.executemany(user_sql, user)

cursor.execute('select * from Read.users')
print(' -------------  Users:  -------------')
for user in cursor.fetchall():
    print(user[1])

# inserting players
players_sql = 'INSERT INTO players (name, nationality, team, tshirt) VALUES (%s, %s, %s, %s)'
players = [
      ('Cristiano Ronaldo', 'Portugal', 'Real Madrid', '7'),
      ('Leonel Messi', 'Argentina', 'Barcelona', '10'),
      ('Kyllian Mbape', 'Franca', 'PSG', '7')
]
cursor.executemany(players_sql, players)

cursor.execute('select * from Read.players')
print(' -------------  players:  -------------')
for players in cursor.fetchall():
    print(players[1])

# committing if not nothing takes effect
conn.commit()

cursor.close()
conn.close()