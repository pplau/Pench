# coding: utf-8

import sys
#sys.path.append('/root/pench')

#import paramiko
import threading
import time
import os
import re 


def get_conf():
	return {'node_list':['node1', 'node2', 'node3']}

def ssh_exec_cmd(cmd, conn=None, last=None, interval=None):
	# last is iostat or vmstat excute time, interval is thier monitor interval
	# 1.excute cmd  2.log runtime data  3.return log's path #
	os.popen(cmd)




def run_pench(conf, last=None, interval=None):
    # start iostat in each server node #
	for node in conf['node_list']:
		cmd = "iostat 1 10 > /Users/PP/Downloads/"+node+".out"
		mon_thread = threading.Thread(target=ssh_exec_cmd,args=(cmd, None, last, interval))
		mon_thread.start()
		#mon_thread.join()
		
    


class Analysis :

	def __init__(self, conf):
		#self.data_path = conf['data_path']
		self.node_list = conf['node_list']
		self.io_openfile_list = []
		self.vm_openfile_list = []

		self.__prepare_data__()


	def __prepare_data__(self):
		#os.system('cd /root/pench/data')
		for node in self.node_list:
			path = '/Users/PP/Downloads/'+node+'.out'
			#os.system('mkdir '+path)
			#os.system('scp root@'+node+':/root/iostat.out '+path)
			#os.system('scp root@'+node+':/root/vmstat.out '+path)
			iofile = open(path)
			self.io_openfile_list.append(iofile)
			#vmfile = open(path+'vmstat.out')
			#self.io_openfile_list.append(vmfile)


	def __clean__(self):
		pass


	def avg_read(self):
		for f in self.io_openfile_list:
			print "reading file: "
			count = 1
			read_kb = 0
			for line in f.readlines():
				word_list = re.split(r'\s+', line)
				if count>2:
					read_kb = read_kb+float(word_list[1])
				count = count+1
			print read_kb




if __name__=='__main__':

	#init()
	res = -1
	conf = get_conf()
	last=10
	interval=1
	print "iostat running..."
	run_pench(conf, last, interval)
	time.sleep(last+1)

	print "Please input 1 to jump to analyse."
	print "Please input 2 to stop."
	print "Please enter a operation code: "

	while True:
		tag = raw_input()
		if tag is '1':
			print "jump to analyse "
			aly = Analysis(conf)
			aly.avg_read()

		elif tag is '2':
			exit()

		else :
			pass


		





