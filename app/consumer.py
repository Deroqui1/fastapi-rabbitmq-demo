import pika
import json
import os
import time

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "rabbitmq")

def callback(ch, method, properties, body):
    data = json.loads(body)
    print(f"📩 Mensagem recebida: {data}")

def start_consumer():
    while True:
        try:
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(host=RABBITMQ_HOST)
            )
            channel = connection.channel()
            channel.queue_declare(queue='mensagens')
            channel.basic_consume(queue='mensagens', on_message_callback=callback, auto_ack=True)
            print("👂 Aguardando mensagens. Pressione CTRL+C para sair.")
            channel.start_consuming()
        except pika.exceptions.AMQPConnectionError:
            print("❌ RabbitMQ ainda não está pronto, tentando novamente em 5s...")
            time.sleep(5)

if __name__ == "__main__":
    start_consumer()
