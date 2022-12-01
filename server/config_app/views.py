import os
from django.core.handlers.wsgi import WSGIRequest
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from config_app.models import User
from db.connection import connect_db
from db.settings import setting

connection = connect_db()
file_path = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))

if not os.path.isfile(f"{file_path}/db/setting"):
    setting(connection)
    f = open(f"{file_path}/db/setting", "w")
    f.write("This file is for checking whether it is set or not")
    f.close()
connection.select_db("games")

def index(request: WSGIRequest) -> JsonResponse:
    if request.method == "GET":
        print(User.check_exist_user(connection, "asdasd"))
        return JsonResponse({"message": "get success"}, status=200)
    
    elif request.method == "POST":
        return JsonResponse({"message": "post success"}, status=200)
    
    else:
        return JsonResponse({"message": "else success"}, status=200)   
    
    
def profile(request: WSGIRequest) -> JsonResponse:    
    if request.method == "GET":
        try:
            id = request.GET["id"]
            user = User.load_user(connection, id)
            
            return JsonResponse({f"user_no{user.user_no}" : f"{user}"}, status=200)
        
        except:
            return JsonResponse({"message": "data required"}, status=428)
    
    else:
        return JsonResponse({"message": "method error"}, status=405)
    

@method_decorator(csrf_exempt, name="dispatch")
def check_user(request: WSGIRequest) -> JsonResponse:
    if request.method == "POST":
        try:
            id = request.POST["id"]

            return {
                False: JsonResponse({"message": "not exist"}, status=200),
                True: JsonResponse({"message": "exist"}, status=409)
            } [User.check_exist_user(connection, id)]
            
        except:
            return JsonResponse({"message": "data required"}, status=428)
        
    else:
        return JsonResponse({"message": "method error"}, status=405)
        

@method_decorator(csrf_exempt, name="dispatch")
def check_nickname(request: WSGIRequest) -> JsonResponse:
    if request.method == "POST":
        try:
            nickname = request.POST["nickname"]

            return {
                False: JsonResponse({"message": "not exist"}, status=200),
                True: JsonResponse({"message": "exist"}, status=409)
            } [User.check_exist_nickname(connection, nickname)]
            
        except:
            return JsonResponse({"message": "data required"}, status=428)
        
    else:
        return JsonResponse({"message": "method error"}, status=405)


@method_decorator(csrf_exempt, name="dispatch")
def login(request: WSGIRequest) -> JsonResponse:
    if request.method == "POST":
        try:
            id = request.POST["id"]
            pwd = request.POST["pwd"]
            
            print(f"detected : {type(id)}, {pwd}")
            
            cursor = connection.cursor()
            cursor.execute(f"SELECT * FROM user WHERE id = '{id}';")
            result = cursor.fetchall()
            cursor.close()
            if result is ():
                return JsonResponse({"message": "fail"}, status=401)
            user = User(*result[0])
            
            if user.login(connection, pwd):
                request.session["check_login"] = user.id
                return JsonResponse({"message": "success"}, status=200)

            else:
                return JsonResponse({"message": "fail"}, status=401)
            
        except:
            return JsonResponse({"message": "data required"}, status=428)
    
          
    else:
        return JsonResponse({"message": "method error"}, status=405)
    

@method_decorator(csrf_exempt, name="dispatch")
def signup(request: WSGIRequest) -> JsonResponse:
    if request.method == "POST":
        try:
            id = request.POST["id"]
            nickname = request.POST["nickname"]
            pwd = request.POST["pwd"]
            email = request.POST["email"]
            phone = request.POST["phone"]
            
            return {
                True: JsonResponse({"message": "success"}, status=200),
                False: JsonResponse({"message": "fail"}, status=401)
            } [User.insert_user(connection, User(id=id, nickname=nickname, pwd=pwd, email=email, phone=phone))]
            
        except:
            return JsonResponse({"message": "data required"}, status=428)
        
    else:
        return JsonResponse({"message": "method error"}, status=405)
    
    
@method_decorator(csrf_exempt, name="dispatch")
def update_nickname(request: WSGIRequest) -> JsonResponse:
    if request.method == "POST":
        try:
            id = request.POST["id"]
            nickname = request.POST["nickname"]
            
            if request.session.get("check_login") is None:
                return JsonResponse({"message": "session has timed out"}, status=403)
            
            if request.session.get("check_login") != id:
                return JsonResponse({"message": "access denied"}, status=403)

            user = User.load_user(connection, id)
            
            if user.nickname == nickname:
                return JsonResponse({"message": "same nickname"}, status=401)
            
            return {
                True: JsonResponse({"message": "success"}, status=200),
                False: JsonResponse({"message": "nickname already exist"}, status=401)
            } [user.update_nickname(connection, nickname)]
        
        except:
            return JsonResponse({"message": "data required"}, status=428)
        
    else:
        return JsonResponse({"message": "method error"}, status=405)


@method_decorator(csrf_exempt, name="dispatch")
def update_email(request: WSGIRequest) -> JsonResponse:
    if request.method == "POST":
        try:
            id = request.POST["id"]
            email = request.POST["email"]
            user = User.load_user(connection, id)
            print(user)
            
            if request.session.get("check_login") is None:
                return JsonResponse({"message": "session has timed out"}, status=403)
            
            if request.session.get("check_login") != id:
                return JsonResponse({"message": "access denied"}, status=403)
            
            if user.email == email:
                return JsonResponse({"message": "same email"}, status=401)
            
            return {
                True: JsonResponse({"message": "success"}, status=200),
                False: JsonResponse({"message": "fail"}, status=401)
            } [user.update_email(connection, email)]
        
        except:
            return JsonResponse({"message": "data required"}, status=428)
        
    else:
        return JsonResponse({"message": "method error"}, status=405)
    
    
@method_decorator(csrf_exempt, name="dispatch")
def update_phone(request: WSGIRequest) -> JsonResponse:
    if request.method == "POST":
        try:
            id = request.POST["id"]
            phone = request.POST["phone"]
            user = User.load_user(connection, id)
            
            if request.session.get("check_login") is None:
                return JsonResponse({"message": "session has timed out"}, status=403)   
            
            if request.session.get("check_login") != id:
                return JsonResponse({"message": "access denied"}, status=403)
            
            if user.phone == phone:
                return JsonResponse({"message": "same phone"}, status=401)
            
            return {
                True: JsonResponse({"message": "success"}, status=200),
                False: JsonResponse({"message": "fail"}, status=401)
            } [user.update_phone(connection, phone)]
        
        except:
            return JsonResponse({"message": "data required"}, status=428)
            
    else:
        return JsonResponse({"message": "method error"}, status=405)
    

@method_decorator(csrf_exempt, name="dispatch")
def delete_user(request: WSGIRequest) -> JsonResponse:
    if request.method == "POST":
        try:
            id = request.POST["id"]
            pwd = request.POST["pwd"]
            
            if request.session.get("check_login") is None:
                return JsonResponse({"message": "session has timed out"}, status=403)   
            
            if request.session.get("check_login") != id:
                return JsonResponse({"message": "access denied"}, status=403)
            
            user = User.load_user(connection, id)
            
            if user.login(connection, pwd):
                User.delete_user(connection, id)
                return JsonResponse({"message": "success"}, status=200)
            
            else:
                return JsonResponse({"message": "wrong password"}, status=401)
            
        except:
            return JsonResponse({"message": "data required"}, status=428)
        
    else:
        return JsonResponse({"message": "method error"}, status=405)