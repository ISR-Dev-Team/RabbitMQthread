#!/usr/bin/env python
import pika
import threading
import sys

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
channel.exchange_declare(exchange='direct_logs', exchange_type='direct')
severities = sys.argv[1:]
print("%s" % severities)

def callback(ch, method, properties, body):
    print(" [x] %r:%r" % (method.routing_key, body))


# Define a function for the thread
def print_time(threadName):
    result = channel.queue_declare(queue='', exclusive=True)
    queue_name = result.method.queue
    for severity in severities:
        channel.queue_bind(exchange='direct_logs', queue=queue_name, routing_key=severity)

    print(" %s: [*] Waiting for logs. To exit press CTRL+C" % (threadName))
    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
    channel.start_consuming()


#print_time("Thread-1")
t1 = threading.Thread(target=print_time, args= ("RThread-1", ))
#t2 = threading.Thread(target=print_time, args= ("RThread-2", ))
# starting thread 1
t1.start()
#t2.start()
print('Start')
