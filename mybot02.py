import telebot
import datetime
import time
import pandas as pd
import logging
import sys
import os

# CCSSantander
# CCSSantander_bot

#bot = telebot.TeleBot("1139297477:AAGRzt_zZ5pQApX9v3dpPN-kMLKhQrcCcn8")
bot = telebot.TeleBot("1245786001:AAEGA4bpp1AI56Hyydate-L9R6I2nM_BOE8")

#########################   

# Librerias locales
from sartools.wx2 import wxlei
from sartools.odas import waves

@bot.message_handler(commands=['start'])
def send_welcome(message):
	#print(message)  # imprimo el message por consola para obtener el diccionario
	chatid = message.chat.id
	nombreUsuario = message.chat.first_name + " " + message.chat.last_name
	print("Ha activado el bot (START): ",nombreUsuario)
	saludo = "Hola {} bienvenido al bot"
	bot.send_message(chatid, saludo.format(nombreUsuario))

@bot.message_handler(commands = ["wxsdr"])
def wx_sdr(message):
	chatid = message.chat.id
	nombreUsuario = message.chat.first_name + " " + message.chat.last_name
	print("Ha activado el bot (WXSDR): ",nombreUsuario)
	texto_devolver = wxlei()
	bot.send_message(chatid,texto_devolver)
	#print(texto_devolver)

@bot.message_handler(commands = ["odas"])
def odas_sdr(message):
	chatid = message.chat.id
	nombreUsuario = message.chat.first_name + " " + message.chat.last_name
	print("Ha activado el bot (ODAS): ",nombreUsuario)
	texto_devolver1 = waves()
	bot.send_message(chatid,texto_devolver1)
	#print(texto_devolver1)

@bot.message_handler(commands = ["del"])
def delete (message):
	dir = "C:/Datos_Boyas/"
	fich = os.listdir(dir)
	chatid =message.chat.id
	nombreUsuario = message.chat.first_name + " " + message.chat.last_name
	print("Ha activado el bot (DEL): ",nombreUsuario)
	for item in fich:
		if item.endswith(".txt"):
			os.remove(dir+item)
	mensaje = "Los ficheros de 'C:/Datos_Boyas/' han sido borrados"
	bot.send_message(chatid,mensaje)

@bot.message_handler(commands=['help']) # Ayuda sobre comandos
def help (message):
	chatid = message.chat.id
	nombreUsuario = message.chat.first_name + " " + message.chat.last_name
	print("Ha activado el bot (HELP): ",nombreUsuario)
	bot.send_message(chatid,"""
	#### Valid options ####
	This bot accepts commands:
	/start
	/help
	/wxsdr
	/odas
	/del
""")

print("""
The bot is working...
CTRL-C to stop the bot
""")
#print("El bot se esta ejecutando")
bot.polling()
