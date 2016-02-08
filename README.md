# rcmd - remote command
#### Descrição

rcmd é um programa desenvolvido para executar o mesmo comando em diversos servidores. rcmd utiliza a implementação de Threads do Python, o que barateia seu custo de execução e agiliza o retorno da execução dos comandos remotos.

#### Pré-requisitos

rcmd utiliza o módulo Paramiko para criar e gerenciar as conexões SSH. Para instalar deve ser simples como:

```
pip install paramiko
```

Caso isto não funcione é possível baixar e compilar o módulo manualmente: https://pypi.python.org/pypi/paramiko/

#### Uso

```
Uso: usage: ./rcmd.py [-h] -H [HOSTS [HOSTS ...]] [-l LOGIN] -c COMANDO [-p PASSWORD]
optional arguments:
  -h, --help            show this help message and exit
  -H [HOSTS [HOSTS ...]], --hosts [HOSTS [HOSTS ...]]
                        Um ou mais hosts para conectar
  -l LOGIN, --login LOGIN
                        Login utilizado para conectar no(s) servidor(es)
  -c COMANDO, --comando COMANDO
                        Comando a executar (Utilize aspas para varios args)
  -p PASSWORD, --password PASSWORD
                        Senha do login. Se nao fornecido um prompt surgira.
                        
```

#### Exemplos

rcmd aceita a execução de um comando para um unico host:

```
root@osboxes:/opt/scripts/rcmd# ./rcmd.py -H 192.168.56.101 -c "uname -nsr" -l mvarge
Password:
Thread-0-192.168.56.101::INFO: Linux centos7 3.10.0-327.el7.x86_64
```

Ou para diversos hosts, bem como expansão de shell:

```
root@osboxes:/opt/scripts/rcmd# ./rcmd.py -H 192.168.56.101 192.168.56.10{2,3} -c "uname -nsr" -l mvarge
Password:
Thread-2-192.168.56.103::INFO: Linux centos6 2.6.32-573.el6.x86_64
Thread-0-192.168.56.101::INFO: Linux centos7 3.10.0-327.el7.x86_64
Thread-1-192.168.56.102::INFO: Linux osboxes 4.2.0-16-generic`
```

Teste com 100 conexões (42 segundos):

```bash
root@osboxes:/opt/scripts/rcmd# DATA=`echo date +%H:%M:%S`
root@osboxes:/opt/scripts/rcmd# $DATA;./rcmd.py -H `python -c "print '192.168.56.103 ' * 100"` -c "uname -nsr" -l mvarge;$DATA
11:20:45
Password:
Thread-3-192.168.56.103::INFO: Linux centos6 2.6.32-573.el6.x86_64
Thread-4-192.168.56.103::INFO: Linux centos6 2.6.32-573.el6.x86_64
Thread-5-192.168.56.103::INFO: Linux centos6 2.6.32-573.el6.x86_64
[... varias conexões omitidas ...]
Thread-96-192.168.56.103::INFO: Linux centos6 2.6.32-573.el6.x86_64
Thread-97-192.168.56.103::INFO: Linux centos6 2.6.32-573.el6.x86_64
Thread-98-192.168.56.103::INFO: Linux centos6 2.6.32-573.el6.x86_64
Thread-88-192.168.56.103::INFO: Linux centos6 2.6.32-573.el6.x86_64
11:21:27
```

stdout e stderr são implementados conforme o padrão, então é possível:

```
root@osboxes:/opt/scripts/rcmd# ./rcmd.py -H 192.168.56.103 192.168.56.104 -c "uname -nsr" -l mvarge
Password:
192.168.56.104::ERROR: [Errno None] Unable to connect to port 22 on  or 192.168.56.104
Thread-0-192.168.56.103::INFO: Linux centos6 2.6.32-573.el6.x86_64
root@osboxes:/opt/scripts/rcmd#
root@osboxes:/opt/scripts/rcmd# ./rcmd.py -H 192.168.56.103 192.168.56.104 -c "uname -nsr" -l mvarge 2> erros.log
Password:
Thread-0-192.168.56.103::INFO: Linux centos6 2.6.32-573.el6.x86_64
root@osboxes:/opt/scripts/rcmd# cat erros.log
192.168.56.104::ERROR: [Errno None] Unable to connect to port 22 on  or 192.168.56.104
```

#### Outros
Qualquer dúvida, sugestão, melhorias, bugs, etc: marcelo.varge@gmail.com
