from kivy.app import App
from kivy_garden.mapview import MapMarker, MapView
from kivy.clock import Clock
from lineMapLayer import LineMapLayer

from WebSocketHandler import WebSocketHandler
from LiveCsvEmulator import LiveCsvEmulator

from misc import line_colors

from random import choices


class MapViewApp(App):
    def __init__(self, **kwargs):
        super().__init__()

        self.mapview: MapView
        self.loop_thread = None
        self.i = 0

        self.layers = {}
        self.markers = {}
        self.positions = {}
        self.potholes = []

        self.tracked_agent_ids = [
            0,
            5,
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

        for i, agent_id in enumerate(self.tracked_agent_ids):
            layer = LineMapLayer(color=line_colors[i])
            self.layers[agent_id] = layer

            self.mapview.add_layer(layer, mode='scatter')

            if agent_id == 0 or agent_id == 5:
                LiveCsvEmulator(agent_id=agent_id,
                                on_message=lambda data_dict,
                                                  agent_id=agent_id: self.update_layer_with_data(agent_id,
                                                                                                 data_dict)).start()



            # # TODO uncomment the following block to enable websocket
            # WebSocketHandler(agent_id,
            #                  on_message=lambda data_dict,
            #                                    agent_id=agent_id: self.update_layer_with_data(agent_id,
            #                                                                                   data_dict)).start()

            m = self.add_marker((50.45040418715659, 30.524494274265045), source='images/car.png')
            self.markers[agent_id] = m

            self.positions[agent_id] = (50.45040418715659, 30.524494274265045)

            Clock.schedule_interval(self.update, 0.2)

        print('App started')

    def update_layer_with_data(self, agent_id, data_dict):
        point = (data_dict['agent_data']['gps']['latitude'], data_dict['agent_data']['gps']['longitude'])

        self.layers[agent_id].add_point(point)
        self.positions[agent_id] = point

        if choices([True, False], weights=[3, 97], k=1)[0]:
            self.potholes.append(point)

    def update(self, *args):
        for layer in self.layers.values():
            layer.update_layer()

        for agent_id in self.tracked_agent_ids:
            self.markers[agent_id] = self.update_marker(self.markers[agent_id], self.positions[agent_id])

        for pothole in self.potholes:
            self.set_pothole_marker(pothole)

    def add_marker(self, point: tuple[float, float], **kwargs) -> MapMarker:
        lat = float(point[0])
        lon = float(point[1])

        if 'source' in kwargs:
            marker = MapMarker(lat=lat, lon=lon, source=kwargs['source'])
        else:
            marker = MapMarker(lat=lat, lon=lon)
        self.mapview.add_marker(marker)
        return marker

    def update_marker(self, marker: MapMarker, point: tuple[float, float]) -> MapMarker:
        self.mapview.remove_marker(marker)
        return self.add_marker(point, source=marker.source)

    def set_pothole_marker(self, point):
        return self.add_marker(point, source='images/pothole.png')


if __name__ == "__main__":
    MapViewApp().run()
