# 图表模板使用指南

## 概述
本指南介绍如何使用项目中创建的可复用图表模板系统，用于快速生成标准化、高质量的数据可视化图表。

## 项目结构
项目采用模块化设计，便于维护和扩展：

```
chart_templates_project/
├── config/           # 配置文件
│   └── chart_templates.json
├── src/              # 源代码
│   └── chart_template_functions.py
├── examples/         # 示例文件
│   ├── images/       # 示例图片
│   └── demo_usage.py
├── reports/          # 报告文件
│   ├── data_analysis_report_template.md
│   ├── chart_catalog_report.html
│   ├── chart_analysis_report.md
│   └── summary_report.md
├── docs/             # 文档
│   ├── README.md (本文件)
│   └── file_list.md
└── tests/            # 测试文件
```

## 快速开始

### 1. 安装依赖
```bash
pip install matplotlib seaborn pandas numpy
```

### 2. 基础使用
```python
# 导入模板类
from src.chart_template_functions import ChartTemplates

# 创建实例
templates = ChartTemplates()

# 准备数据
import pandas as pd
data = pd.read_csv('your_data.csv')

# 创建热力图示例
plt = templates.create_heatmap(
    data=data,
    title='你的图表标题',
    xlabel='X轴标签',
    ylabel='Y轴标签',
    cmap='YlOrRd'  # 颜色方案
)

# 保存图表
plt.savefig('output.png', dpi=300, bbox_inches='tight')
plt.close()
```

## 可用模板函数

### 1. create_heatmap() - 创建热力图
**适用场景：** 二维数据密度、相关性分析、聚类结果展示

```python
plt = templates.create_heatmap(
    data,                    # DataFrame或二维数组
    title='热力图',          # 图表标题
    xlabel='X轴',           # X轴标签
    ylabel='Y轴',           # Y轴标签
    cmap='YlOrRd',          # 颜色映射
    figsize=(14, 10),       # 图表尺寸
    annot=True,             # 是否显示数值
    fmt='.1f'               # 数值格式
)
```

### 2. create_line_chart() - 创建折线图
**适用场景：** 时间序列趋势、多指标对比

```python
plt = templates.create_line_chart(
    x_data,                 # X轴数据（如时间列表）
    y_data_list,            # Y轴数据列表（多个序列）
    labels,                 # 图例标签列表
    title='折线图',         # 图表标题
    xlabel='时间',          # X轴标签
    ylabel='数值',          # Y轴标签
    figsize=(12, 8)         # 图表尺寸
)
```

### 3. create_bar_chart() - 创建柱状图
**适用场景：** 分类数据比较、排名展示

```python
plt = templates.create_bar_chart(
    categories,             # 类别列表
    values,                 # 数值列表
    title='柱状图',         # 图表标题
    xlabel='类别',          # X轴标签
    ylabel='数值',          # Y轴标签
    figsize=(10, 6)         # 图表尺寸
)
```

### 4. create_pie_chart() - 创建饼图
**适用场景：** 比例关系展示、份额分布

```python
plt = templates.create_pie_chart(
    labels,                 # 标签列表
    sizes,                  # 数值列表
    title='饼图',           # 图表标题
    figsize=(8, 8)          # 图表尺寸
)
```

### 5. create_scatter_plot() - 创建散点图
**适用场景：** 相关性分析、聚类可视化

```python
plt = templates.create_scatter_plot(
    x_data,                 # X轴数据
    y_data,                 # Y轴数据
    colors=None,            # 颜色数据（可选）
    sizes=None,             # 点大小数据（可选）
    title='散点图',         # 图表标题
    xlabel='X轴',           # X轴标签
    ylabel='Y轴',           # Y轴标签
    figsize=(10, 8)         # 图表尺寸
)
```

### 6. create_multi_column_bar() - 创建多列条形图
**适用场景：** 多组数据对比、分类细分比较、多维度分析

