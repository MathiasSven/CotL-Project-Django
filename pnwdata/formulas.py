from .models import AllianceConfig
import sys

if not ('migrate' in sys.argv):
    config = AllianceConfig.objects.filter(enabled=True).first()
else:
    config = None


def next_city_cost(current_count: int, manifest_destiny=False):
    return (50000 * ((current_count - 1) ** 3) + 150000 * current_count + 75000) * (0.95 if manifest_destiny else 1)


def infra_cost(current_infra: float, desired_infra: float):
    return ((((current_infra - 10) ** 2.2) / 710) + 300) * desired_infra


def war_chest(city_count: int):
    return {
        'money': city_count * config.wc_money,
        'food': city_count * config.wc_food,
        'uranium': city_count * config.wc_uranium,
        'gasoline': city_count * config.wc_gasoline,
        'munitions': city_count * config.wc_munitions,
        'steel': city_count * config.wc_steel,
        'aluminum': city_count * config.wc_aluminum
    }


units_per_improvement = {
    'barracks': 3000,
    'factory': 250,
    'hangar': 15,
    'drydock': 5,
}


def mmr(city_count: int):
    return {
        'soldiers': int(config.mmr[0]) * units_per_improvement['barracks'] * city_count,
        'tanks': int(config.mmr[1]) * units_per_improvement['factory'] * city_count,
        'aircraft': int(config.mmr[2]) * units_per_improvement['hangar'] * city_count,
        'ships': int(config.mmr[3]) * units_per_improvement['drydock'] * city_count
    }
