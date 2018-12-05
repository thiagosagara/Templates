import pexpect
import sys

# Usando um arquivo externo para carregar os equipamentos, ao inves de colocar tudo no mesmo arquivo.
file_equips = 'equips.txt'

usuario = 'carlos'
senha = '1234'
enable = '1234'

# Abre o arquivo em modo de leitura
abre_devices = open(file_equips, 'r')

# carrega todos os equipamentos que estão no arquivo
# o splitlines serve para colocar um 'enter' entre os equipamentos, do contrario ele vai concatenar tudo em uma linha só
le_devices = abre_devices.read().splitlines()

# cria um loop para executar um conjunto de comandos para cada equipamento na lista (equips.txt)
for ic in le_devices:
  objeto = pexpect.spawn('telnet %s' % (ic), encoding='utf-8')
  print('Logando no equipamento %s' % (ic))
  objeto.logfile = sys.stdout
  objeto.expect('Username:')
  objeto.sendline(usuario)
  objeto.expect('Password:')
  objeto.sendline(senha)
  
  # cria uma variavel para validar em qual prompt a console caiu, se caiu no '>' ele vai dar um enable;
  prompt = objeto.expect(['>','#'])
  if prompt == 0:
    objeto.sendline('enable')
    objeto.sendline(enable)
    print('dentro do if')

  objeto.sendline('sh ip int br')
  objeto.send('exit\n')
  objeto.expect(pexpect.EOF)
