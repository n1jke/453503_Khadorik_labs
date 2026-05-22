"""Matplotlib chart generation tests."""

import os

import pytest
from django.conf import settings

from agency.charts import (
    generate_deals_by_type_chart,
    generate_property_types_chart,
)


@pytest.mark.django_db
def test_generate_deals_chart(deal):
    path = generate_deals_by_type_chart()
    full = os.path.join(settings.MEDIA_ROOT, path)
    assert os.path.isfile(full)
    assert path.startswith('charts/')


@pytest.mark.django_db
def test_generate_types_chart(real_estate):
    path = generate_property_types_chart()
    assert os.path.isfile(os.path.join(settings.MEDIA_ROOT, path))
