from ctypes import *
import time
import struct
import argparse
 
def parseDWORD(data):
    return struct.unpack("I",data.raw[:4])[0]

read_file = windll.kernel32.ReadFile
write_file = windll.kernel32.WriteFile
close_handle = windll.kernel32.CloseHandle


bmc51lib = cdll.LoadLibrary("BMC51xUSB.dll")
handle = bmc51lib.open_dev()
if handle==-1:
    raise Exception("invalid handle")
close_handle(handle)

handle_write = bmc51lib.open_file("PIPE00")
handle_read  = bmc51lib.open_file("PIPE01")
if handle_read==-1:
    raise Exception("invalid handle")
if handle_write==-1:
    raise Exception("invalid handle")



def getuserWarnings():
    write_buffer = c_buffer("230101".decode("hex"), 3)
    number_of_bytes_written = c_buffer("", 4)
    
    retval = write_file(handle_write, write_buffer, 3, number_of_bytes_written, 0)
    if parseDWORD(number_of_bytes_written)!=3:
        raise Exception("wrong number of number_of_bytes_written")
    time.sleep(0.3)

    read_buffer = c_buffer("", 0x1000)
    number_of_bytes_read = c_buffer("",4)
    read_file(handle_read, read_buffer, 0x40, number_of_bytes_read,0)
    number_of_bytes_read_int = parseDWORD(number_of_bytes_read)
    print "first read: " +str(number_of_bytes_read_int)
    open("userwarnings","wb").write(read_buffer[:number_of_bytes_read_int])
    

def getuserDB():
    write_buffer = c_buffer("230201".decode("hex"), 3) 
    number_of_bytes_written = c_buffer("",4)

    retval = write_file(handle_write, write_buffer, 3, number_of_bytes_written, 0)
    if parseDWORD(number_of_bytes_written)!=3:
        raise Exception("wrong number of number_of_bytes_written")
    time.sleep(0.3)

    #18ef68

    #first read
    read_buffer = c_buffer("", 0x1000)
    number_of_bytes_read = c_buffer("",4)
    read_file(handle_read, read_buffer, 0x40, number_of_bytes_read,0)
    number_of_bytes_read_int = parseDWORD(number_of_bytes_read)
    print "first read: " +str(number_of_bytes_read_int)
    number_of_records = parseDWORD(read_buffer)
    print "number of records: " + str(number_of_records)
    
    outputfd = open("userdb","wb")

    # second read
    number_of_bytes_read = c_buffer("",4)
    read_file(handle_read, read_buffer, 0x200, number_of_bytes_read,0)
    number_of_bytes_read_int = parseDWORD(number_of_bytes_read)
    print "second read: " +str(number_of_bytes_read_int)
    outputfd.write(read_buffer[:number_of_bytes_read_int])

    # second read
    number_of_bytes_read = c_buffer("",4)
    read_file(handle_read, read_buffer, 0x200, number_of_bytes_read,0)
    number_of_bytes_read_int = parseDWORD(number_of_bytes_read)
    print "third read: " +str(number_of_bytes_read_int)
    outputfd.write(read_buffer[:number_of_bytes_read_int])
    
    outputfd.close()

def getuserSpeed():
    write_buffer = c_buffer("230301".decode("hex"), 3)
    number_of_bytes_written = c_buffer("", 4)
    
    retval = write_file(handle_write, write_buffer, 3, number_of_bytes_written, 0)
    if parseDWORD(number_of_bytes_written)!=3:
        raise Exception("wrong number of number_of_bytes_written")
    time.sleep(0.3)

    read_buffer = c_buffer("", 0x1000)
    number_of_bytes_read = c_buffer("",4)
    read_file(handle_read, read_buffer, 0x40, number_of_bytes_read,0)
    number_of_bytes_read_int = parseDWORD(number_of_bytes_read)
    print "first read: " + str(number_of_bytes_read_int)
    open("userspeed","wb").write(read_buffer)
    

def test(n):
	
    # 230101 - get user warnings
    # 230102 - set user warnings
    # 230201 - get user db
    # 230301 - get user speed

    #write_buffer = c_buffer(n.decode("hex"), 3)
    write_buffer = c_buffer(n.decode("hex"), 20)
    number_of_bytes_written = c_buffer("", 4)
    #retval = write_file(handle_write, write_buffer, 3, number_of_bytes_written, 0)
    retval = write_file(handle_write, write_buffer, 20, number_of_bytes_written, 0)
    #if parseDWORD(number_of_bytes_written) != 3:
    #    raise Exception("wrong number of number_of_bytes_written")
    time.sleep(0.3)
    print "wrote: " + str(parseDWORD(number_of_bytes_written))
            
    read_buffer = c_buffer("", 0x1000)
    number_of_bytes_read = c_buffer("",4)
    read_file(handle_read, read_buffer, 0x40, number_of_bytes_read,0)
    number_of_bytes_read_int = parseDWORD(number_of_bytes_read)
    print number_of_bytes_read_int
    open(n,"wb").write(read_buffer)

# user setting 230102


#ret_01 = bmc51lib.OpenUsbDevice()
#ret_02 = bmc51lib.OpenOneDevice()
#ret_03 = bmc51lib.open_file("\\\\?\\usb#vid_0e1&pid_0001#6&24bfad55%0%1#{8e120c45-4968-4188-ba19-9a82361c8fa8}")
#ret_04 = bmc51lib.OpenUsbDevice()

def main():
    parser = argparse.ArgumentParser(description='Communicate with c50')
    parser.add_argument('--get-user-warnings', dest='get_user_warnings', action='store_true')
    parser.add_argument('--get-user-db', dest='get_user_db', action='store_true')
    parser.add_argument('--get-user-speed', dest='get_user_speed', action='store_true')
    parser.add_argument('--test', dest='test' )
    args = parser.parse_args()

    #print "args = " +str(dir(args))
    #print "gudb = " + str(args.get_user_db)
    #print "test = " + str(args.test)
    if (args.get_user_warnings):
        getuserWarnings()
    if (args.get_user_db): 
        getuserDB()
    if (args.get_user_speed):
        getuserSpeed()
    if (args.test):
        test(args.test)
    
main()
