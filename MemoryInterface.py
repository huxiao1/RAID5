'''
THIS MODULE INTERACTS WITH THE MEMORY
''' 
import time, client_stub,sys


#HANDLE FOR MEMORY OPERATIONS
client_stub = client_stub.client_stub()


#REQUEST TO BOOT THE FILE SYSTEM
def Initialize_My_FileSystem():
    print("File System Initializing......")
    time.sleep(2)
    state = client_stub.Initialize()
    print("File System Initialized!")
"""
#TANSLATE VIRTUAL BLK NUMBER TO LOCAL BLK NUMBER
def block_number_translate(virtual_block_number):
	a = virtual_block_number
	local_block_number = (a/3) +12
	check_server_num = (local_block_number-12)%4
	check = a+(a/3)+1-(a/3)*4
	if check == check_server_num:
		server_number = check - 1
	else:
		server_number = check

	return server_number, local_blk_number

#REQUEST A SERVER TO RETURN INODE NUMBER AND INODE 
def round_robin():

	a=client_stub.round_robin()

	return a
"""
#REQUEST TO FETCH THE INODE FROM INODE NUMBER FROM SERVER
def inode_number_to_inode(inode_number):
	
   	return client_stub.inode_number_to_inode(inode_number)


#REQUEST THE DATA FROM THE SERVER
def get_data_block( virtual_block_number):
    	return ''.join(client_stub.get_data_block(virtual_block_number))


#REQUESTS THE VALID BLOCK NUMBER FROM THE SERVER 
def get_valid_data_block():
										
	
	virtual_block_number=client_stub.get_valid_data_block()									
    	return virtual_block_number


#REQUEST TO MAKE BLOCKS RESUABLE AGAIN FROM SERVER
def free_data_block(virtual_block_number):
	
    	client_stub.free_virtual_dblock(virtual_block_number)
	client_stub.free_data_block(virtual_block_number)


#REQUEST TO WRITE DATA ON THE THE SERVER
def update_data_block(virtual_block_number, block_data):
	
    	client_stub.update_data_block(virtual_block_number, block_data)
	# update parity of this blk in server.

#REQUEST TO UPDATE THE UPDATED INODE IN THE INODE TABLE FROM SERVER
def update_inode_table(inode, inode_number):
    	client_stub.update_inode_table(inode, inode_number)

#REQUEST FOR THE STATUS OF FILE SYSTEM FROM SERVER
def status():
    	return client_stub.status()
"""
#REQUEST THE VALID BLOCK NUMBER FROM THE VIRTUAL LIST
def get_virtual_valid_dblock():
    return ( client_stub.get_virtual_valid_dblock() )
"""
#print(round_robin())
def corruptData(serverNum):
	client_stub.corruptData(serverNum)
