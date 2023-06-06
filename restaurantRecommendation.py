import warnings
from skfuzzy import control as ctrl
import skfuzzy as fuzz
import numpy as np
from matplotlib import pyplot as plt
from skfuzzy.control.fuzzyvariable import FuzzyVariableVisualizer

from utils import images


class RestaurantRecommendation:
    
    def __init__(self):
        self.price_range = (10,150)      
        self.price = ctrl.Antecedent(np.arange(self.price_range[0], self.price_range[1]+1, 1), 'price')
        
        self.price['cheap'] = fuzz.trimf(self.price.universe, [10, 10, 30])
        self.price['affordable'] = fuzz.trapmf(self.price.universe, [25, 35, 45, 55])
        self.price['expensive'] = fuzz.trapmf(self.price.universe, [40, 60, 70, 90])
        self.price['very_expensive'] = fuzz.trapmf(self.price.universe, [80, 120, 150, 150])

        fig, _ = FuzzyVariableVisualizer(self.price).view()
        plt.savefig(images[0][1])
        
        self.cuisine_range=(0,10)
        self.cuisine = ctrl.Antecedent(np.arange(self.cuisine_range[0], self.cuisine_range[1]+.5, 0.5), 'cuisine')

        self.cuisine['bad'] = fuzz.trimf(self.cuisine.universe, [0, 0, 4])
        self.cuisine['acceptable'] = fuzz.trapmf(self.cuisine.universe, [3, 4.5, 5.5, 7])
        self.cuisine['good'] = fuzz.trimf(self.cuisine.universe, [6, 10, 10])
        fig, _ = FuzzyVariableVisualizer(self.cuisine).view()
        plt.savefig(images[1][1])

        self.location_range = (0,20)
        self.location = ctrl.Antecedent(np.arange(self.location_range[0], self.location_range[1]+.5, 0.5), 'location')

        self.location['close'] = fuzz.trimf(self.location.universe, [0, 0, 5])
        self.location['normal'] = fuzz.trapmf(self.location.universe, [4, 6.5, 7.5, 10])
        self.location['far'] = fuzz.trapmf(self.location.universe, [8, 11, 13, 15])
        self.location['very_far'] = fuzz.trimf(self.location.universe, [14, 20, 20])
        fig, _ = FuzzyVariableVisualizer(self.location).view()
        plt.savefig(images[2][1])

        self.recommendation = ctrl.Consequent(np.arange(0, 10.5, 0.5), 'recommendation')

        self.recommendation['bad'] = fuzz.trimf(self.recommendation.universe, [0, 0, 4])
        self.recommendation['acceptable'] = fuzz.trimf(self.recommendation.universe, [3, 4.5, 6])
        self.recommendation['recommended'] = fuzz.trimf(self.recommendation.universe, [5, 6.5, 8])
        self.recommendation['highly_recommended'] = fuzz.trimf(self.recommendation.universe, [7, 10, 10])

        fig, _ = FuzzyVariableVisualizer(self.recommendation).view()
        plt.savefig(images[3][1])

        self.recommendation_ctrl= self.rules()
        self.recommender = ctrl.ControlSystemSimulation(self.recommendation_ctrl)
        
    def rules(self):
        return ctrl.ControlSystem([
            ctrl.Rule(  # 1
                self.price['cheap'] &
                (self.cuisine['good']) &
                ~self.location['very_far']

                , self.recommendation['highly_recommended']
            ),

            ctrl.Rule(  # 2
                self.price['cheap'] &
                (self.cuisine['good']) &
                self.location['very_far']

                , self.recommendation['recommended']
            ),

            ctrl.Rule(  # 3
                self.price['cheap'] &
                (self.cuisine['acceptable']) &
                self.location['close']

                , self.recommendation['recommended']
            ),

            ctrl.Rule(  # 4
                self.price['cheap'] &
                (self.cuisine['acceptable']) &
                ~self.location['close']

                , self.recommendation['acceptable']
            ),

            ctrl.Rule(  # 5 6 11 16
                (self.price['cheap'] & self.cuisine['bad']) |
                (~self.price['cheap'] & ~self.cuisine['good'])
                , self.recommendation['bad']
            ),

            ctrl.Rule(  # 7
                self.price['affordable'] &
                (self.cuisine['acceptable']) &
                (self.location['close'] | self.location['normal'])

                , self.recommendation['acceptable']
            ),

            ctrl.Rule(  # 8
                self.price['affordable'] &
                (self.cuisine['acceptable']) &
                ~(self.location['close'] | self.location['normal'])

                , self.recommendation['bad']
            ),

            ctrl.Rule(  # 9
                self.price['affordable'] &
                (self.cuisine['good']) &
                (self.location['close'] | self.location['normal'])

                , self.recommendation['recommended']
            ),

            ctrl.Rule(  # 10
                self.price['affordable'] &
                (self.cuisine['good']) &
                (self.location['close'] | self.location['normal'])

                , self.recommendation['acceptable']
            ),

            ctrl.Rule(  # 12
                self.price['expensive'] &
                (self.cuisine['good']) &
                (self.location['close'])

                , self.recommendation['recommended']
            ),

            ctrl.Rule(  # 13
                self.price['expensive'] &
                (self.cuisine['good']) &
                (self.location['normal'])

                , self.recommendation['acceptable']
            ),

            ctrl.Rule(  # 14
                self.price['expensive'] &
                (self.cuisine['good']) &
                ~(self.location['close'] | self.location['normal'])

                , self.recommendation['bad']
            )
        ])

    def set_inputs(self, c, p, l):
        self.recommender.input['cuisine'] = c
        self.recommender.input['price'] = p
        self.recommender.input['location'] = l

        self.recommender.compute()
        fig, _ = FuzzyVariableVisualizer(self.recommendation).view(sim=self.recommender)
        plt.savefig(images[4][1])

        return self.recommender.output['recommendation']
