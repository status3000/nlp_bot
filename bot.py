from dataclasses import InitVar
from email import message
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import os
import json
import logging
from config import TOKEN
from model import summery_gen
from recog_text import img_loader 
from Parsing_lenta import lenta_parse
from Parsing_habr import parser
from LaBSE_ner import ner_recognition
from money import money_result
from recog_text import check_detect

import markup as nav
# import keybord lib
from aiogram.types import InlineKeyboardMarkup
from aiogram.types import InlineKeyboardButton
#for delayed posting
from apscheduler.schedulers.asyncio import AsyncIOScheduler 
import asyncio
import aioschedule

import time

from gtts import gTTS
import wikipedia, re

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
import aioredis
from aiogram.contrib.fsm_storage.memory import MemoryStorage

json_file_path = 'users.json'
users_dict = []

json_money_path = 'users_money.json'
dict_money = []

storage = MemoryStorage()

scheduler = AsyncIOScheduler()

logging.basicConfig(level=logging.INFO)

class Condi(StatesGroup):
    Init = State()
    NewsChs = State()
    Habr_Model_pars = State()
    Lenta_Model_pars = State()
    Wiki_pars = State()
    Model = State()
    Additional = State()
    Photo_det = State()
    Photo_dig = State()

    Check_News_pars = State()
    NER = State()

    Money = State()
    Money_count_people = State()
    Money_name_people = State()
    Money_name_count = State()
    Money_result = State()
    Chekinput = State()
    ManulChek = State()



bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=storage)

wikipedia.set_lang("ru")

@dp.message_handler(commands=['start'], state = '*')
async def process_start_command(message: types.Message, state: FSMContext):
    await Condi.Init.set()
    await message.reply("Привет!\nЯ твой БОТ, который поможет экономить твое время и быть в курсе интересующих тебя событий!", reply_markup=nav.mainMenu)


@dp.message_handler(state = Condi.Init)
async def echo_message(msg: types.Message, state: FSMContext):
    if msg.text == '📚Доп. функции📚':
        await Condi.Additional.set()
        await msg.answer('📚Выберите функцию📚', reply_markup = nav.featchMenu)
    
    elif msg.text == '📋Проверить новости📋':
        await msg.answer('Можем найти свежие новости по Вашим предыдущим запросам. Искать?', reply_markup = nav.NewSendMenu)
        await Condi.Check_News_pars.set()
        # await bot.send_message(msg.from_user.id, 'Проверяем новости по вашим предыдущим запросам', reply_markup = nav.backMain)

    elif msg.text == '📋Выбрать тему новости📋':
        await msg.answer('📋Выбрать сайт для поиска новости📋', reply_markup = nav.news2Menu)
        await Condi.NewsChs.set()

        
@dp.message_handler(state = Condi.Additional)
async def echo_message(msg: types.Message, state: FSMContext):
    if msg.text == 'Summary своего текста':
        await Condi.Model.set()
        await bot.send_message(msg.from_user.id, '✏️Отправьте свой текст:', reply_markup = nav.backMain)
    elif msg.text == 'Summary по фото текста':
        await bot.send_message(msg.from_user.id, '✏️Отправьте фото докумета с текстом:', reply_markup = nav.backMain)
        await Condi.Photo_det.set()
    elif msg.text == ('Оцифровать документ'):
        await bot.send_message(msg.from_user.id, '✏️Отправьте фото докумета с текстом:', reply_markup = nav.backMain)
        await Condi.Photo_dig.set()
    elif msg.text == ('Выделить сущности (NER)'):
        await bot.send_message(msg.from_user.id, '✏️Отправьте свой текст:', reply_markup = nav.backMain)
        await Condi.NER.set()
    elif msg.text == ('Кто кому должен денег?'):
        await bot.send_message(msg.from_user.id, 'Сколько людей было на вечеринке?', reply_markup = nav.backMain)
        await Condi.Money.set()
    elif msg.text == 'Главное Меню':
        await Condi.Init.set()
        await bot.send_message(msg.from_user.id,'Главное Меню', reply_markup = nav.mainMenu)


