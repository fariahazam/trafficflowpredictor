import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd

class ChartBuilder:
    GROUPS = {'hour': 'Hour of day', 'day_of_week': 'Day of week',
              'month': 'Month', 'year': 'Year'}

    def build(self, df: pd.DataFrame, group_by: str = 'hour', title: str = '') -> matplotlib.figure.Figure:
        fig, ax = plt.subplots(figsize=(9, 5))
        if df.empty:
            ax.text(0.5, 0.5, 'No data matches these filters',
                    ha='center', va='center')
            ax.axis('off')
            return fig
        avg = df.groupby(group_by)['traffic_volume'].mean()
        ax.plot(avg.index, avg.values, marker='o')
        ax.set_xlabel(self.GROUPS[group_by])
        ax.set_ylabel('Average traffic volume (vehicles/hr)')
        ax.set_title(title)
        ax.grid(alpha=0.3)
        fig.tight_layout()
        return fig