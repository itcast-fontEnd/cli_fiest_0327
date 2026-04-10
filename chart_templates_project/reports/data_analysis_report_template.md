# 数据分析报告模板

## 报告概述
- **报告名称**: [在此填写报告名称]
- **分析目标**: [简要说明本次分析的目标]
- **数据来源**: [数据文件/数据库]
- **分析日期**: [年-月-日]
- **分析师**: [姓名]

## 数据概览

### 数据集描述
- **数据量**: [行数 × 列数]
- **时间范围**: [开始日期 - 结束日期]
- **关键指标**: [列出关键指标]
- **数据质量**: [完整性、准确性评估]

### 样本数据预览
```python
# 数据加载代码示例
import pandas as pd
data = pd.read_csv('your_data.csv')
print(f"数据形状: {data.shape}")
print(data.head())
```

## 分析方法

### 分析框架
1. **数据预处理**: 清洗、转换、标准化
2. **描述性分析**: 统计摘要、分布分析
3. **探索性分析**: 相关性、趋势、模式识别
4. **深度分析**: 聚类、预测、优化
5. **结论与建议**: 业务洞察、行动建议

### 使用工具
- **编程语言**: Python
- **核心库**: pandas, numpy, matplotlib, seaborn
- **图表模板**: 本项目提供的标准化图表模板

## 分析结果

### 1. 数据分布分析

#### 1.1 分类数据分布
使用柱状图展示各类别的数量分布。

```python
from src.chart_template_functions import ChartTemplates

# 初始化模板
templates = ChartTemplates()

# 创建柱状图
categories = ['类别A', '类别B', '类别C', '类别D']
values = [120, 85, 150, 95]
plt = templates.create_bar_chart(
    categories=categories,
    values=values,
    title='分类数据分布',
    xlabel='类别',
    ylabel='数量'
)
plt.savefig('../examples/images/distribution_bar_chart.png', dpi=300)
plt.close()
```

![柱状图示例](../examples/images/distribution_bar_chart.png)

**分析要点**:
- 类别C数量最多，占比XX%
- 类别B数量最少，占比XX%
- 建议重点关注类别C的表现

#### 1.2 比例关系分析
使用饼图展示各部分占比关系。

```python
# 创建饼图
labels = ['部分A', '部分B', '部分C', '部分D']
sizes = [30, 25, 35, 10]
plt = templates.create_pie_chart(
    labels=labels,
    sizes=sizes,
    title='各部分占比分析'
)
plt.savefig('../examples/images/proportion_pie_chart.png', dpi=300)
plt.close()
```

![饼图示例](../examples/images/proportion_pie_chart.png)

### 2. 趋势分析

#### 2.1 时间序列趋势
使用折线图展示关键指标随时间的变化趋势。

```python
# 创建折线图
x_data = ['1月', '2月', '3月', '4月', '5月', '6月']
y_data_list = [
    [120, 135, 142, 158, 165, 180],  # 产品A
    [85, 92, 105, 98, 110, 125],     # 产品B
    [150, 142, 138, 155, 168, 175]   # 产品C
]
labels = ['产品A', '产品B', '产品C']

plt = templates.create_line_chart(
    x_data=x_data,
    y_data_list=y_data_list,
    labels=labels,
    title='各产品月度销售趋势',
    xlabel='月份',
    ylabel='销售额（万元）'
)
plt.savefig('../examples/images/trend_line_chart.png', dpi=300)
plt.close()
```

![折线图示例](../examples/images/trend_line_chart.png)

**趋势分析**:
- 产品A持续增长，6月达到峰值
- 产品B波动较大，4月有所回落
- 产品C呈V型反弹，恢复增长势头

#### 2.2 多指标组合分析
使用条形折线组合图展示数量与比例的双重指标。

```python
# 创建条形折线组合图
categories = ['北京', '上海', '广州', '深圳', '杭州']
bar_values = [120, 95, 85, 110, 75]      # 销售额
line_values = [0.15, 0.18, 0.12, 0.16, 0.14]  # 增长率

plt = templates.create_bar_line_combo(
    categories=categories,
    bar_values=bar_values,
    line_values=line_values,
    bar_label='销售额（万元）',
    line_label='增长率',
    title='各城市销售额与增长率对比'
)
plt.savefig('../examples/images/combo_chart.png', dpi=300)
plt.close()
```

![组合图示例](../examples/images/combo_chart.png)

### 3. 相关性分析

#### 3.1 二维相关性分析
使用散点图分析两个变量之间的关系。

```python
# 创建散点图
np.random.seed(42)
x_data = np.random.normal(100, 15, 100)
y_data = x_data * 0.8 + np.random.normal(0, 10, 100)

plt = templates.create_scatter_plot(
    x_data=x_data,
    y_data=y_data,
    title='销售额与客户满意度关系',
    xlabel='销售额（万元）',
    ylabel='客户满意度（分）'
)
plt.savefig('../examples/images/correlation_scatter.png', dpi=300)
plt.close()
```

![散点图示例](../examples/images/correlation_scatter.png)

**相关性结论**:
- 销售额与客户满意度呈正相关关系
- 相关系数约为0.75，相关性较强
- 建议提升服务质量以促进销售

#### 3.2 多维数据密度分析
使用热力图展示二维数据密度或相关性矩阵。

