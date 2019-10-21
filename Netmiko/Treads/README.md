# Utilização


 Prereqs:
  - Netmiko
  - pprint
	- arquivo devices-creds.txt
	- arquivo devices-file.txt

Para instalação do prereq utilize:

	`pip install netmiko
	pip install pprint`
 
 
O script utiliza o netmiko e a função de multithread para abrir sessões simultaneas (por padrão ele abre 5).

Ele le os arquivos .txt, e cria dicionarios com eles.
Com base nesses dicionarios utiliza a função run_config, que necessariamente é quem vai executar os comandos.

no script ele usa o seguinte diretório como base: */opt/scripts/py/r2d2/dev/*, caso queria manter o mesmo, crie a mesma arvore de diretório, ou altere a linha 98 do script.

Cabe ressaltar que ele vai procurar nessa pasta o arquivo cmd.txt (arquivo dos comandos).


Créditos para as funções: David Bombal, só adicionei algumas outras coisas.
