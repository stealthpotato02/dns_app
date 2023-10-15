# Sai Krishna Bommavaram
import urllib.request

from flask import Flask, abort, request, redirect
import ast

import socket

app = Flask(__name__)


@app.route('/fibonacci')
def us_server():  # put application's code here
    hostname = request.args.get('hostname')  # gets the argument form the request query
    fs_port = request.args.get('fs_port')
    fs_port = int(fs_port)  # convert the string sent into integer
    number = request.args.get('number')
    number = int(number)
    as_ip = request.args.get('as_ip')
    as_port = request.args.get('as_port')
    as_port = int(as_port)
    dns_req_dict = {'Type': 'A', 'Name': hostname}

    if hostname is not None and fs_port is not None and number is not None and as_ip is not None and as_port is not None:
        # UDP Socket Programming
        dns_query = str(dns_req_dict)
        bytes_sent = str.encode(dns_query)
        buffer = 1024
        us_udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        as_address = (as_ip, as_port)
        us_udp_socket.sendto(bytes_sent, as_address)
        dns_response_as_server = us_udp_socket.recvfrom(buffer)
        msg = 'Message from AS_Server is {}'.format(dns_response_as_server[0])
        fs_details = dns_response_as_server[0].decode('utf-8')
        print("Successfully received IP address")
        fs_detail = ast.literal_eval(fs_details)  # converts string to dictionary
        fs_ip = str(fs_detail['VALUE'])
        fibonacci_request_string = "http://" + fs_ip + ":" + str(fs_port) + "/fibonacci?number=" + str(number)
        fibonacci_answer = urllib.request.urlopen(
            fibonacci_request_string)  # the urllib function gets all the details from the FS url
        return fibonacci_answer, 200
    else:
        abort(404)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=8080)
