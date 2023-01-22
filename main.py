import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import sqlite3

token = '5769347442:AAF2wIDcdGTLUZ2jiVCOjUVBcd3RXVY2ahw'

bot = telebot.TeleBot(token)

connect = sqlite3.connect('marks.db')
cursor = connect.cursor()
names = 'Математика, ИКТ, Искусство, Биология, Химия, Физика, Экономика, Русский_язык, Казахский_язык, Английский_язык, География, История_Казахстана, Всемирная_История, ФК'
names = names.split(', ')
for name in names:
	cursor.execute(f"""CREATE TABLE IF NOT EXISTS {name}(
		user_id INTEGER PRIMARY KEY,
		A INTEGER,
		B INTEGER,
		C INTEGER,
		D INTEGER,
		Final INTEGER
	)""")
connect.commit()



class MainFilter(telebot.custom_filters.AdvancedCustomFilter):
    key='text'
    @staticmethod
    def check(message, text):
        return True


@bot.message_handler(commands=['start'])
def start(message):
	funcs = ['Вставить оценки по предмету', 'Доступные DP предметы', 'DP группы', 'Зарегистрироваться']
	buttons = []
	for i in funcs:
		buttons.append([InlineKeyboardButton(i, callback_data=i)])
	bot.send_photo(message.chat.id, reply_markup=InlineKeyboardMarkup(buttons), photo=open('logo.png', 'rb'), caption=f'Здравствуйте, {message.from_user.first_name}! \nДоступны следующие функции:')

@bot.callback_query_handler(func=lambda call: call.data=='DP группы')
def groups(call):
	bot.send_document(call.from_user.id, document=open('dpgroups.png','rb'))

@bot.callback_query_handler(func=lambda call: call.data=='Зарегистрироваться')
def registration(call):
	connect = sqlite3.connect('marks.db')
	cursor = connect.cursor()
	cursor.execute(f"""CREATE TABLE IF NOT EXISTS users(
		user_id INTEGER PRIMARY KEY,
		password TEXT
	)""")
	connect.commit()
	bot.send_message(call.from_user.id, "/recordpass [your password]")

@bot.message_handler(commands=['recordpass'])
def recordpass(message):
	connect = sqlite3.connect('marks.db')
	cursor = connect.cursor()
	user_id = message.chat.id
	cursor.execute(f"SELECT user_id FROM users WHERE user_id = {user_id}")
	data = cursor.fetchone()
	try:
		password = message.text.split(' ')[1]
		if data is None:
			cursor.execute(f"""INSERT INTO users (user_id, password) VALUES (?,?)""", (user_id, password))
			connect.commit()
			bot.send_message(message.chat.id, f'Вы успешно зарегистрированы. \nВаш логин: {user_id}\nВаш пароль: {password}')
		else:
			cursor.execute(f"""UPDATE users
							SET password = ?
							WHERE user_id = ?""", (password, user_id))
			connect.commit()
			bot.send_message(message.chat.id, f'Вы успешно поменяли пароль. \nВаш логин: {user_id}\nВаш пароль: {password}')
	except:
		bot.send_message(message.chat.id, "Возможно, вы неправильно ввели команду: \n/recordpass [password]")

@bot.callback_query_handler(func=lambda call: call.data=='Доступные DP предметы')
def available(call):
	connect = sqlite3.connect('marks.db')
	cursor = connect.cursor()
	dpsubjects = []
	names = 'Математика, ИКТ, Искусство, Биология, Химия, Физика, Экономика, Русский_язык, Казахский_язык, Английский_язык, География, История_Казахстана, Всемирная_История, ФК'
	names = names.split(', ')
	for subject in names:
		people_id = call.from_user.id
		cursor.execute(f"SELECT user_id FROM {subject} WHERE user_id = {people_id}")
		data = cursor.fetchone()
		if data is None:
			pass
		else:
			cursor.execute(f"SELECT Final FROM {subject} WHERE user_id = {people_id}")
			final = cursor.fetchone()[0]
			if final >= 6:
				dpsubjects.append(subject)
			else:
				pass

	bot.send_message(people_id, 'You can choose these subjects: '+', '.join(dpsubjects))

	summOfMarks = 0
	toPrint = True
	for subject in names:
		people_id = call.from_user.id
		cursor.execute(f"SELECT Final FROM {subject} WHERE user_id = {people_id}")
		data = cursor.fetchone()
		if data is None:
			bot.send_message(people_id, 'Вы не можете посчитать GPA, сначала заполните все оценки. Заполните оценку по предмету '+ subject)
			toPrint = False
			break
		else:
			data = data[0]
			if data >= 0 and data <=1:
				summOfMarks += 2
			elif data >=2 and data <= 3:
				summOfMarks += 3
			elif data >=4 and data <=5:
				summOfMarks += 4 
			elif data >= 6:
				summOfMarks += 5
			else: 
				bot.send_message(people_id, f'Ваши оценки по предмету {subject} вставлены неправильно. ')
				break

	if toPrint == True:

		bot.send_message(people_id, f'Ваш GPA равен {summOfMarks/14}.')



