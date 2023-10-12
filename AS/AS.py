import ast
from flask import Flask, abort
import socket

app = Flask(__name__)
# Socket Programming for AS server
AS_IP = '0.0.0.0'
AS_Port = 53533
buffer_size = 1024


def get_fs_body(as_ip, as_port):
    as_fs_udp_socket = socket.socket(family=socket.AF_INET,
                                     type=socket.SOCK_DGRAM)
    as_fs_udp_socket.bind((as_ip, as_port))
    msg_from_as = "FS Server has successfully registered to Authoritative Server"
    send_bytes = str.encode(msg_from_as)
    while True:
        bytes_address_pair = as_fs_udp_socket.recvfrom(buffer_size)
        msg_from_fs = bytes_address_pair[0]
        fs_address = bytes_address_pair[1]  # ('127.0.0.1', 52311)
        fs_ip = bytes_address_pair[1][0]
        fs_msg = "Message from FS Server is {}".format(msg_from_fs)
        fs_ip = "IP address of FS server is {}".format(fs_ip)
        print(fs_msg)
        print(fs_ip)
        as_fs_udp_socket.sendto(send_bytes, fs_address)
        return msg_from_fs


def dns_us_request_response(as_ip, as_port):
    as_us_udp_socket = socket.socket(family=socket.AF_INET,
                                     type=socket.SOCK_DGRAM)
    as_us_udp_socket.bind((as_ip, as_port))
    while True:
        bytes_address_pair = as_us_udp_socket.recvfrom(buffer_size)
        msg_from_us = bytes_address_pair[0]
        us_address = bytes_address_pair[1]  # ('127.0.0.1', 52311)
        us_ip = bytes_address_pair[1][0]
        us_msg = "Message from US Server is {}".format(msg_from_us)
        us_ip = "IP address of US server is {}".format(us_ip)
        return msg_from_us, us_address, as_us_udp_socket


def dns_lookup(fs_dict, us_dict):
    fs_dict = str(fs_dict, encoding='utf-8')  # converts dictionary to string
    us_dict = str(us_dict, encoding='utf-8')
    us_dict = ast.literal_eval(us_dict)  # ast module converts string into dictionary
    fs_dict = ast.literal_eval(fs_dict)
    if us_dict['Type'] == fs_dict['TYPE'] and us_dict['Name'] == fs_dict['NAME']:
        return 200
    else:
        return 404


def send_message_to_us_server(us_values, check_value, fs_dict):
    us_address = us_values[1]
    as_us_udp_socket = us_values[2]
    if check_value == 200:
        fs_dict = fs_dict.decode('utf-8')
        msg_from_as = str(fs_dict)
        send_bytes = str.encode(msg_from_as)  # need to convert string into bytes
        as_us_udp_socket.sendto(send_bytes, us_address)
        return "Success", 200
    else:
        abort(400)


FS_Dict = get_fs_body(AS_IP, AS_Port)  # function that extracts the bytes sent by fibonacci server
US_Values = dns_us_request_response(AS_IP, AS_Port)  # returns that data sent by US server and  its address
US_Dict = US_Values[0]
check_val = dns_lookup(FS_Dict, US_Dict)
print(check_val)
send_message_to_us_server(US_Values, check_val, FS_Dict)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=53533)  # DNS server operates on port 53
