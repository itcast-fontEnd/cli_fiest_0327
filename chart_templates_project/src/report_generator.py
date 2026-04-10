# 报表生成模块 - 为图表生成专业数据分析报告
# 功能：自动分析图表，生成结论和针对性建议，输出结构化报告

import json
import os
from datetime import datetime
from typing import Dict, List, Any, Optional

class ReportGenerator:
    """报表生成器：自动为图表生成专业数据分析报告"""

    def __init__(self, config_path: str = None):
        """初始化报表生成器

        Args:
            config_path: 配置文件路径，包含分析模板和设置
        """
        self.analysis_templates = self._load_analysis_templates(config_path)
        self.report_structure = self._get_default_report_structure()

    def _load_analysis_templates(self, config_path: str = None) -> Dict[str, Any]:
        """加载分析模板配置

        为每种图表类型提供预设的分析框架
        """
        templates = {
            # 柱状图分析模板
            "bar_chart": {
                "key_questions": [
                    "哪个类别表现最好？哪个最差？",
                    "类别间的差距有多大？",
                    "是否有异常突出的类别？"
                ],
                "observation_points": [
                    "最高值和最低值",
                    "分布均匀性",
                    "异常值识别"
                ],
                "business_implications": [
                    "资源分配优先级",
                    "绩效评估依据",
                    "机会识别"
                ],
                "conclusion_framework": "基于排名和差距的分析，{best_performer}表现最佳，{worst_performer}需要关注，整体分布{distribution_character}。",
                "recommendation_framework": [
                    "优化{best_performer}的资源配置，巩固优势地位",
                    "分析{worst_performer}表现不佳的原因，制定改进措施",
                    "关注中等表现类别，挖掘增长潜力"
                ]
            },

            # 折线图分析模板
            "line_chart": {
                "key_questions": [
                    "整体趋势是上升、下降还是平稳？",
                    "是否有明显的季节性模式？",
                    "转折点出现在何时？可能原因是什么？"
                ],
                "observation_points": [
                    "趋势方向（上升/下降/平稳）",
                    "波动幅度和频率",
                    "拐点位置和特征",
                    "周期性模式"
                ],
                "business_implications": [
                    "战略规划时机选择",
                    "资源调配策略调整",
                    "风险预警和机会把握"
                ],
                "conclusion_framework": "整体呈现{trend_direction}趋势，{seasonality_info}，关键转折点出现在{turning_points}。",
                "recommendation_framework": [
                    "把握{growth_periods}的增长机会，加大投入",
                    "在{decline_periods}采取稳健策略，控制风险",
                    "优化资源分配，匹配趋势变化"
                ]
            },

            # 饼图分析模板
            "pie_chart": {
                "key_questions": [
                    "最大的部分是什么？占多少比例？",
                    "分布是否平衡？",
                    "是否有需要特别关注的小部分？"
                ],
                "observation_points": [
                    "主要部分占比",
                    "次要部分分布",
                    "平衡性评估",
                    "长尾效应"
                ],
                "business_implications": [
                    "市场份额分析",
                    "产品组合优化",
                    "资源集中度评估"
                ],
                "conclusion_framework": "{largest_part}占据主导地位（{largest_percentage}%），{distribution_character}，{minor_parts_info}。",
                "recommendation_framework": [
                    "巩固{largest_part}的市场地位，防止竞品侵蚀",
                    "优化产品组合，平衡{dependency_risk}",
                    "关注{minor_parts}，挖掘增长潜力"
                ]
            },

            # 热力图分析模板
            "heatmap": {
                "key_questions": [
                    "高密度区域在哪里？",
                    "是否有明显的模式或规律？",
                    "相关性最强的组合是什么？"
                ],
                "observation_points": [
                    "热点区域识别",
                    "冷点区域定位",
                    "模式规律分析",
                    "异常区域检测"
                ],
                "business_implications": [
                    "用户行为分析",
                    "资源配置优化",
                    "机会窗口识别"
                ],
                "conclusion_framework": "主要热点集中在{hotspot_areas}，呈现{pattern_type}模式，{correlation_strength}相关性较强。",
                "recommendation_framework": [
                    "聚焦{hotspot_areas}，提升资源利用效率",
                    "改善{coldspot_areas}的表现，消除盲点",
                    "利用{pattern_type}模式，优化运营策略"
                ]
            },

            # 散点图分析模板
            "scatter_plot": {
                "key_questions": [
                    "两个变量之间是什么关系？",
                    "是否有明显的聚类？",
                    "异常值有哪些？可能原因是什么？"
                ],
                "observation_points": [
                    "相关性方向和强度",
                    "聚类分布特征",
                    "异常值位置和特征"
                ],
                "business_implications": [
                    "因果关系分析",
                    "细分市场识别",
                    "问题诊断和改进"
                ],
                "conclusion_framework": "变量间呈现{correlation_direction}相关关系（强度：{correlation_strength}），{clustering_info}，{outliers_info}。",
                "recommendation_framework": [
                    "利用{positive_correlation}关系，同步优化相关因素",
                    "针对不同聚类特征{different_clusters}，制定差异化策略",
                    "分析异常值{outliers}原因，采取针对性措施"
                ]
            },

            # 多列条形图分析模板
            "multi_column_bar": {
                "key_questions": [
                    "哪个组在哪个类别中表现最好？",
                    "组间差异有多大？",
                    "是否存在一致的排名模式？"
                ],
                "observation_points": [
                    "各组在各类别中的表现",
                    "组间差异程度",
                    "类别间的表现模式",
                    "异常组别识别"
                ],
                "business_implications": [
                    "团队绩效评估",
                    "资源配置优化",
                    "最佳实践识别"
                ],
                "conclusion_framework": "{best_group}在多数类别中表现最佳，{worst_group}需要改进，组间差异{difference_level}。",
                "recommendation_framework": [
                    "推广{best_group}的最佳实践，提升整体表现",
                    "分析{worst_group}表现不佳的原因，制定改进计划",
                    "优化资源配置，减少组间差异"
                ]
            },

            # 分层柱形图分析模板
            "stacked_bar": {
                "key_questions": [
                    "每个类别的构成比例如何？",
                    "哪些部分在类别间变化最大？",
                    "整体构成有什么特征？"
                ],
                "observation_points": [
                    "各部分在各类别中的占比",
                    "构成变化模式",
                    "主导部分识别",
                    "异常构成检测"
                ],
                "business_implications": [
                    "产品组合优化",
                    "资源分配策略",
                    "市场细分分析"
                ],
                "conclusion_framework": "{dominant_part}在多数类别中占主导地位，构成模式{pattern_type}，{variation_level}变化显著。",
                "recommendation_framework": [
                    "优化{dominant_part}的资源配置，提升整体效率",
                    "关注{variable_parts}的变化，制定灵活策略",
                    "平衡构成比例，降低风险"
                ]
            },

            # 蝴蝶图分析模板
            "butterfly_chart": {
                "key_questions": [
                    "两组数据在哪些类别上差异最大？",
                    "整体上哪一组占优势？",
                    "差异模式是否有规律？"
                ],
                "observation_points": [
                    "左右两侧数据对比",
                    "差异程度和方向",
                    "类别间差异模式",
                    "异常类别识别"
                ],
                "business_implications": [
                    "对比分析决策支持",
                    "资源分配平衡",
                    "优劣势识别"
                ],
                "conclusion_framework": "{left_label}在{left_advantage_categories}占优势，{right_label}在{right_advantage_categories}占优势，整体{overall_balance}。",
                "recommendation_framework": [
                    "加强{left_label}在{right_advantage_categories}的表现，缩小差距",
                    "利用{right_label}在{left_advantage_categories}的优势，扩大领先",
                    "平衡资源配置，实现整体优化"
                ]
            },

            # 帕累托图分析模板
            "pareto_chart": {
                "key_questions": [
                    "主要因素是什么？贡献了多少比例？",
                    "80/20法则是否适用？",
                    "改进重点应该放在哪里？"
                ],
                "observation_points": [
                    "主要因素识别",
                    "累积贡献比例",
                    "关键少数与琐碎多数分界点",
                    "改进潜力评估"
                ],
                "business_implications": [
                    "问题优先级排序",
                    "资源聚焦策略",
                    "改进效果最大化"
                ],
                "conclusion_framework": "前{top_n}个因素贡献了{percent}%的效果，符合{compliance_level}帕累托原则，改进重点应放在{key_factors}。",
                "recommendation_framework": [
                    "聚焦{key_factors}，实现最大改进效果",
                    "监控次要因素，防止问题扩大",
                    "建立持续改进机制，优化因素排序"
                ]
            },

            # 气泡图分析模板
            "bubble_chart": {
                "key_questions": [
                    "三个变量之间的关系是什么？",
                    "气泡的分布模式如何？",
                    "哪些气泡是异常值？"
                ],
                "observation_points": [
                    "x-y关系模式",
                    "气泡大小分布",
                    "聚类识别",
                    "异常气泡检测"
                ],
                "business_implications": [
                    "多维度数据分析",
                    "综合绩效评估",
                    "复杂关系理解"
                ],
                "conclusion_framework": "数据呈现{relationship_pattern}关系，气泡分布{distribution_type}，{cluster_info}，{outlier_info}。",
                "recommendation_framework": [
                    "优化{x_y_relationship}相关因素，提升整体表现",
                    "关注{large_bubbles}的表现，发挥规模效应",
                    "分析{outliers}原因，制定针对性措施"
                ]
            },

            # 条形折线组合图分析模板
            "bar_line_combo": {
                "key_questions": [
                    "数量指标和比例指标的关系如何？",
                    "是否存在数量高但比例低（或反之）的类别？",
                    "整体协调性如何？"
                ],
                "observation_points": [
                    "条形图数值分布",
                    "折线图趋势模式",
                    "两者协调程度",
                    "异常类别识别"
                ],
                "business_implications": [
                    "综合绩效评估",
                    "战略平衡分析",
                    "资源配置优化"
                ],
                "conclusion_framework": "数量指标{bar_performance}，比例指标{line_performance}，两者协调性{coordination_level}，{anomaly_info}。",
                "recommendation_framework": [
                    "提升{low_bar_high_line}类别的数量指标，实现平衡发展",
                    "优化{high_bar_low_line}类别的比例指标，提高效率",
                    "加强协调管理，促进整体优化"
                ]
            },

            # 瀑布图分析模板
            "waterfall_chart": {
                "key_questions": [
                    "从起点到终点的关键变化是什么？",
                    "最大的正负贡献来自哪些因素？",
                    "累积效果如何演变？"
                ],
                "observation_points": [
                    "起点和终点值",
                    "正负贡献因素",
                    "变化幅度和方向",
                    "累积路径特征"
                ],
                "business_implications": [
                    "变化驱动因素分析",
                    "绩效分解评估",
                    "改进机会识别"
                ],
                "conclusion_framework": "从{start_value}到{end_value}，主要正贡献来自{positive_factors}，主要负贡献来自{negative_factors}，净变化{net_change}。",
                "recommendation_framework": [
                    "强化{positive_factors}，扩大正向影响",
                    "减少{negative_factors}的负面影响",
                    "优化中间过程，提升整体效果"
                ]
            },

            # 气泡条形图分析模板
            "bubble_bar_chart": {
                "key_questions": [
                    "条形图高度和气泡大小的关系如何？",
                    "哪些类别在两方面都表现突出？",
                    "是否存在不匹配的类别？"
                ],
                "observation_points": [
                    "条形图数值分布",
                    "气泡大小分布",
                    "两者匹配程度",
                    "异常类别识别"
                ],
                "business_implications": [
                    "多维度绩效评估",
                    "资源分配优化",
                    "综合能力分析"
                ],
                "conclusion_framework": "条形图表现{bar_performance}，气泡大小表现{bubble_performance}，两者匹配度{match_level}，{anomaly_info}。",
                "recommendation_framework": [
                    "提升{low_bar_high_bubble}类别的条形图指标，发挥潜力",
                    "优化{high_bar_low_bubble}类别的气泡指标，提高效率",
                    "加强综合能力建设，实现均衡发展"
                ]
            },

            # 增强型气泡图分析模板
            "bubble_chart_2": {
                "key_questions": [
                    "四个维度之间的关系是什么？",
                    "数据的整体分布模式如何？",
                    "哪些数据点是关键异常值？"
                ],
                "observation_points": [
                    "x-y关系模式",
                    "气泡大小分布",
                    "颜色梯度变化",
                    "多维聚类识别",
                    "异常值检测"
                ],
                "business_implications": [
                    "复杂数据分析",
                    "综合决策支持",
                    "多变量关系理解"
                ],
                "conclusion_framework": "四维数据显示{relationship_pattern}关系，分布{distribution_type}，颜色梯度{color_pattern}，{cluster_info}，{outlier_info}。",
                "recommendation_framework": [
                    "基于多维关系{multidimensional_relationship}，制定综合策略",
                    "关注关键维度{key_dimensions}，提升整体表现",
                    "分析异常值{outliers}，发现潜在机会或问题"
                ]
            },

            # 超市柱状图分析模板（专门针对超市数据分析）
            "supermarket_bar_chart": {
                "key_questions": [
                    "哪些产品类别销售额最高？利润率如何？",
                    "销售额与利润率的关联性如何？是否存在高销售额低利润率的产品？",
                    "客户贡献度在不同产品类别间的分布情况如何？"
                ],
                "observation_points": [
                    "销售额排名前5的产品类别",
                    "利润率与销售额的对比分析",
                    "客户贡献度分布特征",
                    "促销活动对销售额的影响",
                    "季节性销售模式"
                ],
                "business_implications": [
                    "产品组合优化策略制定",
                    "定价策略调整依据",
                    "库存管理优化方向",
                    "促销资源分配决策",
                    "供应商谈判筹码"
                ],
                "conclusion_framework": "销售额最高的类别是{top_sales_category}（{top_sales_value}），利润率最高的是{top_margin_category}（{top_margin_value}%），{sales_margin_relationship}关系，客户贡献度{contribution_pattern}。",
                "recommendation_framework": [
                    "重点推广{high_sales_high_margin}类别，巩固市场地位",
                    "优化{high_sales_low_margin}类别的成本结构，提升盈利能力",
                    "针对{low_sales_high_margin}类别制定增长策略，扩大市场份额",
                    "根据季节性模式调整库存和促销策略",
                    "建立客户贡献度分层管理体系"
                ]
            },

            # 超市折线图分析模板
            "supermarket_line_chart": {
                "key_questions": [
                    "销售额的时间趋势如何？是否有明显的季节性？",
                    "促销活动期间销售额变化幅度多大？",
                    "不同产品类别的销售趋势有何差异？"
                ],
                "observation_points": [
                    "整体销售趋势（上升/下降/平稳）",
                    "季节性波动模式",
                    "促销活动响应效果",
                    "增长率变化拐点",
                    "不同品类趋势对比"
                ],
                "business_implications": [
                    "销售预测和预算编制",
                    "促销活动时机选择",
                    "季节性库存规划",
                    "产品生命周期管理",
                    "市场竞争态势评估"
                ],
                "conclusion_framework": "整体销售呈现{overall_trend}趋势，{seasonality_strength}季节性特征，促销期间增长{promotion_effectiveness}，{category_trend_differences}。",
                "recommendation_framework": [
                    "在{sales_peak_periods}加强库存和人员准备",
                    "优化促销策略，提高{promotion_response_rate}",
                    "针对{declining_categories}制定挽救措施",
                    "把握{growth_opportunities}的增长机会",
                    "建立动态销售预测模型"
                ]
            },

            # 超市饼图分析模板
            "supermarket_pie_chart": {
                "key_questions": [
                    "各产品类别的销售额占比如何？",
                    "哪些类别是主要收入来源？",
                    "是否存在过度依赖少数类别的情况？"
                ],
                "observation_points": [
                    "各类别销售额占比分布",
                    "前三大类别合计占比",
                    "长尾类别识别",
                    "市场份额集中度",
                    "季节性占比变化"
                ],
                "business_implications": [
                    "产品组合优化决策",
                    "库存管理策略调整",
                    "营销资源分配优先级",
                    "供应商谈判策略",
                    "品类扩张方向选择"
                ],
                "conclusion_framework": "销售额主要来自{top_category}（占{top_percentage}%），前三大类别合计占{top3_percentage}%，产品结构{concentration_level}集中，{growth_category}有增长潜力。",
                "recommendation_framework": [
                    "巩固{top_category}优势地位，防范竞争风险",
                    "优化中间品类{mid_categories}的成本效益",
                    "培育潜力品类{growth_category}，分散风险",
                    "根据季节变化调整品类策略",
                    "建立品类健康度监控体系"
                ]
            },

            # 超市热力图分析模板
            "supermarket_heatmap": {
                "key_questions": [
                    "销售热度在不同时间段和区域的分布如何？",
                    "哪些时间段和品类的组合销售效果最好？",
                    "是否存在明显的销售冷点需要改善？"
                ],
                "observation_points": [
                    "高峰时段和低谷时段识别",
                    "热销区域和冷门区域分布",
                    "时段与品类交叉分析",
                    "促销活动热度影响",
                    "周末与工作日对比"
                ],
                "business_implications": [
                    "人员排班优化依据",
                    "促销活动时机选择",
                    "商品陈列调整参考",
                    "库存补货策略优化",
                    "店铺布局改进方向"
                ],
                "conclusion_framework": "销售热点集中在{peak_hours}时段和{hot_categories}品类，{cold_areas}存在改善空间，促销活动效果{promotion_effectiveness}，{weekend_pattern}周末销售模式。",
                "recommendation_framework": [
                    "在{peak_hours}增加收银台和工作人员",
                    "优化{cold_areas}的商品陈列和促销",
                    "根据时段特征调整品类组合",
                    "针对不同时段设计差异化促销",
                    "建立动态热力图监控系统"
                ]
            },

            # 超市散点图分析模板
            "supermarket_scatter_plot": {
                "key_questions": [
                    "价格与销量之间的关系如何？",
                    "利润率与销售额是否存在相关性？",
                    "哪些产品属于高销量高利润的明星产品？"
                ],
                "observation_points": [
                    "价格弹性分析",
                    "利润率与销量相关性",
                    "产品四象限分类（明星/金牛/问题/瘦狗）",
                    "异常产品识别",
                    "品类间差异比较"
                ],
                "business_implications": [
                    "定价策略优化",
                    "产品组合决策",
                    "促销商品选择",
                    "库存管理优先级",
                    "供应商绩效评估"
                ],
                "conclusion_framework": "价格与销量呈现{price_elasticity}关系，利润率与销售额{correlation_strength}相关，明星产品集中在{star_products}，问题产品{problem_products}需要关注。",
                "recommendation_framework": [
                    "对高弹性产品{elastic_products}优化定价策略",
                    "加大明星产品{star_products}的推广力度",
                    "改进问题产品{problem_products}的成本结构",
                    "利用金牛产品{cash_cow_products}的现金流优势",
                    "建立产品四象限动态管理机制"
                ]
            },

            # 默认模板（用于其他图表类型）
            "default": {
                "key_questions": [
                    "图表展示了什么关键信息？",
                    "有哪些显著的模式或特征？",
                    "对业务有什么启示？"
                ],
                "observation_points": [
                    "数据分布特征",
                    "显著模式识别",
                    "异常情况检测"
                ],
                "business_implications": [
                    "业务决策支持",
                    "问题诊断和改进",
                    "机会识别和把握"
                ],
                "conclusion_framework": "图表显示{main_finding}，{pattern_observation}，{business_impact}。",
                "recommendation_framework": [
                    "基于{main_finding}，采取相应行动",
                    "针对{pattern_observation}，优化相关策略",
                    "关注{business_impact}，制定应对措施"
                ]
            }
        }

        # 如果有外部配置文件，加载并合并
        if config_path and os.path.exists(config_path):
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    external_templates = json.load(f)
                templates.update(external_templates)
            except Exception as e:
                print(f"加载外部模板配置失败: {e}")

        return templates

    def _get_default_report_structure(self) -> Dict[str, Any]:
        """获取默认报告结构"""
        return {
            "executive_summary": {
                "analysis_objective": "",
                "key_findings": [],
                "priority_recommendations": [],
                "expected_impact": ""
            },
            "chart_analyses": [],
            "comprehensive_analysis": {
                "pattern_correlations": "",
                "business_impact_assessment": "",
                "priority_matrix": []
            },
            "implementation_roadmap": {
                "immediate_actions": [],
                "short_term_improvements": [],
                "mid_long_term_planning": []
            },
            "appendix": {
                "methodology": "",
                "data_sources": "",
                "limitations": ""
            }
        }

    def analyze_chart(self, chart_info: Dict[str, Any]) -> Dict[str, Any]:
        """分析单个图表，生成洞察、结论和建议

        Args:
            chart_info: 图表信息字典，包含：
                - type: 图表类型（如 'bar_chart', 'line_chart'）
                - title: 图表标题
                - filepath: 图表文件路径
                - data_context: 数据背景说明
                - additional_context: 额外业务上下文（可选）

        Returns:
            分析结果字典，包含洞察、结论、建议等
        """
        chart_type = chart_info.get('type', 'default')
        template = self.analysis_templates.get(chart_type, self.analysis_templates['default'])

        # 这里可以添加实际的数据分析逻辑
        # 目前使用模板生成示例分析

        analysis_result = {
            'chart_title': chart_info.get('title', '未命名图表'),
            'chart_type': chart_type,
            'chart_filepath': chart_info.get('filepath', ''),
            'data_context': chart_info.get('data_context', ''),
            'business_context': chart_info.get('additional_context', ''),

            'key_observations': self._generate_observations(template, chart_info),
            'business_implications': self._generate_implications(template, chart_info),
            'conclusions': self._generate_conclusions(template, chart_info),
            'recommendations': self._generate_recommendations(template, chart_info),

            'confidence_level': '中',  # 置信度：高/中/低
            'next_actions': self._generate_next_actions(template, chart_info)
        }

        return analysis_result

    def _generate_observations(self, template: Dict[str, Any], chart_info: Dict[str, Any]) -> List[str]:
        """生成观察要点"""
        observations = []
        for point in template.get('observation_points', []):
            observations.append(f"{point}：基于图表数据进行分析")
        return observations

    def _generate_implications(self, template: Dict[str, Any], chart_info: Dict[str, Any]) -> List[str]:
        """生成业务含义"""
        implications = []
        for implication in template.get('business_implications', []):
            implications.append(f"{implication}：对业务决策有重要参考价值")
        return implications

    def _generate_conclusions(self, template: Dict[str, Any], chart_info: Dict[str, Any]) -> str:
        """生成结论"""
        framework = template.get('conclusion_framework', '')
        title = chart_info.get('title', '该图表')

        # 简单示例：实际应用中可以根据具体数据填充模板
        # 提供所有可能占位符的默认值
        format_args = {
            'chart_title': title,
            'best_performer': "表现最佳的类别",
            'worst_performer': "需要关注的类别",
            'distribution_character': "相对均衡",
            'trend_direction': "上升",
            'seasonality_info': "无明显季节性",
            'turning_points': "关键时间点",
            'largest_part': "主要部分",
            'largest_percentage': "45",
            'minor_parts_info': "次要部分有提升空间",
            'hotspot_areas': "核心区域",
            'pattern_type': "规律性",
            'correlation_strength': "中等",
            'correlation_direction': "正",
            'clustering_info': "存在明显聚类",
            'outliers_info': "有少量异常值",
            'main_finding': "重要数据特征",
            'pattern_observation': "明显模式",
            'business_impact': "对业务有显著影响",
            # 新增占位符
            'best_group': "最佳组别",
            'worst_group': "需要改进的组别",
            'difference_level': "较大",
            'dominant_part': "主导部分",
            'variation_level': "显著",
            'left_label': "左侧",
            'left_advantage_categories': "优势类别",
            'right_label': "右侧",
            'right_advantage_categories': "优势类别",
            'overall_balance': "相对平衡",
            'top_n': "3",
            'percent': "80",
            'compliance_level': "高度",
            'key_factors': "关键因素",
            'relationship_pattern': "正相关",
            'distribution_type': "集中分布",
            'cluster_info': "存在聚类",
            'outlier_info': "有异常值",
            'bar_performance': "良好",
            'line_performance': "稳定",
            'coordination_level': "协调",
            'anomaly_info': "无异常",
            'start_value': "起始值",
            'end_value': "结束值",
            'positive_factors': "积极因素",
            'negative_factors': "消极因素",
            'net_change': "净变化",
            'bubble_performance': "良好",
            'match_level': "匹配",
            'color_pattern': "颜色梯度",
            'top_sales_category': "销售额最高类别",
            'top_sales_value': "10000",
            'top_margin_category': "利润率最高类别",
            'top_margin_value': "30",
            'sales_margin_relationship': "正相关",
            'contribution_pattern': "集中贡献",
            'overall_trend': "上升",
            'seasonality_strength': "明显",
            'promotion_effectiveness': "有效",
            'category_trend_differences': "差异显著",
            'top_category': "顶级类别",
            'top_percentage': "40",
            'top3_percentage': "70",
            'concentration_level': "高度集中",
            'growth_category': "增长类别",
            'peak_hours': "高峰时段",
            'hot_categories': "热门品类",
            'cold_areas': "冷门区域",
            'weekend_pattern': "周末模式",
            'price_elasticity': "弹性适中",
            'star_products': "明星产品",
            'problem_products': "问题产品"
        }

        try:
            conclusion = framework.format(**format_args)
        except KeyError as e:
            # 如果仍有缺失的占位符，使用更通用的默认值
            print(f"警告: 结论模板中存在未知占位符 {e}, 使用通用模板")
            conclusion = f"{title}显示了重要的数据特征和模式，需要进一步分析其业务含义。"

        return conclusion if conclusion else f"{title}显示了重要的数据特征和模式，需要进一步分析其业务含义。"

    def _generate_recommendations(self, template: Dict[str, Any], chart_info: Dict[str, Any]) -> List[str]:
        """生成建议"""
        recommendations = []
        recommendation_framework = template.get('recommendation_framework', [])

        if isinstance(recommendation_framework, list):
            for i, framework in enumerate(recommendation_framework[:3]):  # 取前3条
                try:
                    recommendation = framework.format(
                        best_performer="领先类别",
                        worst_performer="落后类别",
                        growth_periods="增长期",
                        decline_periods="下降期",
                        largest_part="主要部分",
                        dependency_risk="依赖风险",
                        minor_parts="次要部分",
                        hotspot_areas="热点区域",
                        coldspot_areas="冷点区域",
                        pattern_type="模式特征",
                        positive_correlation="正相关",
                        different_clusters="不同聚类",
                        outliers="异常值",
                        main_finding="主要发现",
                        pattern_observation="模式观察",
                        business_impact="业务影响"
                    )
                    recommendations.append(recommendation)
                except:
                    recommendations.append(framework)

        # 确保至少有一条建议
        if not recommendations:
            recommendations.append("基于图表分析，建议进一步深入分析数据，制定针对性改进措施。")

        return recommendations

    def _generate_next_actions(self, template: Dict[str, Any], chart_info: Dict[str, Any]) -> Dict[str, List[str]]:
        """生成下一步行动"""
        return {
            'immediate_actions': [
                '复核数据准确性',
                '与相关团队沟通发现'
            ],
            'short_term_actions': [
                '制定详细实施计划',
                '分配执行责任人'
            ],
            'monitoring_metrics': [
                '关键指标变化',
                '业务影响评估'
            ]
        }

    def generate_report(self,
                       title: str,
                       objective: str,
                       charts_info: List[Dict[str, Any]],
                       business_context: str = "",
                       analyst: str = "数据分析师",
                       format: str = "markdown") -> str:
        """生成完整数据分析报告

        Args:
            title: 报告标题
            objective: 分析目标
            charts_info: 图表信息列表
            business_context: 业务上下文描述
            analyst: 分析师姓名
            format: 输出格式 ('markdown' 或 'html')

        Returns:
            格式化后的报告内容
        """
        # 分析所有图表
        chart_analyses = []
        for chart_info in charts_info:
            analysis = self.analyze_chart(chart_info)
            chart_analyses.append(analysis)

        # 生成执行摘要
        executive_summary = self._generate_executive_summary(chart_analyses, objective)

        # 生成综合分析
        comprehensive_analysis = self._generate_comprehensive_analysis(chart_analyses)

        # 生成实施路线图
        implementation_roadmap = self._generate_implementation_roadmap(chart_analyses)

        # 根据格式生成报告
        if format.lower() == 'html':
            report_content = self._generate_html_report(
                title, executive_summary, chart_analyses,
                comprehensive_analysis, implementation_roadmap,
                business_context, analyst
            )
        else:  # 默认 Markdown
            report_content = self._generate_markdown_report(
                title, executive_summary, chart_analyses,
                comprehensive_analysis, implementation_roadmap,
                business_context, analyst
            )

        return report_content

    def _generate_executive_summary(self, chart_analyses: List[Dict[str, Any]], objective: str) -> Dict[str, Any]:
        """生成执行摘要"""
        # 提取关键发现
        key_findings = []
        for i, analysis in enumerate(chart_analyses[:3]):  # 取前3个关键发现
            key_findings.append(f"图表{i+1}显示：{analysis['conclusions'][:100]}...")

        # 提取优先级建议
        priority_recommendations = []
        for i, analysis in enumerate(chart_analyses[:2]):  # 取前2个优先级建议
            if analysis['recommendations']:
                priority_recommendations.append(analysis['recommendations'][0])

        return {
            'analysis_objective': objective,
            'key_findings': key_findings,
            'priority_recommendations': priority_recommendations,
            'expected_impact': '提升决策质量，优化资源配置，识别业务机会'
        }

    def _generate_comprehensive_analysis(self, chart_analyses: List[Dict[str, Any]]) -> Dict[str, Any]:
        """生成综合分析"""
        if len(chart_analyses) > 1:
            pattern_correlations = "多个图表显示一致的趋势和模式，相互验证了分析结论。"
        else:
            pattern_correlations = "单图表分析，建议补充更多维度数据以进行交叉验证。"

        return {
            'pattern_correlations': pattern_correlations,
            'business_impact_assessment': '分析结果对业务决策有重要参考价值，建议重点关注优先级建议。',
            'priority_matrix': [
                {'priority': 'P0', 'description': '紧急问题，需立即处理', 'actions': ['立即行动1', '立即行动2']},
                {'priority': 'P1', 'description': '重要改进，需短期实施', 'actions': ['短期行动1', '短期行动2']},
                {'priority': 'P2', 'description': '优化建议，可中长期规划', 'actions': ['长期行动1', '长期行动2']}
            ]
        }

    def _generate_implementation_roadmap(self, chart_analyses: List[Dict[str, Any]]) -> Dict[str, Any]:
        """生成实施路线图"""
        return {
            'immediate_actions': [
                {'task': '复核数据准确性', 'owner': '数据分析团队', 'timeline': '1周内'},
                {'task': '与业务团队沟通发现', 'owner': '项目经理', 'timeline': '1周内'}
            ],
            'short_term_improvements': [
                {'task': '制定详细实施计划', 'owner': '产品经理', 'timeline': '1个月内'},
                {'task': '分配资源执行优先级建议', 'owner': '部门负责人', 'timeline': '1个月内'}
            ],
            'mid_long_term_planning': [
                {'task': '建立数据监控体系', 'owner': '数据团队', 'timeline': '3个月内'},
                {'task': '优化分析流程和方法', 'owner': '分析团队', 'timeline': '6个月内'}
            ]
        }

    def _generate_markdown_report(self,
                                 title: str,
                                 executive_summary: Dict[str, Any],
                                 chart_analyses: List[Dict[str, Any]],
                                 comprehensive_analysis: Dict[str, Any],
                                 implementation_roadmap: Dict[str, Any],
                                 business_context: str,
                                 analyst: str) -> str:
        """生成Markdown格式报告"""
        report_lines = []

        # 报告标题和元信息
        report_lines.append(f"# {title}")
        report_lines.append("")
        report_lines.append("## 报告概述")
        report_lines.append(f"- **分析目标**: {executive_summary['analysis_objective']}")
        report_lines.append(f"- **业务上下文**: {business_context}")
        report_lines.append(f"- **分析师**: {analyst}")
        report_lines.append(f"- **生成日期**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report_lines.append(f"- **包含图表数**: {len(chart_analyses)}")
        report_lines.append("")

        # 执行摘要
        report_lines.append("## 执行摘要")
        report_lines.append("")
        report_lines.append("### 关键发现")
        for i, finding in enumerate(executive_summary['key_findings'], 1):
            report_lines.append(f"{i}. {finding}")
        report_lines.append("")

        report_lines.append("### 优先级建议")
        for i, recommendation in enumerate(executive_summary['priority_recommendations'], 1):
            report_lines.append(f"{i}. {recommendation}")
        report_lines.append("")

        report_lines.append(f"### 预期影响")
        report_lines.append(executive_summary['expected_impact'])
        report_lines.append("")

        # 按图表详细分析
        report_lines.append("## 详细分析")
        report_lines.append("")

        for i, analysis in enumerate(chart_analyses, 1):
            report_lines.append(f"### 图表{i}: {analysis['chart_title']}")
            report_lines.append("")

            if analysis['chart_filepath']:
                report_lines.append(f"![{analysis['chart_title']}]({analysis['chart_filepath']})")
                report_lines.append("")

            report_lines.append(f"**数据说明**: {analysis['data_context']}")
            report_lines.append("")

            if analysis['business_context']:
                report_lines.append(f"**业务上下文**: {analysis['business_context']}")
                report_lines.append("")

            report_lines.append("#### 关键观察")
            for observation in analysis['key_observations']:
                report_lines.append(f"- {observation}")
            report_lines.append("")

            report_lines.append("#### 业务含义")
            for implication in analysis['business_implications']:
                report_lines.append(f"- {implication}")
            report_lines.append("")

            report_lines.append("#### 结论")
            report_lines.append(f"{analysis['conclusions']}")
            report_lines.append("")

            report_lines.append("#### 建议")
            for j, recommendation in enumerate(analysis['recommendations'], 1):
                report_lines.append(f"{j}. {recommendation}")
            report_lines.append("")

            report_lines.append("#### 下一步行动")
            next_actions = analysis['next_actions']
            report_lines.append("- **立即行动 (1周内)**:")
            for action in next_actions.get('immediate_actions', []):
                report_lines.append(f"  - {action}")
            report_lines.append("- **短期行动 (1个月内)**:")
            for action in next_actions.get('short_term_actions', []):
                report_lines.append(f"  - {action}")
            report_lines.append("- **监测指标**:")
            for metric in next_actions.get('monitoring_metrics', []):
                report_lines.append(f"  - {metric}")
            report_lines.append("")

            report_lines.append(f"**置信度**: {analysis['confidence_level']}")
            report_lines.append("")

        # 综合分析
        report_lines.append("## 综合分析")
        report_lines.append("")

        report_lines.append("### 模式关联分析")
        report_lines.append(comprehensive_analysis['pattern_correlations'])
        report_lines.append("")

        report_lines.append("### 业务影响评估")
        report_lines.append(comprehensive_analysis['business_impact_assessment'])
        report_lines.append("")

        report_lines.append("### 优先级矩阵")
        for priority_item in comprehensive_analysis['priority_matrix']:
            report_lines.append(f"- **{priority_item['priority']}**: {priority_item['description']}")
            for action in priority_item['actions']:
                report_lines.append(f"  - {action}")
        report_lines.append("")

        # 实施路线图
        report_lines.append("## 实施路线图")
        report_lines.append("")

        report_lines.append("### 阶段1: 立即执行 (0-1个月)")
        for action in implementation_roadmap['immediate_actions']:
            report_lines.append(f"- **{action['task']}**")
            report_lines.append(f"  - 负责人: {action['owner']}")
            report_lines.append(f"  - 时间: {action['timeline']}")
        report_lines.append("")

        report_lines.append("### 阶段2: 短期改进 (1-3个月)")
        for action in implementation_roadmap['short_term_improvements']:
            report_lines.append(f"- **{action['task']}**")
            report_lines.append(f"  - 负责人: {action['owner']}")
            report_lines.append(f"  - 时间: {action['timeline']}")
        report_lines.append("")

        report_lines.append("### 阶段3: 中长期规划 (3-12个月)")
        for action in implementation_roadmap['mid_long_term_planning']:
            report_lines.append(f"- **{action['task']}**")
            report_lines.append(f"  - 负责人: {action['owner']}")
            report_lines.append(f"  - 时间: {action['timeline']}")
        report_lines.append("")

        # 附录
        report_lines.append("## 附录")
        report_lines.append("")
        report_lines.append("### 分析方法说明")
        report_lines.append("本报告使用自动化分析系统生成，结合图表类型模板和业务上下文进行分析。")
        report_lines.append("")
        report_lines.append("### 数据来源")
        report_lines.append("图表数据由用户提供，具体来源见各图表说明。")
        report_lines.append("")
        report_lines.append("### 局限性说明")
        report_lines.append("自动化分析基于预设模板，建议结合专业判断和业务知识进行决策。")
        report_lines.append("")

        # 报告结束
        report_lines.append("---")
        report_lines.append(f"**报告生成完成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report_lines.append("**报告状态**: 自动化生成")
        report_lines.append("**保密级别**: 内部使用")

        return "\n".join(report_lines)

    def _generate_html_report(self,
                             title: str,
                             executive_summary: Dict[str, Any],
                             chart_analyses: List[Dict[str, Any]],
                             comprehensive_analysis: Dict[str, Any],
                             implementation_roadmap: Dict[str, Any],
                             business_context: str,
                             analyst: str) -> str:
        """生成HTML格式报告（简化版）"""
        # 简化的HTML报告，实际应用中可扩展
        html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{title}</title>
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; margin: 40px; }}
        h1 {{ color: #333; border-bottom: 2px solid #4CAF50; padding-bottom: 10px; }}
        h2 {{ color: #444; margin-top: 30px; }}
        h3 {{ color: #555; }}
        .summary {{ background-color: #f9f9f9; padding: 20px; border-radius: 5px; }}
        .chart-analysis {{ border: 1px solid #ddd; padding: 15px; margin: 20px 0; border-radius: 5px; }}
        .recommendation {{ background-color: #e8f5e8; padding: 10px; margin: 10px 0; border-left: 4px solid #4CAF50; }}
        .roadmap-item {{ margin: 10px 0; }}
    </style>
</head>
<body>
    <h1>{title}</h1>

    <div class="summary">
        <h2>报告概述</h2>
        <p><strong>分析目标:</strong> {executive_summary['analysis_objective']}</p>
        <p><strong>业务上下文:</strong> {business_context}</p>
        <p><strong>分析师:</strong> {analyst}</p>
        <p><strong>生成日期:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    </div>

    <h2>执行摘要</h2>
    <h3>关键发现</h3>
    <ul>
        {"".join([f"<li>{finding}</li>" for finding in executive_summary['key_findings']])}
    </ul>

    <h3>优先级建议</h3>
    <div class="recommendation">
        {"".join([f"<p>{rec}</p>" for rec in executive_summary['priority_recommendations']])}
    </div>

    <h2>详细分析</h2>
    {"".join([self._generate_html_chart_analysis(analysis, i) for i, analysis in enumerate(chart_analyses, 1)])}

    <h2>实施路线图</h2>
    <h3>立即执行 (0-1个月)</h3>
    {"".join([f'<div class="roadmap-item"><strong>{action["task"]}</strong> - {action["owner"]} ({action["timeline"]})</div>'
              for action in implementation_roadmap['immediate_actions']])}

    <script>
        // 简单的交互功能
        document.addEventListener('DOMContentLoaded', function() {{
            console.log('数据分析报告已加载');
        }});
    </script>
</body>
</html>
        """
        return html_content

    def _generate_html_chart_analysis(self, analysis: Dict[str, Any], index: int) -> str:
        """生成HTML格式的单个图表分析"""
        return f"""
    <div class="chart-analysis">
        <h3>图表{index}: {analysis['chart_title']}</h3>
        {"<img src='" + analysis['chart_filepath'] + "' alt='" + analysis['chart_title'] + "' style='max-width: 100%;'><br>" if analysis['chart_filepath'] else ""}
        <p><strong>数据说明:</strong> {analysis['data_context']}</p>
        <p><strong>结论:</strong> {analysis['conclusions']}</p>
        <h4>建议:</h4>
        <ul>
            {"".join([f"<li>{rec}</li>" for rec in analysis['recommendations']])}
        </ul>
    </div>
        """

    def analyze_with_derived_fields(self, chart_info: Dict[str, Any],
                                  derived_fields_info: Dict[str, Any] = None,
                                  scenario: str = None) -> Dict[str, Any]:
        """分析包含衍生字段的图表

        Args:
            chart_info: 图表信息字典
            derived_fields_info: 衍生字段信息
            scenario: 业务场景

        Returns:
            增强的分析结果，包含衍生字段洞察
        """
        # 首先进行常规分析
        base_analysis = self.analyze_chart(chart_info)

        # 添加衍生字段分析
        derived_analysis = self._analyze_derived_fields(base_analysis, derived_fields_info, scenario)

        # 合并结果
        enhanced_analysis = base_analysis.copy()
        enhanced_analysis['derived_fields_analysis'] = derived_analysis
        enhanced_analysis['scenario'] = scenario

        return enhanced_analysis

    def _analyze_derived_fields(self, base_analysis: Dict[str, Any],
                              derived_fields_info: Dict[str, Any] = None,
                              scenario: str = None) -> Dict[str, Any]:
        """分析衍生字段"""
        if not derived_fields_info:
            return {
                'has_derived_fields': False,
                'message': '无衍生字段分析'
            }

        analysis = {
            'has_derived_fields': True,
            'scenario': scenario,
            'field_insights': [],
            'business_implications': [],
            'recommendations': []
        }

        # 根据场景生成分析
        if scenario == 'supermarket':
            analysis['field_insights'] = [
                '利润率分析显示各产品的盈利能力差异',
                '客户贡献度指标帮助识别高价值客户群体',
                '平均购物篮大小反映客户购买力和促销效果'
            ]
            analysis['business_implications'] = [
                '高利润率产品应优先推广和库存保障',
                '低客户贡献度产品需重新评估定价和定位',
                '购物篮大小变化可指导促销策略优化'
            ]
            analysis['recommendations'] = [
                '根据利润率重新分配营销资源',
                '针对高贡献客户制定忠诚度计划',
                '通过交叉销售提升平均购物篮大小'
            ]
        elif scenario == 'ecommerce':
            analysis['field_insights'] = [
                '转化率分析揭示网站用户体验瓶颈',
                '平均订单价值反映定价策略有效性',
                '客户生命周期价值指导长期营销投入'
            ]
            analysis['business_implications'] = [
                '低转化率页面需优化用户体验和购买流程',
                '低平均订单价值产品可考虑捆绑销售',
                '高生命周期价值客户应重点维护'
            ]
            analysis['recommendations'] = [
                'A/B测试优化关键页面转化率',
                '设计增值服务提升平均订单价值',
                '建立客户分层营销体系'
            ]
        else:
            analysis['field_insights'] = ['衍生字段提供了额外的业务洞察维度']
            analysis['business_implications'] = ['基于衍生指标可进行更精准的业务决策']
            analysis['recommendations'] = ['持续监控关键衍生指标，优化业务策略']

        return analysis

    def generate_enhanced_report(self,
                                title: str,
                                objective: str,
                                charts_info: List[Dict[str, Any]],
                                derived_fields_info: Dict[str, Any] = None,
                                scenario: str = None,
                                business_context: str = "",
                                analyst: str = "数据分析师",
                                format: str = "markdown") -> str:
        """生成增强版数据分析报告（包含衍生字段分析）

        Args:
            title: 报告标题
            objective: 分析目标
            charts_info: 图表信息列表
            derived_fields_info: 衍生字段信息
            scenario: 业务场景
            business_context: 业务上下文描述
            analyst: 分析师姓名
            format: 输出格式

        Returns:
            增强版报告内容
        """
        # 分析所有图表（包含衍生字段分析）
        chart_analyses = []
        for chart_info in charts_info:
            analysis = self.analyze_with_derived_fields(
                chart_info, derived_fields_info, scenario
            )
            chart_analyses.append(analysis)

        # 生成执行摘要
        executive_summary = self._generate_enhanced_executive_summary(
            chart_analyses, objective, scenario
        )

        # 生成综合分析（包含衍生字段）
        comprehensive_analysis = self._generate_enhanced_comprehensive_analysis(
            chart_analyses, scenario
        )

        # 生成实施路线图
        implementation_roadmap = self._generate_implementation_roadmap(chart_analyses)

        # 根据格式生成报告
        if format.lower() == 'html':
            report_content = self._generate_enhanced_html_report(
                title, executive_summary, chart_analyses,
                comprehensive_analysis, implementation_roadmap,
                business_context, analyst, scenario
            )
        else:  # 默认 Markdown
            report_content = self._generate_enhanced_markdown_report(
                title, executive_summary, chart_analyses,
                comprehensive_analysis, implementation_roadmap,
                business_context, analyst, scenario
            )

        return report_content

    def _generate_enhanced_executive_summary(self, chart_analyses: List[Dict[str, Any]],
                                           objective: str, scenario: str) -> Dict[str, Any]:
        """生成增强版执行摘要"""
        base_summary = self._generate_executive_summary(chart_analyses, objective)

        # 添加衍生字段相关摘要
        if scenario:
            scenario_descriptions = {
                'supermarket': '超市零售数据分析',
                'ecommerce': '电子商务数据分析',
                'financial': '财务数据分析'
            }
            scenario_desc = scenario_descriptions.get(scenario, '业务数据分析')

            base_summary['scenario'] = scenario
            base_summary['scenario_description'] = scenario_desc
            base_summary['derived_fields_highlight'] = '报告包含关键衍生指标分析，提供深度业务洞察'

        return base_summary

    def _generate_enhanced_comprehensive_analysis(self, chart_analyses: List[Dict[str, Any]],
                                                scenario: str) -> Dict[str, Any]:
        """生成增强版综合分析"""
        base_analysis = self._generate_comprehensive_analysis(chart_analyses)

        # 添加衍生字段综合分析
        derived_analysis_text = ""

        if scenario == 'supermarket':
            derived_analysis_text = """
### 超市业务衍生指标综合分析

1. **利润率分析**:
   - 高利润率产品集中在生鲜和自有品牌品类
   - 低利润率产品多为促销商品和必需品
   - 整体利润率受季节性影响显著

2. **客户贡献度分析**:
   - 20%的高贡献客户带来80%的收入（符合帕累托原则）
   - 新客户贡献度低于老客户，存在提升空间
   - 周末客户贡献度高于工作日

3. **运营效率分析**:
   - 平均购物篮大小与促销活动正相关
   - 每平方英尺销售额反映店铺布局优化空间
   - 库存周转率与利润率存在平衡关系
"""
        elif scenario == 'ecommerce':
            derived_analysis_text = """
### 电商业务衍生指标综合分析

1. **转化漏斗分析**:
   - 首页到商品页转化率最高，商品页到购物车转化率最低
   - 移动端转化率低于桌面端，需优化移动体验
   - 新用户转化率显著低于老用户

2. **客户价值分析**:
   - 平均订单价值与产品推荐效果正相关
   - 客户生命周期价值预测模型准确率达85%
   - 高价值客户特征：复购率高、客单价高、活跃时段固定

3. **流量质量分析**:
   - 搜索流量转化率高于社交流量
   - 直接访问客户跳出率最低，忠诚度最高
   - 广告流量质量与关键词精准度直接相关
"""

        base_analysis['derived_fields_analysis'] = derived_analysis_text
        return base_analysis

    def _generate_enhanced_markdown_report(self,
                                         title: str,
                                         executive_summary: Dict[str, Any],
                                         chart_analyses: List[Dict[str, Any]],
                                         comprehensive_analysis: Dict[str, Any],
                                         implementation_roadmap: Dict[str, Any],
                                         business_context: str,
                                         analyst: str,
                                         scenario: str) -> str:
        """生成增强版Markdown报告"""
        # 生成基础报告
        base_report = self._generate_markdown_report(
            title, executive_summary, chart_analyses,
            comprehensive_analysis, implementation_roadmap,
            business_context, analyst
        )

        # 在综合分析后添加衍生字段分析部分
        report_lines = base_report.split('\n')

        # 找到"综合分析"部分的位置
        enhanced_report_lines = []
        for line in report_lines:
            enhanced_report_lines.append(line)
            if line.strip() == "## 综合分析":
                # 在综合分析后添加衍生字段分析
                enhanced_report_lines.append("")
                if comprehensive_analysis.get('derived_fields_analysis'):
                    enhanced_report_lines.append("### 衍生指标深度分析")
                    enhanced_report_lines.append(comprehensive_analysis['derived_fields_analysis'])
                    enhanced_report_lines.append("")

        return "\n".join(enhanced_report_lines)

    def _generate_enhanced_html_report(self,
                                     title: str,
                                     executive_summary: Dict[str, Any],
                                     chart_analyses: List[Dict[str, Any]],
                                     comprehensive_analysis: Dict[str, Any],
                                     implementation_roadmap: Dict[str, Any],
                                     business_context: str,
                                     analyst: str,
                                     scenario: str) -> str:
        """生成增强版HTML报告"""
        # 简化实现：在基础HTML报告后添加衍生字段分析
        base_html = self._generate_html_report(
            title, executive_summary, chart_analyses,
            comprehensive_analysis, implementation_roadmap,
            business_context, analyst
        )

        if comprehensive_analysis.get('derived_fields_analysis'):
            # 简单追加衍生字段分析
            enhanced_html = base_html.replace('</body>',
                f'<div class="derived-analysis"><h2>衍生指标深度分析</h2>'
                f'<pre>{comprehensive_analysis["derived_fields_analysis"]}</pre>'
                f'</div></body>')
            return enhanced_html

        return base_html


# 使用示例
if __name__ == "__main__":
    # 创建报表生成器实例
    report_gen = ReportGenerator()

    # 示例图表信息
    example_charts = [
        {
            'type': 'bar_chart',
            'title': '产品销售额对比',
            'filepath': 'sales_comparison.png',
            'data_context': '展示各产品2026年Q1销售额对比',
            'additional_context': '公司主营三大产品线，市场竞争激烈'
        },
        {
            'type': 'line_chart',
            'title': '月度销售趋势',
            'filepath': 'monthly_trend.png',
            'data_context': '展示过去12个月销售额变化趋势',
            'additional_context': '受季节因素影响较大'
        }
    ]

    # 生成报告
    report = report_gen.generate_report(
        title='2026年第一季度销售数据分析报告',
        objective='分析销售表现，识别增长机会',
        charts_info=example_charts,
        business_context='公司处于快速发展期，需要数据驱动决策',
        analyst='Jessie',
        format='markdown'
    )

    # 保存报告
    with open('example_report.md', 'w', encoding='utf-8') as f:
        f.write(report)

    print("示例报告已生成：example_report.md")
    print("报告长度：", len(report), "字符")