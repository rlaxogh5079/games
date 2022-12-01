import bcrypt
import pymysql
from django.db import models
from datetime import datetime
from typing_extensions import Self

class User(models.Model):
    user_no = models.IntegerField(max_length = 1, db_index=True, unique=True)
    id = models.CharField(max_length = 15, primary_key=True)
    nickname = models.CharField(max_length = 15, unique=True)
    pwd = models.CharField(max_length = 60)
    email = models.TextField()
    phone = models.CharField(max_length = 13)
    create_time = models.TimeField()
    last_time = models.TimeField()
    level = models.IntegerField()
    exp = models.BigIntegerField()
    grade_no = models.IntegerField()
    
    
    def __init__(self, user_no: int = -1, id: str = "", nickname: str = "", pwd: str = "", email: str = "", phone: str = "", create_time: datetime = datetime.now(), last_time: datetime = datetime.now(), level: int = 1, exp: int = 0, grade_no: int = 1) -> None:
        self.user_no = user_no
        self.id = id
        self.nickname = nickname
        self.pwd = bcrypt.hashpw(pwd.encode("utf-8"), bcrypt.gensalt()).decode("utf-8") if len(pwd) != 60 and pwd != "" else pwd
        self.email = email
        self.phone = phone
        self.create_time = create_time
        self.last_time = last_time
        self.level = level
        self.exp = exp
        self.grade_no = grade_no
        
        
    def __str__(self) -> str:
        return f"""{{nickname: '{self.nickname}', email: '{self.email}', phone: '{self.phone}', create_time: '{self.create_time}', last_time: '{self.last_time}', level: {self.level}, exp: {self.exp}, grade_no: {self.grade_no}}}"""
    
    
    @staticmethod
    def check_exist_user(connection: pymysql.connections.Connection, id: str) -> bool:
        cursor = connection.cursor()
        cursor.execute(
            f"SELECT * FROM user WHERE id = '{id}';"
        )
        
        result = cursor.fetchall()
        
        return result != ()
    
    
    @staticmethod
    def check_exist_nickname(connection: pymysql.connections.Connection, nickname: str) -> bool:
        cursor = connection.cursor()
        cursor.execute(
            f"SELECT * FROM user WHERE nickname = '{nickname}';"
        )
        
        result = cursor.fetchall()
        
        return result != ()
    
    
    @staticmethod
    def load_user(connection: pymysql.connections.Connection, id: str) -> Self or None:
        cursor = connection.cursor()
        cursor.execute(
            f"SELECT * FROM user WHERE id = '{id}';"
        )
        
        result = cursor.fetchall()
        
        if result == ():
            return None
        
        return User(*result[0])
    
    
    @staticmethod
    def delete_user(connection: pymysql.connections.Connection, id: str) -> bool:
        try:
            cursor = connection.cursor()
            cursor.execute(
                f"DELETE FROM user WHERE id='{id}';"
            )
            
            cursor.execute(
                f"SELECT * FROM user WHERE id = '{id}';"
            )
            
            result = cursor.fetchall()
            connection.commit()
            cursor.close()
            
            return result == ()
                
        except pymysql.err.OperationalError:
            return False

    
    @staticmethod
    def insert_user(connection: pymysql.connections.Connection, user_info: Self) -> bool:
        try:
            cursor = connection.cursor()
            cursor.execute(f"""
                INSERT INTO user(id, nickname, pwd, email, phone) VALUES (
                "{user_info.id}", "{user_info.nickname}", "{user_info.pwd}", "{user_info.email}", "{user_info.phone}"
                );
            """)
            
            connection.commit()
            cursor.close()

        except pymysql.err.IntegrityError:
            print(pymysql.err.IntegrityError(f"'{user_info.id}' already exist"))
            return False
        
        return True
    
    
    def login(self, connection: pymysql.connections.Connection, pwd: str) -> bool:
        return bcrypt.checkpw(pwd.encode("utf-8"), User.load_user(connection, self.id).pwd.encode("utf-8"))
            
    
    def update_last_time(self, connection: pymysql.connections.Connection) -> None:
        try:
            now = datetime.now()
            cursor = connection.cursor()
            cursor.execute(
                f"UPDATE user SET last_time = '{now}' WHERE user_no={self.user_no};"
            )
            
            connection.commit()
            cursor.close()
            
        except:
            pass
        
        
    def update_exp(self, connection: pymysql.connections.Connection, exp: int) -> bool:
        try:
            cursor = connection.cursor()
            cursor.execute(
                f"SELECT level, exp FROM user WHERE user_no = {self.user_no};"
            )
            
            result = cursor.fetchall()
            user_level = result[0][0]
            user_exp = result[0][1] + exp
            
            cursor.execute(
                f"SELECT exp FROM exp WHERE level = {user_level};"
            )
            
            result = cursor.fetchall()
            required_exp = result[0][0]
            
            if user_exp > required_exp:
                user_exp -= required_exp
                user_level += 1
                grade_no = user_level % 10 + 1
                cursor.execute(
                    f"UPDATE user SET level = {user_level}, exp = {user_exp}, grade_no = {grade_no} WHERE user_no = {self.user_no};"
                )
                    
                connection.commit()
                cursor.close()  
                return True
            
            return False
            
        except:
            return False
        
        
    def update_nickname(self, connection: pymysql.connections.Connection, nickname: str) -> bool:
        try:
            cursor = connection.cursor()
            cursor.execute(
                f"UPDATE user SET nickname = '{nickname}' WHERE user_no = {self.user_no};"
            )
            connection.commit()
            cursor.close()

            return True
            
        except:
            return False
        
        
    def update_email(self, connection: pymysql.connections.Connection, email: str) -> bool:
        try:
            cursor = connection.cursor()
            cursor.execute(
                f"UPDATE user SET email = '{email}' WHERE user_no = {self.user_no};"
            )
            connection.commit()
            cursor.close()
            
            return True
        
        except:
            return False
        
        
    def update_phone(self, connection: pymysql.connections.Connection, phone: str) -> bool:
        try:
            cursor = connection.cursor()
            cursor.execute(
                f"UPDATE user SET phone = '{phone}' WHERE user_no = {self.user_no};"
            )
            connection.commit()
            cursor.close()
            
            return True
        
        except:
            return False

