# this is the code before the impl of qchecker

import socket
from time import sleep
import subprocess

client_name = input("Enter client name: ")
server_host = 'in1.endercloud.tech'
server_port = 25567

def connect_to_server(server_host, server_port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = client_socket.connect_ex((server_host, server_port))

    if result:
        return 
    print(f"Connected to the server at {server_host}:{server_port}")
    client_socket.send(client_name.encode('utf-8'))
    
    port_range, ip_range, thread, timeout = client_socket.recv(1024).decode('utf-8').split("??<><>")
    command = f"java -Dfile.encoding=UTF-8 -jar qubo.jar -range {ip_range} -ports {port_range} -th {thread} -ti {timeout}"
    result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    output_lines = result.stdout.splitlines()

    for line in output_lines:
        client_socket.send(line.encode('utf-8'))
        print(line)
        sleep(0.2) #buffer time since cloud shell limits data transfer and can term your account
    client_socket.send("!!".encode('utf-8'))

def main():
    while True:
        connect_to_server(server_host, server_port)

main()