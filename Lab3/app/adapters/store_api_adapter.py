import json
import logging
from typing import List
import requests

from app.entities.processed_agent_data import ProcessedAgentData
from app.interfaces.store_gateway import StoreGateway


class StoreApiAdapter(StoreGateway):

    def __init__(self, api_base_url):
        self.api_base_url = api_base_url

    def save_data(self, processed_agent_data_batch: List[ProcessedAgentData]):
        serialized = [item.model_dump_json() for item in processed_agent_data_batch]
        data_dicts = [json.loads(item) for item in serialized]

        try:
            response = requests.post(f"{self.api_base_url}/processed_agent_data/", json=data_dicts)
            response.raise_for_status()
            logging.info("Data sent to Store API successfully")
        except requests.exceptions.RequestException as e:
            logging.error(f"Error response code while making post request to Store API: {e}")
