#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket, sys, ssl, os
from pathlib import Path
from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfilename

class Principal:

	def __init__(self, root):
		self.inicio = ttk.Label(root, text = "Envie seu arquivo clicando nos botões abaixo: ")
		self.inicio.grid(row = 0, column = 0, columnspan = 2)

		self.lbIpServer = ttk.Label(root, text="Endereço do servidor: ").grid(row=1, column=0)
		self.txtIpServer = ttk.Entry(root)
		self.txtIpServer.insert(0, "localhost")
		endereco = str(self.txtIpServer.get())
		self.txtIpServer.grid(row=1, column=1)

		self.lbPortControl = ttk.Label(root, text="Porta - Controle: ").grid(row=2, column=0)
		self.txtPortControl = ttk.Entry(root)
		self.txtPortControl.insert(0, "9999")
		portassl = int(self.txtPortControl.get())
		self.txtPortControl.grid(row=2, column=1)

		self.lbPortData = ttk.Label(root, text="Porta - Dados: ").grid(row=3, column=0)
		self.txtPortData = ttk.Entry(root)
		self.txtPortData.insert(0, "54321")
		portadados = int(self.txtPortData.get())
		self.txtPortData.grid(row=3, column=1)

		# seleção do arquivo para envio
		arquivo = StringVar()
		self.txtSelectButton = ttk.Entry(root, textvariable = arquivo, width=30)
		self.txtSelectButton.config(state='disabled')
		self.txtSelectButton.grid(row=4, column=1)

		self.btnSelectButton = ttk.Button(root, text = 'Selecionar Arquivo', command = self.askfile)
		self.btnSelectButton.grid(row = 4, column = 0)


		self.btnSend = ttk.Button(root, text = 'Enviar', command = lambda:self.resposta(arquivo.get(), endereco, portassl, portadados))
		self.btnSend.grid(row = 5, column = 0)
		self.btnQuit = ttk.Button(root, text = 'Sair', command = quit)
		self.btnQuit.grid(row = 5, column = 1)

	def askfile(self):
		fname = askopenfilename()
		self.txtSelectButton.config(state='enabled')
		self.txtSelectButton.delete(0, END)
		self.txtSelectButton.insert(0, fname)
		return str(fname)

	def resposta(self, f1, e1, p1, p2):
		janela = Tk()
		conexao = Conexao.conectar(f1, e1, p1, p2)
		mensagem = ttk.Label(janela, text = conexao)
		mensagem.grid(row=0, column=0, columnspan=2)

class Conexao:
	def conectar(nomearquivo, eserver, pssl, pdados):
		try:
			os.stat(nomearquivo)
		except FileNotFoundError:
			return 'Arquivo não existe. Por favor, verifique essa situação.'
		else:
			try:
				s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #tem que ser SOCK_STREAM senão o SSL não funciona
				s2.connect((eserver, pdados)) # essa cnx só existe para mandar o nome do arquivo e nao conflitar
				s2.send(nomearquivo.encode('utf-8')) # manda o nome do arquivo para o server
				s2.shutdown(socket.SHUT_RDWR)
				s2.close() # encerra a cnx
			except ConnectionRefusedError:
				return 'Conexão recusada. Por favor, verifique se a porta está aberta ou existe uma conexão funcional.'
			except:
				return 'Erro Desconhecido'

			try:
				s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				ssl_s1 = ssl.wrap_socket(s1, server_side=False, certfile="./cert/client.pem", keyfile="./cert/client.key") # aqui que funciona a mágica! faz o ssl funcionar
				ssl_s1.connect((eserver, pssl))
			except ConnectionRefusedError:
				return 'Conexão recusada. Por favor, verifique se a porta está aberta ou existe uma conexão funcional.'
			except:
				return 'Erro desconhecido'

			f = open (nomearquivo, "rb") # abre o arquivo pedido
			l = f.read(1024)
			while (l): # faz a leitura e envia o arquivo para o servidor
				ssl_s1.send(l)
				l = f.read(1024)
			f.close()
			ssl_s1.shutdown(socket.SHUT_RDWR)
			ssl_s1.close()
			s1.close()
			return 'Arquivo enviado. Conexão encerrada!'

def main():
	root = Tk()
	janela = Principal(root)
	root.mainloop()

# Cria a instancia
if __name__ == '__main__': main()
