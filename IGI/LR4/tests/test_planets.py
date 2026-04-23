"""planets package tests"""

import pandas as pd
from planets.models import PlanetsDfProcessor


def test_mass_filter():
    data = {
        'PlanetaryMassJpt': [0.5, 0.3, 0.1, 0.2, 1, 2, 3, 4]
    }

    filtered = PlanetsDfProcessor.filter_by_mass(pd.DataFrame(data))

    assert len(filtered) == 3


def test_period_ratio():
    data = {
        'PeriodDays': [40, 102, 0.17, 4, 6],
        'RadiusJpt': [None, None, 0.05, 0.114, 0.071]
    }

    ratio = PlanetsDfProcessor.period_ratio(pd.DataFrame(data))

    assert abs(ratio - 23.53) < 0.001
