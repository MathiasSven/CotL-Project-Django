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
    def next_city_cost(current_count: int, manifest_destiny=False) -> float:
        return (50000 * ((current_count - 1) ** 3) + 150000 * current_count + 75000) * (0.95 if manifest_destiny else 1)

    @staticmethod
    def infra_unit_price(infra: float) -> float:
        return ((abs(infra - 10) ** 2.2) / 710) + 300

    @staticmethod
    def infra_price(current_infra: float, desired_infra: float, cenciveng=False, adv_engineering_corps=False, urbanization=False) -> float:
        current_infra = round(current_infra, 2)
        desired_infra = round(desired_infra, 2)
        difference = desired_infra - current_infra
        cost_decrease_multiplier = 1 - (cenciveng * 5 + adv_engineering_corps * 5 + urbanization * 5) / 100
        value = 0

        if difference > 10000:
            return SyntaxError

        if difference <= 0:
            infra_price = 150
            return infra_price * difference

        while difference > 100:

            if (difference > 0) and (difference % 100 == 0):
                cost_of_chunk = round(Formulas.infra_unit_price(current_infra), 2) * 100
                value += cost_of_chunk
                current_infra += 100
                difference -= 100

            if (difference > 100) and (difference % 100 != 0):
                cost_of_chunk = round(Formulas.infra_unit_price(current_infra), 2) * (difference % 100)
                value += cost_of_chunk
                current_infra += difference % 100
                difference -= difference % 100

        else:
            cost_of_chunk = round(Formulas.infra_unit_price(current_infra), 2) * difference
            value += cost_of_chunk
            return value * cost_decrease_multiplier

    def war_chest(self, city_count: int) -> dict:
        return {
            'money': city_count * self.config.wc_money,
            'food': city_count * self.config.wc_food,
            'uranium': city_count * self.config.wc_uranium,
            'gasoline': city_count * self.config.wc_gasoline,
            'munitions': city_count * self.config.wc_munitions,
            'steel': city_count * self.config.wc_steel,
            'aluminum': city_count * self.config.wc_aluminum
        }

    def mmr(self, city_count: int) -> dict:
        return {
            'soldiers': int(self.config.mmr[0]) * Formulas.units_per_improvement['barracks'] * city_count,
            'tanks': int(self.config.mmr[1]) * Formulas.units_per_improvement['factory'] * city_count,
            'aircraft': int(self.config.mmr[2]) * Formulas.units_per_improvement['hangar'] * city_count,
            'ships': int(self.config.mmr[3]) * Formulas.units_per_improvement['drydock'] * city_count
        }