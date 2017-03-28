# coding: utf-8

import sys
sys.path.append('/root/pench')

import paramiko
import threading
import os
import re


class Analysis :

	def __init__(self, conf):
		#self.data_path = conf['data_path']
		self.node_list = conf['node_list']
		self.osd_device = conf['osd_device']
		self.io_openfile_list = []
		self.vm_openfile_list = []
		self.__prepare_data__()


	def __prepare_data__(self):	
		#os.system('cd /root/pench/data')
		for node in self.node_list:
			path = '/root/data/'
			os.system('mkdir '+path)

			t = paramiko.Transport(sock=(node, 22))
			t.connect(username="root", password="admin123")
			sftp = paramiko.SFTPClient.from_transport(t)
			sftp.get("/root/iostat.out", path+node+"-io.out")
			sftp.get("/root/vmstat.out", path+node+"-vm.out")
			t.close()

			iofile = open(path+node+"-io.out")
			self.io_openfile_list.append(iofile)
			vmfile = open(path+node+'-vm.out')
			self.vm_openfile_list.append(vmfile)


	def __clean__(self):
		for f in self.io_openfile_list:
			f.close()



	def iostat_analysis(self):
		iostat_res = {}
		iostat_res['read_num_count'] = 0
		iostat_res['write_num_count'] = 0
		iostat_res['read_kb_count'] = 0
		iostat_res['write_kb_count'] = 0
		r_wait = []
		w_wait = []

		for f in self.io_openfile_list:
			r_num = 0
			w_num = 0
			r_kb = 0
			w_kb = 0
			for line in f.readlines():
				value_list = re.split(r'\s+', line)
				if value_list[0] == self.osd_device:
					r_num = round(r_num+float(value_list[3]), 2)
					w_num = round(w_num+float(value_list[4]), 2)
					r_kb = round(r_kb+float(value_list[5]) ,2)
					w_kb = round(w_kb+float(value_list[6]), 2)
					#r_wait.append(float(value_list[10]))
					#w_wait.append(float(value_list[11]))
					#iostat_res['read_wait'] = round(sum(r_wait)/len(r_wait), 2)
					#iostat_res['wirte_wait'] = round(sum(w_wait)/len(w_wait), 2)	
			iostat_res['read_num_count'] = iostat_res['read_num_count']+r_num
			iostat_res['write_num_count'] = iostat_res['write_num_count']+w_num
			iostat_res['read_kb_count'] = iostat_res['read_kb_count']+r_kb
			iostat_res['write_kb_count'] = iostat_res['write_kb_count']+w_kb
			
		iostat_res['read_num_count'] = round(iostat_res['read_num_count']/len(self.node_list), 2)
		iostat_res['write_num_count'] = round(iostat_res['write_num_count']/len(self.node_list), 2)
		iostat_res['read_kb_count'] = round(iostat_res['read_kb_count']/len(self.node_list), 2)
		iostat_res['write_kb_count'] = round(iostat_res['write_kb_count']/len(self.node_list), 2)
		return iostat_res

		


	def vmstat_analysis(self):
		vmstat_res = {}
		vmstat_res['i_kb'] = 0
		vmstat_res['o_kb'] = 0
		vmstat_res['i_block_num'] = 0
		vmstat_res['o_block_num'] = 0
		for f in self.vm_openfile_list:
			i_kb = 0
			o_kb = 0
			i_block_num = 0
			o_block_num = 0
			for line in f.readlines():
				value_list = re.split(r'\s+', line)
				if value_list[0] != 'procs' && value_list[0] != 'r':
					i_kb = i_kb+int(value_list[6])
					o_kb = o_kb+int(value_list[7])
					i_block_num = i_block_num+int(value_list[8])
					o_block_num = o_block_num+int(value_list[9])
			vmstat_res['i_kb'] = vmstat_res['i_kb']+i_kb
			vmstat_res['o_kb'] = vmstat_res['o_kb']+o_kb
			vmstat_res['i_block_num'] = vmstat_res['i_block_num']+i_block_num
			vmstat_res['o_block_num'] = vmstat_res['o_block_num']+o_block_num

		vmstat_res['i_kb'] = round(vmstat_res['i_kb']/len(self.node_list), 2)
		vmstat_res['o_kb'] = round(vmstat_res['o_kb']/len(self.node_list), 2)
		vmstat_res['i_block_num'] = round(vmstat_res['i_block_num']/len(self.node_list), 2)
		vmstat_res['o_block_num'] = round(vmstat_res['o_block_num']/len(self.node_list), 2)
		return vmstat_res










