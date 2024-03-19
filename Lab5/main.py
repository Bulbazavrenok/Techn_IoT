import time

from kivy.app import App
from kivy_garden.mapview import MapMarker, MapView
from kivy.clock import Clock
from lineMapLayer import LineMapLayer

import pandas as pd


class MapViewApp(App):
    def __init__(self, **kwargs):
        super().__init__()

        self.mapview: MapView
        self.loop_thread = None
        self.i = 0

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
        self.df = pd.read_csv('sample_gps.csv')

        layer = LineMapLayer()  # some # of layers
        self.l = layer

        self.mapview.add_layer(self.l, mode='scatter')

        self.loop_thread = Clock.schedule_interval(self.update, timeout=3)
        # self.loop_thread = Clock.schedule_interval(self.update, timeout=1)

    def update(self, *args):
        """
        Викликається регулярно для оновлення мапи
        """

        self.l.add_point((self.df.iloc[self.i]['lat'], self.df.iloc[self.i]['lon']))
        self.i += 1

        if self.i >= len(self.df):
            Clock.unschedule(self.loop_thread)

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
