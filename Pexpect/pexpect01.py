
import pexpect
import sys

# Definindo variaveis para não ter que repitir e/ou deixar mais facil a edição no decorrer do script
ic = '192.168.139.138'
usuario = 'carlos'
senha = '1234'
enable = '1234'

# Usando o modelo de formatação com o old-format
objeto = pexpect.spawn('telnet %s' % (ic), encoding='utf-8')
print('Logando no equipamento %s' % (ic))

objeto.logfile = sys.stdout
objeto.expect('Username:')
objeto.sendline(usuario)
objeto.expect('Password:')
objeto.sendline(senha)
objeto.expect('>')
objeto.sendline('enable')
objeto.sendline(enable)
print('dentro do if')

objeto.sendline('sh ip int br')
objeto.send('exit\n')
objeto.expect(pexpect.EOF)
