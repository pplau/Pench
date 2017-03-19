# coding: utf-8

import sys
sys.path.append('/root/pench')

import paramiko
import threading
import time
import os


def init(conf):
	try:
		os.popen('cd '+conf['cosbench_path']+' && sh ./start-all.sh')
		print "inital cosbench success"
		return 0
	except:
		print "inital cosbench error"
		return -1


def get_conf(path=None):
	if path is None:
		print "Configuration: "
		conf = {}
		conf['node_list'] = ['172.16.171.36','172.16.171.37','172.16.171.38','172.16.171.34']
		conf['last'] = 150
		conf['interval'] = 1
		conf['cosbench_path'] = "/root/0.4.2.c4"
		conf['workload_path'] = "/root/0.4.2.c4/conf/s3-config-sample.xml"
		#conf = {'node_list':['172.16.171.36','172.16.171.37','172.16.171.38','172.16.171.34'], 'last':10, 'interval':1,}
		return conf
	else :
		# load the config file
		pass


def log(content):
	pass


def run_cosbench(workload_path="./conf/s3-config-sample.xml"):
	#os.popen('cd '+cosbench_path)
	res = os.popen('cd '+conf['cosbench_path']+' && sh cli.sh submit '+workload_path)


def ssh_connect(ip, username="root", passwd="admin123", tag="pw", key_path="/root"):
	# tag="pw" mean that paramiko use username and pw to login into remote host
	# tag="nopw" mean that paramiko use keys to login into remote host
	ssh = paramiko.SSHClient()
	if tag is "pw":
		try:
			ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
			ssh.connect(hostname=ip,port=22,username=username,password=passwd,timeout=5)
			return ssh
		except:
			return -1

	elif tag is "nopw" :
		try:
			private_key = paramiko.RSAKey.from_private_key_file(key_path)
			ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
			ssh.connect(hostname=ip,port=22,username=username,pkey=private_key)
			return ssh
		except:
			return -1



def ssh_exec_cmd(conn, cmd):
	# last is iostat or vmstat excute time, interval is thier monitor interval
	# 1.excute cmd  2.log runtime data  3.return log's path #
	conn.exec_command(cmd)



def ssh_close(_ssh_fd):
	_ssh_fd.ssh_close()


def run_pench(conf):
	# connect to osd nodes
	connect_list = []
	for node in conf['node_list']:
		connect_list.append(ssh_connect(node))
		
	# start iostat in each server node #
	for conn in connect_list:
		cmd = "iostat -k -x -t "+conf['last']+" "+conf['interval']+" >> /root/iotest.out"
		mon_thread = threading.Thread(target=ssh_exec_cmd,args=(conn, cmd)
		mon_thread.start()    
	# start cosbench in controller #
	cosbanch_thread = threading.Thread(target=run_cosbench,args=())
	cosbanch_thread.start()




if __name__=='__main__':

	conf = get_conf()
	init(conf)
	last=10
	interval=1
	print "iostat running..."
	run_pench(conf)
	time.sleep(last+1)

	print "Please input 1 to jump to analyse."
	print "Please input 2 to stop."
	print "Please enter a operation code: "

	while True:
		tag = raw_input()
		if tag is '1':
			print "jump to analyse "
			exit()

		elif tag is '2':
			exit()

		else :
			pass











