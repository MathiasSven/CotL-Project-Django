from .models import AllianceConfig
import sys


class Formulas:
    units_per_improvement = {
        'barracks': 3000,
        'factory': 250,
        'hangar': 15,
        'drydock': 5,
    }

    def __init__(self):
        if not ('migrate' in sys.argv):
            self.config = AllianceConfig.objects.filter(enabled=True).first()
        else:
            self.config = None

    @staticmethod
    def next_city_cost(current_count: int, manifest_destiny=False):
        return (50000 * ((current_count - 1) ** 3) + 150000 * current_count + 75000) * (0.95 if manifest_destiny else 1)

    @staticmethod
    def infra_cost(current_infra: float, desired_infra: float):
        return ((((current_infra - 10) ** 2.2) / 710) + 300) * desired_infra

    def war_chest(self, city_count: int):
        return {
            'money': city_count * self.config.wc_money,
            'food': city_count * self.config.wc_food,
            'uranium': city_count * self.config.wc_uranium,
            'gasoline': city_count * self.config.wc_gasoline,
            'munitions': city_count * self.config.wc_munitions,
            'steel': city_count * self.config.wc_steel,
            'aluminum': city_count * self.config.wc_aluminum
        }

    def mmr(self, city_count: int):
        return {
            'soldiers': int(self.config.mmr[0]) * Formulas.units_per_improvement['barracks'] * city_count,
            'tanks': int(self.config.mmr[1]) * Formulas.units_per_improvement['factory'] * city_count,
            'aircraft': int(self.config.mmr[2]) * Formulas.units_per_improvement['hangar'] * city_count,
            'ships': int(self.config.mmr[3]) * Formulas.units_per_improvement['drydock'] * city_count
        }
