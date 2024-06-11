from socket import *
import os
import struct

def send_message(conn, message):
    size = len(message)
    conn.send(size.to_bytes(4, byteorder='little'))
    conn.sendall(message.encode())

def receive_message(conn):
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


def ReceiveFile(conn, file_name):
    file_path = "D:/RecivedFiles/" + file_name
    size = int.from_bytes(conn.recv(4), byteorder='little')
    with open(file_path, 'wb') as file:
        temp = 0
        tempb = b''
        while True:
            tempc = conn.recv(size-temp)
            tempb += tempc
            temp = len(tempb)
            if temp >= size:
                break
        file.write(tempb)
        print("File Received")

def main():
    serverName = 'localhost'
    serverPort = 65430
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((serverName, serverPort))
    while True:
        while True:
            message = receive_message(clientSocket)
            if message == "Exit":
                break
            else:
                print(message)
        x = input('\n\n\nEnter The File Number or Exit to close the connection:')
        if x == "Exit":
            break
        else:
            filenum = int(x)
            print("File Number: ", filenum)
        data = filenum.to_bytes(4, byteorder='little')
        clientSocket.send(data)
        filename = receive_message(clientSocket)
        ReceiveFile(clientSocket, filename)
        print("File Received")
    clientSocket.close()


if __name__ == '__main__':
    main()
