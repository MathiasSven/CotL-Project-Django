import django_tables2 as tables
from django.db.models import Sum, Value, FloatField
from django.utils.html import format_html

from .models import *


# noinspection PyMethodMayBeStatic
class SummingColumn(tables.Column):
    def __init__(self, data_type='number'):
        self.data_type = data_type
        super(SummingColumn, self).__init__()

    def render(self, value):
        return f'{"$" if self.data_type == "monetary" else ""}{value:,.2f}'

    def render_footer(self, bound_column, table):
        return f'{"$" if self.data_type == "monetary" else ""}{sum(bound_column.accessor.resolve(row) for row in table.data):,.2f}'


class TaxTable(tables.Table):
    def __init__(self, tax_id):
        q_set = AllianceMember.objects.filter(nation__taxrecord__tax_id=tax_id).annotate()
        net_value_calculator = Resources()
        for resource in Resources._meta.get_fields():
            setattr(net_value_calculator, resource.name, list(q_set.aggregate(Sum(f"nation__taxrecord__{resource.name}")).values())[0])
            annotate_kwargs = {f'taxed_{resource.name}': Sum(f"nation__taxrecord__{resource.name}")}
            q_set = q_set.annotate(**annotate_kwargs)

        q_set = q_set.annotate(net_value=Value(net_value_calculator.net_value_now(), FloatField()))
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
