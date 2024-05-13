# this is the code before the impl of qchecker

import socket
from time import sleep
import subprocess
from json import loads, dumps

try:
    with open("config.json", "r+") as f:
        config = loads(f.read())
    server_host = config["server_host"]
    server_port = config["server_port"]
    print(f"Server IP:Port : {server_host}:{server_port}")

except Exception as e:
    print(e)
    server_host, server_port = input("Enter server ip:port :").split(":")
    with open("config.json", "w") as f:
        f.write(dumps({"server_host": server_host, "server_port": server_port}))


def connect_to_server(server_host, server_port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = client_socket.connect_ex((server_host, int(server_port)))

    if result:
        return
    print(f"Connected to the server at {server_host}:{server_port}")
    client_name = client_socket.recv(1024).decode('utf-8')
    print(f"Client name: {client_name}")

    port_range, ip_range, thread, timeout = client_socket.recv(1024).decode('utf-8').split("??<><>")
    command = f"java -Dfile.encoding=UTF-8 -jar qubo.jar -range {ip_range} -ports {port_range} -th {thread} -ti {timeout}"
    result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    output_lines = result.stdout.splitlines()

    for line in output_lines:
        client_socket.send(line.encode('utf-8'))
        print(client_socket.recv(4096).decode('utf-8'))
        sleep(0.05)
    client_socket.send("!!".encode('utf-8'))
    client_socket.close()
    print("Disconnected from the server")


def main():
    while True:
        connect_to_server(server_host, server_port)


main()
