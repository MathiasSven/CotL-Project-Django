import django_tables2 as tables
from django.db.models import F, Sum

from django.utils.html import format_html

from .models import *
from .formulas import Formulas

import configparser
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
config = configparser.ConfigParser()
config.read(f"{BASE_DIR}/config.ini")


# noinspection PyMethodMayBeStatic
class SummingColumn(tables.Column):
    def __init__(self, data_type='number'):
        self.data_type = data_type
        super(SummingColumn, self).__init__()

    def render(self, value):
        return f'{"$" if self.data_type == "monetary" else ""}{value:,.2f}'

    def render_footer(self, bound_column, table):
        return f'{"$" if self.data_type == "monetary" else ""}{sum(bound_column.accessor.resolve(row) for row in table.data):,.2f}'


class FormatColumn(tables.Column):
    def __init__(self, data_type='number', **kwargs):
        self.data_type = data_type
        super(FormatColumn, self).__init__(**kwargs)

    def render(self, value):
        return f'{"$" if self.data_type == "monetary" else ""}{value:,.2f}'


class TaxTable(tables.Table):
    def __init__(self, tax_id):
        q_set = AllianceMember.objects.filter(nation__taxrecord__tax_id=tax_id).annotate()
        net_value_f_expression = 0
        for resource in Resources._meta.get_fields():
            annotate_kwargs = {f'taxed_{resource.name}': Sum(f"nation__taxrecord__{resource.name}")}
            q_set = q_set.annotate(**annotate_kwargs)
            net_value_f_expression += F(f'nation__taxrecord__{resource.name}') * (Market.objects.get(pk=resource.name).avgprice if resource.name != 'money' else 1)

        q_set = q_set.annotate(net_value=Sum(net_value_f_expression))
        super(TaxTable, self).__init__(q_set)

    nation__nationid = tables.Column()
    nation__nation = tables.Column()

    for resource in Resources._meta.get_fields():
        if resource.name == "money":
            taxed_money = SummingColumn(data_type='monetary')
            continue
        exec(f'taxed_{resource.name} = SummingColumn()')

    # noinspection PyMethodMayBeStatic
    def render_nation__nation(self, value, record):
        return format_html(f"<a href='https://politicsandwar.com/nation/id={record.nation.nationid}' target='_blank'>{value}</a>")

    net_value = SummingColumn(data_type='monetary')


# class ProjectsTable(tables.Table):
#     def __init__(self, tax_id):
#         q_set = Projects.objects.filter(nation__taxrecord__tax_id=tax_id)
#         super(ProjectsTable, self).__init__(q_set)
#
#

def check_authorization(f):
    def wrapper(*args):
        return f(*args, resource_type=2)

    return wrapper


