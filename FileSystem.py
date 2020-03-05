import MemoryInterface, AbsolutePathNameLayer,time,sys

def Initialize_My_FileSystem():
    MemoryInterface.Initialize_My_FileSystem()
    AbsolutePathNameLayer.AbsolutePathNameLayer().new_entry('/', 1)

#HANDLE TO ABSOLUTE PATH NAME LAYER
interface = AbsolutePathNameLayer.AbsolutePathNameLayer()

class FileSystemOperations():

    #MAKES NEW DIRECTORY
    def mkdir(self, path):
        interface.new_entry(path, 1)

    #CREATE FILE
    def create(self, path):
        interface.new_entry(path, 0)
        

    #WRITE TO FILE
    def write(self, path, data, offset=0):
        interface.write(path, offset, data)
      

    #READ
    def read(self, path, offset=0, size=-1):
	print("plz input serverNumber whose data is corrupted, if ur input >3, no server's data is corrupted")
	serverNum = int(raw_input())
	if serverNum<4:
		MemoryInterface.corruptData(serverNum)
	
        read_buffer = interface.read(path, offset, size)
        if read_buffer != -1: print(path + " : " + read_buffer)

    
    #DELETE
    def rm(self, path):
        interface.unlink(path)


    #MOVING FILE
    def mv(self, old_path, new_path):
        interface.mv(old_path, new_path)


    #CHECK STATUS
    def status(self):
        print(MemoryInterface.status())



if __name__ == '__main__':
    Initialize_My_FileSystem()
    my_object = FileSystemOperations()
    print("Please input the waiting time: ")
    waiting=input()
    start = True
    
    while(start == True):
	print("please input the command: ")
	command = raw_input("$ ")
        if command=="mkdir":
            print("please input which directory you want to create: ")
            directory=raw_input()
            my_object.mkdir(directory)
            print("Directory has been created!")

        elif command=="create":
            print("please input the path of the file that you want to create: ")
            file=raw_input()
            my_object.create(file)
            print("File has been created!")

        elif command=="write":
            print("please input the path of the file that you want to write to: ")
            file=raw_input()
	    print("please input the data that you want to write: ")
            data=raw_input()
            print("Please wait until the write is done......")
            time.sleep(waiting)
	    my_object.write(file,data,0)
            print("data has been writed to the file!")
            time.sleep(waiting)
            print("parity has been writed successfully!")

        elif command=="read":
            print("please waite")
            time.sleep(5)
            print("please input which file you want to read: ")
            file=raw_input()
   	    my_object.read(file,0,-1)

        elif command=="mv":
            print("please input which file you want to move: ")
            file=raw_input()
            print("please input where you want to move this file to: ")
            destination=raw_input()
            my_object.mv(file, destination)
            print("File has been moved to the destination!")

        elif command=="rm":
            print("please input which file you want to remove:")
            file=raw_input()
            my_object.rm(file)
            print("File has been removed!")

        elif command=="status":
            my_object.status()

        elif command=="exit":
            print("Command finished!")

            start=False

