# importar os modulos
import pexpect
import sys

# instancia o pexpect para logar no equipamento via telnet
# o 'encoding='utf-8' é necessario quando vc utiliza o python3
objeto = pexpect.spawn('telnet 192.168.139.138', encoding='utf-8')


print('Logando no equipamento 192.168.139.138')

# Usado para mostrar a saida na tela
objeto.logfile = sys.stdout

# comandos baseado em 'espere e faça'
objeto.expect('Username:')
objeto.sendline('carlos')
objeto.expect('Password:')
objeto.sendline('1234')
objeto.expect('>')
objeto.sendline('enable')
objeto.sendline('1234')
objeto.sendline('sh ip int br')
objeto.send('exit\n')

# Espera o fim do arquivo, sem essa linha o script vai ficar esperando o timeout para finalizar.
objeto.expect(pexpect.EOF)
