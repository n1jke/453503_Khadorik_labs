"""models"""

import pandas as pd


class PlanetsDfProcessor():
    """planets dataframe processor"""

    @staticmethod
    def filter_by_mass(df: pd.DataFrame) -> pd.DataFrame:
        """filter dataframe by planetary mass greater than Earth mass"""
        mass_series = df['PlanetaryMassJpt']
        return df[mass_series > 1].reset_index(drop=True)

    @staticmethod
    def period_ratio(df: pd.DataFrame) -> float:
        """ratio of the average period of planets of maximum size and minimum size"""
        period = df['PeriodDays']
        df_copy = df[period.notna()].copy()
        radius = df_copy['RadiusJpt']
        max_mean = df_copy[radius == radius.max()]['PeriodDays'].mean()
        min_mean = df_copy[radius == radius.min()]['PeriodDays'].mean()
        return round(max_mean / min_mean, 2)
