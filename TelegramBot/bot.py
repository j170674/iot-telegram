import logging
import telegram
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import  CallbackQueryHandler
from telegram.ext import Updater
import paho.mqtt.client as mqtt
import time
from bandeco import *
import unicodedata
import re

def removerAcentosECaracteresEspeciais(palavra):
    # Unicode normalize transforma um caracter em seu equivalente em latin.
    nfkd = unicodedata.normalize('NFKD', palavra)
    palavraSemAcento = u"".join([c for c in nfkd if not
                                 unicodedata.combining(c)])
    # Usa expressão regular para retornar a palavra apenas com unicode
    return re.sub('[^a-zA-Z0-9\n:()[] \\\]', '', palavraSemAcento)

# Funções de Handler do BOT
def start(bot,update):
    user_name = update.message.chat.first_name
    message= "Hello %s\n"%(user_name)
    bot.send_message(chat_id=update.message.chat_id, text=message)
    print(update)
def almoco_bot(bot,update):
    global bandeco
    bandeco.atualiza_cardapio()
    cardapio_display_telegram(bot,update,bandeco.almoco,refeicao="Almoço")
    cardapio_display_arduino(bot,update,bandeco.almoco,refeicao="Almoco")
def almoco_veg_bot(bot,update):
    bandeco.atualiza_cardapio()
    cardapio_display_telegram(bot,update,bandeco.almoco_veg,refeicao="Almoço Veg")
    cardapio_display_arduino(bot,update,bandeco.almoco_veg,refeicao="Almoco Veg")

def jantar_bot(bot,update):
    global bandeco
    bandeco.atualiza_cardapio()
    cardapio_display_telegram(bot,update,bandeco.jantar,refeicao="Jantar")
    cardapio_display_arduino(bot,update,bandeco.jantar,refeicao="Jantar")
def jantar_veg_bot(bot,update):
    global bandeco
    bandeco.atualiza_cardapio()
    cardapio_display_telegram(bot,update,bandeco.jantar_veg,refeicao="Jantar Veg")
    cardapio_display_arduino(bot,update,bandeco.jantar_veg,refeicao="Jantar Veg")
def cafe_bot(bot,update):
    global bandeco
    bandeco.atualiza_cardapio()
    user_name = update.message.chat.first_name
    message= """
Olá %s,
Café da Manhã de %s (%s) teremos:
%s """%(
        user_name,
        "%d/%d/%d"%(bandeco.dia_cardapio[0],bandeco.dia_cardapio[0],bandeco.dia_cardapio[2]),
        bandeco.dia_semana,
        bandeco.cafe
)
    bot.send_message(chat_id=update.message.chat_id, text=message)

    esp_message = "-CAFE :\n%s\n%s"%(bandeco.dia_semana.capitalize(),
                               "%d/%d/%d"%(bandeco.dia_cardapio[0],bandeco.dia_cardapio[1],bandeco.dia_cardapio[2]))
    send_esp_display_message(esp_message,bot,update)
    time.sleep(2)
    esp_message = "-CAFE :\n%s"% (bandeco.cafe)
    send_esp_display_message(esp_message,bot,update)
    time.sleep(2)

def user_input(bot,update):

    message = update.message.text
    send_esp_display_message(message,bot,update)
    # Debug comment: print user input
    #bot.send_message(chat_id=update.message.chat_id, text=update.message.text)

def get_temp(bot,update):
    client.connect("mqtt.demo.konkerlabs.net", 1883)
    client.publish(publishAddress,  json.dumps("temp"))

    client_internal = mqtt.Client()
    client_internal.username_pw_set(user, password)
    client_internal.connect("mqtt.demo.konkerlabs.net", 1883)
    client_internal.subscribe(subscribeAddress)
    def on_message(client,data,msg):
        message = msg.payload.decode()
        bot.send_message(chat_id=update.message.chat_id, text=message)
        client.loop_stop()
    client_internal.on_message = on_message
    client_internal.loop_start()
