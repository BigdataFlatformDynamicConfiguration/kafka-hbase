from flask import Flask, jsonify, request, render_template
from kafka import KafkaProducer
from kafka import KafkaConsumer
import threading, logging, time
import subprocess
import happybase
import sys
import json
import socket 

app = Flask(__name__)

kafkaHost = sys.argv[1]
hbaseHost = sys.argv[2]
topicName = socket.gethostbyname(socket.gethostname())
#table_row_cnt = dict()
kafka_offset = dict()

print(topicName);

class Producer(threading.Thread):
    def __init__(self, kafkaHost, data):
        self.data = data
        threading.Thread.__init__(self)
        self.stop_event = threading.Event()
        
    def stop(self):
        self.stop_event.set()

    def run(self):
        producer = KafkaProducer(bootstrap_servers= kafkaHost + ':9092',
                     value_serializer=lambda m: json.dumps(m).encode('utf-8'))
#         producer = KafkaProducer(bootstrap_servers= kafkaHost + ':9092')
        producer.send(topicName, self.data)
        producer.close()
 
class Consumer(threading.Thread):
    def __init__(self, kafkaHost, hbaseHost):
        threading.Thread.__init__(self)
        self.stop_event = threading.Event()
        
    def stop(self):
        self.stop_event.set()

    def run(self):
        consumer = KafkaConsumer(topicName,
                     bootstrap_servers=[ kafkaHost + ':9092'],
                     value_deserializer=lambda m: json.loads(m.decode('utf-8')))

        connection = happybase.Connection(host=hbaseHost, port=9090)
        connection.open()
        
        while not self.stop_event.is_set():
            for message in consumer:
                if message.topic in kafka_offset:
                    if kafka_offset[message.topic] == message.offset:
                        continue
                else: 
                    kafka_offset[message.topic] = message.offset
                    
                kafka_offset[message.topic] = message.offset
                data = json.loads(str(message.value).replace("\'", "\""))
          
                if 'table_name' in data:
                    table_name = data['table_name']
                else:
                    table_name = topicName
                    
                table = connection.table(table_name)
                
                if 'table_name' in data:  
                    b = table.batch()
                    
                    data_list = data['datalist']
                    for i in data_list:  
                        b.put(i['rowkey'], i['data'])
                    b.send()
                
                break
                if self.stop_event.is_set():
                    break
                    
        consumer.close()        

@app.route('/', methods=['GET'])
def index():
    return topicName

@app.route('/create-table', methods=['POST'])
def create_table():
    connection = happybase.Connection(host=hbaseHost, port=9090)
    connection.open()
    # get ?????? ?????? ?????? ????????? dict ???????????? ?????? data ??? ??????
    data = request.get_json()
    #http://ip:2000/create-table?table_name=????????? ??????&column_family_name=cf1
    if 'table_name' in data:
        table_name = data['table_name']
    else :
        return "There is no table name(table_name)."
    
    if 'column_family_name' in data:
        column_family_name = data['column_family_name']
    else:
        column_family_name = {'cf1':{}}

    connection.create_table(table_name,column_family_name)        
    print('Creating the {} table.'.format(table_name))

    return 'Creating the {} table.'.format(table_name)

@app.route('/table-list', methods=['GET'])
def table_list():
    connection = happybase.Connection(host=hbaseHost, port=9090)
    connection.open()
    
    table_list = connection.tables()
    
    result = []
    for table in table_list:
        result.append(table.decode('utf-8'))

    return json.dumps(result)

@app.route('/delete-table', methods=['GET'])
def delete_table():
    connection = happybase.Connection(host=hbaseHost, port=9090)
    connection.open()
    # get ?????? ?????? ?????? ????????? dict ???????????? ?????? data ??? ??????
    data = request.args.to_dict()
    #http://ip:2000/delete-table?table_name=????????? ??????
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
                res = table.scan(filter=data['filter'])
            else:
                res = table.scan()
    
    result = {}
    for key, data in res:
        data = {y.decode('utf-8'):data.get(y).decode('utf-8') for y in data.keys()}
        result[key.decode('utf-8')] = data
    return json.dumps(result)

@app.route('/put-rows', methods=['POST'])
def row_list():
    # post ??? ?????? ?????? ????????? python dict ????????? data ??? ??????
    data = request.get_json()
#     print(data)
    
    tasks = [
        Consumer(kafkaHost, hbaseHost),
        Producer(kafkaHost, data)
    ]
    print('before start')
    tasks[0].daemon = True
    tasks[0].start()
    
    time.sleep(1)
    
    tasks[1].daemon = True
    tasks[1].start()

    print('after start')    
    time.sleep(3)
    print('after sleep')    
    for task in tasks:
        task.stop()
    print('after stop')    
    
    return topicName

# if __name__ == '__main__':

#     listen_port = '2000'

#     ipaddr=subprocess.getoutput("hostname -I").split()[0]
#     print ("Starting the service with ip_addr="+ipaddr)
#     app.run(debug=True,host=ipaddr,port=int(listen_port),threaded=True)

if __name__ == '__main__':
    # hbase ??????
    listen_port = '2000'
    app.run(debug=True, port=int(listen_port), host='0.0.0.0')
    
    #command ex) python app.py test-hbase-master
