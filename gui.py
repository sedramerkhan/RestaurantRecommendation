from tkinter import *

from PIL import ImageTk, Image

from data import *
from restaurantRecommendation import RestaurantRecommendation
from utils import *


class Gui:
    root = Tk()

    def root_config(self):
        self.root.title("Restaurant Recommendation")

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        print(screen_height, screen_width)
        # x, y = 1366, 768
        self.root.geometry('%dx%d+%d+%d' % (screen_width, screen_height, 0, 0))
        self.root.config(bg=BACKGROUND1)

        return screen_width, screen_height

    def __init__(self):
        self.width, self.height = self.root_config()

        self.image_height = int(self.height / 3)
        self.image_width = int(self.width / 3)

        self.image_height_small = int(self.height / 4)
        self.image_width_small = int(self.width / 4.5)

        self.output_value = StringVar()
        # self.output_value()

        self.images_frame = Frame(self.root, bg=BACKGROUND1)
        self.images_frame.pack(fill='x', padx=10)
        self.labels_frame = Frame(self.root, bg=BACKGROUND1)
        self.labels_frame.pack(fill='x', padx=10)

        self.restaurant_recommendation = RestaurantRecommendation()

        self.cuisine_range = self.restaurant_recommendation.cuisine_range
        self.location_range = self.restaurant_recommendation.location_range
        self.price_range = self.restaurant_recommendation.price_range
        self.set_images()
        self.set_labels()

        self.input_frame = Frame(self.root, bg=BACKGROUND1)
        self.input_frame.pack(side='left', padx=5, pady=5, expand=1)  # fill='y',

        self.cuisine, self.selected_cuisine = self.create_option_menu('Cuisine', CUISINE.keys())

        self.price = self.create_entries('Price', "K SP")
        self.location = self.create_entries('Location', "KM")
        self.button = self.create_button()

        self.output_frame = Frame(self.root, bg=BACKGROUND1)
        self.output_frame.pack(side='left', padx=5, pady=5, expand=1)

        self.output_image = Canvas(self.output_frame, height=self.image_height, width=self.image_width)
        self.output_image.pack(padx=5, pady=5)

        self.output_label = Label(self.output_frame, font=FONTBIG, textvariable=self.output_value, width=28) \
            .pack(pady=5)

    def set_images(self):
        for _, image in images[:-1]:
            image_canvas = Canvas(
                self.images_frame, height=self.image_height_small, width=self.image_width_small)
            image_canvas.pack(side='left', padx=15, pady=5)
            image = Image.open(image).resize((self.image_width_small, self.image_height_small))
            img = ImageTk.PhotoImage(image)
            image_canvas.create_image(0, 0, image=img, anchor='nw', tag="image")
            image_canvas.image = img

    def set_labels(self):
        for label, _ in images[:-1]:
            font = "Times 10 roman normal"
            Label(self.labels_frame, text=label, font=font, width=int(self.image_width_small / 6), bg=BACKGROUND1,
                  fg='white') \
                .pack(side='left', pady=10)

    def create_entries(self, text, text2=""):
        frame = Frame(self.input_frame)  # bg=BACKGROUND3
        frame.pack(padx=5, pady=5)

        Label(frame, text=text, font=FONTBIG, width=6) \
            .pack(side='left', padx=5, pady=5)

        entry = Entry(frame, font=FONTBIG, width=10)
        entry.pack(side='left', padx=5, pady=5)

        Label(frame, text=text2, font=FONTSMALL, width=3) \
            .pack(side='left', padx=5, pady=5)
        return entry

    def create_option_menu(self, text, data):
        frame = Frame(self.input_frame)  # bg=BACKGROUND3
        frame.pack(padx=5, pady=5)
        Label(frame, text=text, font=FONTBIG, width=6) \
            .pack(side='left', padx=5, pady=5)

        selected = StringVar()
        selected.set("select")

        menu = OptionMenu(frame, selected, *data)
        menu.config(width=18)
        menu.pack(side='left', padx=5, pady=5)
        return menu, selected

    def create_button(self):
        frame = Frame(self.input_frame, bg=BACKGROUND1)  #
        frame.pack(padx=10, pady=10)
        return Button(frame, text="get recommendation", font=FONTBIG, width=15, bg=BACKGROUND3, command=self.get_inputs) \
            .pack(side='left', padx=10, pady=0)

    def set_image(self, image):
        self.output_image.delete("image")
        image = Image.open(image).resize((self.image_width, self.image_height))
        img = ImageTk.PhotoImage(image)
        self.output_image.create_image(0, 0, image=img, anchor='nw', tag="image")
        self.output_image.image = img

    def get_inputs(self):
        cuisine = self.selected_cuisine.get()
        price = self.price.get()
        location = self.location.get()

        is_num = lambda value: not value.replace('.', '', 1).isdigit()

        if price == "" or location == "":
            self.message_error(MESSAGE[1])
        elif is_num(location) or is_num(price):
            self.message_error(MESSAGE[0])
        elif cuisine == 'select':
            self.message_error(MESSAGE[3])
        else:
            error_message = ""
            c = CUISINE[cuisine]
            p = float(price)
            l = float(location)

            check_valid = lambda value, range, name: MESSAGE[2].format(range[0], range[1], name)+"\n" \
                if value < range[0] or value > range[1] else ""

            error_message += check_valid(p, self.price_range, "Price")
            error_message += check_valid(l, self.location_range, "Location")

            if error_message != "":
                self.message_error(error_message)
                self.output_value.set("")
                self.output_image.delete("image")
            else:

                output = round(self.restaurant_recommendation.set_inputs(c, p, l), 3)
                self.output_value.set(f"the recommendation degree: {output}")
                image = images[4][1]
                self.set_image(image)

    def message_error(self, text):
        warn_label = Label(self.input_frame, font=("Purisa", 10),
                           width=25, bg=BACKGROUND1, fg='white',
                           wraplength=200, text=text)
        warn_label.pack()
        self.input_frame.after(5000, lambda: warn_label.destroy())
        # self.clear_entries()

    def clear_entries(self):
        self.selected_cuisine.set('select')
        self.price.delete(0, 'end')
        self.location.delete(0, 'end')


def main():
    Gui().root.mainloop()
    # print("quit")
    # root.quit()


if __name__ == '__main__':
    main()
