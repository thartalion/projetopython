Transfere arquivo, via SSL, de um computador a outro.

Execute o arquivo inter_serv.py primeiro e depois o inter_cli.py.

A configuração do arquivo é para transferência local. 

O ideal é que inicialize o servidor e logo em seguida pedir para enviar o arquivo do cliente, pois deixei com timeout de 5 segundos para não deixar a tela travada.

A conexão é feita via ssl, com os certificados instalados no diretorio cert, tanto do client, quanto do server.

Fiz a interface gráfica para facilitar o uso e também deixar o projeto mais agradável, pois parecia que tinha pouca coisa.