```python
plt = templates.create_multi_column_bar(
    categories,             # 类别列表
    data_dict,              # 数据字典 {组名: 数值列表}
    title='多列条形图',     # 图表标题
    xlabel='类别',          # X轴标签
    ylabel='数值',          # Y轴标签
    figsize=(12, 8)         # 图表尺寸
)
```

### 7. create_stacked_bar() - 创建分层柱形图
**适用场景：** 构成分析、份额展示、累积效果展示

```python
plt = templates.create_stacked_bar(
    categories,             # 类别列表
    data_layers,            # 数据层列表 [层1数据, 层2数据, ...]
    layer_names,            # 层名称列表
    title='分层柱形图',     # 图表标题
    xlabel='类别',          # X轴标签
    ylabel='数值',          # Y轴标签
    figsize=(12, 8)         # 图表尺寸
)
```

### 8. create_butterfly_chart() - 创建蝴蝶图
**适用场景：** 两组数据对比、男女比例、收支对比、AB测试结果

```python
plt = templates.create_butterfly_chart(
    categories,             # 类别列表
    left_values,            # 左侧数值列表
    right_values,           # 右侧数值列表
    left_label='左侧',      # 左侧标签
    right_label='右侧',     # 右侧标签
    title='蝴蝶图',         # 图表标题
    figsize=(10, 6)         # 图表尺寸
)
```

### 9. create_pareto_chart() - 创建帕累托图
**适用场景：** 问题分析、原因识别、优先级排序、质量改进

```python
plt = templates.create_pareto_chart(
    categories,             # 类别列表
    values,                 # 数值列表
    title='帕累托图',       # 图表标题
    xlabel='类别',          # X轴标签
    ylabel='频次',          # Y轴标签
    figsize=(12, 8)         # 图表尺寸
)
```

### 10. create_bubble_chart() - 创建气泡图
**适用场景：** 三维数据展示、多维度分析、聚类可视化

```python
plt = templates.create_bubble_chart(
    x_data,                 # X轴数据
    y_data,                 # Y轴数据
    sizes,                  # 气泡大小数据
    colors=None,            # 颜色数据（可选）
    title='气泡图',         # 图表标题
    xlabel='X轴',           # X轴标签
    ylabel='Y轴',           # Y轴标签
    size_label='大小',      # 大小标签说明
    figsize=(12, 8)         # 图表尺寸
)
```

### 11. create_bar_line_combo() - 创建条形折线组合图
**适用场景：** 多指标对比、实际vs目标、趋势与数量结合

```python
plt = templates.create_bar_line_combo(
    categories,             # 类别列表
    bar_values,             # 柱状图数值
    line_values,            # 折线图数值
    bar_label='数量',       # 柱状图标签
    line_label='比例',      # 折线图标签
    title='条形折线组合图', # 图表标题
    xlabel='类别',          # X轴标签
    ylabel='数值',          # Y轴标签
    figsize=(12, 8)         # 图表尺寸
)
```

### 12. create_waterfall_chart() - 创建瀑布图
**适用场景：** 财务分析、利润分解、预算变化、累积效果展示

```python
plt = templates.create_waterfall_chart(
    categories,             # 类别列表
    values,                 # 数值列表（包含正负值）
    title='瀑布图',         # 图表标题
    xlabel='类别',          # X轴标签
    ylabel='数值',          # Y轴标签
    figsize=(12, 8)         # 图表尺寸
)
```

### 13. create_bubble_bar_chart() - 创建气泡条形图
**适用场景：** 多维度分析、绩效评估、产品对比、市场细分

```python
plt = templates.create_bubble_bar_chart(
    categories,             # 类别列表
    bar_values,             # 条形图数值
    bubble_sizes,           # 气泡大小数据
    colors=None,            # 颜色数据（可选）
    title='气泡条形图',     # 图表标题
    xlabel='类别',          # X轴标签
    ylabel='数值',          # Y轴标签
    size_label='大小',      # 大小标签说明
    figsize=(12, 8)         # 图表尺寸
)
```

### 14. create_bubble_chart_2() - 创建增强型气泡图
**适用场景：** 四维数据分析、多变量关系、复杂聚类可视化、高级数据分析

