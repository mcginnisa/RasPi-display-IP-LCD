
import I2C_LCD_driver
import socket
import fcntl
import struct
import time
import subprocess
import traceback

#This line opens a log file
#log = open("log.txt", "w")

#time.sleep(10)

mylcd = I2C_LCD_driver.lcd()

def get_ip_address(ifname):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return socket.inet_ntoa(fcntl.ioctl(
            s.fileno(),
            0x8915, 
            struct.pack('256s', ifname[:15])
        )[20:24])
    except:
        return 'No IP on ' + ifname

def get_ip_from_bigger_string(containsIP):
    #will pull out IP of any size and format it nicely, IF IF IF the string begins with the IP!!!
    spaceSlots = containsIP.split(" ") # isolate the IP string with spaces
    spaceSlots = spaceSlots[0] 
    byteList = spaceSlots.split(".") # split the IP up into . seperated entries
    #print(byteList)
    outIP = ''
    for i in range(0,4):
        outIP += byteList[i] + '.'
    outIP = outIP[0:len(outIP)-1] #remove last dot
    return outIP 

def get_ip_wTCPDUMP(ifname):
    #output = subprocess.check_output("hw4_10_21/getIP_withTCPDUMP.sh " + ifname, shell=True)
    subprocess.call("hw4_10_21/getIP_withTCPDUMP.sh " + ifname, shell=True)
        
    with open('temp.txt','r') as myfile:
        TCPDUMPoutputString = myfile.read()
    if TCPDUMPoutputString.find('IP') > 1:
        index = TCPDUMPoutputString.find('IP') #get index of 'IP' in the TCPDUMP output
        containsIP = TCPDUMPoutputString[index+3:index+3+16] #get a string that  starts with the IP
        sourceIP = get_ip_from_bigger_string(containsIP)
    else:
        sourceIP = 'No IP!'
    return sourceIP

    
for i in range(0,20): #time out after x scans
    try:
        time.sleep(1)
        mylcd.lcd_write(0x01) # clear screen
        mylcd.lcd_display_string('eth0, loop ' + str(i), 1) 
        mylcd.lcd_display_string(get_ip_wTCPDUMP('eth0'), 2)
        time.sleep(1)
        mylcd.lcd_write(0x01) # clear screen
        mylcd.lcd_display_string('wlan0, loop ' + str(i), 1) 
        mylcd.lcd_display_string(get_ip_wTCPDUMP('wlan0'), 2)
     
    #except Exception:
    except Exception as e:
        f = open('log.txt', 'w')
        f.write('An exceptional thing happed - %s' % e)
        f.close()
        #traceback.print_exc(file=log)
        continue

