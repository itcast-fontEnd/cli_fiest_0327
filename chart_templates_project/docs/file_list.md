# 图表模板项目文件清单

## 目录结构

```
chart_templates_project/
├── chart_templates.json          # 模板配置文件
├── chart_template_functions.py   # 模板复用函数
├── template_example_bar_chart.png     # 柱状图示例
├── template_example_heatmap.png       # 热力图示例
├── template_example_line_chart.png    # 折线图示例
├── template_example_pie_chart.png     # 饼图示例
├── template_example_scatter_plot.png  # 散点图示例
├── chart_catalog_report.html     # 交互式图表目录
├── chart_analysis_report.md      # 图表分析报告
├── 图表分析总结报告.md           # 项目总结报告
└── README_图表模板使用指南.md    # 使用文档
```

## 文件说明

### chart_templates.json
- **类型**: JSON配置文件
- **描述**: 包含所有图表模板的配置参数，如颜色、样式、布局等
- **用途**: 为图表生成提供统一的样式配置

### chart_template_functions.py
- **类型**: Python脚本
- **描述**: 包含可复用的图表生成函数，基于模板配置创建图表
- **用途**: 提供API接口供其他脚本调用生成标准化图表

### template_example_*.png
- **类型**: 图片文件（PNG格式）
- **描述**: 5种不同类型的图表示例，展示模板应用效果
- **包含**:
  - 柱状图 (bar_chart)
  - 热力图 (heatmap)
  - 折线图 (line_chart)
  - 饼图 (pie_chart)
  - 散点图 (scatter_plot)

### chart_catalog_report.html
- **类型**: HTML报告
- **描述**: 交互式图表目录，可浏览所有可用模板和示例
- **用途**: 可视化展示模板库内容

### chart_analysis_report.md
- **类型**: Markdown报告
- **描述**: 图表分析报告，包含数据分析和可视化结果
- **用途**: 记录分析过程和发现

### 图表分析总结报告.md
- **类型**: Markdown报告
- **描述**: 项目总结报告，汇总图表模板项目的成果和经验
- **用途**: 项目文档和知识沉淀

### README_图表模板使用指南.md
- **类型**: Markdown文档
- **描述**: 详细的使用指南，说明如何配置和使用图表模板
- **用途**: 新用户入门指南

## 使用说明

1. **配置模板**: 修改 `chart_templates.json` 文件调整图表样式
2. **生成图表**: 调用 `chart_template_functions.py` 中的函数生成图表
3. **查看示例**: 参考 `template_example_*.png` 文件了解模板效果
4. **浏览目录**: 打开 `chart_catalog_report.html` 查看所有可用模板
5. **阅读文档**: 查看 `README_图表模板使用指南.md` 获取详细使用说明

## 更新记录

- 2026-04-07: 项目文件夹创建，文件整理完成