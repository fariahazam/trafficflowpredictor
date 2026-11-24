import pandas as pd
import holidays

class TrafficDataLoader:
    """Loads CSV file into pandas dataframe"""
    df: pd.DataFrame | None = None
    def load(self) -> pd.DataFrame:
        """Cleans up data and adds new fields to the dataset"""
        df = pd.read_csv("Metro_Interstate_Traffic_Volume.csv")
        df['date_time'] = pd.to_datetime(df['date_time'], format='%d-%m-%Y %H:%M')
        years = range(df['date_time'].dt.year.min(), df['date_time'].dt.year.max() + 1)
        us_holidays = holidays.US(years=years)  # type: ignore[attr-defined]

        df['holiday'] = (
            df['date_time'].dt.date
        .apply(lambda d: us_holidays.get(d, 'None'))
        .str.replace(r' \(observed\)$', '', regex=True)
        )
        df['is_holiday'] = df['holiday'] != 'None'
        df['year'] = df['date_time'].dt.year
        df['month'] = df['date_time'].dt.month
        df['day'] = df['date_time'].dt.day
        df['hour'] = df['date_time'].dt.hour
        df['day_of_week'] = df['date_time'].dt.dayofweek
        df['is_weekend'] = df['day_of_week'] > 4
        df['temp'] = df['temp'].where(df['temp'] != 0)
        df['temp_f'] = ((df['temp'] -273.15) * 1.8 + 32).round(2)
        df = df.drop(columns=['temp'])

        join_unique = lambda x: ','.join(sorted(x.dropna().unique()))
        agg_dict = {col: 'first' for col in df.columns if col != 'date_time'}
        agg_dict['weather_main'] = join_unique
        agg_dict['weather_description'] = join_unique
        df = df.groupby('date_time').agg(agg_dict).reset_index()
        return df
    @classmethod
    def get_data(cls) -> pd.DataFrame:
        """Returns dataframe"""
        if cls.df is None:
            cls.df = cls().load()
        return cls.df
