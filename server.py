import socket
import sys
import os
import json
import glob
import subprocess

PI_ADDRESS = ''
#PI_ADDRESS = 'localhost'
PI_PORT = 10000
APP_PORT = 10001
SLIDESHOW_ROOT_FOLDER = '/mnt/wdmycloud/Shared Pictures/'
#SLIDESHOW_ROOT_FOLDER = '/Applications/'

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to the port
server_address = (PI_ADDRESS, PI_PORT)
print >>sys.stderr, 'starting up on %s port %s' % server_address
sock.bind(server_address)

# Save status of slideshow
process = subprocess.Popen('ls', stdout=subprocess.PIPE)

def is_running():
    return process.poll() == None

def launch_slideshow(pictures_path):
    os.environ['DISPLAY'] = ':0.0'
    os.environ['XAUTHORITY'] = '/home/pi/.Xauthority'

    cmd = ['/usr/local/bin/feh', '--quiet', '--preload', '--auto-rotate', '-V', '-Z', '-F', '-Y', '-r', '-R 60', '-D 15.0', pictures_path]
    return subprocess.Popen(cmd, stdout=subprocess.PIPE)

# Remove folders with trailing dots
def listdir_nohidden(path):
    folders = []
    for folder in glob.glob(path + '*'):
        file_count = 0
        for file in glob.glob(folder + '/*.*'):
                file_count += 1
        f = []
        f.append(folder.split('/')[len(folder.split('/')) - 1])
        f.append(file_count)
        folders.append(f)
    return sorted(folders, key=lambda x: x[0].lower)

while True:
    print >>sys.stderr, '\nwaiting to receive message'
    data, address = sock.recvfrom(4096)
    ip, port = address

    print >>sys.stderr, 'received %s bytes from %s' % (len(data), address)
    print >>sys.stderr, data

    action, param = data.split(';')

    dataToSendBack = ''
    if action == 'whois':
        print >>sys.stderr, " IM RIGHT HERE !!!" + param
        dataToSendBack = 'iam;'

    if is_running() == False and action =="start":
        process = launch_slideshow(SLIDESHOW_ROOT_FOLDER + param)
        print >>sys.stderr, "Diaporama en cours " + param
        dataToSendBack = 'status;running'

    if is_running() == True and action =="stop":
        print >>sys.stderr, "Diaporama ko"
        process.terminate()
        dataToSendBack = 'status;ko'

    if action == "listfolders":
        dataToSendBack = 'folders;' + json.dumps((listdir_nohidden(SLIDESHOW_ROOT_FOLDER)))

    if action == "getstatus":
        dataToSendBack = 'slideshowstatus;' + str(is_running())

    if dataToSendBack:
        sent = sock.sendto(dataToSendBack, (ip, APP_PORT))
        print >>sys.stderr, 'sent %s bytes back to %s :\n %s' % (sent, address, dataToSendBack)
