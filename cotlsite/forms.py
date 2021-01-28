from django import forms
from dal import autocomplete

from pnwdata.models import AllianceMember


class AllianceMemberForm(forms.ModelForm):
    class Meta:
        model = AllianceMember
        fields = ['nation']
        widgets = {
            'nation': autocomplete.ModelSelect2(url='alliance-members-autocomplete',
                                                attrs={'data-html': True})
        }
