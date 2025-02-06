import mysql.connector as ms
from mysql.connector import errorcode
from Utils import *
from config import *

# Error Handling for Wrong Password and DB doesnt not exist error

while True:
    try:
        con = ms.connect(host='localhost', username=USER, passwd=PASSWORD, database=DATABASE)

    except ms.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("[*] Error: Incorrect Login Credentials")
            print(f'[*] Password updated to `{PASSWORD}`')
            print('[*] Trying again')
            continue

        if err.errno == errorcode.ER_BAD_DB_ERROR:
            print("[*] Error: Database does not exist")
            print(f'[*] Creating Database `{DATABASE}`')

            con = ms.connect(host='localhost', username=USER, passwd=PASSWORD)
            c = con.cursor()
            c.execute(f'create database if not exists {DATABASE};')

            print(f'[*] {DATABASE} created...')
            continue

        else:
            print(f"[*] Error {err.errno}: {err.msg}")
            exit()
    else:
        break

# cursor object
c = con.cursor()

# schema of tables
user_details = ('user_details', {'id': 'int primary key auto_increment', 'name': 'varchar(20)', 'age': 'int',
                 'username': 'varchar(15) unique', 'password': 'varchar(70)'})

user_stats = ('user_stats', {'userid': f'int, foreign key(userid) references {user_details[0]}(id)', 'highscore_nWPM': 'float',
               'highscore_gWPM': 'float', "highscore_time": 'float', "average_WPM": 'float', "average_time": 'float',
               "average_accuracy": 'float'})

games = ('games', {'gameid': 'int primary key auto_increment',
          'userid': f'int, foreign key(userid) references {user_details[0]}(id)',
          'string': 'varchar(150)', 'userinput': 'varchar(150)', 'timetaken': 'float', 'netWPM': 'float',
          'grossWPM': 'float', 'accuracy': 'float', 'error': 'int'})

#word_list = ('word_list', {'word': 'varchar(20)'})

def query(query):
    """Function to run sql query quick"""
    c.execute(query)
    if [True for x in ('insert', 'update') if x in query]:
        con.commit()
    return c.fetchall()


def create_table(name, attr):
    """Create table using given table structure"""
    attributes = ""
    for i in attr:
        attributes += f"{i} {attr[i]}, "

    query = f'create table if not exists {name} ({attributes[:-2]});'
    c.execute(query)
    print(f"[*] Created table `{name}`")


def on_start_setup():
    """setting up environment on first launch"""
    existing_tables = [tablename[0] for tablename in query('show tables;')]
    # print(existing_tables)

    create_table(user_details[0], user_details[1]) if user_details[0] not in existing_tables else None
    create_table(user_stats[0], user_stats[1]) if user_stats[0] not in existing_tables else None
    create_table(games[0], games[1]) if games[0] not in existing_tables else None


def reset():
    """function to reset environment"""
    c.execute(f'drop table {user_stats[0]}')
    c.execute(f'drop table {games[0]}')
    c.execute(f'drop table {user_details[0]}')
    c.execute(f'drop database {DATABASE}')
    # on_start_setup()


def insert_data(table_name, data, headers):
    """insert data into provided table"""

    query = ''
    if len(headers) > 1:
        query = f"insert into {table_name} ({(','.join(headers))}) values {data}"
    elif len(headers) == 1 or len(data) == 1:
        query = f"insert into {table_name} ({(','.join(headers))}) values ('{data}')"

    query = query.replace("'NULL'", "NULL")
    c.execute(query)
    con.commit()


