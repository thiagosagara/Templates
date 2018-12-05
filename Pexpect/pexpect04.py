import pexpect
import sys

file_equips = 'equips.txt'
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
  
  # metodo para validar se a conexão foi recusada ou aceita via telnet, se foi recusada ele tenta acesso via ssh
  metodo = objeto.expect(['Username:','refused'])
  if metodo == 0:
    objeto.sendline(usuario)
    objeto.expect('Password:')
    objeto.sendline(senha)
    prompt = objeto.expect(['>','#'])
    if prompt == 0:
      objeto.sendline('enable')
      objeto.sendline(enable)

    for cmd in le_comandos:
      objeto.sendline(cmd)
    objeto.sendline('end')
    objeto.send('exit\n')
    objeto.expect(pexpect.EOF)
    
  else:
    objeto_ssh = pexpect.spawn('ssh %s@%s' % (usuario, ic), encoding='utf-8')
    objeto_ssh.logfile = sys.stdout
    
    # possui um regex para password com P ou p
    objeto_ssh.expect('[pP]assword:')
    objeto_ssh.sendline(senha)

    prompt = objeto_ssh.expect(['>','#'])
    if prompt == 0:
      objeto_ssh.sendline('enable')
      objeto_ssh.sendline(enable)

    for cmd in le_comandos:
      objeto_ssh.sendline(cmd)

    objeto_ssh.sendline('end')
    objeto_ssh.send('exit\n')
    objeto_ssh.expect(pexpect.EOF)