# noinspection PyMethodMayBeStatic,PyAttributeOutsideInit
class WCTable(tables.Table):
    def __init__(self, tax_id):
        self.formulas = Formulas()
        q_set = AllianceMember.objects.filter(nation__taxrecord__tax_id=tax_id).distinct()
        super(WCTable, self).__init__(q_set)

    nation__nationid = tables.Column()
    nation__nation = tables.Column()

    war_chest_resources = ['money', 'food', 'uranium', 'gasoline', 'munitions', 'steel', 'aluminum']

    def render_nation__nation(self, value, record):
        return format_html(f"<a href='https://politicsandwar.com/nation/id={record.nation.nationid}' target='_blank'>{value}</a>")

    def render_money(self, value, record):
        var = float(self.formulas.war_chest(record.nation.cities)['money'])
        diff = (value / var) * 100.00
        if value < var:
            return format_html(f"<span style='color: red'>${value:,.2f} (%{diff:,.2f})</span>")
        else:
            return format_html(f"<span style='color: green'>${value:,.2f} (%{diff:,.2f})</span>")

    def render_food(self, value, record):
        var = float(self.formulas.war_chest(record.nation.cities)['food'])
        diff = (value / var) * 100.00
        if value < var:
            return format_html(f"<span style='color: red'>{value:,.2f} (%{diff:,.2f})</span>")
        else:
            return format_html(f"<span style='color: green'>{value:,.2f} (%{diff:,.2f})</span>")

    def render_uranium(self, value, record):
        var = float(self.formulas.war_chest(record.nation.cities)['uranium'])
        diff = (value / var) * 100.00
        if value < var:
            return format_html(f"<span style='color: red'>{value:,.2f} (%{diff:,.2f})</span>")
        else:
            return format_html(f"<span style='color: green'>{value:,.2f} (%{diff:,.2f})</span>")

    def render_gasoline(self, value, record):
        var = float(self.formulas.war_chest(record.nation.cities)['gasoline'])
        diff = (value / var) * 100.00
        if value < var:
            return format_html(f"<span style='color: red'>{value:,.2f} (%{diff:,.2f})</span>")
        else:
            return format_html(f"<span style='color: green'>{value:,.2f} (%{diff:,.2f})</span>")

    def render_munitions(self, value, record):
        var = float(self.formulas.war_chest(record.nation.cities)['munitions'])
        diff = (value / var) * 100.00
        if value < var:
            return format_html(f"<span style='color: red'>{value:,.2f} (%{diff:,.2f})</span>")
        else:
            return format_html(f"<span style='color: green'>{value:,.2f} (%{diff:,.2f})</span>")

    def render_aluminum(self, value, record):
        var = float(self.formulas.war_chest(record.nation.cities)['aluminum'])
        diff = (value / var) * 100.00
        if value < var:
            return format_html(f"<span style='color: red'>{value:,.2f} (%{diff:,.2f})</span>")
        else:
            return format_html(f"<span style='color: green'>{value:,.2f} (%{diff:,.2f})</span>")

    def render_steel(self, value, record):
        var = float(self.formulas.war_chest(record.nation.cities)['steel'])
        diff = (value / var) * 100.00
        if value < var:
            return format_html(f"<span style='color: red'>{value:,.2f} (%{diff:,.2f})</span>")
        else:
            return format_html(f"<span style='color: green'>{value:,.2f} (%{diff:,.2f})</span>")

    for resource in war_chest_resources:
        exec(f'{resource} = tables.Column()')


# noinspection PyMethodMayBeStatic
class CityTable(tables.Table):
    def __init__(self, tax_id):
        self.formulas = Formulas()
        q_set = AllianceMember.objects.filter(nation__taxrecord__tax_id=tax_id).distinct().annotate(next_city_cost=self.formulas.next_city_cost(F('nation__cities'), manifest_destiny=True)).annotate(
            withdraw_link=self.formulas.next_city_cost(F('nation__cities'), manifest_destiny=True))
        super(CityTable, self).__init__(q_set)

    nation__nationid = tables.Column()
    nation__nation = tables.Column()

    cityprojecttimerturns = tables.Column(verbose_name='City/Project Timer')

    nation__cities = tables.Column()
    next_city_cost = FormatColumn(data_type='monetary', verbose_name='Next city cost (MD)')

    withdraw_link = tables.Column(verbose_name='Withdraw link (MD)')

    def render_cityprojecttimerturns(self, value, record):
        return format_html(f"<span>{value} Turns</span>")

    def render_next_city_cost(self, value, record):
        suffix = ''
        if record.nation.projects.city_planning:
            value -= 50000000
            suffix += ' (UP)'
        if record.nation.projects.adv_city_planning:
            value -= 100000000
            suffix = suffix[:-1] + '+AUP)'
        return format_html(f"<span>${value:,.2f}{suffix}</span>")

    def render_nation__nation(self, value, record):
        return format_html(f"<a href='https://politicsandwar.com/nation/id={record.nation.nationid}' target='_blank'>{value}</a>")

    def render_withdraw_link(self, value, record):
        suffix = ''
        if record.nation.projects.city_planning:
            value -= 50000000
            suffix += '%20(UP)'
        if record.nation.projects.adv_city_planning:
            value -= 100000000
            suffix = suffix[:-1] + '%20AUP)'
        return format_html(
            f"<a href='https://politicsandwar.com/alliance/id=7452&display=bank&w_type=nation&w_recipient={record.nation.nation.replace(' ', '%20')}&w_note={record.nation.cities + 1}{suffix}%20City&w_money={int(value)}' target='_blank'>Link Here</a>")


