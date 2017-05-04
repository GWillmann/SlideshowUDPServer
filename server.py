import socket
import sys
import os
import json

#PI_ADDRESS = '192.168.1.103'
PI_ADDRESS = 'localhost'
PI_PORT = 10000
APP_PORT = 10001
#SLIDESHOW_ROOT_FOLDER = '/mnt/wdmycloud/Shared Pictures/'
SLIDESHOW_ROOT_FOLDER = '/Applications/'

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to the port
server_address = (PI_ADDRESS, PI_PORT)
print >>sys.stderr, 'starting up on %s port %s' % server_address
sock.bind(server_address)

# Save status of slideshow
slideshowRunning = False 

while True:
    print >>sys.stderr, '\nwaiting to receive message'
    data, address = sock.recvfrom(4096)
    ip, port = address

    print >>sys.stderr, 'received %s bytes from %s' % (len(data), address)
    print >>sys.stderr, data

    action, param = data.split(';')

    if slideshowRunning == False and action =="start":
        slideshowRunning = True
        #        os.system('DISPLAY=:0.0 XAUTHORITY=/home/pi/.Xauthority /usr/local/bin/feh --quiet --preload --auto-rotate -Z -F -Y -r -R 60 -D 15.0 "SLIDESHOW_ROOT_FOLDER"' + param + " &")
        print >>sys.stderr, "Diaporama en cours " + param
        dataToSendBack = 'status;running'
        
    if slideshowRunning == True and action =="stop":
        slideshowRunning = False
        print >>sys.stderr, "Diaporama ko"
        os.system('pkill feh')
        dataToSendBack = 'status;ko'
    
    if action == "listfolders":
        dataToSendBack = 'folders;' + json.dumps(os.listdir(SLIDESHOW_ROOT_FOLDER))
                    
    if dataToSendBack:
        sent = sock.sendto(dataToSendBack, (ip, APP_PORT))
        print >>sys.stderr, 'sent %s bytes back to %s' % (sent, address)
