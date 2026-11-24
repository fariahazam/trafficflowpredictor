from datetime import datetime, time
from .forms import TrafficFilterForm, PredictionForm
from .services.model import TrafficPredictor
from io import BytesIO
import matplotlib.pyplot as plt
from django.http import HttpResponse
from django.shortcuts import render
from .forms import TrafficFilterForm
from .services.data_loader import TrafficDataLoader
from .services.filters import TrafficFilter
from .services.charts import ChartBuilder


def index(request):
    form = TrafficFilterForm(request.GET or None)
    return render(request, 'dashboard/index.html', {'form': form})

def chart_png(request):
    data = request.GET if request.GET else {'day_type': 'both', 'group_by': 'hour'}
    form = TrafficFilterForm(data)
    df = TrafficDataLoader().get_data()
    if form.is_valid():
        c = form.cleaned_data
        f = TrafficFilter(
            day_type=c['day_type'], weather=c['weather'],
            temp_min_f=c['temp_min_f'], temp_max_f=c['temp_max_f'],
            holidays=c['holidays'],
            years=[int(y) for y in c['years']],
            months=[int(m) for m in c['months']])
        fig = ChartBuilder().build(f.apply(df), c['group_by'], 'I-94 West Traffic')
    else:
        print(form.errors)
        fig = ChartBuilder().build(df.iloc[0:0])
    buf = BytesIO()
    fig.savefig(buf, format='png', dpi=100)
    plt.close(fig)                       # prevents memory leaks
    return HttpResponse(buf.getvalue(), content_type='image/png')

def predict(request):
    form = PredictionForm(request.GET or None)
    result, error = None, None
    if form.is_valid():
        c = form.cleaned_data
        when = datetime.combine(c['date'], time(hour=int(c['hour'])))
        try:
            model = TrafficPredictor.get_model()
        except FileNotFoundError:
            error = 'The model has not been trained yet. Run: py manage.py train_model'
        else:
            result = round(model.predict(
                when, weather=c['weather'],
                temp_c=(c['temp_f'] - 32) / 1.8,
                rain=c['rain_1h'], snow=c['snow_1h'], clouds=c['clouds_all']))
    return render(request, 'dashboard/predict.html',
                  {'form': form, 'result': result, 'error': error})