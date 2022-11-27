import pymysql


def load_info() -> dict:
    try:
        f = open("db/user_info.txt", "r")

    except FileNotFoundError:
        raise FileNotFoundError("Don't Remove user_info.txt")

    lines = list(map(lambda x: x.replace("\n", ""), f.readlines()))
    keys, values = list(), list()

    for line in lines:
        split_line = list(map(lambda x: x.strip(), line.split("=")))
        if "" in split_line:
            raise ValueError("Please Enter Information on user_info.txt")
        
        keys.append(split_line[0])
        values.append(split_line[1])

    if len(keys) != len(values):
        raise IndexError("Please Match Keys And Values")
    
    must_info = ["host", "user", "password"]
    for info in must_info:
        if info not in keys:
            raise KeyError("Insufficient information entered")
    
    return {keys[i] : values[i] for i in range(len(keys))}


def connect_db() -> pymysql.connections.Connection:
    user_info = load_info()
    try:
        return pymysql.connect(
            **user_info
        )

    except pymysql.err.OperationalError:
        print(pymysql.err.OperationalError)
        raise pymysql.err.OperationalError("Database doesn't exist")
    
    except TypeError as err:
        argument = str(err).split("argument")[1].replace("'", "").strip()
        raise KeyError(f"Key '{argument}' doesn't exist")
