# Cody Rigby
# POCSD Final Project
# Server Stub 00

import xmlrpclib
from SimpleXMLRPCServer import SimpleXMLRPCServer

import time, Memory, pickle , InodeOps, config, DiskLayout, sys

global portNumber

filesystem = Memory.Operations()
#state = True



class counts():
	def __init__(self):
		self.count=0

counts=counts()


def configure():
	configuration = [config.TOTAL_NO_OF_BLOCKS, config.BLOCK_SIZE, config.MAX_NUM_INODES, config.INODE_SIZE, config.MAX_FILE_NAME_SIZE]
	retVal        = pickle.dumps((configuration))
	return retVal

def Initialize():
	retVal = Memory.Initialize()
	print(Memory.sblock.ADDR_BITMAP_BLOCKS)
	
	for i in range(0, Memory.sblock.TOTAL_NO_OF_BLOCKS):
		if Memory.sblock.ADDR_BITMAP_BLOCKS[i / Memory.sblock.BLOCK_SIZE].block[i % Memory.sblock.BLOCK_SIZE] == -1:
			counts.count=counts.count+1
	retVal = pickle.dumps((retVal))
	return retVal

def addr_inode_table():
	retVal = filesystem.addr_inode_table()
	retVal = pickle.dumps((retVal))
	return retVal

def get_data_block(block_number):
	
	passVal = pickle.loads(block_number)
	passVal = passVal+counts.count
	retVal  = filesystem.get_data_block(passVal)
	retVal  = pickle.dumps((retVal))
	return retVal

def get_valid_data_block():	
	
	retVal = filesystem.get_valid_data_block()
	retVal = pickle.dumps((retVal))
	return retVal

def free_data_block(block_number):  
	passVal = pickle.loads(block_number)
	passVal = passVal + counts.count
	retVal  = filesystem.free_data_block(passVal)
	retVal  = pickle.dumps((retVal))
	return retVal

def update_data_block(block_number, block_data):	
	passVal1 = pickle.loads(block_number)
	passVal1 = passVal1 + counts.count
	passVal2 = pickle.loads(block_data)
	retVal 	 = filesystem.update_data_block(passVal1, passVal2)
	retVal   = pickle.dumps((retVal))
	return retVal

def update_inode_table(inode, inode_number):
	passVal1 = pickle.loads(inode)
	passVal2 = pickle.loads(inode_number)
	retVal 	 = filesystem.update_inode_table(passVal1, passVal2)
	retVal   = pickle.dumps((retVal))
	return retVal

def inode_number_to_inode(inode_number):
	passVal = pickle.loads(inode_number)
	retVal  = filesystem.inode_number_to_inode(passVal)
	retVal  = pickle.dumps((retVal))
	return retVal

def status():
	retVal = filesystem.status()
	retVal = pickle.dumps((retVal))
	return retVal

def corruptData():
	retVal = 'Data Corrupted in server ' + str(portNumber)
	retVal = pickle.dumps((retVal))
	return retVal

portNumber = int(sys.argv[1])
#portNumber = 8000
server = SimpleXMLRPCServer(("localhost",portNumber))
print ("Listening on port " + str(portNumber) +   "...")

server.register_function(corruptData, 			"corruptData")
server.register_function(configure, 		   	"configure")
server.register_function(Initialize, 		   	"Initialize")
server.register_function(addr_inode_table, 	   	"addr_inode_table")
server.register_function(get_data_block, 	   	"get_data_block")
server.register_function(get_valid_data_block, 	"get_valid_data_block")
server.register_function(free_data_block, 		"free_data_block")
server.register_function(update_data_block, 	"update_data_block")
server.register_function(update_inode_table, 	"update_inode_table")
server.register_function(inode_number_to_inode, "inode_number_to_inode")
server.register_function(status, 				"status")
server.serve_forever()
