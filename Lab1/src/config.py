import os


def try_parse(type, value: str):
    try:
        return type(value)
    except Exception:
        return None


# MQTT config
MQTT_BROKER_HOST = os.environ.get('MQTT_BROKER_HOST') or 'mqtt'
MQTT_BROKER_PORT = try_parse(int, os.environ.get('MQTT_BROKER_PORT')) or 1883
MQTT_TOPIC = os.environ.get('MQTT_TOPIC') or 'agent'
# Delay for sending data to mqtt in seconds
DELAY = try_parse(float, os.environ.get('DELAY')) or 1
AGENT_ID = try_parse(float, os.environ.get('AGENT_ID')) or 47

if __name__ == '__main__':
    print("MQTT_BROKER_HOST:", MQTT_BROKER_HOST)
    print("MQTT_BROKER_PORT:", MQTT_BROKER_PORT)
    print("MQTT_TOPIC:", MQTT_TOPIC)
    print("DELAY:", DELAY)