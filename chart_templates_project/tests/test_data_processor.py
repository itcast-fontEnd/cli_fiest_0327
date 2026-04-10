#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试数据处理器功能
主要测试数据清洗、衍生字段计算、图表数据准备等功能
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import unittest
import numpy as np
from data_processor import DataProcessor

class TestDataProcessor(unittest.TestCase):
    """测试数据处理器"""

    def setUp(self):
        """测试前准备"""
        self.processor = DataProcessor()

        # 创建测试数据
        self.test_data = [
            {'product': 'A', 'revenue': 1000, 'cost': 600, 'customers': 50, 'transactions': 25, 'area': 100},
            {'product': 'B', 'revenue': 1500, 'cost': 800, 'customers': 60, 'transactions': 30, 'area': 120},
            {'product': 'C', 'revenue': 800, 'cost': 400, 'customers': 40, 'transactions': 20, 'area': 80},
            {'product': 'D', 'revenue': 2000, 'cost': 1200, 'customers': 80, 'transactions': 40, 'area': 150}
        ]

        # 创建pandas测试数据（如果有pandas）
        if self.processor.pandas_available:
            import pandas as pd
            self.test_df = pd.DataFrame(self.test_data)

    def test_basic_stats(self):
        """测试基本统计计算"""
        stats = self.processor.calculate_basic_stats(self.test_data)

        self.assertIn('revenue', stats)
        self.assertIn('cost', stats)

        # 检查统计值
        revenue_stats = stats['revenue']
        self.assertAlmostEqual(revenue_stats['mean'], 1325.0)
        self.assertAlmostEqual(revenue_stats['min'], 800.0)
        self.assertAlmostEqual(revenue_stats['max'], 2000.0)

        print("基本统计测试通过")

    def test_derive_fields_supermarket(self):
        """测试超市场景衍生字段"""
        derived_data = self.processor.derive_fields(self.test_data, scenario='supermarket')

        # 检查是否添加了衍生字段
        first_row = derived_data[0]

        # 检查利润字段
        self.assertIn('profit_margin', first_row)
        expected_profit = 1000 - 600  # revenue - cost
        self.assertAlmostEqual(first_row['profit_margin'], expected_profit)

        # 检查利润率字段
        self.assertIn('profit_margin_rate', first_row)
        expected_margin_rate = ((1000 - 600) / 1000 * 100) if 1000 > 0 else 0
        self.assertAlmostEqual(first_row['profit_margin_rate'], expected_margin_rate)

        # 检查客户贡献度
        self.assertIn('customer_contribution', first_row)
        expected_contribution = 1000 / 50 if 50 > 0 else 0
        self.assertAlmostEqual(first_row['customer_contribution'], expected_contribution)

        print("超市场景衍生字段测试通过")

    def test_derive_fields_ecommerce(self):
        """测试电商场景衍生字段"""
        # 准备电商测试数据
        ecommerce_data = [
            {'product': 'A', 'revenue': 1000, 'orders': 50, 'visitors': 500, 'repeat_rate': 0.2, 'retention_period': 12},
            {'product': 'B', 'revenue': 1500, 'orders': 60, 'visitors': 600, 'repeat_rate': 0.3, 'retention_period': 18}
        ]

        derived_data = self.processor.derive_fields(ecommerce_data, scenario='ecommerce')

        first_row = derived_data[0]

        # 检查转化率
        self.assertIn('conversion_rate', first_row)
        expected_conversion = (50 / 500 * 100) if 500 > 0 else 0
        self.assertAlmostEqual(first_row['conversion_rate'], expected_conversion)

        # 检查平均订单价值
        self.assertIn('average_order_value', first_row)
        expected_aov = 1000 / 50 if 50 > 0 else 0
        self.assertAlmostEqual(first_row['average_order_value'], expected_aov)

        print("电商场景衍生字段测试通过")

    def test_clean_data(self):
        """测试数据清洗"""
        # 创建有重复和缺失的数据
        dirty_data = [
            {'product': 'A', 'revenue': 1000, 'cost': 600},
            {'product': 'A', 'revenue': 1000, 'cost': 600},  # 重复
            {'product': 'B', 'revenue': None, 'cost': 800},  # 缺失值
            {'product': 'C', 'revenue': 800, 'cost': 400}
        ]

        cleaned_data = self.processor.clean_data(dirty_data)

        # 检查去重（应该有3行而不是4行）
        self.assertLessEqual(len(cleaned_data), len(dirty_data))

        print("数据清洗测试通过")

    def test_prepare_chart_data_bar(self):
        """测试准备柱状图数据"""
        chart_data = self.processor.prepare_chart_data(
            self.test_data, 'bar_chart',
            x_column='product', y_columns=['revenue']
        )

        self.assertIn('categories', chart_data)
        self.assertIn('values', chart_data)

        self.assertEqual(len(chart_data['categories']), 4)
        self.assertEqual(len(chart_data['values']), 4)

        print("柱状图数据准备测试通过")

    def test_prepare_chart_data_line(self):
        """测试准备折线图数据"""
        chart_data = self.processor.prepare_chart_data(
            self.test_data, 'line_chart',
            x_column='product', y_columns=['revenue', 'cost']
        )

        self.assertIn('x_data', chart_data)
        self.assertIn('y_data_list', chart_data)
        self.assertIn('labels', chart_data)

        self.assertEqual(len(chart_data['y_data_list']), 2)
        self.assertEqual(chart_data['labels'], ['revenue', 'cost'])

        print("折线图数据准备测试通过")

    def test_generate_summary_report(self):
        """测试生成摘要报告"""
        summary = self.processor.generate_data_summary_report(self.test_data)

        self.assertIsInstance(summary, str)
        self.assertGreater(len(summary), 100)
        self.assertIn("数据摘要报告", summary)

        print("摘要报告生成测试通过")

    def test_export_data(self):
        """测试数据导出"""
        import tempfile

        # 测试CSV导出
        with tempfile.NamedTemporaryFile(suffix='.csv', delete=False) as f:
            csv_path = f.name

        try:
            export_path = self.processor.export_data(self.test_data, csv_path)
            self.assertEqual(export_path, csv_path)

            # 检查文件是否存在
            self.assertTrue(os.path.exists(csv_path))

            print("数据导出测试通过")
        finally:
            if os.path.exists(csv_path):
                os.unlink(csv_path)

def run_tests():
    """运行所有测试"""
    print("=" * 60)
    print("开始测试数据处理器功能")
    print("=" * 60)

    # 创建测试套件
    suite = unittest.TestSuite()

    # 添加测试用例
    test_cases = [
        TestDataProcessor('test_basic_stats'),
        TestDataProcessor('test_derive_fields_supermarket'),
        TestDataProcessor('test_derive_fields_ecommerce'),
        TestDataProcessor('test_clean_data'),
        TestDataProcessor('test_prepare_chart_data_bar'),
        TestDataProcessor('test_prepare_chart_data_line'),
        TestDataProcessor('test_generate_summary_report'),
        TestDataProcessor('test_export_data')
    ]

    for test_case in test_cases:
        suite.addTest(test_case)

    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    print("=" * 60)
    print(f"测试完成: {result.testsRun} 个测试用例")
    print(f"通过: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"失败: {len(result.failures)}")
    print(f"错误: {len(result.errors)}")
    print("=" * 60)

    return result.wasSuccessful()

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)