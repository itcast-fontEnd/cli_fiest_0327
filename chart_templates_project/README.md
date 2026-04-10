# 图表模板项目

## 项目简介

这是一个可复用的数据可视化图表模板系统，提供标准化的图表生成函数和配置，帮助数据分析师快速创建高质量、风格一致的图表。

## 快速导航

- 📚 **[详细使用指南](docs/README.md)** - 完整的使用说明和示例
- ⚙️ **[配置文件](config/)** - 图表模板配置
- 📊 **[示例代码](examples/)** - 使用示例和演示脚本
- 📈 **[报告模板](reports/)** - 数据分析报告模板
- 🧪 **[测试文件](tests/)** - 功能测试

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 运行演示

```bash
python examples/demo_usage.py
```

### 3. 在项目中使用

```python
from src.chart_template_functions import ChartTemplates

# 初始化模板
templates = ChartTemplates()

# 创建图表
plt = templates.create_bar_chart(
    categories=['A', 'B', 'C'],
    values=[10, 20, 15],
    title='示例图表'
)

# 保存图表
plt.savefig('output.png', dpi=300, bbox_inches='tight')
plt.close()
```

## 项目结构

```
chart_templates_project/
├── config/           # 配置文件
├── src/              # 源代码
├── examples/         # 示例文件
├── reports/          # 报告文件
├── docs/             # 文档
├── tests/            # 测试文件
├── requirements.txt  # 依赖列表
└── setup.py          # 安装配置
```

## 主要功能

- ✅ 11种图表类型的标准化模板
- ✅ 可配置的颜色方案和样式
- ✅ 完整的使用示例和演示脚本
- ✅ 数据分析报告模板
- ✅ 单元测试覆盖

## 支持与反馈

如需帮助或提供反馈，请参考详细文档或联系项目维护者。

---

**版本**: 1.1.0  
**最后更新**: 2026年4月8日