```python
plt = templates.create_bubble_chart_2(
    x_data,                 # X轴数据
    y_data,                 # Y轴数据
    sizes,                  # 气泡大小数据
    colors,                 # 颜色数据（第四维度）
    title='增强型气泡图',   # 图表标题
    xlabel='X轴',           # X轴标签
    ylabel='Y轴',           # Y轴标签
    size_label='大小',      # 大小标签说明
    color_label='颜色',     # 颜色标签说明
    figsize=(12, 8)         # 图表尺寸
)
```

## 模板配置

### 配置文件位置
- `config/chart_templates.json` - 包含所有模板的详细配置

### 配置内容
每个模板包含：
- `description`: 模板描述
- `recommended_size`: 推荐图表尺寸
- `aspect_ratio`: 宽高比
- `color_palette`: 推荐颜色方案
- `best_for`: 适用场景
- `code_snippet`: 代码示例
- `example_use_case`: 使用案例

## 实际应用示例

### 示例1：主播活动分析
```python
# 加载主播活动数据
df_anchor = pd.read_csv('主播活动数据.csv')

# 创建主播活动热力图
plt = templates.create_heatmap(
    data=df_anchor.pivot_table(index='主播', columns='小时', values='活动量'),
    title='主播24小时活动热力图',
    xlabel='小时 (0-23)',
    ylabel='主播',
    cmap='YlOrRd'
)
plt.savefig('主播活动热力图.png', dpi=300)
plt.close()
```

### 示例2：渠道趋势分析
```python
# 加载渠道数据
df_channel = pd.read_csv('渠道数据.csv')

# 创建渠道趋势折线图
channels = ['渠道A', '渠道B', '渠道C']
y_data_list = [
    df_channel[df_channel['渠道'] == '渠道A']['成交量'].values,
    df_channel[df_channel['渠道'] == '渠道B']['成交量'].values,
    df_channel[df_channel['渠道'] == '渠道C']['成交量'].values
]

plt = templates.create_line_chart(
    x_data=range(24),
    y_data_list=y_data_list,
    labels=channels,
    title='各渠道24小时成交量趋势',
    xlabel='小时',
    ylabel='成交量'
)
plt.savefig('渠道趋势图.png', dpi=300)
plt.close()
```

## 高级功能：自动报表生成

除了创建图表，项目还提供了自动报表生成功能，可以基于图表生成专业的数据分析报告。

### 1. 报表生成器介绍

报表生成器 (`src/report_generator.py`) 提供以下功能：
- 为每种图表类型提供预设的分析模板
- 自动生成观察要点、业务含义、结论和建议
- 支持生成完整的数据分析报告（Markdown 或 HTML 格式）
- 包含执行摘要、详细分析、实施路线图等标准报告结构

### 2. 快速开始

```python
# 导入报表生成器
from src.report_generator import ReportGenerator

# 创建实例
report_gen = ReportGenerator()

# 准备图表信息
charts_info = [
    {
        'type': 'bar_chart',           # 图表类型
        'title': '产品销售额对比',     # 图表标题
        'filepath': 'sales_comparison.png',  # 图表文件路径
        'data_context': '展示各产品2026年Q1销售额对比',  # 数据说明
        'additional_context': '公司主营三大产品线，市场竞争激烈'  # 业务上下文
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
    charts_info=charts_info,
    business_context='公司处于快速发展期，需要数据驱动决策',
    analyst='Jessie',
    format='markdown'  # 或 'html'
)

# 保存报告
with open('analysis_report.md', 'w', encoding='utf-8') as f:
    f.write(report)
```

### 3. 分析模板定制

报表生成器为每种图表类型提供了预设的分析模板，包含：
- **关键问题**：针对该图表类型的核心分析问题
- **观察要点**：数据分析的关注点
- **业务含义**：分析结果对业务决策的意义
- **结论框架**：结构化结论模板
- **建议框架**：针对性建议模板

### 4. 支持的分析模板类型

