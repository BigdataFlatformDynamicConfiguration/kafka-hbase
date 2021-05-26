from flask import Flask, jsonify, request, render_template
import subprocess
import happybase
import sys
from waitress import serve

app = Flask(__name__)

hbaseHost = sys.argv[1]

@app.route('/', methods=['GET'])
def index():
    return "hello wolrd!"

@app.route('/create-table', methods=['GET'])
def create_table():
    global connection
    # get 으로 받은 쿼리 인자를 dict 형식으로 받아 data 에 저장
    data = request.args.to_dict()
    #http://ip:2000/create-table?table_name=테이블 이름&column_family_name=cf1
    if 'table_name' in table_name:
        table_name = data['table_name']
    else :
        return "There is no table name(table_name)."
    
    if 'column_family_name' in data:
        column_family_name = data['column_family_name']
    else:
        column_family_name = 'cf1'
        
    print('Creating the {} table.'.format(table_name))

    connection.create_table(
    table_name,
    {
        column_family_name: dict()  # Use default options.
    })
    return 'Creating the {} table.'.format(table_name)

@app.route('/table-list', methods=['GET'])
def table_list():
    connection = happybase.Connection(host=hbaseHost, port=9090)
    connection.open()
    
    print(connection)
    table_list = connection.tables()
    print(table_list)
    
    return str(table_list)

@app.route('/delete-table', methods=['GET'])
def delete_table():
    global connection
    # get 으로 받은 쿼리 인자를 dict 형식으로 받아 data 에 저장
    data = request.args.to_dict()
    #http://ip:2000/delete-table?table_name=테이블 이름
    
    print('Deleting the {} table.'.format(table_name))
    connection.delete_table(table_name)
    
    return 'Deleting the {} table.'.format(table_name)

@app.route('/row-list', methods=['GET'])
def row_list():
    
    return "hello wolrd!"

# if __name__ == '__main__':

#     listen_port = '2000'

#     ipaddr=subprocess.getoutput("hostname -I").split()[0]
#     print ("Starting the service with ip_addr="+ipaddr)
#     app.run(debug=True,host=ipaddr,port=int(listen_port),threaded=True)

if __name__ == '__main__':
    # hbase 연결
    global connection
    
    connection = happybase.Connection(host=hbaseHost, port=9090)
    connection.open()
    print(connection)
   
#     serve(app, host="0.0.0.0", port=2000)
    listen_port = '2000'
    app.run(debug=True, port=int(listen_port), host='0.0.0.0')
    
    #command ex) python app.py test-hbase-master
