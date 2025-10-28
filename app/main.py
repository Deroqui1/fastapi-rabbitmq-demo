from fastapi import FastAPI
import pika
import json
import os

app = FastAPI()

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")

@app.post("/enviar")
def enviar_mensagem(payload: dict):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=RABBITMQ_HOST)
    )
    channel = connection.channel()
    channel.queue_declare(queue='mensagens')

    message = json.dumps(payload)
    channel.basic_publish(exchange='', routing_key='mensagens', body=message)
    connection.close()

    return {"status": "Mensagem enviada com sucesso!", "dados": payload}
