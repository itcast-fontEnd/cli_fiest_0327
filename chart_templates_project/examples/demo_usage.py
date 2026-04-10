#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
图表模板使用演示脚本

这个脚本演示如何使用本项目提供的图表模板系统生成各种类型的图表。
所有生成的图表将保存到 examples/images/ 目录下。

使用方法:
    python demo_usage.py
"""

import os
import sys
import numpy as np
import pandas as pd

# 添加父目录到路径，以便导入模板
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.chart_template_functions import ChartTemplates

def ensure_directory(path):
    """确保目录存在"""
    os.makedirs(path, exist_ok=True)

def create_sample_data():
    """创建示例数据"""
    np.random.seed(42)

    # 折线图数据
    months = ['1月', '2月', '3月', '4月', '5月', '6月']
    product_a = [120 + i*10 + np.random.randint(-5, 5) for i in range(6)]
    product_b = [85 + i*8 + np.random.randint(-8, 8) for i in range(6)]
    product_c = [150 - i*5 + np.random.randint(-10, 10) for i in range(6)]

    # 柱状图数据
    categories = ['北京', '上海', '广州', '深圳', '杭州']
    sales_values = [120, 95, 85, 110, 75]

    # 饼图数据
    pie_labels = ['电子产品', '服装', '食品', '家居', '图书']
    pie_sizes = [35, 25, 20, 15, 5]

    # 散点图数据
    n_points = 50
    scatter_x = np.random.normal(100, 20, n_points)
    scatter_y = scatter_x * 0.7 + np.random.normal(0, 15, n_points)

    # 热力图数据
    heatmap_data = np.random.rand(10, 12) * 100

    return {
        'months': months,
        'product_a': product_a,
        'product_b': product_b,
        'product_c': product_c,
        'categories': categories,
        'sales_values': sales_values,
        'pie_labels': pie_labels,
        'pie_sizes': pie_sizes,
        'scatter_x': scatter_x,
        'scatter_y': scatter_y,
        'heatmap_data': heatmap_data
    }

def demo_basic_charts(templates, data, output_dir):
    """演示基础图表"""
    print("正在生成基础图表...")

    # 1. 折线图
    plt = templates.create_line_chart(
        x_data=data['months'],
        y_data_list=[data['product_a'], data['product_b'], data['product_c']],
        labels=['产品A', '产品B', '产品C'],
        title='各产品月度销售趋势',
        xlabel='月份',
        ylabel='销售额（万元）'
    )
    plt.savefig(os.path.join(output_dir, 'demo_line_chart.png'), dpi=300, bbox_inches='tight')
    plt.close()
    print("  ✓ 折线图已生成: demo_line_chart.png")

    # 2. 柱状图
    plt = templates.create_bar_chart(
        categories=data['categories'],
        values=data['sales_values'],
        title='各城市销售额对比',
        xlabel='城市',
        ylabel='销售额（万元）'
    )
    plt.savefig(os.path.join(output_dir, 'demo_bar_chart.png'), dpi=300, bbox_inches='tight')
    plt.close()
    print("  ✓ 柱状图已生成: demo_bar_chart.png")

    # 3. 饼图
    plt = templates.create_pie_chart(
        labels=data['pie_labels'],
        sizes=data['pie_sizes'],
        title='产品类别销售占比'
    )
    plt.savefig(os.path.join(output_dir, 'demo_pie_chart.png'), dpi=300, bbox_inches='tight')
    plt.close()
    print("  ✓ 饼图已生成: demo_pie_chart.png")

    # 4. 散点图
    plt = templates.create_scatter_plot(
        x_data=data['scatter_x'],
        y_data=data['scatter_y'],
        title='销售额与利润关系',
        xlabel='销售额（万元）',
        ylabel='利润（万元）'
    )
    plt.savefig(os.path.join(output_dir, 'demo_scatter_plot.png'), dpi=300, bbox_inches='tight')
    plt.close()
    print("  ✓ 散点图已生成: demo_scatter_plot.png")

    # 5. 热力图
    plt = templates.create_heatmap(
        data=pd.DataFrame(data['heatmap_data']),
        title='区域销售热力图',
        xlabel='月份',
        ylabel='区域',
        cmap='YlOrRd'
    )
    plt.savefig(os.path.join(output_dir, 'demo_heatmap.png'), dpi=300, bbox_inches='tight')
    plt.close()
    print("  ✓ 热力图已生成: demo_heatmap.png")

def demo_advanced_charts(templates, data, output_dir):
    """演示高级图表"""
    print("\n正在生成高级图表...")

    # 1. 多列条形图
    data_dict = {
        '第一季度': [30, 25, 35, 28, 32],
        '第二季度': [35, 30, 40, 32, 38],
        '第三季度': [40, 35, 45, 38, 42]
    }

    plt = templates.create_multi_column_bar(
        categories=data['categories'],
        data_dict=data_dict,
        title='各城市季度销售额对比',
        xlabel='城市',
        ylabel='销售额（万元）'
    )
    plt.savefig(os.path.join(output_dir, 'demo_multi_column_bar.png'), dpi=300, bbox_inches='tight')
    plt.close()
    print("  ✓ 多列条形图已生成: demo_multi_column_bar.png")

    # 2. 分层柱形图
    data_layers = [
        [10, 15, 20, 25, 30],  # 线上销售
        [15, 20, 15, 10, 20],  # 线下销售
        [5, 10, 5, 15, 10]     # 批发销售
    ]
    layer_names = ['线上销售', '线下销售', '批发销售']

    plt = templates.create_stacked_bar(
        categories=data['categories'],
        data_layers=data_layers,
        layer_names=layer_names,
        title='各城市销售渠道构成',
        xlabel='城市',
        ylabel='销售额（万元）'
    )
    plt.savefig(os.path.join(output_dir, 'demo_stacked_bar.png'), dpi=300, bbox_inches='tight')
    plt.close()
    print("  ✓ 分层柱形图已生成: demo_stacked_bar.png")

    # 3. 蝴蝶图
    left_values = [120, 85, 150, 95, 110]    # 男性用户
    right_values = [95, 105, 120, 85, 100]   # 女性用户

    plt = templates.create_butterfly_chart(
        categories=data['categories'],
        left_values=left_values,
        right_values=right_values,
        left_label='男性用户',
        right_label='女性用户',
        title='各产品用户性别分布对比'
    )
    plt.savefig(os.path.join(output_dir, 'demo_butterfly_chart.png'), dpi=300, bbox_inches='tight')
    plt.close()
    print("  ✓ 蝴蝶图已生成: demo_butterfly_chart.png")

    # 4. 帕累托图
    problem_categories = ['质量问题A', '质量问题B', '质量问题C', '质量问题D', '质量问题E']
    problem_values = [45, 32, 28, 22, 15]

    plt = templates.create_pareto_chart(
        categories=problem_categories,
        values=problem_values,
        title='质量问题帕累托分析',
        xlabel='问题类型',
        ylabel='发生频次'
    )
    plt.savefig(os.path.join(output_dir, 'demo_pareto_chart.png'), dpi=300, bbox_inches='tight')
    plt.close()
    print("  ✓ 帕累托图已生成: demo_pareto_chart.png")

    # 5. 气泡图
    n_bubbles = 20
    bubble_x = np.random.uniform(50, 150, n_bubbles)
    bubble_y = np.random.uniform(20, 80, n_bubbles)
    bubble_sizes = np.random.uniform(100, 1000, n_bubbles)
    bubble_colors = np.random.uniform(0, 100, n_bubbles)

    plt = templates.create_bubble_chart(
        x_data=bubble_x,
        y_data=bubble_y,
        sizes=bubble_sizes,
        colors=bubble_colors,
        title='产品多维度分析气泡图',
        xlabel='销售额（万元）',
        ylabel='利润率（%）',
        size_label='市场份额'
    )
    plt.savefig(os.path.join(output_dir, 'demo_bubble_chart.png'), dpi=300, bbox_inches='tight')
    plt.close()
    print("  ✓ 气泡图已生成: demo_bubble_chart.png")

    # 6. 条形折线组合图
    bar_values = [120, 95, 85, 110, 75]      # 销售额
    line_values = [0.15, 0.18, 0.12, 0.16, 0.14]  # 增长率

    plt = templates.create_bar_line_combo(
        categories=data['categories'],
        bar_values=bar_values,
        line_values=line_values,
        bar_label='销售额（万元）',
        line_label='增长率',
        title='各城市销售额与增长率对比'
    )
    plt.savefig(os.path.join(output_dir, 'demo_bar_line_combo.png'), dpi=300, bbox_inches='tight')
    plt.close()
    print("  ✓ 条形折线组合图已生成: demo_bar_line_combo.png")

def demo_new_charts(templates, data, output_dir):
    """演示新添加的图表类型"""
    print("\n正在生成新图表类型...")

    # 1. 瀑布图
    waterfall_categories = ['起始', '新增', '减少', '调整', '最终']
    waterfall_values = [100, 50, -30, 20, 140]  # 最后一个值应该是累积值或0，但这里我们将使用原始变化值

    plt = templates.create_waterfall_chart(
        categories=waterfall_categories,
        values=waterfall_values,
        title='项目预算变化瀑布图',
        xlabel='阶段',
        ylabel='预算（万元）'
    )
    plt.savefig(os.path.join(output_dir, 'demo_waterfall_chart.png'), dpi=300, bbox_inches='tight')
    plt.close()
    print("  ✓ 瀑布图已生成: demo_waterfall_chart.png")

    # 2. 气泡条形图
    bubble_bar_categories = ['产品A', '产品B', '产品C', '产品D', '产品E']
    bar_values = [120, 95, 85, 110, 75]      # 条形图高度（销售额）
    bubble_sizes = [500, 300, 400, 600, 200] # 气泡大小（市场份额）

    plt = templates.create_bubble_bar_chart(
        categories=bubble_bar_categories,
        bar_values=bar_values,
        bubble_sizes=bubble_sizes,
        title='产品销售额与市场份额气泡条形图',
        xlabel='产品',
        ylabel='销售额（万元）',
        size_label='市场份额'
    )
    plt.savefig(os.path.join(output_dir, 'demo_bubble_bar_chart.png'), dpi=300, bbox_inches='tight')
    plt.close()
    print("  ✓ 气泡条形图已生成: demo_bubble_bar_chart.png")

    # 3. 增强型气泡图（气泡图2）
    n_enhanced = 15
    enhanced_x = np.random.uniform(50, 150, n_enhanced)      # 销售额
    enhanced_y = np.random.uniform(10, 30, n_enhanced)       # 利润率
    enhanced_sizes = np.random.uniform(100, 500, n_enhanced) # 市场份额
    enhanced_colors = np.random.uniform(0, 100, n_enhanced)  # 增长率

    plt = templates.create_bubble_chart_2(
        x_data=enhanced_x,
        y_data=enhanced_y,
        sizes=enhanced_sizes,
        colors=enhanced_colors,
        title='产品四维数据分析增强型气泡图',
        xlabel='销售额（万元）',
        ylabel='利润率（%）',
        size_label='市场份额',
        color_label='增长率（%）'
    )
    plt.savefig(os.path.join(output_dir, 'demo_bubble_chart_2.png'), dpi=300, bbox_inches='tight')
    plt.close()
    print("  ✓ 增强型气泡图已生成: demo_bubble_chart_2.png")

def main():
    """主函数"""
    print("=" * 60)
    print("图表模板演示脚本")
    print("=" * 60)

    # 设置输出目录
    output_dir = os.path.join(os.path.dirname(__file__), 'images')
    ensure_directory(output_dir)

    # 创建示例数据
    data = create_sample_data()

    # 初始化模板
    try:
        templates = ChartTemplates()
        print("✓ 图表模板初始化成功")
    except Exception as e:
        print(f"✗ 图表模板初始化失败: {e}")
        print("请确保 config/chart_templates.json 文件存在")
        return

    # 演示基础图表
    demo_basic_charts(templates, data, output_dir)

    # 演示高级图表
    demo_advanced_charts(templates, data, output_dir)

    # 演示新图表类型
    demo_new_charts(templates, data, output_dir)

    print("\n" + "=" * 60)
    print("演示完成！")
    print(f"所有图表已保存到: {output_dir}")
    print("=" * 60)

    # 生成文件清单
    generated_files = []
    for file in os.listdir(output_dir):
        if file.startswith('demo_') and file.endswith('.png'):
            generated_files.append(file)

    print(f"共生成 {len(generated_files)} 个演示图表:")
    for i, file in enumerate(sorted(generated_files), 1):
        print(f"  {i:2d}. {file}")

    print("\n使用说明:")
    print("1. 查看生成的图表文件了解模板效果")
    print("2. 参考 src/chart_template_functions.py 了解所有可用函数")
    print("3. 参考 reports/data_analysis_report_template.md 学习如何在分析报告中使用")

if __name__ == "__main__":
    main()