@dp.message_handler(state = Condi.Photo_det, content_types=['document', 'photo','text'])
async def get_photo(message: types.Message):
    if message.text == 'Главное Меню':
        await Condi.Init.set()
        await bot.send_message(message.from_user.id,'Главное Меню', reply_markup = nav.mainMenu)
    else:
        user_id = message.from_user.id
        img_path = 'input.jpg'
        await message.photo[-1].download(img_path)
        photo_text = img_loader(img_path)
        sum_user = summery_gen(photo_text)
        await bot.send_message(user_id, sum_user, reply_markup = nav.backMain)


@dp.message_handler(state = Condi.Photo_dig, content_types=['document', 'photo','text'])
async def get_photo(message: types.Message):
    if message.text == 'Главное Меню':
        await Condi.Init.set()
        await bot.send_message(message.from_user.id,'Главное Меню', reply_markup = nav.mainMenu)
    else:
        user_id = message.from_user.id
        img_path = 'input.jpg'
        await message.photo[-1].download(img_path)
        photo_text = img_loader(img_path)
        await bot.send_message(user_id, photo_text, reply_markup = nav.backMain)


@dp.message_handler(state = Condi.Model)
async def echo_message(msg: types.Message, state: FSMContext):
    user_id = msg.from_user.id

    if msg.text == 'Главное Меню':
        await Condi.Init.set()
        await bot.send_message(msg.from_user.id,'Главное Меню', reply_markup = nav.mainMenu)        
    else:
        user_text = msg.text
       
        sum_user = summery_gen(user_text)

        await Condi.Init.set()
        await bot.send_message(msg.from_user.id, sum_user, parse_mode=types.ParseMode.HTML,  reply_markup = nav.mainMenu)

@dp.message_handler(state = Condi.NER)
async def echo_message(msg: types.Message, state: FSMContext):
    user_id = msg.from_user.id

    if msg.text == 'Главное Меню':
        await Condi.Init.set()
        await bot.send_message(msg.from_user.id,'Главное Меню', reply_markup = nav.mainMenu)        
    else:
        user_text = msg.text
       
        sum_user = ner_recognition(user_text) #summery_gen(user_text)

        await Condi.Init.set()
        await bot.send_message(msg.from_user.id, sum_user, parse_mode=types.ParseMode.HTML,  reply_markup = nav.mainMenu)

@dp.message_handler(state = Condi.NewsChs)
async def echo_message(msg: types.Message):

    user_id = msg.from_user.id

    if msg.text == '📋Habr📋':
        await Condi.Habr_Model_pars.set()
        await bot.send_message(msg.from_user.id, 'Введите интересующую тему:', reply_markup = nav.backMain)
    elif msg.text == '📋Lenta📋':
        await Condi.Lenta_Model_pars.set()
        await bot.send_message(msg.from_user.id, 'Введите интересующую тему:', reply_markup = nav.backMain)
    elif msg.text == '📋Wiki📋':
        await Condi.Wiki_pars.set()
        await bot.send_message(msg.from_user.id, 'Введите интересующую тему:', reply_markup = nav.backMain)
    elif msg.text == 'Главное Меню':
        await Condi.Init.set()
        await bot.send_message(msg.from_user.id,'Главное Меню', reply_markup = nav.mainMenu)

