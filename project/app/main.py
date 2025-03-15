from fastapi import FastAPI, status
import pika

app = FastAPI()

# Define connection parameters once
params = pika.ConnectionParameters(
    host='localhost',
    heartbeat=600,
    blocked_connection_timeout=300
)

@app.post("/v1/sms", status_code=status.HTTP_200_OK)
def send_sms():
    # Create a new connection for each request
    connection = pika.BlockingConnection(params)
    channel = connection.channel()

    # creating a queue
    channel.queue_declare(queue='hello')

    # send to queue
    channel.basic_publish(exchange='', routing_key='hello', body='Hello World!')
    print(" [x] Sent 'Hello World!'")

    # close connection
    connection.close()

    return {"status": "ok", "message": "successfully queued sms"}
