import time

import pandas as pd

from typing import Callable

from threading import Thread


class LiveCsvEmulator(Thread):
    def __init__(self, agent_id: int):
        super().__init__()
        self.agent_id = agent_id
        self.df = pd.read_csv(f'gps_{agent_id}.csv')

    def set_action(self, action: Callable):
        self.action = action

    def run(self):
        agent_id = self.agent_id
        df = self.df

        data_dict = {
            "road_state": "string",
            "agent_data": {
                "agent_id": agent_id,
                "accelerometer": {
                    "x": 0,
                    "y": 0,
                    "z": 0
                },
                "gps": {
                    "latitude": 0,
                    "longitude": 0
                },
                "timestamp": "2024-03-20T16:35:25.819Z"
            }
        }

        for i in range(len(df)):
            data_dict['agent_data']['gps']['latitude'] = df.iloc[i]['lat']
            data_dict['agent_data']['gps']['longitude'] = df.iloc[i]['lon']
            self.action(data_dict)

            time.sleep(1)
