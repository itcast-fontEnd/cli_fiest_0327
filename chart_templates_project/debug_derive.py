#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
调试衍生字段计算
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from data_processor import DataProcessor

# 创建测试数据
test_data = [
    {'product': 'A', 'revenue': 1000, 'cost': 600, 'customers': 50, 'transactions': 25, 'area': 100},
    {'product': 'B', 'revenue': 1500, 'cost': 800, 'customers': 60, 'transactions': 30, 'area': 120},
]

print("测试数据:", test_data)

# 创建处理器
processor = DataProcessor()

# 测试衍生字段
print("\n1. 测试超市场景衍生字段:")
derived_data = processor.derive_fields(test_data, scenario='supermarket')
print("衍生后的数据:")
for row in derived_data:
    print(row)

# 测试公式求值
print("\n2. 测试公式求值:")
row = test_data[0]
formula = 'revenue - cost'
print(f"公式: {formula}")
print(f"revenue: {row['revenue']}, cost: {row['cost']}")

# 测试基础公式求值
result = processor._evaluate_formula_basic(row, formula)
print(f"_evaluate_formula_basic 结果: {result}")

# 测试更复杂的公式
print("\n3. 测试复杂公式:")
formula2 = '(revenue - cost) / revenue * 100 if revenue > 0 else 0'
print(f"公式: {formula2}")
result2 = processor._evaluate_formula_basic(row, formula2)
print(f"_evaluate_formula_basic 结果: {result2}")

# 如果有pandas，测试pandas版本
if processor.pandas_available:
    print("\n4. 测试pandas版本:")
    import pandas as pd
    df = pd.DataFrame(test_data)

    # 测试简单公式
    result_pd = processor._evaluate_formula_pandas(df, formula)
    print(f"_evaluate_formula_pandas '{formula}' 结果:")
    print(result_pd)

    # 测试复杂公式
    result_pd2 = processor._evaluate_formula_pandas(df, formula2)
    print(f"\n_evaluate_formula_pandas '{formula2}' 结果:")
    print(result_pd2)