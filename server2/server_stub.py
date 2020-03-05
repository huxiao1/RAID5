# SKELETON CODE FOR SERVER STUB HW4
import xmlrpclib
from SimpleXMLRPCServer import SimpleXMLRPCServer

import time, Memory, pickle , InodeOps, config, DiskLayout


filesystem = Memory.Operations()

# FUNCTION DEFINITIONS 

# example provided for initialize
def Initialize():
	retVal = Memory.Initialize()
	retVal = pickle.dumps(retVal)
	return retVal

''' WRITE CODE HERE FOR REST OF FUNCTIONS'''



server = SimpleXMLRPCServer(("",8000))
print ("Listening on port 8000...")
def status():
    return pickle.dumps(filesystem.status())

def get_data_block(block_number):
    retVal=pickle.loads(block_number)
    return pickle.dumps(filesystem.get_data_block(retVal))

def get_valid_data_block():
    return pickle.dumps(filesystem.get_valid_data_block())

def free_data_block(block_number):
    retVal=pickle.loads(block_number)
    return pickle.dumps(filesystem.free_data_block(retVal))

def update_data_block(block_number,block_data):
    retVal=pickle.loads(block_number)
    retVal2=pickle.loads(block_data)
    return pickle.dumps(filesystem.update_data_block(retVal,retVal2))

def update_inode_table(inode,inode_number):
    retVal=pickle.loads(inode)
    retVal2=pickle.loads(inode_number)
    return pickle.dumps(filesystem.update_inode_table(retVal, retVal2))

def inode_number_to_inode(inode_number):
    retVal=pickle.loads(inode_number)
    return pickle.dumps(filesystem.inode_number_to_inode(retVal))
    
# REGISTER FUNCTIONS
server.register_introspection_functions()
server.register_function(status,"status")
#example provided for initialize
server.register_function(Initialize, 		   	"Initialize")
server.register_function(get_data_block,'get_data_block')
server.register_function(get_valid_data_block,'get_valid_data_block')
server.register_function(free_data_block,'free_data_block')
server.register_function(update_data_block,'update_data_block')
server.register_function(update_inode_table,'update_inode_table')
server.register_function(inode_number_to_inode,'inode_number_to_inode')

# run the server
server.serve_forever()
