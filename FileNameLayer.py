'''
THIS MODULE ACTS LIKE FILE NAME LAYER AND PATH NAME LAYER (BOTH) ABOVE INODE LAYER.
IT RECIEVES INPUT AS PATH (WITHOUT INITIAL '/'). THE LAYER IMPLEMENTS LOOKUP TO FIND INODE NUMBER OF THE REQUIRED DIRECTORY.
PARENTS INODE NUMBER IS FIRST EXTRACTED BY LOOKUP AND THEN CHILD INODE NUMBER BY RESPECTED FUNCTION AND BOTH OF THEM ARE UPDATED
'''
import InodeNumberLayer

#HANDLE OF INODE NUMBER LAYER
interface = InodeNumberLayer.InodeNumberLayer()

class FileNameLayer():

	#PLEASE DO NOT MODIFY
	#RETURNS THE CHILD INODE NUMBER FROM THE PARENTS INODE NUMBER
	def CHILD_INODE_NUMBER_FROM_PARENT_INODE_NUMBER(self, childname, inode_number_of_parent):
		inode = interface.INODE_NUMBER_TO_INODE(inode_number_of_parent)
		if not inode: 
			print("Error FileNameLayer: Lookup Failure!")
			return -1
		if inode.type == 0:
			print("Error FileNameLayer: Invalid Directory!")
			return -1
		if childname in inode.directory: 
			return inode.directory[childname]
		print("Error FileNameLayer: Lookup Failure!")
		return -1

	#PLEASE DO NOT MODIFY
	#RETUNS THE PARENT INODE NUMBER FROM THE PATH GIVEN FOR A FILE/DIRECTORY 
	#lian jie fu wen jian jia de inode number
	def LOOKUP(self, path, inode_number_cwd):   
		name_array = path.split('/')

		if len(name_array) == 1: 
			return inode_number_cwd
		else:
			child_inode_number = self.CHILD_INODE_NUMBER_FROM_PARENT_INODE_NUMBER(name_array[0], inode_number_cwd)
			if child_inode_number == -1: 
				return -1
			return self.LOOKUP("/".join(name_array[1:]), child_inode_number)

	#PLEASE DO NOT MODIFY
	#MAKES NEW ENTRY OF INODE
	def new_entry(self, path, inode_number_cwd, type):
		if path == '/': #SPECIAL CASE OF INITIALIZING FILE SYSTEM
			interface.new_inode_number(type, inode_number_cwd, "root")
			return True
		parent_inode_number = self.LOOKUP(path, inode_number_cwd)
		parent_inode = interface.INODE_NUMBER_TO_INODE(parent_inode_number) 
		childname = path.split('/')[-1]
		if not parent_inode: return -1
		if childname in parent_inode.directory:
			print("Error FileNameLayer: File already exists!")
			return -1
		child_inode_number = interface.new_inode_number(type, parent_inode_number, childname)  #make new child
		if child_inode_number != -1:
			parent_inode.directory[childname] = child_inode_number
			interface.update_inode_table(parent_inode, parent_inode_number)


	#IMPLEMENTS READ
	def read(self, path, inode_number_cwd, offset, length):
		'''WRITE YOUR CODE HERE'''
		name_array=path.split('/')
		parent_inode_number=self.LOOKUP(path, inode_number_cwd)
		child_inode_number=self.CHILD_INODE_NUMBER_FROM_PARENT_INODE_NUMBER(name_array[-1], parent_inode_number)
		return interface.read(child_inode_number, offset,length, parent_inode_number)

	
	#IMPLEMENTS WRITE
	def write(self, path, inode_number_cwd, offset, data):
		'''WRITE YOUR CODE HERE'''
		name_array=path.split('/')
		parent_inode_number=self.LOOKUP(path, inode_number_cwd)
		child_inode_number=self.CHILD_INODE_NUMBER_FROM_PARENT_INODE_NUMBER(name_array[-1], parent_inode_number)
		interface.write(child_inode_number, offset, data, parent_inode_number)
		return True

	#HARDLINK
	def link(self, old_path, new_path, inode_number_cwd):
		name_array_old = old_path.split('/')
		name_array_new = new_path.split('/')
		name = name_array_new[-1]
		parent_inode_number_old=self.LOOKUP(old_path,inode_number_cwd)
		result = '/' in new_path
		if not result:
			parent_inode_number_new = self.CHILD_INODE_NUMBER_FROM_PARENT_INODE_NUMBER(name_array_old[0], inode_number_cwd)
		else:
			parent_inode_number_new = self.LOOKUP(new_path,inode_number_cwd)
		child_inode_number=self.CHILD_INODE_NUMBER_FROM_PARENT_INODE_NUMBER(name_array_old[-1], parent_inode_number_old)
		parent_inode_new = interface.INODE_NUMBER_TO_INODE(parent_inode_number_new)
		child_inode = interface.INODE_NUMBER_TO_INODE(child_inode_number)
		parent_inode_old = interface.INODE_NUMBER_TO_INODE(parent_inode_number_old)
		parent_inode_new.directory[child_inode.name] = child_inode_number
		interface.update_inode_table(parent_inode_new,parent_inode_number_new)
		interface.link(child_inode_number,name,parent_inode_number_new)
		return True
	
	#REMOVES THE FILE/DIRECTORY
	def unlink(self, path, inode_number_cwd):
		if path == "": 
			print("Error FileNameLayer: Cannot delete root directory!")
			return -1
		name_array = path.split('/')
		parent_inode_number = self.LOOKUP(path,inode_number_cwd)
		parent_inode = interface.INODE_NUMBER_TO_INODE(parent_inode_number)
		child_inode_number = self.CHILD_INODE_NUMBER_FROM_PARENT_INODE_NUMBER(name_array[-1], parent_inode_number)
		child_inode = interface.INODE_NUMBER_TO_INODE(child_inode_number)
		del parent_inode.directory[child_inode.name]
		interface.update_inode_table(parent_inode,parent_inode_number)
		interface.unlink(child_inode_number,parent_inode_number,child_inode.name)
		return True

	#MOVE
	def mv(self, old_path, new_path, inode_number_cwd):
		'''WRITE YOUR CODE HERE'''
		self.link(old_path, new_path, inode_number_cwd)
		self.unlink(old_path,inode_number_cwd)
		return True
