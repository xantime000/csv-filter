import csv
from tabulate import tabulate
import argparse

def parse_condition(condition: str):
    for op in ['>=', '<=', '>', '<', '=']:
        if op in condition:
            col, val = condition.split(op)
            return col.strip(), op, val.strip()
    raise ValueError("Фильтр принимает только >=, <=, >, <, =")

def apply_filter(rows, column, operator, value):
    result = []
    for row in rows:
        cell = row[column]
        try:
            cell = float(cell)
            value = float(value)
        except ValueError:
            pass

        if operator == '=' and cell == value:
            result.append(row)
        elif operator == '>' and cell > value:
            result.append(row)
        elif operator == '<' and cell < value:
            result.append(row)
        elif operator == '>=' and cell >= value:
            result.append(row)
        elif operator == '<=' and cell <= value:
            result.append(row)
    return result

def parse_aggregate(aggregate: str):
    if '=' not in aggregate:
        raise ValueError("Агрегация должна быть в формате column=agg")
    column, agg_type = aggregate.split('=')
    agg_type = agg_type.strip().lower()
    if agg_type not in ['avg', 'min', 'max']:
        raise ValueError("Допустимые агрегации: avg, min, max")
    return column.strip(), agg_type

def apply_aggregation(rows, column, agg_type):
    values = [float(row[column]) for row in rows]
    if not values:
        raise ValueError("Нет значений для агрегации")

    if agg_type == 'avg':
        result = sum(values) / len(values)
    elif agg_type == 'min':
        result = min(values)
    elif agg_type == 'max':
        result = max(values)
    else:
        raise ValueError(f"Неизвестный тип агрегации: {agg_type}")

    return {f'{agg_type}({column})': round(result, 2)}

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', required=True)
    parser.add_argument('--where')
    parser.add_argument('--aggregate')
    args = parser.parse_args()

    with open(args.file, newline='', encoding='utf-8') as csvfile:
        read = csv.DictReader(csvfile)
        rows = list(read)

    if args.where:
        column, operator, value = parse_condition(args.where)
        rows = apply_filter(rows, column, operator, value)

    if args.aggregate:
        column, agg_type = parse_aggregate(args.aggregate)
        result = apply_aggregation(rows, column, agg_type)
        print(tabulate([result], headers="keys"))
    else:
        print(tabulate(rows, headers="keys"))




