from pathlib import Path
from datetime import datetime

import holidays
import joblib # type: ignore[import-untyped]
import pandas as pd
from sklearn.compose import ColumnTransformer # type: ignore[import-untyped]
from sklearn.ensemble import HistGradientBoostingRegressor # type: ignore[import-untyped]
from sklearn.metrics import mean_absolute_error, r2_score # type: ignore[import-untyped]
from sklearn.pipeline import Pipeline # type: ignore[import-untyped]
from sklearn.preprocessing import OneHotEncoder # type: ignore[import-untyped]

MODEL_PATH = Path(__file__).resolve().parents[2] / 'traffic_model.joblib'


class TrafficPredictor:
    """Predicts hourly I-94 West traffic volume"""
    NUM = ['hour', 'day_of_week', 'month', 'is_weekend', 'is_holiday',
           'temp_c', 'rain_1h', 'snow_1h', 'clouds_all']
    CAT = ['weather_main']
    _instance = None

    def __init__(self) -> None:
        """Build an untrained pipeline of a weather encoder and a gradient boosting regressor"""
        pre = ColumnTransformer(
            [('cat', OneHotEncoder(handle_unknown='ignore', sparse_output=False), self.CAT)],
            remainder='passthrough')
        self.pipeline = Pipeline([
            ('pre', pre),
            ('model', HistGradientBoostingRegressor(random_state=42))])

    def train(self, df: pd.DataFrame) -> None:
        """Train on the cleaned data, refit on all rows and save the model"""
        df = df.copy()
        df['weather_main'] = df['weather_main'].str.split(',').str[0]
        x, y = df[self.NUM + self.CAT], df['traffic_volume']

        train = df['year'] <= 2016
        self.pipeline.fit(x[train], y[train])
        pred = self.pipeline.predict(x[~train])
        print(f"MAE: {mean_absolute_error(y[~train], pred):.0f} vehicles/hr, "
              f"R2: {r2_score(y[~train], pred):.3f}")

        self.pipeline.fit(x, y)
        joblib.dump(self.pipeline, MODEL_PATH)

    @classmethod
    def get_model(cls) -> 'TrafficPredictor':
        """Return the saved model, raise FileNotFoundError if it hasn't been trained."""
        if cls._instance is None:
            inst = cls()
            inst.pipeline = joblib.load(MODEL_PATH)   # FileNotFoundError if untrained
            cls._instance = inst
        return cls._instance

    def predict(self, when: datetime, weather: str = 'Clear', temp_c: float = 10.0,
                rain: float = 0.0, snow: float = 0.0, clouds: float = 0) -> float:
        """Return predicted vehicles per hour for 
        a date and hour under provided weather conditions"""
        us_h = holidays.US(years=when.year)
        row = pd.DataFrame([{
            'hour': when.hour, 'day_of_week': when.weekday(), 'month': when.month,
            'is_weekend': when.weekday() > 4, 'is_holiday': when.date() in us_h,
            'temp_c': temp_c, 'rain_1h': rain, 'snow_1h': snow,
            'clouds_all': clouds, 'weather_main': weather}])
        return max(0.0, float(self.pipeline.predict(row)[0]))
