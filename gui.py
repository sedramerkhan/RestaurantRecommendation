from tkinter import *

from PIL import ImageTk, Image

BACKGROUND1 = "#5d3891"
BACKGROUND3 = "#E0AA3E"
BACKGROUND2 = "lightgrey"
BUTTON = "midnightblue"
FONT = "Times 15 roman normal"

IMAGE_HIEGHT = 400
IMAGE_WIDTH = 400


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
        self.price = self.create_entries('Price')
        self.location = self.create_entries('Location')
        self.button = self.create_button()

        self.output_frame = Frame(self.root, bg=BACKGROUND1)
        self.output_frame.pack(side='left', padx=5, pady=5, fill='y')
        
        self.output_image = Canvas(self.output_frame, height=IMAGE_HIEGHT, width=IMAGE_WIDTH)
        self.output_image.pack( padx=5, pady=5)

        self.output_label = Label(self.output_frame,textvariable =self.output_value,width=10,height=10)\
        .pack(pady=5)

    def create_entries(self, text):
        frame = Frame(self.input_frame, )  # bg=BACKGROUND3
        frame.pack(padx=5, pady=5)

        Label(frame, text=text, font=FONT, width=10) \
            .pack(side='left', padx=5, pady=5)

        entry = Entry(frame,  font=FONT, width=5) \
            .pack(side='left', padx=5, pady=5)
        return entry

    def create_button(self):
        frame = Frame(self.input_frame, bg=BACKGROUND1)  #
        frame.pack(padx=10, pady=10)
        return Button(frame, text="get recommendation", font=FONT, width=15, bg=BACKGROUND3,command=self.command) \
            .pack(side='left', padx=10, pady=0)

    def set_image(self, image):
        self.output_image.delete("image")
        image = Image.open(image).resize((IMAGE_WIDTH, IMAGE_HIEGHT))
        img = ImageTk.PhotoImage(image)
        self.output_image.create_image(0, 0, image=img, anchor='nw', tag="image")
        self.output_image.image = img

    def command(self):
        self.output_value.set(6)
        self.image = "ondemand_video.png"
        self.set_image(self.image)
        
def main():
    Gui().root.mainloop()
    # print("quit")
    # root.quit()


if __name__ == '__main__':
    main()