报表生成器支持所有14种图表类型的分析模板：
- 柱状图 (`bar_chart`) - 分类比较分析
- 折线图 (`line_chart`) - 趋势分析
- 饼图 (`pie_chart`) - 比例分析
- 热力图 (`heatmap`) - 密度和相关性分析
- 散点图 (`scatter_plot`) - 相关性和聚类分析
- 多列条形图 (`multi_column_bar`) - 多组对比分析
- 分层柱形图 (`stacked_bar`) - 构成分析
- 蝴蝶图 (`butterfly_chart`) - 两组对比分析
- 帕累托图 (`pareto_chart`) - 优先级分析
- 气泡图 (`bubble_chart`) - 三维数据分析
- 条形折线组合图 (`bar_line_combo`) - 多指标分析
- 瀑布图 (`waterfall_chart`) - 累积变化分析
- 气泡条形图 (`bubble_bar_chart`) - 多维度分析
- 增强型气泡图 (`bubble_chart_2`) - 四维数据分析

### 5. 报告结构

生成的报告包含以下标准部分：
1. **执行摘要** - 关键发现和优先级建议
2. **详细分析** - 每个图表的深入分析
3. **综合分析** - 模式关联和业务影响评估
4. **实施路线图** - 具体行动计划和时间表
5. **附录** - 方法论和数据来源说明

## 最佳实践

### 1. 数据准备
- 确保数据格式正确
- 处理缺失值
- 适当的数据归一化

### 2. 图表选择
- 趋势分析 → 折线图
- 分类比较 → 柱状图、多列条形图、蝴蝶图
- 比例展示 → 饼图、分层柱形图、瀑布图
- 密度分析 → 热力图
- 相关性 → 散点图、气泡图、增强型气泡图
- 优先级排序 → 帕累托图
- 多指标对比 → 条形折线组合图
- 多维度分析 → 气泡条形图
- 三维数据展示 → 气泡图
- 四维数据分析 → 增强型气泡图

### 3. 视觉优化
- 使用模板推荐的颜色方案
- 保持一致的图表尺寸
- 添加清晰的标题和标签
- 合理使用图例

### 4. 输出设置
- 使用dpi=300保证打印质量
- 使用bbox_inches='tight'避免裁剪
- 选择合适的文件格式（PNG用于网络，PDF用于印刷）

## 文件说明

### 核心文件
- `config/chart_templates.json` - 模板配置文件
- `src/chart_template_functions.py` - 模板函数实现

### 示例文件
- `examples/images/template_example_*.png` - 各种图表类型的示例
- `examples/demo_usage.py` - 完整使用示例脚本

### 分析报告
- `reports/chart_catalog_report.html` - 交互式图表目录
- `reports/chart_analysis_report.md` - 详细分析报告
- `reports/summary_report.md` - 项目总结报告
- `reports/data_analysis_report_template.md` - 数据分析报告模板

## 故障排除

### 常见问题
1. **导入错误**：确保已安装matplotlib和seaborn
2. **中文显示问题**：检查系统中文字体配置
3. **图表尺寸异常**：检查输入数据的维度
4. **颜色方案无效**：使用matplotlib内置颜色方案名称

### 调试建议
```python
# 打印模板配置
import json
with open('config/chart_templates.json', 'r', encoding='utf-8') as f:
    templates_config = json.load(f)
    print(json.dumps(templates_config, indent=2, ensure_ascii=False))
```

## 扩展开发

### 添加新模板
1. 在`config/chart_templates.json`中添加新模板配置
2. 在`src/chart_template_functions.py`的`ChartTemplates`类中添加新方法
3. 更新使用示例和文档

### 自定义样式
- 修改`chart_template_functions.py`中的默认参数
- 创建子类覆盖默认样式
- 添加自定义颜色方案

## 支持与反馈
- 查看`reports/chart_catalog_report.html`获取详细图表目录
- 参考示例代码快速上手
- 根据实际需求调整模板参数

---

**最后更新：** 2026年4月8日  
**版本：** 1.1.0  
**作者：** 数据分析团队