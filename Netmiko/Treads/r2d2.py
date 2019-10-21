# r2d2.py -     Efetua configurações em todos os equpamentos do arquivo (devices-file.txt)
#                       Com base no arquivo de credenciais (devices-creds.txt)
#
# Homepage      : https://thiagosagara.blogspot.com/
# Autor         : thiagosagara@gmail.com
#
#-------------------------------------------------------------------------------------
# Este programa utiliza os arquivos devices-file.txt e devices-creds.txt para acesso aos
# ICs e gera um arquivo na pasta evidencias com o nome <IC>.cfg com a saida dos comandos.
#
#-------------------------------------------------------------------------------------
#
# Histórico:
#
#       v1.0 XX/XX/XXXX, Thiago Marques
#               - Versão inicial
#       v1.1 16/11/2017, Thiago Marques
#               - Iniciando a documentação
#
# COPYRIGHT: Programa desenvolvido com Python3 (GPL)
#



from pprint import pprint
from netmiko import ConnectHandler
#import json
from time import time

from multiprocessing.dummy import Pool as ThreadPool

def read_devices( devices_filename ):

  # cria um dicionario para armazenar as informacoes dos equipamentos
  devices = {}

  # Abre o arquivo recebido do programa
  with open( devices_filename ) as devices_file:

    for device_line in devices_file:
      # separa as informacoes do arquivo de equipamentos
      ic_info = device_line.strip().split(',')

      # Cria um dicionario generico para cada equipamento no arquivo
      # na linha abaixo, ele joga esta informacao no dicionario criado no comeco da funcao
      ic = {'ipaddr':  ic_info[0],
            'type':    ic_info[1],
            'name':    ic_info[2]}
#            'verbose': ic_info[3]}

      # Alimenta o dicionario princial (devices) com as informacoes do generico
      # utiliza o IP do equipamento como chave no dicionario
      devices[ic['ipaddr']] = ic

    print('\n----- Equipamentos --------------------------')
    pprint( devices )

    return devices

def read_device_creds( device_creds_filename ):

  print('\n... Coletando credenciais ...\n')

  # cria um dicionario para armazenar as informacoes das credenciais
  devices_creds = {}

  # Abre o arquivo recebido do programa
  with open( device_creds_filename ) as devices_creds_file:

    for device_creds_line in devices_creds_file:
      # separa as informacoes do arquivo de credenciais
      ic_info = device_creds_line.strip().split(',')

      # Cria um dicionario generico para cada equipamento no arquivo
      # na linha abaixo, ele joga esta informacao no dicionario criado no comeco da funcao
      ic_creds = {'ipaddr':     ic_info[0],
                  'username':   ic_info[1],
                  'password':   ic_info[2],
                  'secret':     ic_info[3]}

      # Alimenta o dicionario princial (devices) com as informacoes do generico
      # utiliza o IP do equipamento como chave no dicionario
      devices_creds[ic_creds['ipaddr']] = ic_creds


  print('\n----- devices_creds --------------------------')

  pprint( devices_creds )

  return devices_creds

