
# 根据chart_templates.json创建的通用图表函数
import json
import os
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# 设置中文字体支持
import matplotlib
matplotlib.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']
matplotlib.rcParams['axes.unicode_minus'] = False

class ChartTemplates:
    def __init__(self, config_path=None):
        # 如果未提供配置路径，使用基于模块位置的默认路径
        if config_path is None:
            # 获取当前文件所在目录（src目录）
            current_dir = os.path.dirname(os.path.abspath(__file__))
            # 构建默认配置文件路径：../config/chart_templates.json
            config_path = os.path.join(current_dir, '..', 'config', 'chart_templates.json')
            config_path = os.path.normpath(config_path)

        # 确保配置文件存在
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"配置文件未找到: {config_path}")

        with open(config_path, 'r', encoding='utf-8') as f:
            self.templates = json.load(f)

    def create_heatmap(self, data, title='热力图', xlabel='X轴', ylabel='Y轴',
                      cmap='YlOrRd', figsize=(10, 7), **kwargs):
        """创建热力图"""
        plt.figure(figsize=figsize)
        sns.heatmap(data, cmap=cmap, linewidths=0.5,
                   cbar_kws={'label': '数值'}, **kwargs)
        plt.title(title, fontsize=14)
        plt.xlabel(xlabel, fontsize=12)
        plt.ylabel(ylabel, fontsize=12)
        plt.tight_layout(pad=1.0)
        return plt

    def create_line_chart(self, x_data, y_data_list, labels, title='折线图',
                         xlabel='时间', ylabel='数值', figsize=(9, 6)):
        """创建折线图"""
        plt.figure(figsize=figsize)
        for i, y_data in enumerate(y_data_list):
            plt.plot(x_data, y_data, label=labels[i], linewidth=2, marker='o')
        plt.title(title, fontsize=14)
        plt.xlabel(xlabel, fontsize=12)
        plt.ylabel(ylabel, fontsize=12)
        plt.legend(fontsize=10)
        plt.grid(True, alpha=0.3)
        plt.tight_layout(pad=1.0)
        return plt

    def create_bar_chart(self, categories, values, title='柱状图',
                        xlabel='类别', ylabel='数值', figsize=(8, 5)):
        """创建柱状图"""
        plt.figure(figsize=figsize)
        colors = plt.cm.Set3(np.arange(len(categories)) / len(categories))
        plt.bar(categories, values, color=colors, edgecolor='black')
        plt.title(title, fontsize=14)
        plt.xlabel(xlabel, fontsize=12)
        plt.ylabel(ylabel, fontsize=12)
        plt.xticks(rotation=45, ha='right')
        # 添加数值标签
        for i, v in enumerate(values):
            plt.text(i, v, f'{v:.1f}', ha='center', va='bottom')
        plt.tight_layout(pad=1.0)
        return plt

    def create_pie_chart(self, labels, sizes, title='饼图', figsize=(6, 6)):
        """创建饼图"""
        plt.figure(figsize=figsize)
        colors = plt.cm.Set2(np.arange(len(labels)) / len(labels))
        plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%',
                startangle=90, textprops={'fontsize': 10})
        # 添加中心圆
        centre_circle = plt.Circle((0,0), 0.70, fc='white')
        fig = plt.gcf()
        fig.gca().add_artist(centre_circle)
        plt.title(title, fontsize=14)
        plt.tight_layout(pad=1.0)
        return plt

    def create_scatter_plot(self, x_data, y_data, colors=None, sizes=None,
                           title='散点图', xlabel='X轴', ylabel='Y轴',
                           figsize=(8, 6.4)):
        """创建散点图"""
        plt.figure(figsize=figsize)
        scatter = plt.scatter(x_data, y_data, c=colors, s=sizes,
                            alpha=0.6, cmap='viridis')
        if colors is not None:
            plt.colorbar(scatter, label='颜色值')
        plt.title(title, fontsize=14)
        plt.xlabel(xlabel, fontsize=12)
        plt.ylabel(ylabel, fontsize=12)
        plt.grid(True, alpha=0.3)
        plt.tight_layout(pad=1.0)
        return plt

    def create_multi_column_bar(self, categories, data_dict, title='多列条形图',
                               xlabel='类别', ylabel='数值', figsize=(9, 6)):
        """创建多列条形图"""
        plt.figure(figsize=figsize)
        x = np.arange(len(categories))
        width = 0.8 / len(data_dict)

        for i, (group_name, values) in enumerate(data_dict.items()):
            offset = (i - len(data_dict)/2 + 0.5) * width
            plt.bar(x + offset, values, width, label=group_name,
                   edgecolor='black')

        plt.title(title, fontsize=14)
        plt.xlabel(xlabel, fontsize=12)
        plt.ylabel(ylabel, fontsize=12)
        plt.xticks(x, categories, rotation=45, ha='right')
        plt.legend(fontsize=10)
        plt.tight_layout(pad=1.0)
        return plt

    def create_stacked_bar(self, categories, data_layers, layer_names,
                          title='分层柱形图', xlabel='类别', ylabel='数值',
                          figsize=(9, 6)):
        """创建分层柱形图"""
        plt.figure(figsize=figsize)
        x = np.arange(len(categories))
        bottom = np.zeros(len(categories))

        for i, (layer_name, values) in enumerate(zip(layer_names, data_layers)):
            plt.bar(x, values, bottom=bottom, label=layer_name,
                   edgecolor='black')
            bottom += values

        plt.title(title, fontsize=14)
        plt.xlabel(xlabel, fontsize=12)
        plt.ylabel(ylabel, fontsize=12)
        plt.xticks(x, categories, rotation=45, ha='right')
        plt.legend(fontsize=10, loc='upper left')
        plt.tight_layout(pad=1.0)
        return plt

    def create_butterfly_chart(self, categories, left_values, right_values,
                              left_label='左侧', right_label='右侧',
                              title='蝴蝶图', figsize=(8, 5)):
        """创建蝴蝶图"""
        plt.figure(figsize=figsize)
        y_pos = np.arange(len(categories))

        # 确保输入为NumPy数组
        left_values = np.array(left_values)
        right_values = np.array(right_values)

        plt.barh(y_pos, left_values, color='skyblue', edgecolor='black',
                label=left_label)
        plt.barh(y_pos, -right_values, color='lightcoral', edgecolor='black',
                label=right_label)

        plt.title(title, fontsize=14)
        plt.yticks(y_pos, categories)
        plt.xlabel('数值', fontsize=12)
        plt.legend(fontsize=10)

        # 添加数值标签
        for i, v in enumerate(left_values):
            plt.text(v, i, f'{v:.2f}', ha='left', va='center', fontsize=9)
        for i, v in enumerate(right_values):
            plt.text(-v, i, f'{v:.2f}', ha='right', va='center', fontsize=9)

        plt.tight_layout(pad=1.0)
        return plt

    def create_pareto_chart(self, categories, values, title='帕累托图',
                           xlabel='类别', ylabel='频次', figsize=(9, 6)):
        """创建帕累托图"""
        plt.figure(figsize=figsize)

        # 按值排序
        sorted_indices = np.argsort(values)[::-1]
        sorted_categories = [categories[i] for i in sorted_indices]
        sorted_values = [values[i] for i in sorted_indices]

        # 计算累积百分比
        cumsum = np.cumsum(sorted_values)
        cumsum_percent = cumsum / cumsum[-1] * 100

        # 创建双轴
        fig, ax1 = plt.subplots(figsize=figsize)

        # 柱状图
        bars = ax1.bar(range(len(sorted_categories)), sorted_values,
                      color='skyblue', edgecolor='black', alpha=0.7)
        ax1.set_xlabel(xlabel, fontsize=12)
        ax1.set_ylabel(ylabel, fontsize=12)
        ax1.set_xticks(range(len(sorted_categories)))
        ax1.set_xticklabels(sorted_categories, rotation=45, ha='right')

        # 累积曲线
        ax2 = ax1.twinx()
        ax2.plot(range(len(sorted_categories)), cumsum_percent,
                color='red', marker='o', linewidth=2)
        ax2.set_ylabel('累积百分比 (%)', fontsize=12)
        ax2.set_ylim(0, 110)
        ax2.grid(True, alpha=0.3)

        plt.title(title, fontsize=14)
        plt.tight_layout(pad=1.0)
        return plt

    def create_bubble_chart(self, x_data, y_data, sizes, colors=None,
                           title='气泡图', xlabel='X轴', ylabel='Y轴',
                           size_label='大小', figsize=(9, 6)):
        """创建气泡图"""
        plt.figure(figsize=figsize)

        # 标准化大小用于显示
        scaled_sizes = (sizes - sizes.min()) / (sizes.max() - sizes.min()) * 500 + 50

        scatter = plt.scatter(x_data, y_data, s=scaled_sizes, c=colors,
                             alpha=0.6, cmap='viridis', edgecolors='black')

        if colors is not None:
            plt.colorbar(scatter, label='颜色')

        plt.title(title, fontsize=14)
        plt.xlabel(xlabel, fontsize=12)
        plt.ylabel(ylabel, fontsize=12)
        plt.grid(True, alpha=0.3)

        # 添加图例说明大小
        import matplotlib.patches as mpatches
        size_info = f'大小表示: {size_label}'
        plt.text(0.02, 0.98, size_info, transform=plt.gca().transAxes,
                fontsize=10, verticalalignment='top',
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

        plt.tight_layout(pad=1.0)
        return plt

    def create_bar_line_combo(self, categories, bar_values, line_values,
                             bar_label='数量', line_label='比例',
                             title='条形折线组合图', xlabel='类别', ylabel='数值',
                             figsize=(9, 6)):
        """创建条形折线组合图"""
        fig, ax1 = plt.subplots(figsize=figsize)

        # 柱状图
        bars = ax1.bar(categories, bar_values, color='skyblue',
                      edgecolor='black', alpha=0.7, label=bar_label)
        ax1.set_xlabel(xlabel, fontsize=12)
        ax1.set_ylabel(bar_label, fontsize=12)
        ax1.tick_params(axis='y')
        ax1.set_xticklabels(categories, rotation=45, ha='right')

        # 折线图（第二个y轴）
        ax2 = ax1.twinx()
        line = ax2.plot(categories, line_values, color='red', marker='o',
                       linewidth=2, label=line_label)
        ax2.set_ylabel(line_label, fontsize=12, color='red')
        ax2.tick_params(axis='y', labelcolor='red')

        # 合并图例
        lines1, labels1 = ax1.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax1.legend(lines1 + lines2, labels1 + labels2, fontsize=10)

        plt.title(title, fontsize=14)
        plt.tight_layout(pad=1.0)
        return plt

    def create_waterfall_chart(self, categories, values, title='瀑布图',
                              xlabel='类别', ylabel='数值', figsize=(9, 6)):
        """创建瀑布图"""
        plt.figure(figsize=figsize)

        # 计算累积值
        cumulative = np.zeros(len(categories))
        for i in range(len(categories)):
            cumulative[i] = cumulative[i-1] + values[i] if i > 0 else values[i]

        # 创建条形图
        colors = []
        for val in values:
            if val >= 0:
                colors.append('lightgreen')
            else:
                colors.append('lightcoral')

        plt.bar(categories, values, bottom=np.append(0, cumulative[:-1]),
               color=colors, edgecolor='black')

        # 添加连接线
        for i in range(len(categories)-1):
            plt.plot([i, i+1], [cumulative[i], cumulative[i]],
                    color='gray', linestyle='--', linewidth=1)

        plt.title(title, fontsize=14)
        plt.xlabel(xlabel, fontsize=12)
        plt.ylabel(ylabel, fontsize=12)
        plt.xticks(rotation=45, ha='right')
        plt.grid(True, alpha=0.3)
        plt.tight_layout(pad=1.0)
        return plt

    def create_bubble_bar_chart(self, categories, bar_values, bubble_sizes,
                               colors=None, title='气泡条形图',
                               xlabel='类别', ylabel='数值', size_label='大小',
                               figsize=(9, 6)):
        """创建气泡条形图"""
        plt.figure(figsize=figsize)

        # 创建条形图
        x_pos = np.arange(len(categories))
        bars = plt.bar(x_pos, bar_values, color='skyblue',
                      edgecolor='black', alpha=0.7)

        # 创建气泡图（叠加在条形图上）
        scaled_sizes = (bubble_sizes - bubble_sizes.min()) / (bubble_sizes.max() - bubble_sizes.min()) * 500 + 50

        if colors is None:
            colors = plt.cm.viridis(np.arange(len(categories)) / len(categories))

        scatter = plt.scatter(x_pos, bar_values, s=scaled_sizes, c=colors,
                             alpha=0.8, edgecolors='black')

        plt.title(title, fontsize=14)
        plt.xlabel(xlabel, fontsize=12)
        plt.ylabel(ylabel, fontsize=12)
        plt.xticks(x_pos, categories, rotation=45, ha='right')
        plt.grid(True, alpha=0.3)

        # 添加图例说明
        import matplotlib.patches as mpatches
        size_info = f'气泡大小表示: {size_label}'
        plt.text(0.02, 0.98, size_info, transform=plt.gca().transAxes,
                fontsize=10, verticalalignment='top',
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

        plt.tight_layout(pad=1.0)
        return plt

    def create_bubble_chart_2(self, x_data, y_data, sizes, colors,
                             title='增强型气泡图', xlabel='X轴', ylabel='Y轴',
                             size_label='大小', color_label='颜色', figsize=(9, 6)):
        """创建增强型气泡图（四维数据）"""
        plt.figure(figsize=figsize)

        # 标准化大小用于显示
        scaled_sizes = (sizes - sizes.min()) / (sizes.max() - sizes.min()) * 500 + 50

        # 创建气泡图
        scatter = plt.scatter(x_data, y_data, s=scaled_sizes, c=colors,
                             alpha=0.7, cmap='viridis', edgecolors='black')

        plt.colorbar(scatter, label=color_label)

        plt.title(title, fontsize=14)
        plt.xlabel(xlabel, fontsize=12)
        plt.ylabel(ylabel, fontsize=12)
        plt.grid(True, alpha=0.3)

        # 添加图例说明
        import matplotlib.patches as mpatches
        size_info = f'大小表示: {size_label}, 颜色表示: {color_label}'
        plt.text(0.02, 0.98, size_info, transform=plt.gca().transAxes,
                fontsize=10, verticalalignment='top',
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

        plt.tight_layout(pad=1.0)
        return plt

    def generate_analysis_report(self, charts_info, title, objective,
                                business_context="", analyst="数据分析师",
                                output_format="markdown", output_path=None):
        """生成数据分析报告

        基于已生成的图表，创建包含洞察、结论和建议的专业报告。

        Args:
            charts_info: 图表信息列表，每个元素为字典，包含：
                - type: 图表类型（如 'bar_chart', 'line_chart'）
                - title: 图表标题
                - filepath: 图表文件路径
                - data_context: 数据背景说明
                - additional_context: 额外业务上下文（可选）
            title: 报告标题
            objective: 分析目标
            business_context: 业务上下文描述
            analyst: 分析师姓名
            output_format: 输出格式 ('markdown' 或 'html')
            output_path: 报告保存路径，如为None则返回内容字符串

        Returns:
            如果output_path为None，返回报告内容字符串；否则保存到文件并返回文件路径
        """
        try:
            # 动态导入ReportGenerator避免循环依赖
            from .report_generator import ReportGenerator

            report_gen = ReportGenerator()
            report_content = report_gen.generate_report(
                title=title,
                objective=objective,
                charts_info=charts_info,
                business_context=business_context,
                analyst=analyst,
                format=output_format
            )

            if output_path:
                import os
                # 确保目录存在
                os.makedirs(os.path.dirname(output_path), exist_ok=True)
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(report_content)
                return output_path
            else:
                return report_content

        except ImportError as e:
            print(f"无法导入ReportGenerator模块: {e}")
            print("请确保report_generator.py文件存在")
            return None
        except Exception as e:
            print(f"生成报告时出错: {e}")
            return None

    def create_chart_with_analysis(self, chart_type, chart_args,
                                  chart_title, save_path,
                                  data_context, business_context=""):
        """创建图表并生成分析文本

        一键生成图表和对应的分析内容。

        Args:
            chart_type: 图表类型（如 'bar_chart', 'line_chart'）
            chart_args: 创建图表所需的参数字典
            chart_title: 图表标题
            save_path: 图表保存路径
            data_context: 数据背景说明
            business_context: 业务上下文

        Returns:
            包含图表文件路径和分析文本的字典
        """
        # 根据图表类型调用对应方法
        chart_methods = {
            'heatmap': self.create_heatmap,
            'line_chart': self.create_line_chart,
            'bar_chart': self.create_bar_chart,
            'pie_chart': self.create_pie_chart,
            'scatter_plot': self.create_scatter_plot,
            'multi_column_bar': self.create_multi_column_bar,
            'stacked_bar': self.create_stacked_bar,
            'butterfly_chart': self.create_butterfly_chart,
            'pareto_chart': self.create_pareto_chart,
            'bubble_chart': self.create_bubble_chart,
            'bar_line_combo': self.create_bar_line_combo,
            'waterfall_chart': self.create_waterfall_chart,
            'bubble_bar_chart': self.create_bubble_bar_chart,
            'bubble_chart_2': self.create_bubble_chart_2
        }

        if chart_type not in chart_methods:
            raise ValueError(f"不支持的图表类型: {chart_type}")

        # 生成图表
        method = chart_methods[chart_type]
        plt_obj = method(**chart_args)

        # 保存图表
        plt_obj.savefig(save_path, dpi=300, bbox_inches='tight')
        plt_obj.close()

        # 生成分析
        chart_info = {
            'type': chart_type,
            'title': chart_title,
            'filepath': save_path,
            'data_context': data_context,
            'additional_context': business_context
        }

        try:
            from .report_generator import ReportGenerator
            report_gen = ReportGenerator()
            analysis = report_gen.analyze_chart(chart_info)

            return {
                'chart_path': save_path,
                'analysis': analysis,
                'success': True
            }
        except Exception as e:
            print(f"生成分析时出错: {e}")
            return {
                'chart_path': save_path,
                'analysis': None,
                'success': False,
                'error': str(e)
            }

    def create_analysis_with_derived_fields(self, data, chart_type,
                                          x_column=None, y_columns=None,
                                          chart_title="", save_path="chart.png",
                                          data_context="", business_context="",
                                          scenario=None, derivation_rules=None,
                                          cleaning_rules=None):
        """创建包含衍生字段的完整分析

        加载数据 -> 清洗 -> 衍生字段 -> 生成图表 -> 生成分析

        Args:
            data: 输入数据（文件路径、DataFrame或数据列表）
            chart_type: 图表类型
            x_column: X轴列名
            y_columns: Y轴列名列表
            chart_title: 图表标题
            save_path: 图表保存路径
            data_context: 数据背景说明
            business_context: 业务上下文
            scenario: 业务场景（如 'supermarket', 'ecommerce'）
            derivation_rules: 自定义衍生规则
            cleaning_rules: 自定义清洗规则

        Returns:
            包含图表、分析和数据摘要的字典
        """
        try:
            # 导入数据处理器
            from .data_processor import DataProcessor

            # 创建数据处理器
            processor = DataProcessor()

            # 1. 加载数据（如果是文件路径）
            if isinstance(data, str):
                loaded_data = processor.load_data(data)
            else:
                loaded_data = data

            # 2. 数据清洗
            cleaned_data = processor.clean_data(loaded_data, cleaning_rules)

            # 3. 衍生字段
            derived_data = processor.derive_fields(cleaned_data, derivation_rules, scenario)

            # 4. 准备图表数据
            chart_args = processor.prepare_chart_data(
                derived_data, chart_type, x_column, y_columns
            )

            # 5. 生成图表和分析
            result = self.create_chart_with_analysis(
                chart_type=chart_type,
                chart_args=chart_args,
                chart_title=chart_title,
                save_path=save_path,
                data_context=data_context,
                business_context=business_context
            )

            # 6. 生成数据摘要报告
            data_summary = processor.generate_data_summary_report(derived_data)

            # 7. 获取衍生字段信息
            derived_fields_info = self._get_derived_fields_info(processor, derived_data, scenario)

            # 合并结果
            result.update({
                'data_summary': data_summary,
                'derived_fields': derived_fields_info,
                'data_processor_used': True,
                'scenario': scenario
            })

            return result

        except Exception as e:
            print(f"创建包含衍生字段的分析时出错: {e}")
            import traceback
            traceback.print_exc()

            return {
                'success': False,
                'error': str(e),
                'data_processor_used': False
            }

    def _get_derived_fields_info(self, processor, data, scenario=None):
        """获取衍生字段信息"""
        # 简单实现：返回字段列表
        # 实际应用中可以从数据中提取衍生字段信息

        derived_fields = []

        if scenario == 'supermarket':
            derived_fields = [
                {'name': 'profit_margin', 'description': '利润 = 收入 - 成本', 'formula': 'revenue - cost'},
                {'name': 'profit_margin_rate', 'description': '利润率 (%) = (收入 - 成本) / 收入 * 100', 'formula': '(revenue - cost) / revenue * 100'},
                {'name': 'customer_contribution', 'description': '客户贡献度 = 收入 / 客户数', 'formula': 'revenue / customers'},
                {'name': 'basket_size', 'description': '平均购物篮大小 = 收入 / 交易次数', 'formula': 'revenue / transactions'},
                {'name': 'sales_per_sqft', 'description': '每平方英尺销售额 = 收入 / 店铺面积', 'formula': 'revenue / area'},
                {'name': 'gross_margin', 'description': '毛利率 (%) = (收入 - 商品成本) / 收入 * 100', 'formula': '(revenue - cost_of_goods) / revenue * 100'},
                {'name': 'inventory_turnover', 'description': '库存周转率 = 销售成本 / 平均库存', 'formula': 'cost_of_goods / average_inventory'},
                {'name': 'customer_traffic', 'description': '客流量 = 客户数 / 营业小时数', 'formula': 'customers / operating_hours'},
                {'name': 'sales_per_customer', 'description': '客单价 = 收入 / 客户数', 'formula': 'revenue / customers'},
                {'name': 'promotion_effectiveness', 'description': '促销效果 (%) = (促销期收入 - 基线收入) / 基线收入 * 100', 'formula': '(promotion_revenue - baseline_revenue) / baseline_revenue * 100'},
                {'name': 'waste_rate', 'description': '损耗率 (%) = 损耗成本 / 收入 * 100', 'formula': 'waste_cost / revenue * 100'},
                {'name': 'labor_productivity', 'description': '人工生产率 = 收入 / 人工工时', 'formula': 'revenue / labor_hours'}
            ]
        elif scenario == 'ecommerce':
            derived_fields = [
                {'name': 'conversion_rate', 'description': '转化率 (%) = 订单数 / 访客数 * 100', 'formula': 'orders / visitors * 100'},
                {'name': 'average_order_value', 'description': '平均订单价值 = 收入 / 订单数', 'formula': 'revenue / orders'},
                {'name': 'customer_lifetime_value', 'description': '客户生命周期价值 = 收入 * 复购率 * 留存周期', 'formula': 'revenue * repeat_rate * retention_period'},
                {'name': 'bounce_rate', 'description': '跳出率 (%) = 跳出会话数 / 总会话数 * 100', 'formula': 'bounced_sessions / total_sessions * 100'}
            ]

        return {
            'scenario': scenario,
            'fields': derived_fields,
            'count': len(derived_fields)
        }

# 使用示例
# templates = ChartTemplates()
# plt = templates.create_heatmap(data, title='主播活动热力图')
# plt.savefig('output.png', dpi=300, bbox_inches='tight')
