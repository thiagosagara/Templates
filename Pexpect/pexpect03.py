import pexpect
import sys

file_equips = 'equips.txt'

# cria agora uma variavel para os comandos que iremos executar
file_comandos = 'cmd.txt'

usuario = 'carlos'
senha = '1234'
enable = '1234'

abre_devices = open(file_equips, 'r')
le_devices = abre_devices.read().splitlines()

abre_comandos = open(file_comandos, 'r')
le_comandos = abre_comandos.read().splitlines()

for ic in le_devices:
  objeto = pexpect.spawn('telnet %s' % (ic), encoding='utf-8')
  print('Logando no equipamento %s' % (ic))
  objeto.logfile = sys.stdout
  objeto.expect('Username:')
  objeto.sendline(usuario)
  objeto.expect('Password:')
  objeto.sendline(senha)
  prompt = objeto.expect(['>','#'])
  if prompt == 0:
    objeto.sendline('enable')
    objeto.sendline(enable)
  
  # cria um dor para executar os comandos do arquivo (cmd.txt)
  for cmd in le_comandos:
    objeto.sendline(cmd)
  objeto.sendline('end')
  objeto.send('exit\n')
  objeto.expect(pexpect.EOF)
