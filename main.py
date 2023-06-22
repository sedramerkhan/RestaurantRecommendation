from gui import Gui
from restaurant_recommendation import RestaurantRecommendation
from config import images_paths, files_paths
import pandas as pd


def load_data(path):
    return pd.read_csv(path).to_dict(orient='records')



def main():
    cuisines = load_data(files_paths['cuisines'])
    cuisines = {cuisine['country']: cuisine['score'] for cuisine in cuisines}
    restaurants = load_data(files_paths['restaurants'])

    restaurant_recommendation = RestaurantRecommendation(images_paths)
    gui = Gui(restaurant_recommendation, cuisines, restaurants, images_paths)
    gui.root.mainloop()


if __name__ == '__main__':
    main()