```python
# 创建热力图示例数据
import seaborn as sns
data = sns.load_dataset('flights').pivot_table(
    index='month', columns='year', values='passengers'
)

plt = templates.create_heatmap(
    data=data,
    title='航班乘客数量热力图',
    xlabel='年份',
    ylabel='月份',
    cmap='YlOrRd',
    annot=True,
    fmt='d'
)
plt.savefig('../examples/images/density_heatmap.png', dpi=300)
plt.close()
```

![热力图示例](../examples/images/density_heatmap.png)

### 4. 高级分析

#### 4.1 帕累托分析
使用帕累托图识别主要因素。

```python
# 创建帕累托图
categories = ['问题A', '问题B', '问题C', '问题D', '问题E', '问题F']
values = [45, 32, 28, 22, 15, 8]

plt = templates.create_pareto_chart(
    categories=categories,
    values=values,
    title='质量问题帕累托分析',
    xlabel='问题类型',
    ylabel='发生频次'
)
plt.savefig('../examples/images/pareto_chart.png', dpi=300)
plt.close()
```

![帕累托图示例](../examples/images/pareto_chart.png)

**帕累托分析结论**:
- 前3个问题（A、B、C）占总问题的68%
- 解决这3个关键问题可显著改善质量

#### 4.2 分组对比分析
使用蝴蝶图进行两组数据对比。

```python
# 创建蝴蝶图
categories = ['产品A', '产品B', '产品C', '产品D', '产品E']
left_values = [120, 85, 150, 95, 110]    # 男性用户
right_values = [95, 105, 120, 85, 100]   # 女性用户

plt = templates.create_butterfly_chart(
    categories=categories,
    left_values=left_values,
    right_values=right_values,
    left_label='男性用户',
    right_label='女性用户',
    title='产品用户性别分布对比'
)
plt.savefig('../examples/images/butterfly_chart.png', dpi=300)
plt.close()
```

![蝴蝶图示例](../examples/images/butterfly_chart.png)

## 关键发现

### 主要发现
1. **发现一**: [用一句话概括]
   - 支持数据: [具体数据]
   - 影响分析: [对业务的影响]

2. **发现二**: [用一句话概括]
   - 支持数据: [具体数据]
   - 影响分析: [对业务的影响]

3. **发现三**: [用一句话概括]
   - 支持数据: [具体数据]
   - 影响分析: [对业务的影响]

### 异常点识别
- **异常点1**: [描述]
  - 可能原因: [分析原因]
  - 建议行动: [处理建议]
- **异常点2**: [描述]
  - 可能原因: [分析原因]
  - 建议行动: [处理建议]

## 结论与建议

### 主要结论
1. **业务表现**: [总体评价]
2. **关键成功因素**: [识别成功因素]
3. **主要挑战**: [识别主要问题]

### 具体建议
#### 短期建议（1-3个月）
1. **建议一**: [具体可执行建议]
   - 预期效果: [量化预期]
   - 负责人: [指定负责人]

2. **建议二**: [具体可执行建议]
   - 预期效果: [量化预期]
   - 负责人: [指定负责人]

#### 中长期建议（3-12个月）
1. **战略建议**: [战略性建议]
   - 实施路径: [实施步骤]
   - 所需资源: [资源需求]

### 后续分析计划
1. **深化分析**: [需要进一步分析的方向]
2. **数据完善**: [数据收集改进建议]
3. **监控指标**: [建议监控的关键指标]

## 附录

### A. 分析方法详细说明
[详细技术细节、算法说明等]

### B. 数据质量报告
[数据清洗、处理过程记录]

### C. 模板使用说明
本项目提供的图表模板位于`../src/chart_template_functions.py`，包含以下功能:

| 函数名 | 用途 | 适用场景 |
|--------|------|----------|
| `create_heatmap()` | 创建热力图 | 二维数据密度、相关性矩阵 |
| `create_line_chart()` | 创建折线图 | 时间序列趋势、多指标对比 |
| `create_bar_chart()` | 创建柱状图 | 分类数据比较、排名展示 |
| `create_pie_chart()` | 创建饼图 | 比例关系展示、份额分布 |
| `create_scatter_plot()` | 创建散点图 | 相关性分析、聚类可视化 |
| `create_multi_column_bar()` | 创建多列条形图 | 多组数据对比、分类细分 |
| `create_stacked_bar()` | 创建分层柱形图 | 构成分析、份额展示 |
| `create_butterfly_chart()` | 创建蝴蝶图 | 两组数据对比 |
| `create_pareto_chart()` | 创建帕累托图 | 主要因素识别 |
| `create_bubble_chart()` | 创建气泡图 | 三维数据可视化 |
| `create_bar_line_combo()` | 创建条形折线组合图 | 多指标组合展示 |

**使用方法**:
```python
# 1. 导入模板
from src.chart_template_functions import ChartTemplates

# 2. 创建实例
templates = ChartTemplates()

# 3. 生成图表
plt = templates.create_bar_chart(categories, values, title='示例图表')

# 4. 保存图表
plt.savefig('output.png', dpi=300, bbox_inches='tight')
plt.close()
```

### D. 报告更新记录
| 版本 | 日期 | 修改内容 | 修改人 |
|------|------|----------|--------|
| 1.0 | 2026-04-08 | 初始版本 | [姓名] |

---
**报告完成时间**: [年-月-日 时:分]  
**报告状态**: [草稿/终稿]  
**保密级别**: [内部公开/机密]