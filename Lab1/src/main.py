import time

from paho.mqtt import client as mqtt_client

import config
from file_datasource import FileDatasource
from schema.aggregated_data_schema import AggregatedDataSchema


def connect_mqtt(broker: str, port: int) -> mqtt_client.Client:
    """Create MQTT client"""
    print(f"CONNECT TO {broker}:{port}")

    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print(f"Connected to MQTT Broker ({broker}:{port})!")
        else:
            print("Failed to connect {broker}:{port}, return code %d\n", rc)
            exit(rc)

    client = mqtt_client.Client()
    client.on_connect = on_connect
    client.connect(broker, port)
    client.loop_start()
    return client


def publish(client: mqtt_client.Client, topic: str, datasource, delay: float) -> None:
    datasource.startReading()
    print(f"Started publishing to topic `{topic}` with agent_id={config.AGENT_ID}")
    while True:
        list_of_data = datasource.read()
        time.sleep(delay)
        for data in list_of_data:
            msg = AggregatedDataSchema().dumps(data)
            result = client.publish(topic, msg)
            status = result[0]
            if status == 0:
                # print(f"Sent `{msg}` to topic `{topic}`")
                # print(f"Sent data over MQTT to topic `{topic}`")
                pass
            else:
                print(f"Failed to send message to topic {topic}")


def run():
    # Prepare mqtt client
    client = connect_mqtt(config.MQTT_BROKER_HOST, config.MQTT_BROKER_PORT)
    # Prepare datasource
    datasource = FileDatasource("data/accelerometer.csv",
                                "data/gps.csv",
                                "data/parking.csv")
    # Infinitely publish data
    publish(client, config.MQTT_TOPIC, datasource, config.DELAY)


if __name__ == '__main__':
    run()
