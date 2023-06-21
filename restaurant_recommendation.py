import warnings
from skfuzzy import control as ctrl
import skfuzzy as fuzz
import numpy as np
from matplotlib import pyplot as plt
from skfuzzy.control.fuzzyvariable import FuzzyVariableVisualizer


class RestaurantRecommendation:

    def __init__(self, images_paths):
        self.images_paths = images_paths

        self.price_range = (10, 150)
        self.price = ctrl.Antecedent(
            np.arange(self.price_range[0], self.price_range[1]+1, 1), 'price')

        self.price['cheap'] = fuzz.trapmf(self.price.universe, [10, 10, 30,40])
        self.price['affordable'] = fuzz.trimf(self.price.universe, [20, 40, 60])
        self.price['expensive'] = fuzz.trimf(self.price.universe, [40, 60, 80])
        self.price['very_expensive'] = fuzz.trapmf(self.price.universe, [60, 100, 150, 150])

        fig, _ = FuzzyVariableVisualizer(self.price).view()
        plt.savefig(images_paths['price'])

        self.cuisine_range = (0, 5)
        step = .01
        self.cuisine = ctrl.Antecedent(
            np.arange(self.cuisine_range[0], self.cuisine_range[1]+step, step), 'cuisine')

        self.cuisine['bad'] = fuzz.trimf(self.cuisine.universe, [self.cuisine_range[0], self.cuisine_range[0],3])
        self.cuisine['acceptable'] = fuzz.trimf(self.cuisine.universe, [2.5, 3.25, 4])
        self.cuisine['good'] = fuzz.trimf(self.cuisine.universe, [3.7, 5, 5])
        fig, _ = FuzzyVariableVisualizer(self.cuisine).view()
        plt.savefig(images_paths['cuisine'])

        self.location_range = (0, 20)
        self.location = ctrl.Antecedent(
            np.arange(self.location_range[0], self.location_range[1]+.5, 0.5), 'location')

        self.location['close'] = fuzz.trapmf(self.location.universe, [0, 0,3, 5])
        self.location['normal'] = fuzz.trimf(self.location.universe, [2, 6, 10])
        self.location['far'] = fuzz.trimf(self.location.universe, [6, 11, 15])
        self.location['very_far'] = fuzz.trimf(self.location.universe, [14, 20, 20])
        fig, _ = FuzzyVariableVisualizer(self.location).view()
        plt.savefig(images_paths['location'])

        self.recommendation = ctrl.Consequent(np.arange(0, 10.5, 0.5), 'recommendation')

        self.recommendation['bad'] = fuzz.trimf(self.recommendation.universe, [0, 0, 4])
        self.recommendation['acceptable'] = fuzz.trimf(
            self.recommendation.universe, [3, 4.5, 6])
        self.recommendation['recommended'] = fuzz.trimf(
            self.recommendation.universe, [5, 6.5, 8])
        self.recommendation['highly_recommended'] = fuzz.trimf(
            self.recommendation.universe, [7, 10, 10])

        fig, _ = FuzzyVariableVisualizer(self.recommendation).view()
        plt.savefig(images_paths['recommendation'])

        self.recommendation_ctrl = self.rules()
        self.recommender = ctrl.ControlSystemSimulation(self.recommendation_ctrl)

    def rules(self):
        return ctrl.ControlSystem([
            ctrl.Rule(  # 1
                self.price['cheap'] &
                (self.cuisine['good']) &
                ~self.location['very_far'], self.recommendation['highly_recommended']
            ),

            ctrl.Rule(  # 2
                self.price['cheap'] &
                (self.cuisine['good']) &
                self.location['very_far'], self.recommendation['recommended']
            ),

            ctrl.Rule(  # 3
                self.price['cheap'] &
                (self.cuisine['acceptable']) &
                self.location['close'], self.recommendation['recommended']
            ),

            ctrl.Rule(  # 4
                self.price['cheap'] &
                (self.cuisine['acceptable']) &
                ~self.location['close'], self.recommendation['acceptable']
            ),

            ctrl.Rule(  # 5 6 11 16
                (self.price['cheap'] & self.cuisine['bad']) |
                (~self.price['cheap'] & ~self.cuisine['good']), self.recommendation['bad']
            ),

            ctrl.Rule(  # 7
                self.price['affordable'] &
                (self.cuisine['acceptable']) &
                (self.location['close'] | self.location['normal']
                 ), self.recommendation['acceptable']
            ),

            ctrl.Rule(  # 8
                self.price['affordable'] &
                (self.cuisine['acceptable']) &
                ~(self.location['close'] | self.location['normal']), self.recommendation['bad']
            ),

            ctrl.Rule(  # 9
                self.price['affordable'] &
                (self.cuisine['good']) &
                (self.location['close'] | self.location['normal']
                 ), self.recommendation['recommended']
            ),

            ctrl.Rule(  # 10
                self.price['affordable'] &
                (self.cuisine['good']) &
                (self.location['close'] | self.location['normal']
                 ), self.recommendation['acceptable']
            ),

            ctrl.Rule(  # 12
                self.price['expensive'] &
                (self.cuisine['good']) &
                (self.location['close']), self.recommendation['recommended']
            ),

            ctrl.Rule(  # 13
                self.price['expensive'] &
                (self.cuisine['good']) &
                (self.location['normal']), self.recommendation['acceptable']
            ),

            ctrl.Rule(  # 14
                self.price['expensive'] &
                (self.cuisine['good']) &
                ~(self.location['close'] | self.location['normal']), self.recommendation['bad']
            )
        ])

    def set_inputs(self, c, p, l):
        self.recommender.input['cuisine'] = c
        self.recommender.input['price'] = p
        self.recommender.input['location'] = l

        self.recommender.compute()
        fig, _ = FuzzyVariableVisualizer(self.recommendation).view(sim=self.recommender)
        plt.savefig(self.images_paths['recommendation output'])

        return self.recommender.output['recommendation']


# cuisine: 5.0, price: 150.0 location: 10.0