def config_worker( device_and_creds ):

  # Recebe os dicionarios de equipamentos e credenciais do programa
  device = device_and_creds[0]
  creds  = device_and_creds[1]
  # local dos comandos
  os.chdir('/opt/scripts/py/r2d2/dev/')
  arq_comandos = 'cmds.txt'
  global output
  output = ''


  #--------------------------------------------------------------------------------------------------------
  # Aqui ele comeca a usar o netmiko, mas pode fazer com pexpect tb
  # so remover dessa linha para baixo e fazer algo como:
  #
  #
  #     with open('device_list.csv') as csvfile:
  #      readCSV = csv.reader(csvfile, delimiter=',')
  #      next(readCSV, None)
  #      for row in readCSV:
  #          hostname = device['name']
  #          ip_address = device['ipaddr']
  #          username = creds['username']
  #          passwd = creds['password']
  #          timestr = time.strftime("%Y%m%d-%H%M%S")
  #          print("Collecting info for device:" + hostname)
  #          child = pexpect.spawn('telnet ' + ip_address, encoding = 'utf-8')
  #          fout = open(hostname + 'logs' + timestr + '.txt', 'w')
  #          child.logfile = fout
  #          child.expect('Login:')
  #          child.sendline(username)
  #          child.expect('[pP]assword:')
  #          child.sendline(passswd')
  #
  #--------------------------------------------------------------------------------------------------------

  #----- O exemplo abaixo e usando o netmiko
  #---- Escolha do tipo (plataform) dos equipamentos ----
  #--- Toma o cisco_ios como default
  if   device['type'] == 'cisco_nxos': device_type = 'cisco_nxos'
  elif device['type'] == 'cisco_ios':  device_type = 'cisco_ios'
  elif device['type'] == 'cisco-wlc':  device_type = 'cisco_wlc'
  elif device['type'] == 'brocade':    device_type = 'brocade_nos'
  elif device['type'] == 'bigip':      device_type = 'f5_ltm'
  elif device['type'] == 'linux':      device_type = 'linux'
  else:                                device_type = 'cisco_ios'

  print('---- Conectando no equipamento {0}, username={1}, password={2}'.format( device['ipaddr'],
                                                                                creds['username'], creds['password'] ))

  #---- Cria instancia da sessao e se conecta com os parametros coletados
  session = ConnectHandler( device_type=device_type, ip=device['ipaddr'],
                              username=creds['username'], password=creds['password'], secret=creds['secret'] )

  #---- Comandos para Nexus

  if device_type == 'cisco_nxos':

    print('---- Gerando configuracao do equipamento {0}'.format( device['name']))

    f = open(arq_comandos, 'r')
    lista_comandos = f.read().splitlines()
    for cmd in lista_comandos:
      output = session.send_command(cmd, expect_string=r'Carlos123')
      with open( config_filename, 'a' ) as config_out:  config_out.write( output )
      print('config executada')
    f.close()
    session.disconnect()

  #---- Comandos para IOS
  if device_type == device_type == 'cisco_ios':

    print('---- Gerando configuracao do equipamento {0}'.format( device['name']))
    f = open(arq_comandos, 'r')
    lista_comandos = f.read().splitlines()
    for cmd in lista_comandos:
      output = session.send_command(cmd, expect_string=r'Carlos123')
      with open( config_filename, 'a' ) as config_out:  config_out.write( output )
      print('config executada')
    f.close()
    session.disconnect()

  if device_type == 'cisco_wlc':
    comandos = ['config paging disable','show run-config']
    print('---- Gerando configuracao do equipamento {0}'.format( device['name']))
    for cmd in comandos:
      output = session.send_command(cmd)

  if device_type == 'brocade_nos':
    comandos = ['skip-page-display','show running-config']
    print('---- Gerando configuracao do equipamento {0}'.format( device['name']))
    for cmd in comandos:
      output = session.send_command(cmd)

  if device_type == 'f5_ltm':
    comandos = ['rm /var/local/ucs/bkpucs.ucs','tmsh save sys ucs bkpucs']
    print('---- Gerando configuracao do equipamento {0}'.format( device['name']))
    for cmd in comandos:
      output = session.send_command(cmd)

  if device_type == 'linux':
    comandos = ['cat /equipamentos > /backup','cat /credenciais > /backup_cred']
    print('---- Gerando configuracao do equipamento {0}'.format( device['name']))
    for cmd in comandos:
      output = session.send_command(cmd)


  #---- Salvando configuracoes
  # Cria um arquivo para cada equipamento
  config_filename = device['ipaddr'] + '.cfg'

  print('\n>>>>> Equipamento    \033[1;32m{0}\033[m configurado com \033[1;44m sucesso \033[m'.format(device['ipaddr']))
  print('>>>>> Criando arquivo: \033[1;32mevidencias/{0}\033[m'.format(config_filename))
  with open( config_filename, 'w' ) as config_out:  config_out.write( output )
  os.system('mv *cfg evidencias/')
  print('>>>>> Deslogando do    \033[1;32m{0}\033[m'.format(device['ipaddr']))


  return

#==============================================================================
# ---- Inicio do programa
#==============================================================================
if __name__ == '__main__':
  devices = read_devices( 'devices-file.txt' )
  creds   = read_device_creds( 'devices-creds.txt' )

  num_threads_str = input( '\nQuantidade de processos (5): ' ) or '5'
  num_threads     = int( num_threads_str )
  #num_threads  = 3

  #---- Cria a lista e passa como parametro para a funcao de automatizacao
  config_params_list = []
  for ipaddr,device in devices.items():
    config_params_list.append( ( device, creds[ipaddr] ) )

  # loga o tempo inicial
  starting_time = time()

  # cria os pools e lo
  print('\n--- Criando o pool de conexao\n')
  threads = ThreadPool( num_threads )
  results = threads.map( config_worker, config_params_list )

  # Fecha as conexoes
  threads.close()
  threads.join()

  print('\n---- Fim das configs, Tempo gasto=', time()-starting_time)

