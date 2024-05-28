from django.shortcuts import *
from .models import User,Product_Item,Feedback_Item,Custom_Item_I
from django.views.decorators.csrf import *
from django.http import HttpResponseBadRequest, JsonResponse
import telebot
import datetime

def send_message(message):
    bot = telebot.TeleBot('7106013224:AAG0k3sTngklHE5oYA8O42wyCDEc84w93Ys')
    chat_id = '-1002123715413'
    
    bot.send_message(chat_id,message)
# Create your views here.
def registration(request:HttpResponse):
    try:
        request.COOKIES["username"]
        return redirect("/shop/main/")
    except:
        if(request.method=="POST"):
            username=request.POST.get("username")
            email=request.POST.get("email")
            password=request.POST.get("password")
            if(len(username)>20 or len(password)>25 or len(email)>50):
                return render(request,"shop/registration.html",{'error':"Проверьте правильность заполнения полей!"})
            else:
                
                try:
                    user=User.objects.get(username=username)
                    return render(request,"shop/registration.html",{'error':"Такой пользователь уже существует!"})
                except:
                    user=User(username=username,password=password,email=email)
                    user.save()
                    responce=redirect("/shop/main/")
                    responce.set_cookie("username",username)
                    responce.set_cookie("email",email)
                    responce.set_cookie("password",password)
                    return responce
        return render(request,"shop/registration.html")

def login(request):
    try:
        request.COOKIES["username"]
        return redirect("/shop/main/")
    except:
        if(request.method=="POST"):
            username=request.POST.get("username")
            password=request.POST.get("password")
            try:
                user=User.objects.get(username=username,password=password)
                responce=redirect("/shop/main/")
                responce.set_cookie("username",username)
                responce.set_cookie("email",user.email)
                responce.set_cookie("password",password)
                return responce
            except:
                return render(request,"shop/login.html",{'error':"Неверный логин или пароль!"})
        return render(request,"shop/login.html")
            
@csrf_exempt
def main(request):
    try:
        request.COOKIES["username"]
        
        username=str(request.COOKIES["username"])

        feedbacks=None
        feedbacks_sort=[]


        if(request.method=="POST"):
            if "quit" in request.POST:
                print("x")
                responce=redirect("/shop/main/")
                responce.delete_cookie("username")
                responce.delete_cookie("email")
                responce.delete_cookie("password")
                return responce
            elif "action" in request.POST:
                action=str(request.POST.get("action"))
                if(action=="delete_feedback"):
                    header=str(request.POST.get("header"))
                    description=str(request.POST.get("description"))
                    username=str(request.POST.get("username"))
                    try:
                        feedback=Feedback_Item.objects.get(username=username,header=header,description=description)
                        feedback.delete()
                        

                        
                    except Exception as ex:
                        print(ex)
                else:
                    try:
                        raiting=int(request.POST.get("rating"))
                        header=str(request.POST.get("header"))
                        description=str(request.POST.get("description"))
                        username=str(request.COOKIES["username"])
                        date=datetime.datetime.now().date()
                        try:
                            feedback=Feedback_Item.objects.get(username=username,header=header,description=description)
                        except:
                            try:
                                feedbacks=Feedback_Item.objects.filter(username=username,date=date)
                                if(len(feedbacks)<2):
                                    feedback=Feedback_Item(rating=raiting,username=username,header=header,description=description,date=date)
                                    feedback.save()
                            except Exception as ex: 
                                print(ex)
                    except Exception as ex:
                            print(ex)
                    

            else:
                card_num=int(request.POST.get("card_num"))
                username=str(request.COOKIES["username"])
                try:
                    product=Product_Item.objects.get(username=username,card_num=card_num)
                    if(product.count<10):
                        product.count+=1
                        product.save()
                except:
                    product=Product_Item(username=username,card_num=card_num,count=1)
                    product.save()
        




        feedbacks=Feedback_Item.objects.all()
        feedbacks_sort=[]
        middle_rating=0
        count_rating=1
        for i in feedbacks:
            if(i.username==username and username!="admin"):
                feedbacks_sort.append(i)
                middle_rating+=i.rating
                count_rating+=1
            elif i.username!="admin":
                feedbacks_sort.insert(0,i)
                middle_rating+=i.rating
                count_rating+=1
        for i in feedbacks:
            if(i.username=="admin"):
                feedbacks_sort.append(i)

        user=""
        if username=="admin":
            user="True"
        if count_rating>1 : count_rating-=1
        
        return render(request,"shop/main.html",{"feedbacks":list(reversed(feedbacks_sort)),"rang":range(0,5),"user":user,"username":username,"middle_rating":str(middle_rating/count_rating)[:3].replace('.', ',')})

    except:
        return redirect("/")
    

