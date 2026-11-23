from dataclasses import dataclass, field
import pandas as pd

NO_HOLIDAYS = '__none__'
ALL_HOLIDAYS = '__all__'

@dataclass
class TrafficFilter:
    day_type: str = 'both'            # 'weekday' | 'weekend' | 'both'
    weather: list = field(default_factory=list)   # e.g. ['Rain', 'Snow']
    temp_min_f: float | None = None
    temp_max_f: float | None = None
    holiday_mode: str = field(default_factory=list)
    years: list = field(default_factory=list)
    months: list = field(default_factory=list)

    def apply(self, df: pd.DataFrame) -> pd.DataFrame:
        if self.day_type == 'weekend':
            df = df[df['is_weekend']]
        elif self.day_type == 'weekday':
            df = df[~df['is_weekend']]

        if self.weather:
            pattern = '|'.join(self.weather)
            df = df[df['weather_main'].str.contains(pattern, na=False)]

        if self.temp_min_f is not None:
            df = df[df['temp_f'] >= self.temp_min_f]
        if self.temp_max_f is not None:
            df = df[df['temp_f'] <= self.temp_max_f]

        if self.holidays:
            mask = pd.Series(False, index=df.index)
            if NO_HOLIDAYS in self.holidays:
                mask |= ~df['is_holiday']
            if ALL_HOLIDAYS in self.holidays:
                mask |= df['is_holiday']
            names = [h for h in self.holidays if h not in (NO_HOLIDAYS, ALL_HOLIDAYS)]
            if names:
                mask |= df['holiday'].isin(names)
            df = df[mask]

        if self.years:
            df = df[df['year'].isin(self.years)]
        if self.months:
            df = df[df['month'].isin(self.months)]
        return df