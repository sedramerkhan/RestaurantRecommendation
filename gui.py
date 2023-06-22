from tkinter import *
from tkinter.ttk import Combobox

from PIL import ImageTk, Image

from gmap import GMap
from gui_config import *


class Gui:
    root = Tk()

    def root_config(self):
        self.root.title("Restaurant Recommendation")

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        print(screen_height, screen_width)
        # x, y = 1366, 768
        self.root.geometry('%dx%d+%d+%d' % (screen_width, screen_height, 0, 0))
        self.root.config(bg=PURPLE)

        return screen_width, screen_height

    def __init__(self, restaurant_recommendation, cuisines, restaurants, images_paths):
        self.width, self.height = self.root_config()

        self.image_height = int(self.height / 3)
        self.image_width = int(self.width / 3)

        self.image_height_small = int(self.height / 4)
        self.image_width_small = int(self.width / 4.5)

        self.output_value = StringVar()
        # self.output_value()

        self.images_frame = Frame(self.root, bg=PURPLE)
        self.images_frame.pack(fill='x', padx=10)
        self.labels_frame = Frame(self.root, bg=PURPLE)
        self.labels_frame.pack(fill='x', padx=10)

        self.restaurant_recommendation = restaurant_recommendation
        self.cuisines = cuisines
        self.restaurants = restaurants
        self.images_paths = images_paths

        self.cuisine_range = self.restaurant_recommendation.cuisine_range
        self.location_range = self.restaurant_recommendation.location_range
        self.price_range = self.restaurant_recommendation.price_range
        self.set_images()
        self.set_labels()

        self.input_frame = Frame(self.root, bg=PURPLE)

        self.cuisine_list = self.create_option_menu('Cuisine', list(self.cuisines.keys()))
        self.cuisine = self.create_entries('Cuisine Value')
        self.price = self.create_entries('Price', "K SP")
        self.location = self.create_entries('Location', "KM")
        self.button = self.create_button()

        def onSelect(evt):
            w = evt.widget
            selections = w.curselection()
            varname = self.cuisine.cget("textvariable")
            print("hello world")
            if selections:
                values = list(map(lambda x: self.cuisines[w.get(x)], selections))
                avg = sum(values) / len(selections)
                self.cuisine.setvar(varname, round(avg, 3))
                print("the value is:", w.curselection(), values, avg)
            else:
                self.cuisine.setvar(varname, "")

        self.cuisine_list.bind("<<ListboxSelect>>", onSelect)

        self.output_frame = Frame(self.root, bg=PURPLE)
        self.output_image = Canvas(
            self.output_frame, height=self.image_height, width=self.image_width)
        self.output_label = Label(self.output_frame, font=FONTBIG, textvariable=self.output_value, width=28) \
            .pack(pady=5)

        self.map = GMap(self, cuisines, restaurants, self.height, self.width)

        self.map.get_widget().pack(side='left', padx=5, pady=5, expand=1)
        self.input_frame.pack(side='left', padx=5, pady=5, expand=1)
        self.output_frame.pack(padx=10, pady=5, expand=1)
        self.output_image.pack(padx=5, pady=5)

    def set_images(self):
        for _, image_path in list(self.images_paths.items())[:-1]:
            image_canvas = Canvas(
                self.images_frame, height=self.image_height_small, width=self.image_width_small)
            image_canvas.pack(side='left', padx=15, pady=5)
            image_path = Image.open(image_path).resize(
                (self.image_width_small, self.image_height_small))
            img = ImageTk.PhotoImage(image_path)
            image_canvas.create_image(0, 0, image=img, anchor='nw', tag="image")
            image_canvas.image = img

    def set_labels(self):
        for key, _ in list(self.images_paths.items())[:-1]:
            font = "Times 10 roman normal"
            Label(self.labels_frame, text=key, font=font, width=int(self.image_width_small / 6), bg=PURPLE,
                  fg='white') \
                .pack(side='left', pady=10)

    def create_entries(self, text, text2=""):
        frame = Frame(self.input_frame)  # bg=BACKGROUND3
        frame.pack(padx=5, pady=5)

        Label(frame, text=text, font=FONTBIG, width=10) \
            .pack(side='left', padx=5, pady=5)

        var = StringVar()
        entry = Entry(frame, font=FONTBIG, width=10, textvariable=var)
        entry.pack(side='left', padx=5, pady=5)

        Label(frame, text=text2, font=FONTSMALL, width=3) \
            .pack(side='left', padx=5, pady=5)
        return entry

    def create_option_menu(self, text, data):

        frame = Frame(self.input_frame)  # bg=BACKGROUND3
        frame.pack(padx=5, pady=5)
        Label(frame, text=text, font=FONTBIG, width=10) \
            .pack(side='left', padx=5, pady=5)

        scrollbar = Scrollbar(frame)
        scrollbar.pack(side=RIGHT, fill=Y)

        cuisines_list = Listbox(frame, selectmode="multiple", yscrollcommand=scrollbar.set,exportselection=False)
        cuisines_list.pack(padx=10, pady=10, expand=YES, fill="both")

        for each_item in range(len(data)):
            cuisines_list.insert(END, data[each_item])
            cuisines_list.itemconfig(each_item, bg="#DDDDDD" if each_item %
                                     2 == 0 else "#CDCDCD")
        scrollbar.config(command=cuisines_list.yview)

        return cuisines_list

    def create_button(self):
        frame = Frame(self.input_frame, bg=PURPLE)  #
        frame.pack(padx=10, pady=10)
        return Button(frame, text="get recommendation", font=FONTBIG, width=15, bg=GOLD, command=self.get_inputs) \
            .pack(side='left', padx=10, pady=0)

    def set_image(self, image):
        self.output_image.delete("image")
        image = Image.open(image).resize((self.image_width, self.image_height))
        img = ImageTk.PhotoImage(image)
        self.output_image.create_image(0, 0, image=img, anchor='nw', tag="image")
        self.output_image.image = img

    def get_inputs(self):
        cuisine_value = self.cuisine.get()
        price = self.price.get()
        location = self.location.get()
        print(f"{cuisine_value=},{price=},{location=}")
        def is_not_num(value):
            return not value.replace('.', '', 1).isdigit()

        if price == "" or location == "" or cuisine_value == "":
            self.message_error(MESSAGE[1])
        elif is_not_num(location) or is_not_num(price) or is_not_num(cuisine_value):
            self.message_error(MESSAGE[0])

        else:
            error_message = ""
            c = float(cuisine_value)
            p = float(price)
            l = float(location)

            def check_valid(value, range, name):
                return MESSAGE[2].format(range[0], range[1], name) + "\n" \
                    if value < range[0] or value > range[1] else ""

            error_message += check_valid(p, self.price_range, "Price")
            error_message += check_valid(l, self.location_range, "Location")
            error_message += check_valid(c, self.cuisine_range, "Cuisine Value")

            if error_message != "":
                self.message_error(error_message)
                self.output_value.set("")
                self.output_image.delete("image")
            else:
                print(f"cuisine: {c}, price: {p} location: {l}")
                output = round(self.restaurant_recommendation.set_inputs(c, p, l), 3)
                self.output_value.set(f"the recommendation degree: {output}")
                image = self.images_paths['recommendation output']
                self.set_image(image)

    def message_error(self, text):
        warn_label = Label(self.input_frame, font=("Purisa", 10),
                           width=25, bg=PURPLE, fg='white',
                           wraplength=200, text=text)
        warn_label.pack()
        self.input_frame.after(5000, lambda: warn_label.destroy())
        # self.clear_entries()

    def clear_entries(self):
        self.price.delete(0, 'end')
        self.location.delete(0, 'end')
