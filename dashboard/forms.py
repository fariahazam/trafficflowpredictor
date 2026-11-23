import calendar
import re
import holidays as holidays_lib
from django import forms
from .services.filters import NO_HOLIDAYS, ALL_HOLIDAYS

def _us_holiday_choices():
    us = holidays_lib.US(years=range(2012, 2019))
    # skip "(observed)" entries, then order by calendar position
    base = [(d, n) for d, n in us.items() if '(observed)' not in n]
    base.sort(key=lambda item: (item[0].month, item[0].day))
    names = dict.fromkeys(n for _, n in base)        # unique, order kept
    return [(NO_HOLIDAYS, 'No holidays (regular days)'),
            (ALL_HOLIDAYS, 'All holidays')] + [(n, n) for n in names]
    
class TrafficFilterForm(forms.Form):
    day_type = forms.ChoiceField(
        choices=[('both', 'Both'), ('weekday', 'Weekdays'), ('weekend', 'Weekends')],
        initial='both')
    weather = forms.MultipleChoiceField(
        required=False, widget=forms.CheckboxSelectMultiple,
        choices=[(w, w) for w in ['Clear', 'Clouds', 'Rain', 'Snow', 'Mist', 'Fog', 'Drizzle', 'Thunderstorm']])
    temp_min_f = forms.FloatField(required=False, label='Minimum Temperature (°F)')
    temp_max_f = forms.FloatField(required=False, label='Maximum Temperature (°F)')
    holidays = forms.MultipleChoiceField(
        required=False, widget=forms.CheckboxSelectMultiple,
        choices=_us_holiday_choices(), label='Holidays')
    years = forms.MultipleChoiceField(
        required=False, widget=forms.CheckboxSelectMultiple,
        choices=[(y, y) for y in range(2012, 2019)])
    months = forms.MultipleChoiceField(
        required=False, widget=forms.CheckboxSelectMultiple,
        choices=[(m, calendar.month_name[m]) for m in range(1, 13)])
    group_by = forms.ChoiceField(
        choices=[('hour', 'Hour'), ('day_of_week', 'Day of week'),
                 ('month', 'Month'), ('year', 'Year')])