# trafficflowpredictor
A Django web app for exploring hourly traffic volume on I-94 West (2012-2018) and predicting traffic for future dates. Charts are drawn with matplotlib, and predictions come from a scikit-learn model trained on the same data.

**Features:**

**Traffic explorer** (/)

- Filter by weekdays, weekends, or both
- Filter by weather condition (Clear, Clouds, Rain, Snow, Mist, Fog, Drizzle, Thunderstorm)
- Filter by minimum and maximum temperature (°F)
- Filter by holiday: no holidays, all holidays, or individual US holidays
- Filter by year and month
- Group the chart by hour of day, day of week, month, or year, with readable axis labels (for example 4 PM, Mon, Jan)

**Traffic Prediction** (/predict/)

- Pick a date, hour, and assumed conditions (weather, temperature, rain, snow, cloud cover)
- Returns the predicted traffic volume in vehicles per hour
- Weekday, month, weekend, and US holiday features are computed from the date 
- Weather is an input you supply

**Tech Stack:**

- Python, Django
- pandas, numpy
- matplotlib (Agg backend, charts returned as PNG)
- scikit-learn (gradient boosting pipeline), joblib
- holidays (US holiday calendar)

**Limitations:**

The dataset covers 2012-2018 only, and some periods have missing hours, so averages for those stretches rest on less data.
