#!/usr/bin/env python
import threading, logging, time
import multiprocessing
import sys

from kafka import KafkaConsumer, KafkaProducer
import happybase


class Producer(threading.Thread):
    def __init__(self, kafkaHost):
        threading.Thread.__init__(self)
        self.stop_event = threading.Event()
        
    def stop(self):
        self.stop_event.set()

    def run(self):
        producer = KafkaProducer(bootstrap_servers= kafkaHost + ':9092')
        print("producer: " + str(producer))

        while not self.stop_event.is_set():
            producer.send('my-topic1', b"<<<<<<<<< my-topic test")
            producer.send('my-topic1', b">>>>>>>>>> test")
            time.sleep(1)

        producer.close()


# class Consumer(multiprocessing.Process):
#     def __init__(self, kafkaHost, hbaseHost):
#         multiprocessing.Process.__init__(self)
#         self.stop_event = multiprocessing.Event()
        
#     def stop(self):
#         self.stop_event.set()
        
#     def run(self):
#         f=open("log","w")
#         consumer = KafkaConsumer('my-topic1',
#                          bootstrap_servers= kafkaHost+':9092')
#         print("consumer: " + consumer)
#         f.write("consumer: " + consumer + "\n")

#         connection = happybase.Connection(host=hbaseHost, port=9090)
#         connection.open()
#         print("connection: " + connection)
#         f.write("connection: " + connection + "\n")

#         table = connection.table('my-topic11')
#         print("table: " + table)
#         f.write("table: " + table + "\n")
        
#         count = 0
#         while not self.stop_event.is_set():
#             for message in consumer:
#                 count += 1
#                 print("message: " + message.value)
#                 f.write("message: " + message.value + "\n")
                
#                 table.put('row-key' + str(count), {'cf:col1': message.value})
#                 if self.stop_event.is_set():
#                     break

#         for key, data in table.scan():
#             print(key, data)
            
#         f.close()
#         consumer.close()

class Consumer(threading.Thread):
    def __init__(self, kafkaHost, hbaseHost):
        threading.Thread.__init__(self)
        self.stop_event = threading.Event()
        
    def stop(self):
        self.stop_event.set()

    def run(self):
        consumer = KafkaConsumer('my-topic1',
                         bootstrap_servers=[ kafkaHost + ':9092'])
        print("consumer: "+ str(consumer))
        
        connection = happybase.Connection(host=hbaseHost, port=9090)
        connection.open()

        table = connection.table('my-topic11')
        
        count = 0
        while not self.stop_event.is_set():
            for message in consumer:
                count += 1
                print ("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition,
                                                  message.offset, message.key,
                                                  message.value))
                table.put('row-key' + str(count), {'cf:col1': message.value})
                if self.stop_event.is_set():
                    break

        for key, data in table.scan():
            print(key, data)
            
        consumer.close()
        
        
def main(kafkaHost, hbaseHost):

    tasks = [
        Producer(kafkaHost),
        Consumer(kafkaHost, hbaseHost)
    ]

    for t in tasks:
        t.daemon = True
        t.start()

    time.sleep(5)
    
    for task in tasks:
        task.stop()

    for task in tasks:
        task.join()
        
        
if __name__ == "__main__":
    logging.basicConfig(
        format='%(asctime)s.%(msecs)s:%(name)s:%(thread)d:%(levelname)s:%(process)d:%(message)s',
        level=logging.INFO
        )
    kafkaHost = sys.argv[1]
    hbaseHost = sys.argv[2]
    main(kafkaHost, hbaseHost)
