# coding: utf-8

import sys
sys.path.append('/root/pench')

import paramiko
import threading
import os


class Analysis :

	def __init__(self, conf):
		self.data_path = conf['data_path']
		self.node_list = conf['node_list']
		self.osd_device = conf['osd_device']
		self.io_openfile_list = []
		self.vm_openfile_list = []
		self.__prepare_data__()


	def __prepare_data__(self):
		#os.system('cd /root/pench/data')
		for node in self.node_list:
			path = '/root/data/'+node
			os.system('mkdir '+path)
			os.system('scp root@'+node+':/root/iostat.out '+path)
			#os.system('scp root@'+node+':/root/vmstat.out '+path)
			iofile = open(path+'iostat.out')
			self.io_openfile_list.append(iofile)
			#vmfile = open(path+'vmstat.out')
			#self.io_openfile_list.append(vmfile)


	def __clean__(self):
		for f in self.io_openfile_list:
			f.close()



	def iostat_analysis(self):
		iostat_res = {}
		for f in self.io_openfile_list:
			iostat_res['read_num_count'] = 0
			iostat_res['write_num_count'] = 0
			iostat_res['read_kb_count'] = 0
			iostat_res['write_kb_count'] = 0
			r_wait = []
			w_wait = []
			for line in f.readlines():
				value_list = re.split(r'\s+', line)
				if value_list[0] is self.osd_device:
					iostat_res['read_num_count'] = iostat_res['read_num_count']+float(value_list[3])
					iostat_res['write_num_count'] = iostat_res['write_num_count']+float(value_list[4])
					iostat_res['read_kb_count'] = iostat_res['read_kb_count']+float(value_list[5])
					iostat_res['write_kb_count'] = iostat_res['write_kb_count']+float(value_list[6])
					r_wait.append(float(value_list[10]))
					w_wait.append(float(value_list[11]))
			iostat_res['read_wait'] = round(sum(r_wait)/len(r_wait), 2)
			iostat_res['wirte_wait'] = round(sum(w_wait)/len(w_wait), 2)
			return iostat_res

			

	def mem_util(self):
		pass


	def mem_ip(self):
		pass


	def mem_op(self):
		pass








