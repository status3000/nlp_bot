from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

btnMain = KeyboardButton('Главное Меню')

#--- Main Menu ---
btnNews = KeyboardButton('📋Выбрать тему новости📋')
btnCheckNews = KeyboardButton('📋Проверить новости📋')
btnOther = KeyboardButton('📚Доп. функции📚')
mainMenu = ReplyKeyboardMarkup(resize_keyboard= True).add(btnNews,btnCheckNews, btnOther)

#--- Menu of Theme of news ---
btnWebChs = KeyboardButton('📋Выбрать сайт для поиска новости📋')
newsMenu = ReplyKeyboardMarkup(resize_keyboard= True).add(btnWebChs,btnOther, btnMain)


#--- Menu of Theme of news_2 ---
btnHabr = KeyboardButton('📋Habr📋')
btnLenta = KeyboardButton('📋Lenta📋')
btnWiki = KeyboardButton('📋Wiki📋')
news2Menu = ReplyKeyboardMarkup(resize_keyboard=True).add(btnHabr,btnLenta, btnWiki, btnMain)

# --- Other Menu ---
btnInfo = KeyboardButton('Summary своего текста')
btnPhoto = KeyboardButton('Summary по фото текста')
btnDig = KeyboardButton('Оцифровать документ')
btnNER = KeyboardButton('Выделить сущности (NER)')
btnMoney = KeyboardButton('Кто кому должен денег?')
#btnMoney = KeyboardButton('🐭Rat🐭')
featchMenu = ReplyKeyboardMarkup(resize_keyboard=True).add(btnInfo, btnPhoto, btnDig, btnMoney, btnNER, btnMain)


backMain = ReplyKeyboardMarkup(resize_keyboard=True).add(btnMain)


NewSend = KeyboardButton('Искать новости по предыдущим запросам')

NewSendMenu = ReplyKeyboardMarkup(resize_keyboard=True).add(NewSend, btnMain)

# --- chek Menu ---
btnChekUpload = KeyboardButton('✏️Загрузка чека✏️')
btnChekIgnor = KeyboardButton('✏️Ввод суммы вручную✏️')
ChekMenu = ReplyKeyboardMarkup(resize_keyboard=True).add(btnChekUpload, btnChekIgnor, btnMain)

# --- chek Menu --- yes/no
btnChekUploadYes = KeyboardButton('Да, все верно!')
btnChekUploadNo = KeyboardButton('Нет, введу сам!')
ChekMenuYesNo = ReplyKeyboardMarkup(resize_keyboard=True).add(btnChekUploadYes, btnChekUploadNo, btnMain)