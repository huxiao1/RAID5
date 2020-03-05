# SKELETON CODE FOR CLIENT STUB HW4
import xmlrpclib, config, pickle, os, sys, subprocess, time


portNum=8000


severNum = 4
virtual_datablk_list=[-1 for _ in range(((config.INODE_SIZE - 63 - config.MAX_FILE_NAME_SIZE) / 2))]   
#initial virtual_datablk_list '-1'

class client_stub():



	def __init__(self):
		self.flag=-1
		self.corruptserver=5
		

		print('running server #8000' )
		self.proxy0 = xmlrpclib.ServerProxy("http://localhost:8000/")
		print('running server #8001' )
		self.proxy1 = xmlrpclib.ServerProxy("http://localhost:8001/")
		print('running server #8002' )
		self.proxy2 = xmlrpclib.ServerProxy("http://localhost:8002/")
		print('running server #8003' )	
		self.proxy3 = xmlrpclib.ServerProxy("http://localhost:8003/")
		os.system('gnome-terminal -e \"python server_stub.py 8000\"')
		
		os.system('gnome-terminal -e \"python server_stub.py 8001\"')
		
		os.system('gnome-terminal -e \"python server_stub.py 8002\"')
		
		os.system('gnome-terminal -e \"python server_stub.py 8003\"')
		time.sleep(1)
		
		self.proxy=[]
		self.proxy.append(self.proxy0)
		self.proxy.append(self.proxy1)
		self.proxy.append(self.proxy2)
		self.proxy.append(self.proxy3)

		
	def XOR(self, a, b):
    		#print(a, b)
    		c = []
    		if len(b) > len(a):
        		a, b = b, a
        		state = False  # keep a>=b
    		l_max = len(a)
    		l_min = len(b)
    		for i in range(l_max - l_min):
        		c.append(ord(a[i]) ^ 0) #translate to ascii save addtional bit of a in c
    		for i in range(0, l_min):
        		c.append(ord(a[l_max - l_min + i]) ^ ord(b[i]))
    		for i in range(l_max):
        		c[i] = chr(c[i])
    		retVal = ''.join(c)
  
  		return retVal
				
  	
	def update_parity(self,local_block_offset):
		a = local_block_offset
		parity_snumber = a%severNum
		passVal = pickle.dumps(local_block_offset)
		retVal=[]
		parity=[]
		for i in range (severNum):
			if (i != parity_snumber):

				retVal.append( pickle.loads(self.proxy[i].get_data_block(passVal)))
				
		a1=retVal[0]
		a2=retVal[1]
		a3=retVal[2]
		array1=[]
		array2=[]
		array3=[]
		for i in range (len(a1)):
			if a1[i]!='\0':
				array1.append(a1[i])
			if a2[i]!='\0':
				array2.append(a2[i])
			if a3[i]!='\0':
				array3.append(a3[i])
		array1=''.join(array1)
		array2=''.join(array2)
		array3=''.join(array3)
				
		zhongjianzhi=self.XOR(array1, array2)
    		c = self.XOR(zhongjianzhi,a3)

		passVal2 = pickle.dumps(c)
		
		self.proxy[parity_snumber].update_data_block(passVal,passVal2)
	
		
		

	#TRANSLATE VIRTUAL BLOCK NUMBER TO SERVER'S LOCAL BLOCK NUMBER AND SERVER NUMBER
	def block_number_translate(self,virtual_block_number) :
		a = virtual_block_number
		lbn = a/(severNum-1)
		check_server_num = (lbn)%severNum
		check = a+(a/(severNum-1))+1-(a/(severNum-1))*severNum
		if check == check_server_num:
			server_number = check - 1
		else:
			server_number = check
		local_Block_offset = lbn
   		
		return server_number, local_Block_offset

	
	#REQUEST A SERVER TO RETURN INODE NUMBER AND INODE 
	def round_robin(self):
		self.flag=self.flag+1
		if (self.flag>=severNum):
			self.flag=0
		return self.flag
	
	#REQUEST THE VALID BLOCK NUMBER FROM THE VIRTUAL LIST
	def get_virtual_valid_dblock(self):
		for i in range (((config.INODE_SIZE - 63 - config.MAX_FILE_NAME_SIZE) / 2)*3):
			if virtual_datablk_list[i]==-1:
				virtual_datablk_list[i]=i
				return i
	##REQUEST TO MAKE BLOCKS REUSABLE AGAIN FROM THE VIRTUAL LIST
	def free_virtual_dblock(self,virtual_block_number):
		virtual_datablk_list[virtual_block_number]==-1
		return True
		

	# DEFINE FUNCTIONS HERE
	# example provided for initialize
	def Initialize(self):
		try :
			self.proxy0.Initialize()
			self.proxy1.Initialize()
			self.proxy2.Initialize()
			self.proxy3.Initialize()
		except Exception as err :
			print("time out error of initialize")
			quit()

	def addr_inode_table(self):
		try :
			
			retVal0=self.proxy0.addr_inode_table()
			retVal1=self.proxy1.addr_inode_table()
			retVal2=self.proxy2.addr_inode_table()
			retVal3=self.proxy3.addr_inode_table()
			return retVal0
		except Exception as err :
			print("time out error of addr_inode_table")
			quit()
			
		
	def inode_number_to_inode(self,inode_number):				
											
		try:														
			server_number = self.round_robin()	
									
			
			passVal = pickle.dumps(inode_number)
			retVal = self.proxy[server_number].inode_number_to_inode(passVal)
			return pickle.loads(retVal)

		except Exception as err:
			print("time out error of inode_number_to_inode")
			quit()




	#REQUEST THE DATA FROM THE SERVER
	def get_data_block(self,virtual_block_number):
		try:	
			server_number, local_Block_offset = self.block_number_translate(virtual_block_number )
			if server_number== self.corruptserver:
				print('data in server '+str(server_number)+' is corrupted')
				print('you are now reading data from XOR result:')
				retVal=[]
				
				passVal= pickle.dumps(local_Block_offset)
				for i in range(severNum):
					if (i!=server_number):
						retVal.append( pickle.loads(self.proxy[i].get_data_block(passVal)))
				a1=retVal[0]
				a2=retVal[1]
				a3=retVal[2]
				array1=[]
				array2=[]
				array3=[]
				for i in range (len(a1)):
					if a1[i]!='\0':
						array1.append(a1[i])
					if a2[i]!='\0':
						array2.append(a2[i])
					if a3[i]!='\0':
						array3.append(a3[i])
				array1=''.join(array1)
				array2=''.join(array2)
				array3=''.join(array3)
				
		
				zhongjianzhi=self.XOR(array1, array2)
    		
    				c = self.XOR(zhongjianzhi,a3)
				
				return ''.join(c)
			else:
				print("you are now reading data from server:"+str(server_number))
				passVal = pickle.dumps(local_Block_offset)
				retVal= pickle.loads(self.proxy[server_number].get_data_block(passVal))
				return ''.join(retVal)
		except Exception as err:
			print("time out error of get_data_block")
			quit()


	
	#REQUESTS THE VALID BLOCK NUMBER FROM THE SERVER 
	def get_valid_data_block(self):
		try:	
			
			virtual_block_number = self.get_virtual_valid_dblock()	
			
			server_number, local_Block_offset =self. block_number_translate(virtual_block_number)
			
			for i in range (severNum):
				self.proxy[i].get_valid_data_block()
			

			return virtual_block_number
		except Exception as err:
			print("time out error of get_valid_data_block")
			quit()

	

	#REQUEST TO MAKE BLOCKS REUSABLE AGAIN FROM SERVER
	def free_data_block(self,virtual_block_number):
		try:	
			
			server_number, local_Block_offset = self.block_number_translate(virtual_block_number)
			passVal = pickle.dumps(local_Block_offset)
			self.proxy[server_number].free_data_block((passVal))	
		except Exception as err:
			print("time out error of free_data_block")
			quit()



	#REQUEST TO WRITE DATA ON THE THE SERVER////AT THE SAME TIME , UPDATE PARITY.
	def update_data_block(self,virtual_block_number,block_data):
		try:
			server_number, local_Block_offset =self. block_number_translate(virtual_block_number)
			a2 = pickle.dumps(local_Block_offset)
			a3 = pickle.dumps(block_data)
			
			print("you are now in server "+ str(server_number))
			self.proxy[server_number].update_data_block(a2,a3)
			print("parity is now in server "+ str((local_Block_offset)%4))
			self.update_parity(local_Block_offset)
		
		except Exception as err:
			print("time out error of update_data_block")
			quit()



	#REQUEST TO UPDATE THE UPDATED INODE IN THE INODE TABLE FROM SERVER
	def update_inode_table(self,inode, inode_number):			
		try:
			
			a1 = pickle.dumps(inode)
			a2 = pickle.dumps(inode_number)
			retVal0=self.proxy[0].update_inode_table(a1, a2)
			retVal1=self.proxy[1].update_inode_table(a1, a2)
			retVal2=self.proxy[2].update_inode_table(a1, a2)
			retVal3=self.proxy[3].update_inode_table(a1, a2)
			
		except Exception as err:
			print("time out error of get_data_block")
			quit()



	#REQUEST FOR THE STATUS OF FILE SYSTEM FROM SERVER
	def status(self):							
		try:
			retVal0=pickle.loads(self.proxy[0].status())
			retVal1=pickle.loads(self.proxy[1].status())
			retVal2=pickle.loads(self.proxy[2].status())
			retVal3=pickle.loads(self.proxy[3].status())
			
			return retVal0+retVal1+retVal2+retVal3
		except Exception as err:
			print("time out error of status")
			quit()
#client1=client_stub()
	def corruptData(self,serverNum):
			
		self.corruptserver=serverNum
	