@dp.message_handler(state = Condi.Lenta_Model_pars)
async def echo_message(msg: types.Message):
    user_id = msg.from_user.id
    if msg.text == 'Главное Меню':
        await Condi.Init.set()
        await bot.send_message(msg.from_user.id,'Главное Меню', reply_markup = nav.mainMenu)
    else:
        prompt = msg.text
        await bot.send_message(msg.from_user.id,'Ищем новости по Вашему запросу, ожидайте...')

        #добавляем юзера и запрос в базу    
        update_json(user_id, prompt, 'lenta')    
        
        start = time.time()
        model_res = lenta_parse(prompt, 1)   
        # print(len(model_res))
        print(f'time of lenta parsing: {time.time()-start}')

        if model_res == 'На данный запрос не найдены новости. Введите новый запрос:':
            ans = model_res 
            
        else:
            # key_word = model_res[0]
            ans = []
            # ans = summery_gen(key_word) + '\n' + model_res[1]
            articles = model_res[0]
            links = model_res[1]
            start = time.time()
            for i in range(len(articles)):
                # ans.append(ner_recognition(summery_gen(articles[i])) + '\n' + links[i])
                # ans.append(summery_gen(articles[i]) + '\n' + links[i])
                sum_text = summery_gen(articles[i])
                language = 'ru'
                myobj = gTTS(text=sum_text, lang=language, slow=False)
                result = myobj.save(f'voicefile_{user_id}_{i}.ogg')
                ans.append(sum_text + '\n' + links[i])
        print(f'time of lenta summary: {time.time()-start}')
        await Condi.NewsChs.set()
        for i in range(len(ans)):
            await bot.send_message(msg.from_user.id, ans[i], parse_mode=types.ParseMode.HTML, reply_markup = nav.news2Menu)
            audio = open(f'voicefile_{user_id}_{i}.ogg', 'rb')
            await bot.send_audio(msg.from_user.id, audio)
            audio.close()

@dp.message_handler(state = Condi.Habr_Model_pars)
async def echo_message(msg: types.Message):
    user_id = msg.from_user.id
    
    if msg.text == 'Главное Меню':
        await Condi.Init.set()
        await bot.send_message(msg.from_user.id,'Главное Меню', reply_markup = nav.mainMenu)
    else:

        prompt = msg.text
        await bot.send_message(msg.from_user.id,'Ищем новости по Вашему запросу, ожидайте...')
        #добавляем юзера и запрос в базу    
        update_json(user_id, prompt, 'habr')    

        model_res = parser(prompt, 1)
        # print(len(model_res))
        if model_res == 'На данный запрос не найдены новости. Введите новый запрос:':
            ans = model_res 
            
        else:
            # key_word = model_res[0]
            ans = []
            # ans = summery_gen(key_word) + '\n' + model_res[1]
            articles = model_res[0]
            links = model_res[1]
            for i in range(len(articles)):
                # ans.append(ner_recognition(summery_gen(articles[i])) + '\n' + links[i])
                sum_text = summery_gen(articles[i])
                language = 'ru'
                myobj = gTTS(text=sum_text, lang=language, slow=False)
                result = myobj.save(f'voicefile_{user_id}_{i}.ogg')
                ans.append(sum_text + '\n' + links[i])

        await Condi.NewsChs.set()
        for i in range(len(ans)):
            await bot.send_message(msg.from_user.id, ans[i], parse_mode=types.ParseMode.HTML)
            audio = open(f'voicefile_{user_id}_{i}.ogg', 'rb')
            await bot.send_audio(msg.from_user.id, audio)
        await bot.send_message(msg.from_user.id, 'Выберите пункт меню:', reply_markup = nav.news2Menu)

@dp.message_handler(state = Condi.Wiki_pars)
async def echo_message(msg: types.Message):
    user_id = msg.from_user.id
    
    if msg.text == 'Главное Меню':
        await Condi.Init.set()
        await bot.send_message(msg.from_user.id,'Главное Меню', reply_markup = nav.mainMenu)
    else:

        prompt = msg.text
        
        await bot.send_message(msg.from_user.id,'Ищем статью по Вашему запросу, ожидайте...')
        #добавляем юзера и запрос в базу    
        # update_json(user_id, prompt, 'habr')   
        
        url = wikipedia.page(prompt, auto_suggest=False).url
        logging.info('Ищу статью в вики...')
        page = wikipedia.page(prompt, auto_suggest=False)
        wikitext=page.content[:600]
        wikimas=wikitext.split('.')
        wikimas = wikimas[:-1]
        wikitext2 = ''
        for x in wikimas:
            if not('==' in x):
                if(len((x.strip()))>3):
                    wikitext2=wikitext2+x+'.'
                else:
                    break
        wikitext2=re.sub('\([^()]*\)', '', wikitext2)
        wikitext2=re.sub('\([^()]*\)', '', wikitext2)
        wikitext2=re.sub('\{[^\{\}]*\}', '', wikitext2)
        mytext = wikitext2
        language = 'ru'
        myobj = gTTS(text=mytext, lang=language, slow=False)
        myobj.save(f"voicefile_wiki_{user_id}.ogg")
        ans = wikitext2 + '\n' + url 

        await Condi.NewsChs.set()
        
        await bot.send_message(msg.from_user.id, ans)
        audio = open(f"voicefile_wiki_{user_id}.ogg", 'rb')
        await bot.send_audio(msg.from_user.id, audio)
        await bot.send_message(msg.from_user.id, 'Выберите пункт меню:', reply_markup = nav.news2Menu)