def get_hum(bot,update):
    client.connect("mqtt.demo.konkerlabs.net", 1883)
    client.publish(publishAddress,  json.dumps("hum"))

    client_internal = mqtt.Client()
    client_internal.username_pw_set(user, password)
    client_internal.connect("mqtt.demo.konkerlabs.net", 1883)
    client_internal.subscribe(subscribeAddress)
    def on_message(client,data,msg):
        message = msg.payload.decode()
        bot.send_message(chat_id=update.message.chat_id, text=message)
        client.loop_stop()
    client_internal.on_message = on_message
    client_internal.loop_start()

def get_light(bot,update):
    client.connect("mqtt.demo.konkerlabs.net", 1883)
    client.publish(publishAddress,  json.dumps("light"))

    client_internal = mqtt.Client()
    client_internal.username_pw_set(user, password)
    client_internal.connect("mqtt.demo.konkerlabs.net", 1883)
    client_internal.subscribe(subscribeAddress)
    def on_message(client,data,msg):
        message = msg.payload.decode()
        bot.send_message(chat_id=update.message.chat_id, text=message)
        client.loop_stop()
    client_internal.on_message = on_message
    client_internal.loop_start()

def cardapio_display_telegram(bot,update,cardapio,refeicao=None):
    if refeicao:
        user_name = update.message.chat.first_name
        message= """
Olá %s,
%s de %s (%s) teremos:
-Guarnição: %s

-Prato Principal: %s

-Salada: %s

-Sobremesa: %s

-Suco: %s

Obs: %s"""%(
        user_name,
        refeicao,
        "%d/%d/%d"%(bandeco.dia_cardapio[0],bandeco.dia_cardapio[1],bandeco.dia_cardapio[2]),
        bandeco.dia_semana,
        bandeco.extrai_refeicao(cardapio,bandeco.guarnicao),
        bandeco.extrai_refeicao(cardapio,bandeco.prato_principal),
        bandeco.extrai_refeicao(cardapio,bandeco.salada),
        bandeco.extrai_refeicao(cardapio,bandeco.sobremesa),
        bandeco.extrai_refeicao(cardapio,bandeco.suco),
        bandeco.extrai_refeicao(cardapio,bandeco.obs)
)
        bot.send_message(chat_id=update.message.chat_id, text=message)

def cardapio_display_arduino(bot,update,cardapio,refeicao=None):
    if refeicao:
        esp_message = "-%s:\n%s\n%s"%(refeicao,bandeco.dia_semana.capitalize(),
                               "%d/%d/%d"%(bandeco.dia_cardapio[0],bandeco.dia_cardapio[1],bandeco.dia_cardapio[2]))
        time.sleep(2)
        send_esp_display_message(esp_message,bot,update)
        esp_message = "-Guarnicao:\n%s"% bandeco.extrai_refeicao(cardapio,bandeco.guarnicao)
        time.sleep(2)
        send_esp_display_message(esp_message,bot,update)
        esp_message ="-Principal:\n%s"%bandeco.extrai_refeicao(cardapio,bandeco.prato_principal)
        time.sleep(2)
        send_esp_display_message(esp_message,bot,update)
        esp_message ="-Salada:\n%s"%bandeco.extrai_refeicao(cardapio,bandeco.salada)
        time.sleep(2)
        send_esp_display_message(esp_message,bot,update)
        esp_message = "-Sobremesa:\n%s"%bandeco.extrai_refeicao(cardapio,bandeco.sobremesa)
        time.sleep(2)
        send_esp_display_message(esp_message,bot,update)
        esp_message = "-Suco:\n%s"%(bandeco.extrai_refeicao(cardapio,bandeco.suco))
        time.sleep(2)
        send_esp_display_message(esp_message,bot,update)

