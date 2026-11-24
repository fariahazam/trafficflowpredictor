from pathlib import Path
from datetime import datetime

import holidays
import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

MODEL_PATH = Path(__file__).resolve().parents[2] / 'traffic_model.joblib'


class TrafficPredictor:
    NUM = ['hour', 'day_of_week', 'month', 'is_weekend', 'is_holiday',
           'temp_c', 'rain_1h', 'snow_1h', 'clouds_all']
    CAT = ['weather_main']
    _instance = None

    def __init__(self):
        pre = ColumnTransformer(
            [('cat', OneHotEncoder(handle_unknown='ignore', sparse_output=False), self.CAT)],
            remainder='passthrough')
        self.pipeline = Pipeline([
            ('pre', pre),
            ('model', HistGradientBoostingRegressor(random_state=42))])

    def train(self, df: pd.DataFrame) -> None:
        df = df.copy()
        df['weather_main'] = df['weather_main'].str.split(',').str[0]
        X, y = df[self.NUM + self.CAT], df['traffic_volume']

        train = df['year'] <= 2016          # chronological split
        self.pipeline.fit(X[train], y[train])
        pred = self.pipeline.predict(X[~train])
        print(f"MAE: {mean_absolute_error(y[~train], pred):.0f} vehicles/hr, "
              f"R2: {r2_score(y[~train], pred):.3f}")

        self.pipeline.fit(X, y)             # refit on everything
        joblib.dump(self.pipeline, MODEL_PATH)

    @classmethod
    def get_model(cls) -> 'TrafficPredictor':
        if cls._instance is None:
            inst = cls()
            inst.pipeline = joblib.load(MODEL_PATH)   # FileNotFoundError if untrained
            cls._instance = inst
        return cls._instance

    def predict(self, when: datetime, weather='Clear', temp_c=10.0,
                rain=0.0, snow=0.0, clouds=0) -> float:
        us_h = holidays.US(years=when.year)
        row = pd.DataFrame([{
            'hour': when.hour, 'day_of_week': when.weekday(), 'month': when.month,
            'is_weekend': when.weekday() > 4, 'is_holiday': when.date() in us_h,
            'temp_c': temp_c, 'rain_1h': rain, 'snow_1h': snow,
            'clouds_all': clouds, 'weather_main': weather}])
        return max(0.0, float(self.pipeline.predict(row)[0]))