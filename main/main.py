# coding: utf-8

import sys
sys.path.append('/root/pench')

import paramiko
import threading
import time


def init():
	try:
	    os.popen('cd ./cosbench')
        os.popen('sh start-all.sh')
        return "inital cosbench success"
     except:
     	return "inital cosbench error"


def get_conf():
	return conf


def log(content):
	pass


def run_cosbench():
	os.popen('cd ./cosbench')
	os.popen('sh cli.sh submit conf/workload-config.xml')


def ssh_connect(host, username="root", passwd="admin123", tag="pw", key_path="/root"):
	# tag="pw" mean that paramiko use username and pw to login into remote host
	# tag="nopw" mean that paramiko use keys to login into remote host
	if tag is "pw":
		try:
			ssh = paramiko.SSHClient()
			ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
			ssh.connect(hostname=ip,port=22,username=username,passwd=passwd,timeout=5)
			return ssh
		except:
			return "SSH error"
			
	else tag is "nopw" :
		try:
			private_key = paramiko.RSAKey.from_private_key_file(key_path)
			ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
			ssh.connect(hostname=ip,port=22,username=username,pkey=private_key)
			return ssh
		except:
			return "SSH error"



def ssh_exec_cmd(self, conn, cmd, last=None, interval=None):
	# last is iostat or vmstat excute time, interval is thier monitor interval
	# 1.excute cmd  2.log runtime data  3.return log's path #
	count = last
	while (count>0):
		stdin, stdout, stderr = conn.exec_command(cmd)
		time.sleep(interval)
		count = count-1


def ssh_close(_ssh_fd):
	_ssh_fd.ssh_close()


def run_pench(node_list):
	# connect to osd nodes #
    connect_list = []
	for node in node_list:
		connect_list.append(ssh_connect(node))
		
    # start iostat in each server node #
	for conn in connect_list:
		cmd = "iostat 1 1 >> ./"+node+".out"
		mon_thread = threading.Thread(target=ssh_exec_cmd,args=(conn, cmd, None, last, interval))
		mon_thread.start()    
    # start cosbench in controller #
    cosbanch_thread = threading.Thread(target=run_cosbench,args=())
	cosbanch_thread.start()




if __name__=='__main__':

	#init()
	res = -1
	conf = get_conf()
	last=10
	interval=1
	print "iostat running..."
	run_pench(conf['node_list'], last, interval)
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











