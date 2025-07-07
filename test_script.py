import pytest
from csvscript import parse_condition, apply_filter, parse_aggregate, apply_aggregation

def test_parse_condition_basic():
    assert parse_condition("price>500") == ("price", ">", "500")
    assert parse_condition(" brand = samsung ") == ("brand", "=", "samsung")
    assert parse_condition("rating<=4.8") == ("rating", "<=", "4.8")

def test_parse_condition_invalid():
    with pytest.raises(ValueError):
        parse_condition("price@500")

rows = [
    {'name': 'iphone', 'brand': 'apple', 'price': '999', 'rating': '4.9'},
    {'name': 'galaxy', 'brand': 'samsung', 'price': '1199', 'rating': '4.8'},
    {'name': 'redmi', 'brand': 'xiaomi', 'price': '199', 'rating': '4.6'},
    {'name': 'poco', 'brand': 'xiaomi', 'price': '299', 'rating': '4.4'},
]

def test_filter_price_gt():
    result = apply_filter(rows, "price", ">", "500")
    assert len(result) == 2
    assert result[0]['name'] == 'iphone'
    assert result[1]['name'] == 'galaxy'

def test_filter_brand_eq():
    result = apply_filter(rows, "brand", "=", "xiaomi")
    assert len(result) == 2
    assert result[0]['name'] == 'redmi'
    assert result[1]['name'] == 'poco'

def test_parse_aggregate_ok():
    assert parse_aggregate("price=avg") == ("price", "avg")

def test_parse_aggregate_invalid():
    with pytest.raises(ValueError):
        parse_aggregate("price@avg")
    with pytest.raises(ValueError):
        parse_aggregate("price=total")

def test_aggregate_avg():
    result = apply_aggregation(rows, "price", "avg")
    assert result == {"avg(price)": 674.0}

def test_aggregate_min():
    result = apply_aggregation(rows, "price", "min")
    assert result == {"min(price)": 199.0}

def test_aggregate_max():
    result = apply_aggregation(rows, "price", "max")
    assert result == {"max(price)": 1199.0}