# noinspection PyMethodMayBeStatic,DuplicatedCode
class NationGrade(tables.Table):
    def __init__(self, tax_id):
        self.formulas = Formulas()
        q_set = AllianceMember.objects.filter(nation__taxrecord__tax_id=tax_id).distinct().annotate(ph1=F('credits'), ph2=F('credits'), ph3=F('credits'), ph4=F('credits'), ph5=F('nation__cities'),
                                                                                                    ph6=F('nation__cities'), ph7=F('credits'), ph8=F('credits'))
        super(NationGrade, self).__init__(q_set)

    nation__nation = tables.Column()

    nation__minutessinceactive = tables.Column(verbose_name='Hours Since Active')
    ph1 = tables.Column(verbose_name='Inactive days in the last 30 Days')
    ph2 = tables.Column(verbose_name='14 Days')
    ph3 = tables.Column(verbose_name='7 Days')
    ph4 = tables.Column(verbose_name='3 Days')

    ph5 = tables.Column(verbose_name='MMR Percentages')
    ph6 = tables.Column(verbose_name='Net WC')
    ph7 = tables.Column(verbose_name='Net WC p/city')

    ph8 = tables.Column(verbose_name='Overall Score')

    def render_nation__nation(self, value, record):
        return format_html(f"<a href='https://politicsandwar.com/nation/id={record.nation.nationid}' target='_blank'>{value}</a>")

    def render_nation__minutessinceactive(self, value, record):
        return f"{value // 60} H"

    def render_ph1(self, value, record):
        return f"{30 - record.active_days_since(days_ago=29)} Days"

    def render_ph2(self, value, record):
        return f"{14 - record.active_days_since(days_ago=13)} Days"

    def render_ph3(self, value, record):
        return f"{7 - record.active_days_since(days_ago=6)} Days"

    def render_ph4(self, value, record):
        return f"{3 - record.active_days_since(days_ago=2)} Days"

    def render_ph5(self, value, record):
        value_shown = ''
        mmr_values = self.formulas.mmr(value)
        for mmr_value in mmr_values:
            if mmr_values[mmr_value] != 0:
                value_shown += f'{round((getattr(record.nation.nationmilitary, mmr_value)/mmr_values[mmr_value]) * 100)}%/'
            else:
                value_shown += '-/'
        value_shown = value_shown[:-1]
        return value_shown

    def render_ph6(self, value, record):
        resources = [resource.name for resource in Resources._meta.get_fields()]
        resources.pop(0)
        wc_requirements = self.formulas.war_chest(record.nation.cities)
        value_delta = -1 * wc_requirements.pop('money') + record.money
        for resource in resources:
            if resource in wc_requirements:
                value_delta += (getattr(record, resource) - wc_requirements[resource]) * Market.objects.get(resource=resource).avgprice
            else:
                value_delta += getattr(record, resource) * Market.objects.get(resource=resource).avgprice

        if value_delta < 0:
            return format_html(f"<span style='color: red'>${value_delta:,.2f}</span>")
        else:
            return format_html(f"<span style='color: green'>${value_delta:,.2f}</span>")

    def render_ph7(self, value, record):
        resources = [resource.name for resource in Resources._meta.get_fields()]
        resources.pop(0)
        wc_requirements = self.formulas.war_chest(record.nation.cities)
        value_delta = -1 * wc_requirements.pop('money') + record.money
        for resource in resources:
            if resource in wc_requirements:
                value_delta += (getattr(record, resource) - wc_requirements[resource]) * Market.objects.get(resource=resource).avgprice
            else:
                value_delta += getattr(record, resource) * Market.objects.get(resource=resource).avgprice

        value_delta = value_delta / record.nation.cities

        if value_delta < 0:
            return format_html(f"<span style='color: red'>${value_delta:,.2f}</span>")
        else:
            return format_html(f"<span style='color: green'>${value_delta:,.2f}</span>")

    def render_ph8(self, value, record):
        return 0