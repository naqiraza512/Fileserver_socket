from socket import *
from struct import *
import os
import threading

def GetFileList(conn):
    fileList = os.listdir("D:/FileServer")
    for files in fileList:
        file_path = "D:/FileServer/" + files
        file_size = os.path.getsize(file_path)
        message = "File Name: " + files + " File Size: " + str(file_size) +"\n"
        SendMessage(conn, message)
        print("File Name: ", files, "File Size: ", file_size)
    SendMessage(conn, "Exit")

def SendMessage(conn, message):
    size = len(message)
    conn.send(size.to_bytes(4, byteorder='little'))
    conn.sendall(message.encode())

def RecieveMessage(conn):
    size = int.from_bytes(conn.recv(4), byteorder='little')
    temp = 0
    tempb = b''
    while True:
        tempc = conn.recv(size-temp)
        tempb += tempc
        temp += len(tempb)
        if temp == size:
            break
    message = tempb.decode()
    return message

def SendFile(conn, file_name):
    file_path = "D:/FileServer/" + file_name
    file_size = os.path.getsize(file_path)
    SendMessage(conn, file_name)
    size = file_size.to_bytes(4, byteorder='little')
    conn.send(size)
    with open(file_path, 'rb') as file:
        data = file.read(1024)
        while data:
            conn.sendall(data)
            data = file.read(1024)
    print("File Sent")

def GetfileName(x):
    fileList = os.listdir("D:/FileServer")
    file_name = fileList[x-1]
    return file_name

def ClientThread(conn, addr):
    print("Connected to ", addr)
    while True:
        GetFileList(conn)
        messageCode = conn.recv(4)
        message = messageCode.decode()
        if message == "Exit":
            break
        else:
            filenum = int.from_bytes(messageCode, byteorder='little')
        print("File Number: ", filenum)
        x = GetfileName(filenum)
        SendFile(conn, x)
    conn.close()
    print("Connection Closed")


def Main():
    Host = "127.0.0.1"
    port = 65430

    server = socket(AF_INET, SOCK_STREAM)
    server.bind((Host, port))
    server.listen(5)
    print("Server Started")
    try:
        while True:
            conn, addr = server.accept()
            threading.Thread(target=ClientThread, args=(conn,addr)).start()
    except KeyboardInterrupt:
        print("Server Closed")
        server.close()


if __name__ == "__main__":
    Main()