def info(request):
    try:
        request.COOKIES["username"]
        if request.method=="POST":
            if "quit" in request.POST:
                    responce=redirect("/shop/main/")
                    responce.delete_cookie("username")
                    responce.delete_cookie("email")
                    responce.delete_cookie("password")
                    return responce
        return render(request,"shop/info.html")
    except:
        return redirect("/")
@csrf_exempt
def basket(request):
    try:
        request.COOKIES["username"]
        username=str(request.COOKIES["username"])
        try:
            config=[
                    {"header":"Простая\nРпг игра","img_url":"https://media.moddb.com/images/articles/1/240/239626/auto/ZdIh2QZ.png","count":1,"min_cost":48000,"max_cost":200000,"cost":"","card_num":1}
                    ,{"header":"Масштабная\nРпг игра","img_url":"https://img.ixbt.site/live/images/original/07/17/73/2023/07/29/7669dbb1e7.png","count":0,"min_cost":400000,"max_cost":8000000,"cost":"","card_num":2}
                    ,{"header":"Трендовая игра\nДля яндекс игр","img_url":"https://www.onlywhatsapps.com/games/thumbs/ch_1599121822.png","count":0,"min_cost":20000,"max_cost":50000,"cost":"","card_num":3}
                    ,{"header":"Простой онлайн\nШутер","img_url":"https://cubiq.ru/wp-content/uploads/2019/10/2-1.jpeg","count":0,"min_cost":55000,"max_cost":120000,"cost":"","card_num":4}
                    ,{"header":"AAA\nИгра","img_url":"https://images.hdqwalls.com/download/lawbreakers-gunslingers-game-5k-iy-2560x1600.jpg","count":0,"min_cost":1000000,"max_cost":100000000,"cost":"","card_num":5}
                    ,{"header":"Хоррор\nИгра","img_url":"https://www.bonusstage.co.uk/wp-content/uploads/2016/10/Weeping-Doll-Review-Screenshot-1.jpg","count":0,"min_cost":58000,"max_cost":800000,"cost":"","card_num":6}
                    ,{"header":"Визуальная\nНовелла","img_url":"https://i.ytimg.com/vi/y96QbpMtS8k/maxresdefault.jpg","count":0,"min_cost":20000,"max_cost":500000,"cost":"","card_num":7}
                    ,{"header":"Игра\nСимулятор","img_url":"https://m.media-amazon.com/images/I/91HaZRORviL.jpg","count":0,"min_cost":250000,"max_cost":3500000,"cost":"","card_num":8}
                    ,{"header":"Выложить игру в\nЯндекс игры","img_url":"https://habrastorage.org/getpro/habr/upload_files/149/00c/47a/14900c47ae4b78f349f5bc6f2718e52f.png","count":0,"min_cost":2000,"max_cost":10000,"cost":"","card_num":9}
                    ,{"header":"Выложить игру в\nSteam","img_url":"//avatars.mds.yandex.net/i?id=24d7866e15d72b5eac64144e73243814_l-5734612-images-thumbs&n=13","count":0,"min_cost":3000,"max_cost":10000,"cost":"","card_num":10}
                    ,{"header":"Игра\nСтратегия","img_url":"https://fonzon.club/uploads/posts/2022-12/1672023902_1-fonzon-club-p-strategii-bez-interneta-3.jpg","count":0,"min_cost":500000,"max_cost":10000000,"cost":"","card_num":11}
                    ,{"header":"Игра\nПлатформер","img_url":"https://gpstatic.com/acache/34/80/1/us/s9-2d76a10b2c0c5f83cc70284697696d88.jpg","count":0,"min_cost":200000,"max_cost":30000000,"cost":"","card_num":12}
            ]
            products_custom_person=Custom_Item_I.objects.filter(username=username)
            products_custom_person_final=[]
            genres={"sport":"Спортивная игра","race":"Гонки","card_game":"Карточная игра","open_world":"Игра с открытым миром","battle_royale":"Королевская битва","fiting":"Файтинг","interactive_cinema":"Интерактивное кино"}    
            for i in products_custom_person:
                i.game_genre=genres[i.game_genre]
                i.all_cost=str(separate_digits(i.all_cost*i.count))
                products_custom_person_final.insert(0,i)
            products_person=Product_Item.objects.filter(username=username)
            products=[]
            all_cost=0
            for product in products_person:
                config[product.card_num-1]["count"]=product.count
                config[product.card_num-1]["min_cost"]*=product.count
                config[product.card_num-1]["max_cost"]*=product.count
                config[product.card_num-1]["cost"]=separate_digits(int(config[product.card_num-1]["min_cost"]))
                products.insert(0,config[product.card_num-1])
                all_cost+=int((config[product.card_num-1]["min_cost"]))
            for i in products_custom_person_final:
                all_cost+=int(keep_digits_only(remove_spaces(i.all_cost)))
            product_count=len(products)+len(products_custom_person)

            if request.method=="POST":
                if "quit" in request.POST:
                    responce=redirect("/shop/main/")
                    responce.delete_cookie("username")
                    responce.delete_cookie("email")
                    responce.delete_cookie("password")
                    return responce
                else:
                    action=str(request.POST.get("action"))

                    if(action=='delete'):
                        card_num=int(request.POST.get("card_num_delete"))
                        object=Product_Item.objects.filter(username=username,card_num=card_num).delete()
                    elif(action=="delete_custom"):
                        all_cost_item=int(request.POST.get("all_cost"))
                        print(all_cost_item)
                        object=Custom_Item_I.objects.get(username=username,all_cost=all_cost_item).delete()
                    elif(action=="change_custom"):
                        all_cost_item=int(request.POST.get("all_cost"))
                        print(all_cost_item)
                        add=int(request.POST.get("add"))
                        object=Custom_Item_I.objects.get(username=username,all_cost=all_cost_item)
                        if(add==1):
                            if(object.count<10):
                                object.count+=1
                        else:
                            if(object.count>1):
                                object.count-=1
                            else:
                                object=Custom_Item_I.objects.filter(username=username,all_cost=all_cost_item).delete()
                        object.save()
                    elif(action=="send_info"):
                        telegram=add_at_symbol(str(request.POST.get("telegram")))
                        email=str(request.COOKIES["email"])
                        name=str(request.POST.get("name"))
                        second_name=str(request.POST.get("second_name"))

                        products_person_=Product_Item.objects.filter(username=username)
                        products_custom_person_=Custom_Item_I.objects.filter(username=username)
                        genres={"sport":"Спортивная игра","race":"Гонки","card_game":"Карточная игра","open_world":"Игра с открытым миром","battle_royale":"Королевская битва","fiting":"Файтинг","interactive_cinema":"Интерактивное кино"}    
                        for i in products_custom_person_:
                            i.game_genre=genres[i.game_genre]
                        products_=[]
                        for product in products_person_:
                            products_.insert(0,config[product.card_num-1])
                        products_text=""
                        for i in products_:
                            products_text+=f"   Название: \n        {remove_newlines(i['header'])}\n"
                            products_text+=f"       Количество: {i['count']} шт\n"
                            products_text+="---------------------------------\n"
                        products_text+="\n\n Кастомные игры:\n-----------------------------------------------------------\n"
                        for i in products_custom_person_:
                            products_text+=f"    Жанр игры: {i.game_genre}\n"
                            products_text+=f"    Масштаб игры: {i.scale_game} из 6\n"
                            products_text+=f"    Стиль графики: {i.style_graphics}\n"
                            products_text+=f"    Тип графики: {i.type_graphics}\n"
                            products_text+=f"    Количество механик: {i.mechanics}\n"
                            products_text+=f"    Количество: {i.count} шт\n"
                            products_text+=f"    Стоимость: {separate_digits(i.all_cost)} ₽\n"
                            products_text+=f"    Общая стоимость: {separate_digits(i.all_cost*i.count)} ₽\n"
                            products_text+="---------------------------------\n"
                        send_message(f"Заказ: {username}({name} {second_name}) \nПочта: {email}\ntg: {telegram}\nТовары:\n----------------------------------\n{products_text}\nОбщая сумма: {separate_digits(all_cost)} ₽")
                    else:
                        card_num=int(request.POST.get("card_num_change"))
                        add=int(request.POST.get("add"))
                        object=Product_Item.objects.get(username=username,card_num=card_num)
                        if(add==1):
                            if(object.count<10):
                                object.count+=1
                        else:
                            if(object.count>1):
                                object.count-=1
                            else:
                                object=Product_Item.objects.filter(username=username,card_num=card_num).delete()
                        object.save()
            return render(request,"shop/basket.html",{"data":products,"custom_data":reverse_array(products_custom_person),"count_products":product_count,"all_cost":separate_digits(all_cost)})
        except:
            return render(request,"shop/basket.html",{"count_products":0})
            

    except:
        return redirect("/")
