#!/usr/bin/env python
import sys
import threading
import getpass
import argparse
import socket
import time
try:
	import paramiko
except ImportError:
	sys.stderr.write("Sem modulo paramiko instalado.\n")

# Numero maximos de threads simultaneas. Altere este valor sob seu proprio risco
MAX_THREADS = 10


def usage():
	parser = argparse.ArgumentParser(prog=__file__)
	parser.add_argument("-H", "--hosts", nargs='*', required=True,
						help="Um ou mais hosts para conectar")
	parser.add_argument("-l", "--login", 
						help="Login utilizado para conectar no(s) servidor(es)")
	parser.add_argument("-c", "--comando", required=True,
						help="Comando a executar (Utilize aspas para varios args)")
	parser.add_argument("-p", "--password",
						help="Senha do login. Se nao fornecido um prompt surgira.")

	return parser.parse_args()

class Conexao(threading.Thread):
	def __init__(self, t_ID, t_nome, usuario, senha, host, comando):
		threading.Thread.__init__(self)
		self.t_ID = t_ID
		self.t_nome = t_nome
		self.usuario = usuario
		self.senha = senha
		self.host = host
		self.comando = comando
		self.info = "%s::INFO" % host
		self.error = "%s::ERROR" % host

	def run(self):
		if self.existe():
			self.conecta()
		else:
			sys.stderr.write("%s: Host %s nao encontrado.\n" % (self.error, self.host))

	def existe(self):
		try:
			socket.gethostbyname(self.host)
		except socket.gaierror:
			return False
		return True

	def conecta(self):
		try:
			self.ssh = paramiko.SSHClient()
			self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
			self.ssh.connect(self.host,
							 username=self.usuario,
							 password=self.senha,
							 timeout=10)
			stdin, stdout, stderr = self.ssh.exec_command(self.comando)
			if stdout:
				for line in stdout.readlines():
					sys.stdout.write("%s-%s: %s" % (self.t_nome, self.info, line))
			if stderr:
				for line in stderr.readlines():
					sys.stderr.write("%s-%s: %s" % (self.t_nome, self.error, line))
			self.ssh.close()
		except paramiko.AuthenticationException as e:
			sys.stderr.write("%s: %s\n" % (self.error, e))

if __name__ == "__main__":

	options = usage()

	if not options.login:
		usuario = str(raw_input("Login: "))
	else:
		usuario = options.login
	if not options.password:
		senha = getpass.getpass()
	else:
		senha = options.password
	hosts = options.hosts
	comando = options.comando

	catalogo = {}

	for index, host in enumerate(hosts):
			while threading.activeCount() > MAX_THREADS:
				time.sleep(2)
			thread_name = "Thread-" + str(index)
			catalogo[index] = Conexao(index, thread_name, usuario, senha, host, comando)
			catalogo[index].start()
			final = index
