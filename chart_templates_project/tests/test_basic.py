#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
图表模板基本测试

测试图表模板的基本功能是否正常工作。
"""

import sys
import os
import unittest

# 添加父目录到路径，以便导入模板
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.chart_template_functions import ChartTemplates

class TestChartTemplates(unittest.TestCase):
    """测试图表模板类"""

    def setUp(self):
        """测试前准备"""
        self.templates = ChartTemplates()

    def test_initialization(self):
        """测试初始化"""
        self.assertIsNotNone(self.templates)
        self.assertIsNotNone(self.templates.templates)
        self.assertIn('heatmap', self.templates.templates)
        self.assertIn('line_chart', self.templates.templates)

    def test_create_heatmap(self):
        """测试创建热力图"""
        import numpy as np
        data = np.random.rand(5, 5)

        plt = self.templates.create_heatmap(
            data=data,
            title='测试热力图',
            xlabel='X轴',
            ylabel='Y轴'
        )

        self.assertIsNotNone(plt)
        plt.close()

    def test_create_line_chart(self):
        """测试创建折线图"""
        x_data = [1, 2, 3, 4, 5]
        y_data_list = [[1, 2, 3, 4, 5], [5, 4, 3, 2, 1]]
        labels = ['系列A', '系列B']

        plt = self.templates.create_line_chart(
            x_data=x_data,
            y_data_list=y_data_list,
            labels=labels,
            title='测试折线图'
        )

        self.assertIsNotNone(plt)
        plt.close()

    def test_create_bar_chart(self):
        """测试创建柱状图"""
        categories = ['A', 'B', 'C', 'D']
        values = [10, 20, 15, 25]

        plt = self.templates.create_bar_chart(
            categories=categories,
            values=values,
            title='测试柱状图'
        )

        self.assertIsNotNone(plt)
        plt.close()

    def test_create_pie_chart(self):
        """测试创建饼图"""
        labels = ['部分A', '部分B', '部分C']
        sizes = [30, 40, 30]

        plt = self.templates.create_pie_chart(
            labels=labels,
            sizes=sizes,
            title='测试饼图'
        )

        self.assertIsNotNone(plt)
        plt.close()

    def test_method_count(self):
        """测试模板方法数量"""
        # 获取所有以create_开头的方法
        import inspect
        methods = inspect.getmembers(self.templates, predicate=inspect.ismethod)
        create_methods = [name for name, method in methods if name.startswith('create_')]

        # 应该有16个create方法（14个图表创建方法 + 2个创建图表并分析的方法）
        self.assertEqual(len(create_methods), 16)

    def test_template_config(self):
        """测试模板配置完整性"""
        required_keys = ['description', 'recommended_size', 'aspect_ratio',
                        'color_palette', 'best_for', 'code_snippet', 'example_use_case']

        for template_name, config in self.templates.templates.items():
            for key in required_keys:
                self.assertIn(key, config, f"模板 {template_name} 缺少配置项 {key}")

def run_tests():
    """运行测试"""
    # 创建测试套件
    suite = unittest.TestLoader().loadTestsFromTestCase(TestChartTemplates)

    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    return result.wasSuccessful()

if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)