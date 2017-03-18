# coding: utf-8

import sys
#sys.path.append('/root/pench')

#import paramiko
import threading
import time
import os


def get_conf():
	return ['node1', 'node2', 'node3']

def ssh_exec_cmd(cmd, conn=None, last=None, interval=None):
	# last is iostat or vmstat excute time, interval is thier monitor interval
	# 1.excute cmd  2.log runtime data  3.return log's path #
	count = last
	while (count>0):
		os.popen(cmd)
		time.sleep(interval)
		count = count-1
	#print "iostat was finished"


def run_pench(node_list, last=None, interval=None):
    # start iostat in each server node #
	for node in node_list:
		cmd = "iostat 1 1 >> /Users/PP/Downloads/"+node+".out"
		mon_thread = threading.Thread(target=ssh_exec_cmd,args=(cmd, None, last, interval))
		mon_thread.start()
		#mon_thread.join()
		
    



if __name__=='__main__':

	#init()
	res = -1
	node_list = get_conf()
	last=10
	interval=1
	print "iostat running..."
	run_pench(node_list, last, interval)
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


		