@dp.message_handler(state = Condi.Check_News_pars)
async def echo_message(msg: types.Message):
    user_id = msg.from_user.id
    if msg.text == 'Главное Меню':
        await Condi.Init.set()
        await bot.send_message(msg.from_user.id,'Главное Меню', reply_markup = nav.mainMenu)
    elif msg.text == 'Искать новости по предыдущим запросам':
        
        prompt_habr = '' #habr topic
        prompt_lenta = '' # lenta topic

        print(f'checking news for user {user_id}...')

        #проверить, есть ли запрос от юзера в базе   
        
        with open(json_file_path, 'r') as fp:
            users_dict = json.load(fp)
        
        user_exists = False

        for user in users_dict:
            if user_id == user['id']:
                user_exists = True
                if user['habr_topic'] != []:
                    prompt_habr = user['habr_topic']
                    print(prompt_habr)

                if user['lenta_topic']!= []:
                    prompt_lenta = user['lenta_topic']
                    print(prompt_lenta)

                break

        if not(user_exists):
            ans = 'Извините, в базе не найдены Ваши предыдущие запросы. Вернитесь в главное меню и введите запрос в меню "Выбрать тему новости".'
            await bot.send_message(msg.from_user.id, ans, reply_markup = nav.backMain)
        else:

            await bot.send_message(msg.from_user.id, f"Ищем новости по Вашим запросам: {', '.join(prompt_habr)}, {', '.join(prompt_lenta)}. Может занять некоторое время...")
            ans =[]
            for p in prompt_habr:
                model_res = parser(p, 1)
    
                articles = model_res[0]
                links = model_res[1]
                for i in range(len(articles)):
                    ans.append(summery_gen(articles[i]) + '\n' + links[i])
            for p in prompt_lenta:
                model_res = lenta_parse(p, 1)
    
                articles = model_res[0]
                links = model_res[1]
                for i in range(len(articles)):
                    ans.append(summery_gen(articles[i]) + '\n' + links[i])


            for i in range(len(ans)):
                await bot.send_message(msg.from_user.id, ans[i], reply_markup = nav.backMain)

@dp.message_handler()
async def check_news():

    prompt = '' #habr topic
    prompt_lenta = '' # lenta topic

    
    #проверить, есть ли запрос от юзера в базе   
    
    with open(json_file_path, 'r') as fp:
        users_dict = json.load(fp)
    
    # user_exists = False

    for user in users_dict:
        user_id = user['id']
        prompt = '' #habr topic
        prompt_lenta = '' # lenta topic
            
        if user['habr_topic'] != []:
            prompt = user['habr_topic']
            print(prompt)

        if user['lenta_topic']!= []:
            prompt_lenta = user['lenta_topic']
            print(prompt_lenta)

        ans =[]
        for p in prompt:
            model_res = parser(p, 1)

            articles = model_res[0]
            links = model_res[1]
            for i in range(len(articles)):
                ans.append(summery_gen(articles[i]) + '\n' + links[i])
        for p in prompt_lenta:
            model_res = lenta_parse(p, 1)

            articles = model_res[0]
            links = model_res[1]
            for i in range(len(articles)):
                ans.append(summery_gen(articles[i]) + '\n' + links[i])


        for i in range(len(ans)):
            await bot.send_message(user_id, ans[i])

