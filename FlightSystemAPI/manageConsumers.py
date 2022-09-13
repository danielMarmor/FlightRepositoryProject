import json
from FlightSystemAPI.invokeRequests import InvokeRequests
from business.services.genericService import GenericService
from business.services.loggingService import FlightsLogger
from common.not_mapped.DecimalEncoder import DecimalEncoder
import pika
import logging
import threading
import functools


class ManageConsumners:
    READONLY_QUEUE_NAME = 'READONLY'
    WRITE_QUEUE_NAME = 'WRITE'
    RENPONSE_QUEUE_NAME = 'RESPONSE'

    def __init__(self, db_session):
        parameters = pika.ConnectionParameters(host='localhost', port=5672)
        self.connection = pika.BlockingConnection(parameters);
        self.channel = self.connection.channel()
        self.invoke_requests = InvokeRequests(db_session)
        self.logger = FlightsLogger.get_instance().Logger

    def init_consumers(self):
        # THREAD 1
        consumers_thread = threading.Thread(target=self.start_consumers)
        consumers_thread.start()
        # # THREAD 2
        # consumer_write = threading.Thread(target=self.start_write_consumer)
        # consumer_write.start()
        # MAIN THREAD
        # self.init_response_publisher()

    def start_consumers(self):
        try:
            self.channel.queue_delete(self.READONLY_QUEUE_NAME)
            self.channel.queue_delete(self.WRITE_QUEUE_NAME)
            self.channel.queue_delete(self.RENPONSE_QUEUE_NAME)
            self.channel.queue_declare(queue=self.READONLY_QUEUE_NAME, durable=False)
            self.channel.queue_declare(queue=self.WRITE_QUEUE_NAME, durable=False)
            self.channel.queue_declare(queue=self.RENPONSE_QUEUE_NAME, durable=False)
            self.channel.basic_consume(queue=self.READONLY_QUEUE_NAME, on_message_callback=self.read_callback, auto_ack=True)
            self.channel.basic_consume(queue=self.WRITE_QUEUE_NAME, on_message_callback=self.write_callback, auto_ack=True)

            print(' [*] Waiting for messages. To exit press CTRL+C')
            self.channel.start_consuming()
            self.connection.close();
        except KeyboardInterrupt:
            self.connection.close()

    # CALLBACK READ
    def read_callback(self, ch, method, properties, body):
        message = json.loads(body)
        # message = json.loads(body)
        # self.read_invoke(message)
        invoke_thread = threading.Thread(target=self.read_invoke, args=[message])
        invoke_thread.start()

    def read_invoke(self, message):
        try:
            msg_json = json.loads(message);
            correlation_id = msg_json['correlation_id']
            facade_name = msg_json['payload']['facade_name']
            action_id = msg_json['payload']['action_id']
            data = msg_json['payload']['data']
            response = None
            system_exeption = None
            try:
                response = self.invoke_requests.invoke(facade_name, action_id, data)
                system_exeption = None
            # exception during  the invoke itself -
            # will catogorized as valid reponse (200) with action message to the user
            except Exception as exc:
                response = None
                system_exeption = exc
            serialize_response = GenericService.get_serialized_response(response)
            serialized_exception = None if system_exeption is None else str(system_exeption)
            response_body = {'correlation_id': correlation_id,
                             'payload': serialize_response,
                             'exception': serialized_exception
                            }
            self.async_response(self.publish_response, response_body=response_body)
            # CALLBACK WRITE
        # exception during consuming process  -will categorized as server internal errors 501
        except Exception as exc:
            self.handle_unspecified_exc(exc, correlation_id)

    def write_callback(self, ch, method, properties, body):
        message = json.loads(body)
        self.write_invoke(message)

    def write_invoke(self, message):
        try:
            msg_json = json.loads(message);
            correlation_id = msg_json['correlation_id']
            facade_name = msg_json['payload']['facade_name']
            action_id = msg_json['payload']['action_id']
            data = msg_json['payload']['data']
            response = None
            system_exeption = None
            try:
                response = self.invoke_requests.invoke(facade_name, action_id, data)
                system_exeption = None
            # exception during  the invoke itself -
            # will catogorized as valid reponse (200) with action message to the user
            except Exception as exc:
                response = None
                system_exeption = exc
            serialize_response = GenericService.get_serialized_response(response)
            serialized_exception = None if system_exeption is None else str(system_exeption)
            response_body = {'correlation_id': correlation_id,
                            'payload': serialize_response,
                            'exception': serialized_exception
                            }
            self.async_response(self.publish_response, response_body=response_body)
        # exception during consuming process  -will categorized as server internal errors 501
        except Exception as exc:
            self.handle_unspecified_exc(exc, correlation_id)

    def async_response(self, callback, *args, **kwargs):
        if self.connection.is_open:
            self.connection.add_callback_threadsafe(functools.partial(callback, *args, **kwargs))

    def publish_response(self, response_body):
        try:
            message = json.dumps(response_body, default=GenericService.json_serial, cls=DecimalEncoder)
            self.channel.basic_publish(exchange='',
                                       routing_key=self.RENPONSE_QUEUE_NAME,
                                       body=message)
        # exception during serializing - will categorized as server internal error 501
        except Exception as exc:
            correlation_id = response_body['correlation_id']
            self.handle_unspecified_exc(exc, correlation_id)

    def handle_unspecified_exc(self, exc, correlation_id):
        self.logger.log(logging.ERROR, f'publish_response: {str(exc)}')
        internal_error = {'correlation_id': correlation_id,
                          'payload': None,
                          'exception': None,
                          'server_internal_error': 1
                          }
        error_message = json.dumps(internal_error)
        self.channel.basic_publish(exchange='',
                                   routing_key=self.RENPONSE_QUEUE_NAME,
                                   body=error_message)



