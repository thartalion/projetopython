#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# comando para gerar os certificados
# openssl req -new -x509 -days 365 -nodes -receive server.pem -keyout server.key
# openssl req -new -x509 -days 365 -nodes -receive client.pem -keyout client.key

# Como usar:
# python3 server.py
# o arquivo baixado fica no mesmo diretório do arquivo py
#
#
# TO-DO
# usar o mesmo socket para mandar o nome do arquivo e o próprio arquivo
#
#
# Recebe arquivos do client.py

import os, socket, sys, ssl

def main(self):
    porta = 9999 #porta do ssl
    host = 'localhost' # host do ssl

    print("=== Servidor inicializado ===")

    # esse bloco recebe o nome do arquivo, através de uma cnx exclusiva na porta 54321
    s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s2.bind(("localhost",54321))
    s2.listen(1)
    print("Porta 54321 aberta e esperando cnx")

    # aqui informa os dados do cliente conectado
    cnx, endereco = s2.accept()
    print ('Conexão aceita de:', endereco)
    arquivo = os.path.basename(cnx.recv(1024).decode('utf-8'))
    print('Nome do arquivo a receber: ', arquivo)
    cnx.close()
    s2.shutdown(socket.SHUT_RDWR)
    s2.close()

    s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #s1.settimeout(5) # aqui é um truque interessante: não fica esperando eternamente por alguém na cnx
    s1.bind((host, porta))
    s1.listen(1)
    print("Porta do ssl aberta e esperando cnx")

    while True:
        sc, address = s1.accept()
        cnxssl = ssl.wrap_socket(sc, server_side=True, certfile="./cert/server.pem", keyfile="./cert/server.key") # aqui faz o wrap do ssl :: prestar atenção no server_side=True
        f = open("./receive/"+arquivo,'wb') # abre um arquivo dummy para receber o conteúdo e poder gravar
        while True:
            l = cnxssl.recv(1024)
            f.write(l)
            if not l:
                break
        f.close()
        cnxssl.close()
        break
        print("Arquivo recebido!")

    s1.shutdown(socket.SHUT_RDWR)
    s1.close()
    print("Conexão encerrada! Arquivo recebido com sucesso!")

if __name__ == '__main__': main()