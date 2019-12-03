from tkinter import *
from tkinter.messagebox import showerror
import socket
from pickle import loads, dumps
from re import fullmatch

ip_pattern = r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b"

WIDTH = 800
HEIGHT = 600
SEG_SIZE = 20
IN_GAME = True


def connection_menu():
	menu = Toplevel()
	menu.title('Connect')
	menu.geometry('300x80')
	menu.resizable(False, False)
	menu.wm_attributes("-topmost", 1)
	up_label = Label(menu, text='Введите IP компьютера на котором\nзапущен сервер или запустите свой.')
	label = Label(menu, text='IP сервера')
	entry = Entry(menu, width=15)

	def connect():
		ip = entry.get()
		if fullmatch(ip_pattern, ip):
			try:
				conn.connect((ip, 14900))
				menu.destroy()
			except socket.error:
				showerror(title='Упс...', message='Ошибка подключения')
		else:
			showerror(title='Упс...', message='Некорректный IP')

	button = Button(menu, text="Connect", command=connect)
	up_label.pack(expand=1)
	label.pack(side=LEFT, expand=1)
	entry.pack(side=LEFT, expand=1)
	button.pack(side=LEFT, expand=1)


def start_game():
	pass

if __name__ == '__main__':
	root = Tk()
	root.title("Snake")
	root.resizable(False, False)
	c = Canvas(root, width=WIDTH, height=HEIGHT, bg="#DAA520")
	c.grid()
	c.focus_set()
	conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	conn.settimeout(5)
	connection_menu()
	start_game()
	root.mainloop()