def create_user(data):
    """create new user"""
    data = data[:-1] + (hash(data[-1]),)
    insert_data(user_details[0], data, tuple(user_details[1].keys())[1:])

    last_user = get_all_data(user_details[0])[-1]

    insert_data(user_stats[0], (last_user[0], 'NULL', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL', ), tuple(user_stats[1].keys()))


def update_user_data(username,data):

    """update user stats"""
    members = query(f'select id, username from {user_details[0]};')
    members = {user[1]:user[0] for user in members}

    if username in members.keys():
        user_stats_data = query(f'select * from {user_stats[0]} where userid={members[username]};')[0]

        # print(user_stats)

        headers=tuple(games[1].keys())[1:]

        insert_data('games', (members[username],)+data, headers)


        values = [
        f'highscore_nWPM={data[3]}' if user_stats_data[1] is None or data[3] > user_stats_data[1] else f'highscore_nWPM={user_stats_data[1]}',
        f'highscore_gWPM={data[4]}' if user_stats_data[2] is None or data[4] > user_stats_data[2] else f'highscore_gWPM={user_stats_data[2]}',
        f'highscore_time={data[2]}' if user_stats_data[3] is None or data[2] < user_stats_data[3] else f'highscore_time={user_stats_data[3]}',
        f'''average_WPM={average([game[0] for game in query(f"select netWPM from games where userid ='{members[username]}'")])}''',
        f'''average_accuracy={average([game[0] for game in query(f"select accuracy from games where userid ='{members[username]}'")])}''',
        f'''average_time={average([game[0] for game in query(f"select timetaken from games where userid ='{members[username]}'")])}'''
        ]

        update_user_stats= f'''update {user_stats[0]} set {','.join(values)} where userid = {members[username]};'''
        query(update_user_stats)


def view_records(username):
    """view users stats and previous games in table form along with graph"""
    userid = get_user_id(username)
    games = query(f'select userinput,netWPM,grossWPM,timetaken,accuracy,error from games where userid = {userid}')
    stats = query(f'select max(netWPM),max(grossWPM),min(timetaken),round(avg(netWPM)),round(avg(timetaken),1),round(avg(accuracy),1),count(*) from games where userid = {userid}')


    if not games:
        null_data = ('-'.center(30), ' - ', ' - ', ' - ', ' - ', ' - ')
        games.append(null_data)

    headers = ('user input',  'net wpm', 'gross wpm', 'time taken', 'accuracy', 'errors')
    data = [{headers[i]: attr for i, attr in enumerate(row)} for row in games]


    stats = stats[0]

    if stats[6] > 5:
        print(render_graph([game[1] for game in games], {'height': 10, 'offset': 5}))

    print(f'''
           Best Net-WPM : {'%4s' %stats[0]}      Best Gross-WPM : {'%4s' %stats[1]}         Best Time    : {'%4s' %stats[2]}{'s' if stats[2] is not None else ''}
        Average Net-WPM : {'%4s' % stats[3]}        Average Time  : {'%4s' % stats[4]}{'s' if stats[4] is not None else ''}     Average Accuracy : {'%5s' %stats[5]}{'%' if stats[5] is not None else ''}
            Total Games : {str(stats[6]).ljust(7)}
    ''')

    print(render_table(headers, data))


def view_leaderboard(key='highscore_nWPM'):
    """View leaderboard of best players in table form"""

    q = f'''select username,round(highscore_nWPM,1),round(highscore_gWPM,1),round(highscore_time,1),round(average_WPM,1), round(average_time,1),round(average_accuracy,1)
    from {user_stats[0]} as b, {user_details[0]} as a where b.userid = a.id order by {key} {'DESC' if 'time' not in key else 'ASC'} ;'''

    leaderboard = query(q)

    print(f"\n\tSorted By {key+' (↑)' if 'time' not in key else key+' (↓)'}\n")

    headers = ('username', 'highscore NET WPM', 'Highscore gross WPM', 'Best Time', 'AVG wpm', 'avg time', 'avg accuracy')
    data = [{headers[i]: attr for i, attr in enumerate(row)} for row in leaderboard]

    print(render_table(headers, data))


def get_user_id(username):
    """get user_id using username"""
    userid = query(f'select id from {user_details[0]} where username="{username}"')

    if not userid:
        return False

    return int(userid[0][0])


def get_user_details(username):
    """get all user details"""
    creds = query(f"select id,username,password,name from {user_details[0]} where username='{username}';")

    if not creds:
        return False

    return creds[0]


def get_all_data(table_name):
    """get all data from given table"""
    c.execute(f'select * from {table_name}')
    return c.fetchall()


def delete_record(key, table='games'):

    field, value = key
    query = f"delete from {table} where {field}={value};"
    c.execute(query)
    con.commit()


on_start_setup()

if __name__ == '__main__':

    print("[*] resetting env")
    reset()
    # on_start_setup()

    # -----Used during developement----- #

    # delete_record(('gameid',5))

   #';update user_stats set highscore_nWPM=0,highscore_gWPM=0 --

    # data = ('Joe Byjo', 18, 'joe', '1234')
    # data = ('xyz', 19, 'xyz', '1234')
    # create_user(data)

    # insert_data('user_details', ('Guest', 17, 'guest', hash('1234')), tuple(user_details.keys())[1:])
    # insert_data('user_stats', (1, 20, 20, 20, 20, 20, 20), tuple(user_stats.keys()))

    # print(create_user(('Guest', 17, 'guest', hash('1234'))))

    # print(get_all_data('user_stats'))
    # update_user_data('joe',(20,23,2.3))

    # print(get_user_id('asda'))
    # print(login('joe'))

    # print(view_records('joe'))
    # print(view_leaderboard('highscore_time'))