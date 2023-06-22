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

        self.price['cheap'] = fuzz.trapmf(self.price.universe, [10, 10, 30, 40])
        self.price['affordable'] = fuzz.trimf(self.price.universe, [20, 40, 60])
        self.price['expensive'] = fuzz.trimf(self.price.universe, [40, 60, 80])
        self.price['very_expensive'] = fuzz.trapmf(self.price.universe, [60, 100, 150, 150])

        fig, _ = FuzzyVariableVisualizer(self.price).view()
        plt.savefig(images_paths['price'])

        self.cuisine_range = (0, 5)
        step = .01
        self.cuisine = ctrl.Antecedent(
            np.arange(self.cuisine_range[0], self.cuisine_range[1]+step, step), 'cuisine')

        self.cuisine['bad'] = fuzz.trimf(
            self.cuisine.universe, [self.cuisine_range[0], self.cuisine_range[0], 3])
        self.cuisine['acceptable'] = fuzz.trimf(self.cuisine.universe, [2.5, 3.25, 4])
        self.cuisine['good'] = fuzz.trimf(self.cuisine.universe, [3.7, 5, 5])
        fig, _ = FuzzyVariableVisualizer(self.cuisine).view()
        plt.savefig(images_paths['cuisine'])

        self.location_range = (0, 20)
        self.location = ctrl.Antecedent(
            np.arange(self.location_range[0], self.location_range[1]+.5, 0.5), 'location')

        self.location['close'] = fuzz.trapmf(self.location.universe, [0, 0, 3, 5])
        self.location['normal'] = fuzz.trimf(self.location.universe, [2, 6, 10])
        self.location['far'] = fuzz.trimf(self.location.universe, [6, 11, 15])
        self.location['very_far'] = fuzz.trimf(self.location.universe, [14, 20, 20])
        fig, _ = FuzzyVariableVisualizer(self.location).view()
        plt.savefig(images_paths['location'])

        self.recommendation = ctrl.Consequent(
            np.arange(0, 10.5, 0.5), 'recommendation', defuzzify_method='centroid')

        self.recommendation['bad'] = fuzz.trimf(
            self.recommendation.universe, [0, 0, 4])
        self.recommendation['acceptable'] = fuzz.trimf(
            self.recommendation.universe, [3, 4.5, 6])
        self.recommendation['recommended'] = fuzz.trimf(
            self.recommendation.universe, [5, 6.5, 8])
        self.recommendation['highly_recommended'] = fuzz.trimf(
            self.recommendation.universe, [7, 10, 10])

        fig, _ = FuzzyVariableVisualizer(self.recommendation).view()
        plt.savefig(images_paths['recommendation'])

        self.recommendation_ctrl = self.rules()
        self.recommender = ctrl.ControlSystemSimulation(
            self.recommendation_ctrl)

    def rules(self):
        return ctrl.ControlSystem([
            ctrl.Rule(
                self.cuisine['bad'] & self.price['cheap'] & self.location['close'], self.recommendation['acceptable']
            ),

            ctrl.Rule(
                self.cuisine['bad'] & (
                    (self.price['affordable'] | self.price['expensive']
                     | self.price['very_expensive'])
                    | (self.location['normal'] | self.location['far'] | self.location['very_far'])
                ), self.recommendation['bad']
            ),

            ctrl.Rule(
                self.cuisine['good'] & self.price['very_expensive'] & (
                    self.location['far'] | self.location['very_far']), self.recommendation['acceptable']
            ),
            ctrl.Rule(
                self.cuisine['good'] & self.price['expensive'] & (
                    self.location['far'] | self.location['very_far']), self.recommendation['recommended']
            ),
            ctrl.Rule(
                self.cuisine['good'] & (
                    (self.price['cheap'] | self.price['affordable']) |
                    (self.location['close'] | self.location['normal'])
                ), self.recommendation['highly_recommended']
            ),

            ctrl.Rule(
                self.cuisine['acceptable'] & self.price['very_expensive'] & (
                    self.location['far'] | self.location['very_far']), self.recommendation['bad']
            ),
            ctrl.Rule(
                self.cuisine['acceptable'] & self.price['expensive'] & (
                    self.location['far'] | self.location['very_far']), self.recommendation['acceptable']
            ),
            ctrl.Rule(
                self.cuisine['acceptable'] & (
                    (self.price['cheap'] | self.price['affordable']) | (
                        self.location['close'] | self.location['normal'])
                ), self.recommendation['recommended']
            )
        ])

    def set_inputs(self, c, p, l):
        self.recommender.input['cuisine'] = c
        self.recommender.input['price'] = p
        self.recommender.input['location'] = l
        print(f"{self.get_variable_key(self.price,p)} price, {self.get_variable_key(self.cuisine,c)} cuisine, {self.get_variable_key(self.location,l)} destination")
        self.recommender.compute()
        fig, _ = FuzzyVariableVisualizer(
            self.recommendation).view(sim=self.recommender)
        plt.savefig(self.images_paths['recommendation output'])

        return self.recommender.output['recommendation']
    def get_variable_key(self,variable, user_input):
        max_membership = 0
        key_with_max_membership = None

        for key in variable.terms.keys():
            membership = fuzz.interp_membership(variable.universe, variable[key].mf, user_input)
            if membership > max_membership:
                max_membership = membership
                key_with_max_membership = key

        return key_with_max_membership

# cuisine: 5.0, price: 150.0 location: 10.0
