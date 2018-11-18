#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket, sys, ssl, os
from pathlib import Path
from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askdirectory


class Principal:

    root = Tk()
    root.title("Transferir arquivo - servidor")

    def __init__(self):
        pass

    def roda(self):
        self.janela()
        self.root.mainloop()

    def janela(self):
        self.inicio = ttk.Label(self.root, text="Para iniciar o servidor, insira os dados abaixo:")
        self.inicio.grid(row=0, column=0, columnspan=2)

        self.lbIpServer = ttk.Label(self.root, text="Endereço do servidor: ").grid(row=1, column=0)
        self.txtIpServer = ttk.Entry(self.root)
        self.txtIpServer.insert(0, "localhost")
        endereco = str(self.txtIpServer.get())
        self.txtIpServer.grid(row=1, column=1)

        self.lbPortControl = ttk.Label(self.root, text="Porta - Controle: ").grid(row=2, column=0)
        self.txtPortControl = ttk.Entry(self.root)
        self.txtPortControl.insert(0, "9999")
        portassl = int(self.txtPortControl.get())
        self.txtPortControl.grid(row=2, column=1)

        self.lbPortData = ttk.Label(self.root, text="Porta - Dados: ").grid(row=3, column=0)
        self.txtPortData = ttk.Entry(self.root)
        self.txtPortData.insert(0, "54321")
        portadados = int(self.txtPortData.get())
        self.txtPortData.grid(row=3, column=1)

        # seleção do arquivo para envio
        diretorio = StringVar()
        self.txtSelectButton = ttk.Entry(self.root, textvariable=diretorio, width=30)
        self.txtSelectButton.config(state='disabled')
        self.txtSelectButton.grid(row=4, column=1)

        self.btnSelectButton = ttk.Button(self.root, text='Onde salvar', command=self.askfile)
        self.btnSelectButton.grid(row=4, column=0)

        self.btnSend = ttk.Button(self.root, text='Iniciar servidor',
                                  command=lambda: self.conectar(diretorio.get(), endereco, portassl, portadados))
        self.btnSend.grid(row=5, column=0)
        self.btnQuit = ttk.Button(self.root, text='Sair', command=quit)
        self.btnQuit.grid(row=5, column=1)

        self.txtStatus = Text(self.root, width=50, height=20)
        self.txtStatus.grid(row=6, column=0, columnspan=2)

    def status(self):
        print("Retorno")

    def askfile(self):
        fdir = askdirectory()
        self.txtSelectButton.config(state='enabled')
        self.txtSelectButton.delete(0, END)
        self.txtSelectButton.insert(0, fdir)

    def conectar(self, diretorio, eserver, pssl, pdados):
        # esse bloco recebe o nome do arquivo, através de uma cnx exclusiva na porta 54321
        s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s2.bind((eserver, pdados))
        try:
            s2.settimeout(5)
            s2.listen(1)
            self.txtStatus.insert(INSERT, diretorio + '\n')
            self.txtStatus.insert(INSERT, "=== Servidor inicializado ===" + '\n')
            self.txtStatus.insert(INSERT, "Porta de Dados OK" + '\n')
            self.txtStatus.insert(INSERT, "Porta dados aberta e esperando cnx" + '\n')
            self.root.update()
            cnx, endereco = s2.accept()
        except socket.timeout:
            self.txtStatus.insert(INSERT, "Socket Timeout" + '\n')
        else:
            self.txtStatus.insert(INSERT, "Conexão aceita de:" + str(endereco) + '\n')
        arquivo = os.path.basename(cnx.recv(1024).decode('utf-8'))
        self.txtStatus.insert(INSERT, "Nome do arquivo a receber: " + str(arquivo) + '\n')
        cnx.close()
        s2.shutdown(socket.SHUT_RDWR)
        s2.close()

        s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s1.bind((eserver, pssl))
        s1.listen(1)
        self.txtStatus.insert(INSERT, "Porta ssl aberta e esperando cnx" + '\n')

        while True:
            sc, address = s1.accept()
            cnxssl = ssl.wrap_socket(sc, server_side=True, certfile="./cert/server.pem",
                                     keyfile="./cert/server.key")  # aqui faz o wrap do ssl :: prestar atenção no server_side=True
            f = open(diretorio + '/' + arquivo, 'wb')  # abre um arquivo dummy para receber o conteúdo e poder gravar
            while True:
                l = cnxssl.recv(1024)
                f.write(l)
                if not l:
                    break
            f.close()
            cnxssl.close()
            break
            self.txtStatus.insert(INSERT, "Arquivo recebido!" + '\n')

        s1.shutdown(socket.SHUT_RDWR)
        s1.close()
        self.txtStatus.insert(INSERT, "Conexão encerrada! Arquivo recebido com sucesso!" + '\n')


def main():
    tela = Principal()
    tela.roda()


# Cria a instancia
if __name__ == '__main__': main()