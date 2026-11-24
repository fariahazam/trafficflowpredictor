import calendar
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd

matplotlib.use('Agg')

def hour_label(h: int) -> str:
    """Convert a 24-hour value to a 12-hour label"""
    suffix = 'AM' if h < 12 else 'PM'
    return f"{(h % 12) or 12} {suffix}"

class ChartBuilder:
    """Builds a line chart of average traffic volume"""
    GROUPS = {'hour': 'Hour of day', 'day_of_week': 'Day of week',
              'month': 'Month', 'year': 'Year'}  
    TICK_LABELS = {
        'hour': hour_label,
        'day_of_week': lambda d: calendar.day_abbr[d],
        'month': lambda m: calendar.month_abbr[m],   
        'year': str,
    }

    def build(self, df: pd.DataFrame,
              group_by: str = 'hour', title: str = '') -> matplotlib.figure.Figure:
        """Average traffic volume by the chosen group gets plotted, 
        or return a 'No data' figure if df is empty"""
        fig, ax = plt.subplots(figsize=(9, 5))
        if df.empty:
            ax.text(0.5, 0.5, 'No data matches these filters',
                    ha='center', va='center')
            ax.axis('off')
            return fig
        avg = df.groupby(group_by)['traffic_volume'].mean()
        ax.plot(avg.index, avg.values, marker='o')
        ticks = [int(t) for t in avg.index]
        ax.set_xticks(ticks)
        ax.set_xticklabels(
            [self.TICK_LABELS[group_by](t) for t in ticks],
            rotation=45 if group_by == 'hour' else 0,
            ha='right' if group_by == 'hour' else 'center')
        ax.set_xlabel(self.GROUPS[group_by])
        ax.set_ylabel('Average traffic volume (vehicles/hr)')
        ax.set_title(title)
        ax.grid(alpha=0.3)
        fig.tight_layout()
        return fig
   