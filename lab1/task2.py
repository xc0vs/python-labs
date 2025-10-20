"""
Аутентифікація користувачів. Створіть словник в якому зберігаються ім'я користувача(login), 
зашифрований пароль та повне ПІБ користувача. Для хешування пароля використовуйте функцію hashlib.md5().
Зробіть функцію перевірки введеного паролю користувача; пароль користувач вводить з консолі, зчитування за допомогою методу input()
"""

import hashlib

credentials = {"login": "petrenko_o", "password": "526df7eacac2c6d94e4d10ee30ea7a53", "name": "Петренко Олександр Іванович"} #password = b6pHmERu

def check_password():
    p = input("Enter your password: ")
    if hashlib.md5(p.encode()).hexdigest() == credentials["password"]:
        print("Login is succesfull")
    else : print("Password is incorrect")
    
check_password()