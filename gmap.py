import tkinter
import tkintermapview
import pandas as pd
from data import CUISINE


class GMap():
    def __init__(self, master_gui, my_position=(33.4928347, 36.315426)):
        self.master_gui = master_gui
        self.my_position = my_position

        self.map_widget = tkintermapview.TkinterMapView(
            master_gui.root, width=800, height=600, corner_radius=0,
            use_database_only=True, database_path="damascus.db"
        )

        self.map_widget.pack(fill='both', expand=True)
        self.map_widget.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

        self.map_widget.set_position(*my_position)
        self.map_widget.set_zoom(14)
        self.add_marker(my_position, 'my location')

        self.restaurants = self.load_restaurants('csv_files/restaurants.csv')
        for restaurant in self.restaurants:
            self.add_marker((restaurant['lat'], restaurant['lon']), restaurant['name'])

        self.define_commands()

    def define_commands(self):
        def left_click_event(coordinates):
            print("coordinates:", coordinates)

            min_res = min(
                self.restaurants,
                key=lambda r: self.cal_distance(
                    coordinates, (r['lat'], r['lon'])
                )
            )

            if self.cal_distance(coordinates, (min_res['lat'], min_res['lon'])) > 0.3:
                return

            distance = self.cal_distance(self.my_position, (min_res['lat'], min_res['lon']))

            self.set_gui_field_val('location', round(distance, 1))
            self.set_gui_field_val('price', min_res['price'])
            self.set_gui_field_val('cuisine', min_res['cuisine'])
            self.set_gui_field_val('cuisine_value', CUISINE[min_res['cuisine']])

        self.map_widget.add_left_click_map_command(left_click_event)

    def set_gui_field_val(self, field, value):
        gui_field = self.master_gui.__dict__[field]
        varname = gui_field.cget("textvariable")
        gui_field.setvar(varname, value)

    def add_marker(self, position, text):
        self.map_widget.set_marker(*position, text=text)

    def cal_distance(self, c1, c2):
        from math import acos, sin, cos, radians
        lat1, lon1 = radians(c1[0]), radians(c1[1])
        lat2, lon2 = radians(c2[0]), radians(c2[1])

        return acos(sin(lat1)*sin(lat2)+cos(lat1)*cos(lat2)*cos(lon2-lon1))*6371

    def load_restaurants(self, path):
        df = pd.read_csv(path)
        return df.to_dict(orient='records')

    def get_widget(self):
        return self.map_widget


# def add_marker_event(coords):
#     self.map_widget.set_marker(coords[0], coords[1], text='')

# self.map_widget.add_right_click_menu_command(label="Add Marker",
#                                                  command=add_marker_event,
#                                                  pass_coords=True)

# map_widget.delete_all_marker()
