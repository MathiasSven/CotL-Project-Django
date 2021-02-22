def next_city_cost(current_count: int, manifest_destiny=False):
    return (50000 * ((current_count - 1) ** 3) + 150000 * current_count + 75000) * (0.95 if manifest_destiny else 1)


def infra_cost(current_infra: float, desired_infra: float):
    return ((((current_infra - 10) ** 2.2) / 710) + 300) * desired_infra


def war_chest(city_count: int):
    return {
        'money': city_count * 2000000,
        'food': city_count * 5000,
        'uranium': city_count * 75,
        'gasoline': city_count * 1500,
        'munitions': city_count * 1750,
        'steel': city_count * 2000,
        'aluminum': city_count * 1000
    }
