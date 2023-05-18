
# ██╗░░░░░██╗░░░██╗███╗░░░███╗██╗
# ██║░░░░░██║░░░██║████╗░████║██║
# ██║░░░░░██║░░░██║██╔████╔██║██║
# ██║░░░░░██║░░░██║██║╚██╔╝██║██║
# ███████╗╚██████╔╝██║░╚═╝░██║██║
# ╚══════╝░╚═════╝░╚═╝░░░░░╚═╝╚═╝

import sqlite3
import hashlib
import random
import string
import os

Debug = True # True / False

# Генерация токена
def gen_token():
    symbols = "1234567890-=;/.,~!@#$^&*()_+"
    letters = string.ascii_letters
    lenght = random.randint(35, 65)

    random_string = ''.join(random.choice(symbols + letters) for i in range(lenght))
    if Debug == True:
        print(random_string)
    h = hashlib.new('sha256') # decode
    h.update(str.encode(random_string)) # encode
    h.hexdigest()
    if Debug == True:
        print(h.hexdigest())
    
    return str(h.hexdigest())

# Генерация кода безопасности токена
def gen_code():
    a = random.randint(1000000, 9999999)
    if Debug == True:
        print(a)
        
    return int(a)

# Генерация редкости люмы
def gen_rare():
    b = random.randint(1, 1000)
    if b >= 950:
        a = round(random.uniform(9, 10), 10)
    elif b <=900:
        a = round(random.uniform(7, 9), 10)
    elif b >= 850:
        a = round(random.uniform(3, 10), 10)
    elif b <= 800:
        a = round(random.uniform(5, 7), 10)
    elif b >= 750:
        a = round(random.uniform(3, 4), 10)
    elif b >= 700:
        a = round(random.uniform(1, 10), 10)
    elif b <= 650:
        a = round(random.uniform(4, 6), 10)
    elif b >= 400:
        a = round(random.uniform(6, 9), 10)
    elif b <= 250:
        a = round(random.uniform(0, 4), 10)
    elif b <= 100:
        a = round(random.uniform(8, 10), 10)
         
    return a

# Генерация токена аккаунта
def gen_passtoken():
    symbols = "1234567890-=;/.,~!@#$^&*()_+"
    letters = string.ascii_letters
    lenght = random.randint(35, 65)

    random_string = ''.join(random.choice(symbols + letters) for i in range(lenght))
    if Debug == True:
        print(random_string)
        
    return str(random_string)

# инициализация бд люмы
def db_main_LumiBase_initialization():
    if os.path.isfile('Lumi.db'):
        global con
        con = sqlite3.connect('Lumi.db')
        global cur
        cur = con.cursor()
        print('database exists')
    else:
        con = sqlite3.connect('Lumi.db')
        cur = con.cursor()
        cur.execute('CREATE TABLE userbase(id INT, name VARCHAR, passtoken VARCHAR)'), # USERS
        cur.execute('CREATE TABLE lumibase(id INT, code INT, token VARCHAR, owner VARCHAR, rare INT )'), # tokens, VALUTA BLYAT

# Запрос id люма
def get_lumid():
    global con
    global cur
    
    con = sqlite3.connect('Lumi.db')
    cur = con.cursor()
    res = cur.execute('SELECT id FROM lumibase')

    a = res.fetchall()
    if len(a) == 0:
        b = 0
    else:
        b = int(a[-1][0])
        
    if Debug == True:
        print(b)
        
    return b

# Запрос id пользователя люма
def get_lumuserid():
    global con
    global cur
    
    con = sqlite3.connect('Lumi.db')
    cur = con.cursor()
    res = cur.execute('SELECT id FROM userbase')

    a = res.fetchall()
    if len(a) == 0:
        b = 0
    else:
        b = int(a[-1][0])
        
    if Debug == True:
        print(b)
        
    return b

# Создание валюты
def create_lumi():
    global con
    global cur
    
    con = sqlite3.connect('Lumi.db')
    cur = con.cursor()
    
    if (cur.execute('SELECT COUNT(*) FROM lumibase WHERE id IS NULL').fetchone()[0] == 0):
        mas = [ get_lumid() + 1, gen_code(), gen_token(), 'Null', gen_rare() ]
    else:
        mas = [ 1, gen_code(), gen_token(), 'Null', gen_rare() ]
    
    cur.execute('INSERT INTO lumibase (id, code, token, owner, rare) VALUES (?, ?, ?, ?, ?)', mas)
    con.commit()

# Регестрация валюты для пользователя
def give_lum( usr ):
    global con
    global cur
    
    con = sqlite3.connect('Lumi.db')
    cur = con.cursor()
    
    cur.execute("SELECT name FROM userbase")
    res = cur.fetchone()
    
    if (cur.execute('SELECT COUNT(*) FROM lumibase WHERE id IS NULL').fetchone()[0] == 0):
        mas = [ get_lumid() + 1, gen_code(), gen_token(), str(usr), gen_rare() ]
    else:
        mas = [ 1, gen_code(), gen_token(), str(usr), gen_rare() ]
    
    cur.execute('INSERT INTO lumibase (id, code, token, owner, rare) VALUES (?, ?, ?, ?, ?)', mas)
    con.commit()

# Регистрация
def log():
    global con
    global cur
    
    con = sqlite3.connect('Lumi.db')
    cur = con.cursor()
    
    NameLog = input('Введите имя: ')
    login = input('Введите ключь регистрации: ')
    
    cur.execute("SELECT * FROM userbase WHERE name=? AND passtoken=?", (NameLog, login))
    result = cur.fetchone()
    
    cur.execute("SELECT * FROM lumibase WHERE owner = ?", (NameLog,))
    rows = cur.fetchall()
    
    if result:
        print("Имя и токен найдены в базе данных")
        print('{ 1 } = Токены в наличии')
        print('{ 2 } = Получить дозу...')
        print('{ 3 } = Выход')
        select = input('что вы хотите выбрать ?: ')
        if select == '1':
            if rows:
                print(rows)
            else:
                print('u dont have tokenss')
        elif select == '2':
            give_lum(usr=NameLog)
        else:
            return False
    else:
        print("Имя и токен не найдены в базе данных")

# Вход    
def reg():
    global con
    global cur
    
    con = sqlite3.connect('Lumi.db')
    cur = con.cursor()
    
    reg = input('Введите жалаемое имя, которое будет отображаться: ')
    
    if (cur.execute('SELECT COUNT(*) FROM userbase WHERE id IS NULL').fetchone()[0] == 0):
        mas = [ get_lumuserid() + 1, str(reg), gen_passtoken() ]
    else:
        mas = [ 1, str(reg), gen_passtoken() ]
        
    cur.execute('INSERT INTO userbase (id, name, passtoken) VALUES (?, ?, ?)', mas)
    con.commit()


# Вход / Регистрация
def login():
    print('{ 1 } --> Login')
    print('{ 2 } --> Reg')
    select = input('что вы хотите выбрать ?: ')
    if select == '1':
        log()
    elif select == "2":
        reg()
    
def initialization():
    db_main_LumiBase_initialization()
    gen_code()
    gen_token()
    gen_passtoken()
    create_lumi()
    login()
    
initialization()
