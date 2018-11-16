#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# comando para gerar os certificados
# openssl req -new -x509 -days 365 -nodes -receive server.pem -keyout server.key
# openssl req -new -x509 -days 365 -nodes -receive client.pem -keyout client.key

# Como usar:
# python3 client.py
#
# Envia arquivos para o server.py

import socket, sys, ssl

__version__ = "0.0.1"

class Conexao:
    def conectar(self, nomearquivo, endereco, portassl, portadados):

        s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #tem que ser SOCK_STREAM senão o SSL não funciona
        s2.connect((endereco, portadados)) # essa cnx só existe para mandar o nome do arquivo e nao conflitar
        s2.send(nomearquivo.encode('utf-8')) # manda o nome do arquivo para o server
        s2.shutdown(socket.SHUT_RDWR)
        s2.close() # encerra a cnx

        print("Pressione enter para enviar o arquivo")
        input()

        s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ssl_s1 = ssl.wrap_socket(s1, server_side=False, certfile="./cert/client.pem", keyfile="./cert/client.key") # aqui que funciona a mágica! faz o ssl funcionar
        ssl_s1.connect((endereco, portassl))

        f = open (nomearquivo, "rb") # abre o arquivo pedido
        l = f.read(1024)
        while (l): # faz a leitura e envia o arquivo para o servidor
            ssl_s1.send(l)
            l = f.read(1024)
        f.close()
        ssl_s1.shutdown(socket.SHUT_RDWR)
        ssl_s1.close()
        s1.close()
        return "Arquivo enviado. Conexão encerrada!"