from flask import Flask, jsonify, request, render_template
from kafka import KafkaProducer
from kafka import KafkaConsumer
import threading, logging, time
import subprocess
import happybase
import sys
import json

app = Flask(__name__)

kafkaHost = sys.argv[1]
hbaseHost = sys.argv[2]

class Producer(threading.Thread):
    def __init__(self, kafkaHost, data):
        self.data = data
        threading.Thread.__init__(self)
        self.stop_event = threading.Event()
        
    def stop(self):
        self.stop_event.set()

    def run(self):
        producer = KafkaProducer(bootstrap_servers= kafkaHost + ':9092',
                     value_serializer=lambda m: json.dumps(m).encode('ascii'))
        producer.send('my-topic1', self.data)
        producer.close()
 
class Consumer(threading.Thread):
    def __init__(self, kafkaHost, hbaseHost):
        threading.Thread.__init__(self)
        self.stop_event = threading.Event()
        
    def stop(self):
        self.stop_event.set()

    def run(self):
        consumer = KafkaConsumer('my-topic1',
                     bootstrap_servers=[ kafkaHost + ':9092'],
                     value_deserializer=lambda m: json.loads(m.decode('ascii')))
        while not self.stop_event.is_set():
            for message in consumer:
                # message value and key are raw bytes -- decode if necessary!
                # e.g., for unicode: `message.value.decode('utf-8')`
                print ("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition,
                                          message.offset, message.key,
                                          message.value))
        
#         connection = happybase.Connection(host=hbaseHost, port=9090)
#         connection.open()

#         table = connection.table('my-topic11')
        
#         count = 0
#         while not self.stop_event.is_set():
#             for message in consumer:
#                 count += 1
#                 print ("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition,
#                                                   message.offset, message.key,
#                                                   message.value))
#                 table.put('row-key' + str(count), {'cf:col1': message.value})
#                 if self.stop_event.is_set():
#                     break

#         for key, data in table.scan():
#             print(key, data)
            
        consumer.close()        

@app.route('/', methods=['GET'])
def index():
    return "hello wolrd!"

@app.route('/scan', methods=['POST'])
def scan():
    data = request.get_json()
    connection = happybase.Connection(host=hbaseHost, port=9090)
    connection.open()
    table = connection.table(data['table'])
    
    if 'row_start' in data:
        if 'row_stop' in data:
            if 'filter' in data:
                res = table.scan(row_start=data['row_start'], row_stop=data['row_stop'], filter = data['filter'] )
            else:
                res = table.scan(row_start=data['row_start'], row_stop=data['row_stop'])
        else:
            if 'filter' in data:
                res = table.scan(row_start=data['row_start'], filter = data['filter'] )
            else:
                res = table.scan(row_start=data['row_start'])
    else:
        if 'row_stop' in data:
            if 'filter' in data:
                res = table.scan(row_stop=data['row_stop'], filter = data['filter'] )
            else:
                res = table.scan(row_stop=data['row_stop'])
        else:
            if 'filter' in data:
                res = table.scan(row_stop=data['row_stop'])
            else:
                res = table.scan()
    
    print(json.dumps({data:res}))
    return 'hello scan'

@app.route('/create-table', methods=['GET'])
def create_table():
    connection = happybase.Connection(host=hbaseHost, port=9090)
    connection.open()
    # get 으로 받은 쿼리 인자를 dict 형식으로 받아 data 에 저장
    data = request.args.to_dict()
    #http://ip:2000/create-table?table_name=테이블 이름&column_family_name=cf1
    if 'table_name' in data:
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
    connection = happybase.Connection(host=hbaseHost, port=9090)
    connection.open()
    # get 으로 받은 쿼리 인자를 dict 형식으로 받아 data 에 저장
    data = request.args.to_dict()
    #http://ip:2000/delete-table?table_name=테이블 이름
    if 'table_name' in data:
        table_name = data['table_name']
    else :
        return "There is no table name(table_name)."
    
    table_list = connection.tables()
    
    table_name_encode = table_name.encode()

    if table_name_encode in table_list:
        connection.delete_table(table_name, disable=True)    
        print('Deleting the {} table.'.format(table_name))
        return 'Deleting the {} table.'.format(table_name)
    else:
        return 'There is no table name corresponding to hbase.'
    return 'delete table'

@app.route('/row-list', methods=['POST'])
def row_list():
    # post 로 전달 받은 정보를 python dict 형태로 data 에 저장
    data = request.form.to_dict()
    print(data)
    
    tasks = [
        Consumer(kafkaHost, hbaseHost),
        Producer(kafkaHost, data)
    ]

    for t in tasks:
        t.daemon = True
        t.start()
        
    time.sleep(2)
    
    for task in tasks:
        task.stop()

    for task in tasks:
        task.join()
    
    return "hello wolrd!"

# if __name__ == '__main__':

#     listen_port = '2000'

#     ipaddr=subprocess.getoutput("hostname -I").split()[0]
#     print ("Starting the service with ip_addr="+ipaddr)
#     app.run(debug=True,host=ipaddr,port=int(listen_port),threaded=True)

if __name__ == '__main__':
    # hbase 연결
    listen_port = '2001'
    app.run(debug=True, port=int(listen_port), host='0.0.0.0')
    
    #command ex) python app.py test-hbase-master
