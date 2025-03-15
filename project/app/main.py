from fastapi import FastAPI, status
import pika

from app.models.pydantic import SendSmsPayloadSchema

app = FastAPI()

# Define connection parameters once
params = pika.ConnectionParameters(
    host='localhost',
    heartbeat=600,
    blocked_connection_timeout=300
)

@app.post("/v1/sms", status_code=status.HTTP_200_OK)
def send_sms(payload: SendSmsPayloadSchema):
    # initialize body
    body = None

    # Create a new connection for each request
    connection = pika.BlockingConnection(params)
    channel = connection.channel()

    # creating a queue
    channel.queue_declare(queue='hello')

    # prepare body
    body = payload.model_dump_json()
    
    # send to queue
    channel.basic_publish(exchange='', routing_key='hello', body=body)
    print(f" [x] Sent {body}")

    # close connection
    connection.close()

    return {"status": "ok", "message": "successfully queued sms"}
