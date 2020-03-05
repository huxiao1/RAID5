'''
THIS MODULE IS INODE LAYER OF THE FILE SYSTEM. IT INCLUDES THE INODE DEFINITION DECLARATION AND GLOBAL HANDLE OF BLOCK LAYER OF API.
THIS MODULE IS RESPONSIBLE FOR PROVIDING ACTUAL BLOCK NUMBERS SAVED IN INODE ARRAY OF BLOCK NUMBERS TO FETCH DATA FROM BLOCK LAYER.
'''
import datetime, config, BlockLayer, InodeOps

#HANDLE OF BLOCK LAYER
interface = BlockLayer.BlockLayer()

class InodeLayer():

    #RETURNS BLOCK NUMBER FROM RESPECTIVE INODE DIRECTORY
    def INDEX_TO_BLOCK_NUMBER(self, inode, index):
        if index == len(inode.blk_numbers): return -1
        return inode.blk_numbers[index]


    #RETURNS BLOCK DATA FROM INODE
    def INODE_TO_BLOCK(self, inode, offset):
        index = offset / config.BLOCK_SIZE
        block_number = self.INDEX_TO_BLOCK_NUMBER(inode, index)
        if block_number == -1: return ''
        else: return interface.BLOCK_NUMBER_TO_DATA_BLOCK(block_number)


    #MAKES NEW INODE OBJECT
    def new_inode(self, type):
	#print("we get the new inode")
        return InodeOps.Table_Inode(type)


    #FLUSHES ALL THE BLOCKS OF INODES FROM GIVEN INDEX OF MAPPING ARRAY  
    def free_data_block(self, inode, index):
        for i in range(index, len(inode.blk_numbers)):
            interface.free_data_block(inode.blk_numbers[i])
            inode.blk_numbers[i] = -1


    #IMPLEMENTS WRITE FUNCTIONALITY
    def write(self, inode, offset, data):
        #PLACE CODE FROM HW2 HERE
        #check inode value
        if offset < 0:
            print("Error: Wrong offset value!")
            return -1
        #check inode type    
        if(inode.type == 1):
            print("Error: Wrong Inode type!")
            return -1
        #Update the time of access
        inode.time_accessed = str(datetime.datetime.now())[:19]
        #Get the the length of old data to see if offset is right
        old_data = []
        for i in range(0,inode.size,config.BLOCK_SIZE): 
            old_data.append(self.INODE_TO_BLOCK(inode,i))
        old_string = "".join(old_data)
        #in case there is blank data in the string
        nonezero_data = []
        for i in range(len(old_string)):
            if old_string[i] != "\0":
                nonezero_data.append(old_string[i])
            else:
                break
        #check whether the offset exceeds the size of the oringnal file
        if offset > len(nonezero_data):
            print("Error: Wrong offset!")
            return -1
        data_raw = []
        #Get previous data and assemble it with input data
        for i in range(offset):
            data_raw.append(nonezero_data[i])
        new_string = ("".join(data_raw)) + data
        index = offset / config.BLOCK_SIZE
        if inode.size!=0:
        #Clear all the data blocks from the offset
            self.free_data_block(inode,index)
            ###print("the index for",new_string,"is",index)
        #Truncate the string if it exceeds max file size
            if len(new_string) > (((config.INODE_SIZE - 63 - config.MAX_FILE_NAME_SIZE) / 2) * config.BLOCK_SIZE):
                new_string=new_string[0:(((config.INODE_SIZE - 63 - config.MAX_FILE_NAME_SIZE) / 2) * config.BLOCK_SIZE)]  
            if offset != 0:    
                new_string = new_string[offset - offset%config.BLOCK_SIZE:len(new_string)]
            else:
                new_string = new_string[offset:len(new_string)]
        ###print("the whole new_string is",new_string)  
        data_array = []
        for i in range(0,len(new_string),config.BLOCK_SIZE):
            data_array.append(new_string[i : i + config.BLOCK_SIZE])

        #write the data into blocks
        for i in range(len(data_array)):
            valid_block_number = interface.get_valid_data_block()
            interface.update_data_block(valid_block_number, data_array[i])
            inode.blk_numbers[i + index]=valid_block_number
            #print(inode.blk_numbers)
        ###print("the inode content is",self.INODE_TO_BLOCK(inode,0))
        #update inode size
        inode.size=len(new_string)
        #update time_modified
        inode.time_modified = str(datetime.datetime.now())[:19]  
        ##return inode  
	return True



    #IMPLEMENTS THE READ FUNCTION 
    def read(self, inode, offset, length): 
        #PLACE CODE FROM HW2 HERE
        #check inode value
        if offset < 0:
            print("Error: Wrong offset value!")
            return -1
        #check inode type
        if inode.type == 1:
            print("Error: Wrong Inode type!")
            return -1
        #update access time
        inode.time_accessed = str(datetime.datetime.now())[:19]
        #read
        data_read=[]
        if offset > inode.size:
            return "Error: Wrong offset value!"
        else:
            for i in range (len(inode.blk_numbers)):
                if inode.blk_numbers[i]!= -1:
                    data_read.append(interface.BLOCK_NUMBER_TO_DATA_BLOCK(inode.blk_numbers[i]))
                else:
                    break
        data_return=''.join(data_read)
        return data_return[offset:offset+length]
        #return inode
