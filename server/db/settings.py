import pymysql
from random import randint


def check_exist_database(connection: pymysql.connections.Connection, database: str) -> bool:
    cursor = connection.cursor()
    result = cursor.execute(f"SHOW databases LIKE '{database}';")
    cursor.close()

    return result != 0


def create_database(connection: pymysql.connections.Connection) -> None:
    try:
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE games;")
        cursor.close()

    except pymysql.err.ProgrammingError:
        raise pymysql.err.ProgrammingError("'games' Database already exist")


def check_selected_database(connection: pymysql.connections.Connection) -> bool:
    cursor = connection.cursor()
    cursor.execute(f"SELECT DATABASE() FROM DUAL;")
    result = cursor.fetchall()
    cursor.close()
    
    return result[0][0] is not None


def select_database(connection: pymysql.connections.Connection, database: str) -> None:
    if not check_selected_database(connection):
        connection.select_db(database)
    

def check_exist_table(connection: pymysql.connections.Connection, table: str) -> bool:
    cursor = connection.cursor()
    result = cursor.execute(f"SHOW TABLES LIKE '{table}';")
    cursor.close()

    return result != 0


def create_user_table(connection: pymysql.connections.Connection) -> None:
    try:
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE `user` (
                `user_no` INT UNSIGNED DEFAULT NULL AUTO_INCREMENT UNIQUE KEY,
                `id`	VARCHAR(15)	NOT NULL PRIMARY KEY,
                `nickname`	VARCHAR(15)	NOT NULL UNIQUE KEY ,
                `pwd`	VARCHAR(60)	NOT NULL,
                `email`	TEXT	NOT NULL,
                `phone`	VARCHAR(13)	NOT NULL,
                `create_time`	DATETIME    DEFAULT NOW(),
                `last_time`	DATETIME	DEFAULT NOW(),
                `level`	INT UNSIGNED	DEFAULT 1,
                `exp`	INT UNSIGNED	DEFAULT 0,
                `grade_no`	INT	UNSIGNED DEFAULT 1,
                INDEX (user_no)
            );
        """)
        cursor.close()

    except pymysql.err.ProgrammingError:
        raise pymysql.err.ProgrammingError("'user' table already exist")


def create_game_table(connection: pymysql.connections.Connection) -> None:
    try:
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE `game` (
                `game_no`	INT	UNSIGNED NOT NULL PRIMARY KEY,
                `title`	TEXT	NOT NULL,
                `description`	TEXT	NULL	DEFAULT NULL,
                `diff_no`	INT UNSIGNED	NOT NULL
            );
        """)
        cursor.close()

    except pymysql.err.ProgrammingError:
        raise pymysql.err.ProgrammingError("'game' table already exist")


def create_score_table(connection: pymysql.connections.Connection) -> None:
    try:
        cursor = connection.cursor()
        cursor.execute("""          
            CREATE TABLE `score` (
                `game_no`	INT UNSIGNED	NOT NULL,
                `user_no`	INT	UNSIGNED    NOT NULL,
                `score`	FLOAT	NOT NULL,
                `played_at`	DATETIME	NULL	DEFAULT NOW()
            );
        """)
        cursor.close()

    except pymysql.err.ProgrammingError:
        raise pymysql.err.ProgrammingError("'score' table already exist")


def create_difficulty_table(connection: pymysql.connections.Connection) -> None:
    try:
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE `difficulty` (
                `diff_no`	INT UNSIGNED NOT NULL PRIMARY KEY,
                `difficulty_name`	TEXT	NOT NULL
            );
        """)
        
        diff_list = ["매우 쉬움", "쉬움", "보통", "어려움", "매우 어려움"]
        for idx, diff in enumerate(diff_list):
            cursor.execute(
                f"INSERT INTO `difficulty` VALUES ({idx + 1}, '{diff}');"
            )
        connection.commit()
        cursor.close()

    except pymysql.err.ProgrammingError:
        raise pymysql.err.ProgrammingError("'diffciulty' table already exist")
    

def create_user_grade_table(connection: pymysql.connections.Connection) -> None:
    try:
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE `user_grade` (
                `grade_no`	INT	UNSIGNED NOT NULL PRIMARY KEY,
                `grade_name`	TEXT	NOT NULL
            );     
        """)
        
        user_grade_list = ["새내기", "2학년", "3학년", "4학년", "대학원생", "교수"]
        for idx, user_grade in enumerate(user_grade_list):
            cursor.execute(
                f"INSERT INTO `user_grade` VALUES ({idx + 1}, '{user_grade}');"
            )
        
        connection.commit()  
        cursor.close()
        
    except pymysql.err.ProgrammingError:
        raise pymysql.err.ProgrammingError("'user_grade' table already exist")
    

def create_exp_table(connection: pymysql.connections.Connection) -> None:
    try:
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE `exp`(
                `level`	INT	UNSIGNED NOT NULL PRIMARY KEY,
                `exp`	INT UNSIGNED NOT NULL
            );
        """)
        
        exp_list = hash_exp()
        for level in range(1, 60):
            cursor.execute(
                f"INSERT INTO `exp` VALUES ({level}, {exp_list[level - 1]});"
            )
            
        connection.commit()    
        cursor.close()
    
    except pymysql.err.ProgrammingError:
        raise pymysql.err.ProgrammingError("'exp' table already exist")
    
    
def hash_exp() -> list:
    exp_list = list()
    exp_list.append(100)
    for level in range(2, 61):
        exp_list.append(randint(int(exp_list[level - 2] * 1.2), int(exp_list[level - 2] * 1.3)))
        
    return exp_list
        

def setting(connection: pymysql.connections.Connection) -> None:
    if not check_exist_database(connection, "games"):
        create_database(connection)

    select_database(connection, "games")
    
    table_list = ["user", "game", "user_grade", "score", "difficulty", "exp"]

    for table in table_list:
        if not check_exist_table(connection, table):
            eval(f"create_{table}_table(connection)")

