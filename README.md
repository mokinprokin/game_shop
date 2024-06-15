> # game_shop
> Branches
> Веб-приложение в котором можно заказать создание игр

> ## Технологии в приложении:
>> # 1. Jinja  ![Image](https://waksoft.susu.ru/wp-content/uploads/2021/04/transparant-jinja.png)
>>> #### Использование:
>>> 1. Циклов
>>> 2. Условий
>>> 3. создание переменных
>> # 2. Ajax
>> ![Image](https://cdn-icons-png.flaticon.com/512/1183/1183690.png)
>>> #### Использование:
>>> 1. **POST** запросов
>>> 2. **GET** запросов
>> # 3. Javascript
>> ![Image](https://cdn-icons-png.flaticon.com/512/4726/4726005.png)
>> # 4. Models
>> ![Image](https://cdn-icons-png.flaticon.com/512/9853/9853806.png)
>>>### 1. Users
>>>```python
>>> class User(models.Model):
>>>    username=models.CharField(max_length=20)
>>>    email=models.CharField(max_length=50)
>>>    password=models.CharField(max_length=25)
>> ### 2. Product_Item
>>>```python
>>> class Product_Item(models.Model):
>>>    username=models.CharField(max_length=20)
>>>    card_num=models.IntegerField()
>>>    count=models.IntegerField()
>> ### 3. Feedback_Item
>>>```python
>>> class Feedback_Item(models.Model):
>>>     username=models.CharField(max_length=20)
>>>     header=models.TextField()
>>>     description=models.TextField()
>>>     rating=models.IntegerField()
>>>     date=models.TextField()
>> ### 4. Custom_Item
>>>```python
>>> class Custom_Item(models.Model):
>>>    username=models.CharField(max_length=20)
>>>    game_genre=models.TextField()
>>>    all_cost=models.IntegerField()
>>>    count=models.IntegerField()
>>>    scale_game=models.IntegerField()
>>>    style_graphics=models.TextField()
>>>    mechanics=models.IntegerField()
>>>    type_graphics=models.TextField()




  
  