def send_esp_display_message(message,bot,update):
    client.connect("mqtt.demo.konkerlabs.net", 1883)
    message = removerAcentosECaracteresEspeciais(message)
    list_message = []
    while len(message)>75:
        bw = 50 + message[50:].find(" ") # break word
        client.publish(publishAddress,  json.dumps("display$"+message[0:bw]))
        message = "... "+ message[bw:]
        time.sleep(2)
    client.publish(publishAddress,  json.dumps("display$"+message))

def cardapio_options(bot,update):
    keyboard = [[InlineKeyboardButton("Almoço", callback_data='almoco_bot'),
                 InlineKeyboardButton("Almoço Veg",
                                      callback_data='almoco_veg_bot')],
                [InlineKeyboardButton("Jantar", callback_data='jantar_bot'),
                 InlineKeyboardButton("Jantar Veg",
                                      callback_data='jantar_veg_bot')],
                [InlineKeyboardButton("Café Da Manhã",
                                      callback_data='cafe_bot')]]

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text('Escolha uma refeição:', reply_markup=reply_markup)

def sensors_options(bot,update):
    keyboard = [[InlineKeyboardButton("Temperatura", callback_data='get_temp'),
                 InlineKeyboardButton("Luminosidade",
                                      callback_data='get_light')],

                [InlineKeyboardButton("Umidade",
                                      callback_data='get_hum')]]

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text('Escolha um sensor:', reply_markup=reply_markup)

def button_choice(bot,update):
    query = update.callback_query
    query.edit_message_text(text="Opção recebida")
    user_choice = str(query.data)
    eval(user_choice)(bot,update.callback_query)

### MAIN ###
# Setting up logger
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)
#token_telegram = '666164429:AAFPkMnbqRKXqCPvv-OtycJ5K5y4RQ3k_U4'
token_vina = '850097657:AAHEHdl6HrpDYKb2_9nKPFDx1eQkBMyW7xg'
bot = telegram.Bot(token=token_vina)

# CLIENT MQTT
user = "ou83rio3h43j"
password = "anioaDro9R87"
publishAddress = "data/ou83rio3h43j/pub/out"
subscribeAddress = "data/ou83rio3h43j/sub/in"
client = mqtt.Client()
client.username_pw_set(user, password)

# global variable set to craw restaurant data
global bandeco
bandeco = Bandeco()
updater = Updater(token=token_vina)
dispatcher = updater.dispatcher
almoco_handler = CommandHandler('almoco', almoco_bot)
almoco_veg_handler = CommandHandler('almoco_veg', almoco_veg_bot)
jantar_handler = CommandHandler('jantar', jantar_bot)
jantar_veg_handler = CommandHandler('jantar_veg', jantar_veg_bot)
cafe_handler = CommandHandler('cafe', cafe_bot)
start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)
updater.dispatcher.add_handler(CommandHandler('sensors', sensors_options))
updater.dispatcher.add_handler(CommandHandler('cardapio', cardapio_options))
updater.dispatcher.add_handler(CallbackQueryHandler(button_choice))
get_temp_handler = CommandHandler('temp',get_temp)
get_hum_handler = CommandHandler('hum',get_hum)
get_light_handler = CommandHandler('light',get_light)
user_input_handler = MessageHandler(Filters.text,user_input)
sensors_options_handler = CommandHandler("sensors",sensors_options)
dispatcher.add_handler(sensors_options_handler)
dispatcher.add_handler(user_input_handler)
dispatcher.add_handler(almoco_handler)
dispatcher.add_handler(almoco_veg_handler)
dispatcher.add_handler(jantar_handler)
dispatcher.add_handler(jantar_veg_handler)
dispatcher.add_handler(cafe_handler)
dispatcher.add_handler(get_temp_handler)
dispatcher.add_handler(get_hum_handler)
dispatcher.add_handler(get_light_handler)
updater.start_polling()

#updater.idle()
#updater.stop()
#
