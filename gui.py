from tkinter import *

from PIL import ImageTk, Image

BACKGROUND1 = "#5d3891"
BACKGROUND3 = "#E0AA3E"
BACKGROUND2 = "lightgrey"
BUTTON = "midnightblue"


IMAGE_HIEGHT = 400
IMAGE_WIDTH = 400

MESSAGE = [
    "You Have To Enter Only Integers.",
    "You Have To Enter Numbers For All Input Fields.",
    "You Have To Enter Only Integers Between {} and {} in {}",
]


class Gui:
    root = Tk()

    def root_config(self):
        self.root.title("Restaurant Recommendation")

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        print(screen_height, screen_width)
        # x, y = 1366, 768
        self.root.geometry('%dx%d+%d+%d' % (screen_width / 2, screen_height * .6, screen_width / 4, screen_height / 4))
        self.root.config(bg=BACKGROUND1)

    def __init__(self):
        self.root_config()

        self.output_value = StringVar()
        # self.output_value()

        self.input_frame = Frame(self.root, bg=BACKGROUND1)
        self.input_frame.pack(side='left', padx=5, pady=5, fill='y')

        self.cuisine = self.create_entries('Cuisine')
        self.price = self.create_entries('Price',"K SP")
        self.location = self.create_entries('Location',"KM")
        self.button = self.create_button()

        self.output_frame = Frame(self.root, bg=BACKGROUND1)
        self.output_frame.pack(side='left', padx=5, pady=5, fill='y')

        self.output_image = Canvas(self.output_frame, height=IMAGE_HIEGHT, width=IMAGE_WIDTH)
        self.output_image.pack(padx=5, pady=5)

        self.output_label = Label(self.output_frame, textvariable=self.output_value, width=10, height=10) \
            .pack(pady=5)

        # todo: get these values from fuzzy class
        self.cuisine_range = (1, 10)
        self.location_range = (1, 40)
        self.price_range = (10, 150)

    def create_entries(self, text,text2=""):
        frame = Frame(self.input_frame)  # bg=BACKGROUND3
        frame.pack(padx=5, pady=5)

        font1 = "Times 15 roman normal"
        font2 = "Times 12 roman normal"
        Label(frame, text=text, font=font1, width=6) \
            .pack(side='left', padx=5, pady=5)

        entry = Entry(frame, font=font1, width=5)
        entry.pack(side='left', padx=5, pady=5)

        Label(frame, text=text2, font=font2, width=3) \
            .pack(side='left', padx=5, pady=5)
        return entry

    def create_button(self):
        frame = Frame(self.input_frame, bg=BACKGROUND1)  #
        frame.pack(padx=10, pady=10)
        font1 = "Times 15 roman normal"
        return Button(frame, text="get recommendation", font=font1, width=15, bg=BACKGROUND3, command=self.get_inputs) \
            .pack(side='left', padx=10, pady=0)

    def set_image(self, image):
        self.output_image.delete("image")
        image = Image.open(image).resize((IMAGE_WIDTH, IMAGE_HIEGHT))
        img = ImageTk.PhotoImage(image)
        self.output_image.create_image(0, 0, image=img, anchor='nw', tag="image")
        self.output_image.image = img

    def get_inputs(self):
        cuisine = self.cuisine.get()
        price = self.price.get()
        location = self.location.get()

        if cuisine == "" or price == "" or location == "":
            self.message_error(MESSAGE[1])
        elif self.is_not_decimal(cuisine) or self.is_not_decimal(location) or self.is_not_decimal(price):
            self.message_error(MESSAGE[0])
        else:
            error_message = ""
            c = int(cuisine)
            p = int(price)
            l = int(location)

            error_message += self.check_valid(c, self.cuisine_range, 'Cuisine')
            error_message += self.check_valid(p, self.price_range, "Price")
            error_message += self.check_valid(l, self.location_range, "Location")

            if error_message != "":
                self.message_error(error_message)
                self.output_value.set("")
                self.output_image.delete("image")
            else:
                # todo: call fuzzy output function
                self.output_value.set(6)
                image = "ondemand_video.png"
                self.set_image(image)

    def check_valid(self, value, range, name):
        return MESSAGE[2].format(range[0], range[1], name) if value < range[0] or value > range[1] else ""

    def is_not_decimal(self, value):
        return not value.isdecimal()

    def message_error(self, text):
        warn_label = Label(self.input_frame, font=("Purisa", 10),
                           width=25, bg=BACKGROUND1, fg='white',
                           wraplength=200, text=text)
        warn_label.pack()
        self.input_frame.after(5000, lambda: warn_label.destroy())
        self.clear_entries()

    def clear_entries(self):
        self.cuisine.delete(0, 'end')
        self.price.delete(0, 'end')
        self.location.delete(0, 'end')


def main():
    Gui().root.mainloop()
    # print("quit")
    # root.quit()


if __name__ == '__main__':
    main()