@csrf_exempt   
def custom_game(request):
    try:
        username=str(request.COOKIES["username"])
        if request.method=="POST":
            if("mechanics" in request.POST):
                style_graphics=str(request.POST.get("style_graphics"))
                game_genre=str(request.POST.get("game_genre"))
                scale_game=int(request.POST.get("scale_game"))
                type_graphics=str(request.POST.get("type_graphics"))
                mechanics=int(request.POST.get("mechanics"))
                all_cost=int(request.POST.get("all_cost"))
                try:
                    product_custom=Custom_Item_I.objects.get(username=username,all_cost=all_cost)
                except:
                    try:
                        product_custom=Custom_Item_I(username=username,style_graphics=style_graphics,game_genre=game_genre,scale_game=scale_game,type_graphics=type_graphics,mechanics=mechanics,all_cost=all_cost,count=1)
                        product_custom.save()
                    except Exception as ex:
                        print(ex)

            if "quit" in request.POST:
                responce=redirect("/shop/custom/")
                responce.delete_cookie("username")
                responce.delete_cookie("email")
                responce.delete_cookie("password")
                return responce
        return render(request,"shop/create_custom.html")
    except:
        return redirect("/")
    
def separate_digits(number):
    number_str = str(number)[::-1]  # Переворачиваем строку
    result = []
    
    for i in range(len(number_str)):
        result.insert(0, number_str[i])
        if (i + 1) % 3 == 0 and i != len(number_str) - 1:
            result.insert(0, ' ')
    
    return ''.join(result)

def remove_newlines(text):
    return text.replace('\n', ' ')
def add_at_symbol(text):
    if text.startswith('@'):
        return text
    else:
        return '@' + text
    
def remove_spaces(input_string):
    return input_string.replace(' ', '')
def keep_digits_only(input_string):
    return ''.join(filter(str.isdigit, input_string))
def reverse_array(arr):
    return arr[::-1]

        