@dp.message_handler(state = Condi.Money)
async def get_photo(message: types.Message):
    if message.text == 'Главное Меню':
        await Condi.Init.set()
        await bot.send_message(message.from_user.id,'Главное Меню', reply_markup = nav.mainMenu)
    else:
        user_id = message.from_user.id
        
    with open(json_money_path, 'r') as fp:
        dict_money = json.load(fp)
    
    user_exists = False

    for user in dict_money:
        if user_id == user['id']:
            user_exists = True
            user['count_of_people'] = message.text
            user['list_of_names'] = []
            user['list_of_prices'] = []
            break

    if not(user_exists):
        
            dict_money.append({
                                "id": user_id,
                                "count_of_people": message.text,
                                "list_of_names": [],
                                "list_of_prices" : []
                                })
     
     # Verify updated list
    print(dict_money)        
    with open(json_money_path, 'w') as json_file:
        json.dump(dict_money, json_file, ensure_ascii=False,
                            indent=4,  
                            separators=(',',': '))
    print('Successfully appended to the JSON file')
    await Condi.Money_count_people.set()
    await bot.send_message(user_id, 'Введите имена всех присутсвующих!\nВведите имя человека под номером - 1: ', reply_markup = nav.backMain)

@dp.message_handler(state = Condi.Money_count_people)
async def get_text(message: types.Message):
    user_id = message.from_user.id
    with open(json_money_path, 'r') as fp:
            dict_money = json.load(fp)       
 
    for user in dict_money:
        if user_id == user['id']:
            
            count_of_people = user['count_of_people'] 
            list_of_names = user['list_of_names'] 
            list_of_prices = user['list_of_prices']    
            break

    if message.text == 'Главное Меню':
        await Condi.Init.set()
        await bot.send_message(message.from_user.id,'Главное Меню', reply_markup = nav.mainMenu)

    elif len(list_of_names) < int(count_of_people):
        list_of_names.append(message.text)
        print(list_of_names)
        for user in dict_money:
                if user_id == user['id']:
                    user['list_of_names'] = list_of_names 
                    break
        with open(json_money_path, 'w') as json_file:
            json.dump(dict_money, json_file, ensure_ascii=False,
                                indent=4,  
                                separators=(',',': '))        
        if len(list_of_names) != int(count_of_people):
            await message.answer(f'Введите имя человека под номером - {len(list_of_names) + 1}:', reply_markup = nav.backMain)
        else:
            for user in dict_money:
                    if user_id == user['id']:
                        user['list_of_names'] = list_of_names 
                        break
            with open(json_money_path, 'w') as json_file:
                json.dump(dict_money, json_file, ensure_ascii=False,
                                    indent=4,  
                                    separators=(',',': '))
            await Condi.Money_result.set()
            # list_of_prices = []
            await bot.send_message(message.from_user.id, f'Какую сумму потратил {list_of_names[0]}? (можете отправить фото его чека)', reply_markup = nav.ChekMenu)

@dp.message_handler(state = Condi.Money_result, content_types=['document', 'photo','text'])
async def get_text(message: types.Message):
    if message.text == 'Главное Меню':
        await Condi.Init.set()
        await bot.send_message(message.from_user.id,'Главное Меню', reply_markup = nav.mainMenu)
    elif message.text == '✏️Загрузка чека✏️':
            await Condi.Chekinput.set()
            await bot.send_message(message.from_user.id,'Отправьте мне чек:', reply_markup = nav.backMain)                    
    elif message.text == '✏️Ввод суммы вручную✏️':
            await Condi.ManulChek.set()
            await bot.send_message(message.from_user.id,'Введите сумму:', reply_markup = nav.backMain)  


