import socket
import threading
from json import loads, dumps


def split_port_range(port_range, num_nodes):
    num_nodes = int(num_nodes)
    try:
        start, end = map(int, port_range.split('-'))
        if start < 1 or end > 65535 or start > end or num_nodes < 1:
            raise ValueError("Invalid input")

        total_ports = end - start + 1
        ports_per_node = total_ports // num_nodes
        remaining_ports = total_ports % num_nodes

        subranges = []
        current_port = start

        for i in range(num_nodes):
            subrange_start = current_port
            subrange_end = subrange_start + ports_per_node - 1

            if remaining_ports > 0:
                subrange_end += 1
                remaining_ports -= 1

            subranges.append(f"{subrange_start}-{subrange_end}")
            current_port = subrange_end + 1
        for port_range in subranges:
            print(f"   {port_range}")

        return subranges

    except ValueError as e:
        print(f"Error: {e}")
        return []


def handle_client(client_socket, client_name, port_range, ip_range, thread, timeout):
    while True:
        if send_data:
            all = f"{port_range}??<><>{ip_range}??<><>{thread}??<><>{timeout}"
            client_socket.send(all.encode('utf-8'))
            break
    while True:
        recv = client_socket.recv(2048).decode('utf-8')
        if recv == "!!":
            client_socket.close()
            print(f"{client_name} has disconnected")
            break
        else:
            print(recv)


def create_and_handle_server(port_ranges, ip_range, thread, timeout, server_port):
    global send_data
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("0.0.0.0", server_port))
    server_socket.listen(nodes)

    print(f"Server is listening on 0.0.0.0:{server_port} for {nodes} client(s)")

    for i in range(nodes):
        client_socket, client_address = server_socket.accept()
        client_name = client_socket.recv(2048).decode('utf-8')
        print(f"Connection from {client_address[0]}:{client_address[1]}/{client_name}")

        client_thread = threading.Thread(target=handle_client,
                                         args=(client_socket, client_name, port_ranges[i], ip_range, thread, timeout))
        client_thread.start()
    send_data = True

try:
    with open("server_config.json", "r+") as f:
        config = loads(f.read())
    port_range = config["port_range"]
    thread = config["thread"]
    timeout = config["timeout"]
    nodes = config["nodes"]
    server_port = config["server_port"]

except Exception as e:
    print(e)
    print("Enter port range:")
    port_range = input()
    print("Enter thread :")
    thread = input()
    print("Enter timeout :")
    timeout = input()
    print("Enter nodes :")
    nodes = int(input())
    print("Enter server port (must be open and not taken):")
    server_port = int(input())

    with open("server_config.json", "w") as f:
        f.write(dumps({"port_range": port_range, "thread": thread, "timeout": timeout, "nodes": nodes,
                       "server_port": server_port}))


print("Enter IP range(per client): ")
ip_range = input()
send_data = False

create_and_handle_server(split_port_range(port_range, nodes), ip_range, thread, timeout, server_port)
