from kivy.app import App
from kivy_garden.mapview import MapMarker, MapView
from kivy.clock import Clock
from lineMapLayer import LineMapLayer

from WebSocketHandler import WebSocketHandler
from LiveCsvEmulator import LiveCsvEmulator

from misc import line_colors


class MapViewApp(App):
    def __init__(self, **kwargs):
        super().__init__()

        self.mapview: MapView
        self.loop_thread = None
        self.i = 0

        self.tracked_agent_ids = [
            0,
            # 66
        ]

    def build(self):
        """
        Ініціалізує мапу MapView(zoom, lat, lon)
        :return: MapView of a zoomed map
        """
        self.mapview = MapView(zoom=15, lat=50.45040418715659, lon=30.524494274265045)
        return self.mapview

    def on_start(self):
        """
        Встановлює необхідні маркери, викликає функцію для оновлення мапи
        """

        self.layers = {}
        for i, agent_id in enumerate(self.tracked_agent_ids):
            layer = LineMapLayer(color=line_colors[i])
            self.layers[agent_id] = layer

            self.mapview.add_layer(layer, mode='scatter')

            if agent_id == 0:
                csv_emulator_0 = LiveCsvEmulator(agent_id=agent_id)
                csv_emulator_0.set_action(lambda data_dict: self.update_layer_with_data(csv_emulator_0.agent_id,
                                                                                        data_dict))
                csv_emulator_0.start()

            # TODO uncomment the following block to enable websocket

            ws_handler = WebSocketHandler(agent_id)
            ws_handler.set_on_message(lambda data_dict: self.update_layer_with_data(ws_handler.agent_id, data_dict))
            # ws_handler.set_on_message(lambda data_dict: print(data_dict))
            ws_handler.start()

        Clock.schedule_interval(self.update, 0.2)
        print('App started')

    def update_layer_with_data(self, agent_id, data_dict):
        self.layers[agent_id].add_point((data_dict['agent_data']['gps']['latitude'],
                                         data_dict['agent_data']['gps']['longitude']))

    def update(self, *args):
        for layer in self.layers.values():
            layer.update_layer()

    def check_road_quality(self):
        """
        Аналізує дані акселерометра для подальшого визначення
        та відображення ям та лежачих поліцейських
        """

    def update_car_marker(self, point):
        """
        Оновлює відображення маркера машини на мапі
        :param point: GPS координати
        """

    def set_pothole_marker(self, point):
        """
        Встановлює маркер для ями
        :param point: GPS координати
        """

    def set_bump_marker(self, point):
        """
        Встановлює маркер для лежачого поліцейського
        :param point: GPS координати
        """


if __name__ == "__main__":
    MapViewApp().run()
