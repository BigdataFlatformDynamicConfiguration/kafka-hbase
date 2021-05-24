from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

if __name__ == '__main__':

    listen_port = '2000'

    ipaddr=subprocess.getoutput("hostname -I").split()[0]
    print ("Starting the service with ip_addr="+ipaddr)
    app.run(debug=True,host=ipaddr,port=int(listen_port),threaded=True)
