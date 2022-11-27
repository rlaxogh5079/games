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
                `user_no`	INT	NOT NULL AUTO_INCREMENT,
                `id`	VARCHAR(15)	NOT NULL,
                `nickname`	TEXT	NOT NULL,
                `pwd`	VARCHAR(60)	NOT NULL,
                `email`	TEXT	NOT NULL,
                `phone`	VARCHAR(13)	NOT NULL,
                `create_time`	DATETIME    DEFAULT NOW(),
                `last_time`	DATETIME	DEFAULT NOW(),
                `level`	INT	DEFAULT 1,
                `exp`	BIGINT	DEFAULT 0,
                `grade_no`	INT	NOT NULL
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
                `game_no`	INT	NOT NULL,
                `title`	TEXT	NOT NULL,
                `description`	TEXT	NULL	DEFAULT NULL,
                `diff_no`	INT	NOT NULL
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
                `game_no`	INT	NOT NULL,
                `user_no`	INT	NOT NULL,
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
                `diff_no`	INT	NOT NULL,
                `difficulty_name`	TEXT	NOT NULL
            );
        """)
        
        diff_list = ["매우 쉬움", "쉬움", "보통", "어려움", "매우 어려움"]
        for idx, diff in enumerate(diff_list):
            cursor.execute(
                f"INSERT INTO `difficulty` VALUES ({idx + 1}, '{diff}');"
            )
        cursor.close()

    except pymysql.err.ProgrammingError:
        raise pymysql.err.ProgrammingError("'diffciulty' table already exist")
    

def create_user_grade_table(connection: pymysql.connections.Connection) -> None:
    try:
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE `user_grade` (
                `grade_no`	INT	NOT NULL,
                `grade_name`	TEXT	NOT NULL
            );     
        """)
        
        user_grade_list = ["새내기", "2학년", "3학년", "4학년", "대학원생", "교수"]
        for idx, user_grade in enumerate(user_grade_list):
            cursor.execute(
                f"INSERT INTO `user_grade` VALUES ({idx + 1}, '{user_grade}');"
            )
        
        cursor.close()
        
    except pymysql.err.ProgrammingError:
        raise pymysql.err.ProgrammingError("'user_grade' table already exist")
    

def create_exp_table(connection: pymysql.connections.Connection) -> None:
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE `exp`(
            `level`	INT	NOT NULL,
            `exp`	INT NOT NULL
        )
    """)
    exp_list = hash_exp()
    for level in range(1, 60):
        cursor.execute(
            f"INSERT INTO exp VALUE ({level}, {exp_list[level - 1]})"
        )
    cursor.close()
    
    
def hash_exp() -> list:
    exp_list = list()
    exp_list.append(100)
    for level in range(2, 61):
        exp_list.append(randint(int(exp_list[level - 2] * 1.2), int(exp_list[level - 2] * 1.3)))
        
    return exp_list
        

def setting_key(connection: pymysql.connections.Connection) -> None:
    cursor = connection.cursor()
    cursor.execute("""
        ALTER TABLE `user` ADD CONSTRAINT `PK_USER` PRIMARY KEY (
            `id`
        );
    """)
    cursor.execute("""
        ALTER TABLE `game` ADD CONSTRAINT `PK_GAME` PRIMARY KEY (
	        `game_no`
        );
    """)
    cursor.execute("""
        ALTER TABLE `difficulty` ADD CONSTRAINT `PK_DIFFICULTY` PRIMARY KEY (
	        `diff_no`
        );
    """)
    cursor.execute("""
        ALTER TABLE `user_grade` ADD CONSTRAINT `PK_USER_GRADE` PRIMARY KEY (
	        `grade_no`
        );
    """)
    cursor.execute("""
        ALTER TABLE `exp` ADD CONSTRAINT `PK_EXP` PRIMARY KEY (
            `level`
        );
    """)
    cursor.close()


def setting(connection: pymysql.connections.Connection) -> None:
    if not check_exist_database(connection, "games"):
        create_database(connection)

    select_database(connection, "games")
    
    table_list = ["user", "game", "user_grade", "score", "difficulty", "exp"]

    for table in table_list:
        if not check_exist_table(connection, table):
            eval(f"create_{table}_table(connection)")
    
    setting_key(connection)

