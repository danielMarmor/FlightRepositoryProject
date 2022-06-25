import json
import threading
import pika
import functools


class HandleRequests:
    READONLY_QUEUE_NAME = 'READONLY'
    WRITE_QUEUE_NAME = 'WRITE'
    RESPONSE_QUEUE_NAME = 'RESPONSE'

    def __init__(self, pool_events):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()
        self.pool_events = pool_events
        self.counter_correlation_id = 0
        # self.counter_responses = 0
        self.lock_correl_id = threading.Lock()

    def init_channels(self):
        # PUBLISH
        # CONSUME
        consumer_thread = threading.Thread(target=self.start_response_consumer)
        consumer_thread.start()

    def start_response_consumer(self):
        self.channel.queue_delete(self.RESPONSE_QUEUE_NAME)
        self.channel.queue_declare(queue=self.RESPONSE_QUEUE_NAME)
        self.channel.queue_declare(queue=self.READONLY_QUEUE_NAME)
        self.channel.queue_declare(queue=self.WRITE_QUEUE_NAME)
        self.channel.basic_consume(queue=self.RESPONSE_QUEUE_NAME, on_message_callback=self.response_callback,
                                   auto_ack=True)
        print(' [*] Waiting for messages. To exit press CTRL+C')
        self.channel.start_consuming()
        self.channel.queue_delete(self.RESPONSE_QUEUE_NAME)
        self.connection.close()

    def send_request(self, payload, is_write):
        publish_queue_name = None
        if is_write:
            publish_queue_name = self.WRITE_QUEUE_NAME
        else:
            publish_queue_name = self.READONLY_QUEUE_NAME
        # INCREMENT CORRELATION ID
        correlation_id = 0
        with self.lock_correl_id:
            self.counter_correlation_id += 1
            correlation_id = self.counter_correlation_id
        request_body = {'correlation_id': correlation_id, 'payload': payload}
        req_serialized = json.dumps(request_body)
        self.async_request(self.publish_request, publish_queue_name=publish_queue_name, req_serialized=req_serialized)
        return correlation_id

    def async_request(self, callback, *args, **kwargs):
        if self.connection.is_open:
            self.connection.add_callback_threadsafe(functools.partial(callback, *args, **kwargs))

    def publish_request(self, publish_queue_name, req_serialized):
        self.channel.basic_publish(exchange='',
                                   routing_key=publish_queue_name,
                                   body=req_serialized)

    def get_response(self, correlation_id):
        correlation_obj = {'event': threading.Event(),
                           'response': None,
                           'exception': None
                           }
        response_signal = self.pool_events.add(correlation_obj, correlation_id)
        if response_signal:
            if correlation_obj['exception'] is not None:
                exe = correlation_obj['exception']
                raise Exception(exe)
            response = correlation_obj['response']
            # self.counter_responses += 1
            self.pool_events.remove(correlation_id)
            return response
        return None

    def response_callback(self, ch, method, properties, body):
        message = json.loads(body)
        correlation_id = message['correlation_id']
        response = message['payload']
        exception = message['exception']
        self.pool_events.signal(correlation_id, response, exception)
