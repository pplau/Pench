# coding: utf-8

import sys
sys.path.append('/root/pench')

import paramiko
import threading
import time
import os

import analysis.analysis as analysis

conf_path = "/pench/pench.conf"

def init(conf):
	try:
		os.popen('cd '+conf['cosbench_path']+' && sh ./start-all.sh')
		print "inital cosbench success"
		return 0
	except:
		print "inital cosbench error"
		return -1


def get_conf(path=None):
	conf = {}
	if path is None:
		print "Configuration: "
		conf['node_list'] = ['172.16.171.36','172.16.171.37','172.16.171.38','172.16.171.34']
		conf['last'] = 150
		conf['interval'] = 1
		conf['cosbench_path'] = "/root/0.4.2.c4"
		conf['workload_path'] = "/root/0.4.2.c4/conf/s3-config-sample.xml"
		conf['osd_device'] = "sda"
		#conf = {'node_list':['172.16.171.36','172.16.171.37','172.16.171.38','172.16.171.34'], 'last':10, 'interval':1,}
	else :
		# load the config file
		conf_file = open(path)
		for line in conf_file.readlines():
			value_list = re.split('=', line)
			if value_list[0] == "node_list":
				n_list = value_list[2]
				conf['node_list'] = re.split(';', n_list)
			if value_list[0] == "last":
				conf['last'] = value_list[2]
			if value_list[0] == "interval":
				conf['interval'] = value_list[2]
			if value_list[0] == "cosbench_path":
				conf['cosbench_path'] = value_list[2]
			if value_list[0] == "workload_path":
				conf['workload_path'] = value_list[2]
			if value_list[0] == "osd_device":
				conf['osd_device'] = value_list[2]
	return conf


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
		cmd = 'iostat -k -x -t '+str(conf['interval'])+' '+str(conf['last'])+' > /root/iostat.out && '
		cmd = cmd + 'vmstat '+str(conf['interval'])+' '+str(conf['last'])+' > /root/vmstat.out'
		mon_thread = threading.Thread(target=ssh_exec_cmd,args=(conn, cmd))
		mon_thread.start()
	# start cosbench in controller #
	cosbanch_thread = threading.Thread(target=run_cosbench,args=())
	cosbanch_thread.start()




if __name__=='__main__':

	conf = get_conf()
	init(conf)
	print "iostat & vmstat running..."
	run_pench(conf)
	time.sleep(conf['last']+1)

	print "Please input 1 to jump to analyse."
	print "Please input 2 to stop."
	print "Please enter a operation code: "

	while True:
		tag = raw_input()
		if tag is '1':
			print "jump to analyse "
			anyls = analysis.Analysis(conf)
			io_res = anyls.iostat_analysis()
			vm_res = anyls.vmstat_analysis()
			print io_res
			print vm_res
			exit()

		else :
			exit()











