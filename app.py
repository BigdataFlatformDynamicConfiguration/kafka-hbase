from flask import Flask, jsonify, request, render_template
import subprocess

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return "hello wolrd!"

# if __name__ == '__main__':

#     listen_port = '2000'

#     ipaddr=subprocess.getoutput("hostname -I").split()[0]
#     print ("Starting the service with ip_addr="+ipaddr)
#     app.run(debug=True,host=ipaddr,port=int(listen_port),threaded=True)

if __name__ == '__main__':
    listen_port = '2000'
    app.run(debug=True, port=int(listen_port), host='34.64.100.75')