@bot.callback_query_handler(func=lambda call: call.data=='Вставить оценки по предмету')
def insert(call):
	connect = sqlite3.connect('marks.db')
	cursor = connect.cursor()
	cursor.execute(f"""SELECT 
	    name
	FROM 
	    sqlite_master
	WHERE 
	    type ='table' AND 
	    name NOT LIKE 'sqlite_%';""")
	tables = cursor.fetchall()
	buttons=[]
	print(tables)
	for i in tables:
		table = i[0]
		buttons.append([InlineKeyboardButton(table, callback_data=table)])
	bot.send_message(call.from_user.id, reply_markup=InlineKeyboardMarkup(buttons), text=f'Все предметы:')

@bot.callback_query_handler(func=lambda call: True)
def callback(call):
	bot.send_message(call.from_user.id, f'Чтобы написать оценки по предмету {call.data}, напишите:\n{call.data} [оценка по А критерию] [B] [C] [D]')

@bot.message_handler(text=['hi'])
def tablesert(message):
	connect = sqlite3.connect('marks.db')
	cursor = connect.cursor()
	names = 'Математика, ИКТ, Искусство, Биология, Химия, Физика, Экономика, Русский_язык, Казахский_язык, Английский_язык, География, История_Казахстана, Всемирная_История, ФК'
	names = names.split(', ')
	try:
		people_id = message.chat.id
		user_id = message.chat.id

		subject = message.text.split(' ')[0]
		cursor.execute(f"SELECT user_id FROM {subject} WHERE user_id = {people_id}")
		data = cursor.fetchone()

		if data is None:

			if message.text.split(' ')[0] in names:

				table = message.text.split(' ')[0]
				a = int(message.text.split(' ')[1])
				b = int(message.text.split(' ')[2])
				c = int(message.text.split(' ')[3])
				d = int(message.text.split(' ')[4])
				summ = a+b+c+d

				if summ >= 0 and summ<=5:
					mark = 1
				elif summ >= 6 and summ<=9:
					mark = 2
				elif summ >= 10 and summ<=14:
					mark = 3
				elif summ >= 15 and summ<=18:
					mark = 4
				elif summ >= 19 and summ<=23:
					mark = 5
				elif summ >= 24 and summ<=27:
					mark = 6
				elif summ >= 28 and summ<=32:
					mark = 7
				else:
					mark = 4
				cursor.execute(f'''INSERT INTO {table} (user_id, A, B, C, D, Final) VALUES (?,?,?,?,?,?)''', (user_id, a,b,c,d,mark))
				connect.commit()
				bot.send_message(message.chat.id,f'{message.from_user.first_name}, вы успешно записали оценки! \n{a}, {b}, {c}, {d}\n Ваша финальная оценка по предмету - это {mark}')
		else:
			if message.text.split(' ')[0] in names:
				table = message.text.split(' ')[0]
				a = int(message.text.split(' ')[1])
				b = int(message.text.split(' ')[2])
				c = int(message.text.split(' ')[3])
				d = int(message.text.split(' ')[4])
				summ = a+b+c+d
				if summ >= 0 and summ<=5:
					mark = 1
				elif summ >= 6 and summ<=9:
					mark = 2
				elif summ >= 10 and summ<=14:
					mark = 3
				elif summ >= 15 and summ<=18:
					mark = 4
				elif summ >= 19 and summ<=23:
					mark = 5
				elif summ >= 24 and summ<=27:
					mark = 6
				elif summ >= 28 and summ<=32:
					mark = 7
				else:
					mark = 4
				cursor.execute(f"""UPDATE {table}
								SET a = ?,
								b = ?,
								c = ?,
								d = ?,
								final = ?
								WHERE user_id = ?""", (a,b,c,d,mark, user_id))
				connect.commit()
				bot.send_message(message.chat.id,f'{message.from_user.first_name}, вы успешно перезаписали оценки! \n{a}, {b}, {c}, {d}\n Ваша финальная оценка по предмету - это {mark}')
	except:
		bot.send_message(message.chat.id,'Unexpected error, command:\n[предмет] [оценка по А критерию] [B] [C] [D]\nВозможно, неправильное название таблицы.')




bot.add_custom_filter(MainFilter())
bot.polling(none_stop = True)