@dp.message_handler(state = Condi.ManulChek, content_types=['document', 'photo','text'])
async def get_text(message: types.Message):
    user_id = message.from_user.id
    with open(json_money_path, 'r') as fp:
            dict_money = json.load(fp)
        
    for user in dict_money:
        if user_id == user['id']:
            user_exists = True
            count_of_people = user['count_of_people'] 
            list_of_names = user['list_of_names'] 
            list_of_prices = user['list_of_prices']    
            break

    list_of_prices.append(message.text)
    if message.text == 'Главное Меню':
        await Condi.Init.set()
        await bot.send_message(message.from_user.id,'Главное Меню', reply_markup = nav.mainMenu)    
    elif len(list_of_prices) != int(count_of_people):
        for user in dict_money:
                if user_id == user['id']:
                    user['list_of_prices'] = list_of_prices 
                    break
        with open(json_money_path, 'w') as json_file:
            json.dump(dict_money, json_file, ensure_ascii=False,
                                indent=4,  
                                separators=(',',': '))
        await Condi.Money_result.set()
        await message.answer(f'Какую сумму потратил {list_of_names[len(list_of_prices)]}?', reply_markup = nav.ChekMenu)
    else:
        await Condi.Init.set()
        ans = money_result(list_of_names, list_of_prices)
        await bot.send_message(message.from_user.id, ans, reply_markup = nav.mainMen)       


@dp.message_handler(state = Condi.Chekinput, content_types=['document', 'photo','text'])
async def get_photo(message: types.Message):
    if message.text == 'Главное Меню':
        await Condi.Init.set()
        await bot.send_message(message.from_user.id,'Главное Меню', reply_markup = nav.mainMenu)
    user_id = message.from_user.id
    img_path = 'input.jpg'
    await message.photo[-1].download(img_path)
    pred_mount = check_detect(img_path)

    with open(json_money_path, 'r') as fp:
            dict_money = json.load(fp)
        
    for user in dict_money:
        if user_id == user['id']:
            count_of_people = user['count_of_people'] 
            list_of_names = user['list_of_names'] 
            list_of_prices = user['list_of_prices']    
            break

    list_of_prices.append(pred_mount)
    if len(list_of_prices) != int(count_of_people):
        for user in dict_money:
                if user_id == user['id']:
                    user['list_of_prices'] = list_of_prices 
                    break
        with open(json_money_path, 'w') as json_file:
            json.dump(dict_money, json_file, ensure_ascii=False,
                                indent=4,  
                                separators=(',',': '))
        await Condi.Money_result.set()
        await bot.send_message(message.from_user.id, f'Считал Сумму - {pred_mount}')
        await bot.send_message(message.from_user.id, f'Какую сумму потратил {list_of_names[len(list_of_prices)]}? (можете отправить фото его чека)', reply_markup = nav.ChekMenu)
    else:
        await bot.send_message(message.from_user.id, f'Считал Сумму - {pred_mount}')
        ans = money_result(list_of_names, list_of_prices)
        await Condi.Init.set()
        await bot.send_message(message.from_user.id, ans, reply_markup = nav.mainMenu)  

def update_json(user_id, prompt, source):

    with open(json_file_path, 'r') as fp:
        users_dict = json.load(fp)
    
    user_exists = False

    for user in users_dict:
        if user_id == user['id']:
            user_exists = True
            if (source=='habr'):
                if prompt not in user['habr_topic']:
                    user['habr_topic'].append(prompt)
            if (source =='lenta'):
                if prompt not in user['lenta_topic']:
                    user['lenta_topic'].append(prompt)
            break

    if not(user_exists):
        topic = []
        topic.append(prompt)
        if (source=='habr'):
            users_dict.append({
                                "id": user_id,
                                "habr_topic": topic,
                                "lenta_topic": []
                                })
        if (source=='lenta'):
            users_dict.append({
                                "id": user_id,
                                "habr_topic": [],
                                "lenta_topic": topic
                                }) 
 
    # Verify updated list
    print(users_dict)        
    with open(json_file_path, 'w') as json_file:
        json.dump(users_dict, json_file, ensure_ascii=False,
                            indent=4,  
                            separators=(',',': '))
    print('Successfully appended to the JSON file')

# def schedule_jobs():
#     scheduler.add_job(check_news, 'cron', hour = 11, minute=3)
#     # scheduler.add_job(img_loader, 'cron', hour = 18)

async def scheduler():
    aioschedule.every().day.at("09:20").do(check_news)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)

async def on_startup(dp): 
    asyncio.create_task(scheduler())
 
# async def on_startup(dp):
#     schedule_jobs()

if __name__ == '__main__':
    # scheduler.start()
    # executor.start_polling(dp)
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)