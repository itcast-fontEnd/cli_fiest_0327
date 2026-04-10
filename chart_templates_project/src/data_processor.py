# 数据处理器模块 - 数据清洗、特征工程和字段衍生功能
# 功能：加载数据、清洗、计算衍生字段、为图表准备数据

import json
import os
import numpy as np
from typing import Dict, List, Any, Optional, Union, Tuple
from datetime import datetime

class DataProcessor:
    """数据处理器：负责数据清洗、特征工程和字段衍生"""

    def __init__(self, use_pandas: bool = True):
        """初始化数据处理器

        Args:
            use_pandas: 是否尝试使用pandas（如果可用）
        """
        self.use_pandas = use_pandas
        self.pandas_available = False

        if use_pandas:
            try:
                import pandas as pd
                self.pd = pd
                self.pandas_available = True
                print("Pandas 可用，启用高级数据处理功能")
            except ImportError:
                print("Pandas 不可用，使用基础数据处理功能")

    def load_data(self, filepath: str, **kwargs) -> Any:
        """加载数据文件

        支持格式：CSV, Excel, JSON

        Args:
            filepath: 文件路径
            **kwargs: 传递给加载函数的额外参数

        Returns:
            加载的数据（DataFrame或字典/列表）
        """
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"数据文件不存在: {filepath}")

        ext = os.path.splitext(filepath)[1].lower()

        if self.pandas_available:
            import pandas as pd

            if ext == '.csv':
                return pd.read_csv(filepath, **kwargs)
            elif ext in ['.xlsx', '.xls']:
                return pd.read_excel(filepath, **kwargs)
            elif ext == '.json':
                return pd.read_json(filepath, **kwargs)
            else:
                raise ValueError(f"不支持的文件格式: {ext}")
        else:
            # 基础数据加载（仅支持CSV和JSON）
            if ext == '.csv':
                return self._load_csv_basic(filepath, **kwargs)
            elif ext == '.json':
                return self._load_json_basic(filepath, **kwargs)
            else:
                raise ValueError(f"基础模式不支持的文件格式: {ext}，请安装pandas或使用CSV/JSON格式")

    def _load_csv_basic(self, filepath: str, **kwargs) -> List[Dict[str, Any]]:
        """基础CSV加载（不使用pandas）"""
        import csv

        data = []
        with open(filepath, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                data.append(row)
        return data

    def _load_json_basic(self, filepath: str, **kwargs) -> List[Dict[str, Any]]:
        """基础JSON加载"""
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data

    def clean_data(self, data: Any, cleaning_rules: Dict[str, Any] = None) -> Any:
        """数据清洗

        Args:
            data: 输入数据
            cleaning_rules: 清洗规则字典

        Returns:
            清洗后的数据
        """
        if self.pandas_available and isinstance(data, self.pd.DataFrame):
            return self._clean_data_pandas(data, cleaning_rules)
        else:
            return self._clean_data_basic(data, cleaning_rules)

    def _clean_data_pandas(self, df, cleaning_rules: Dict[str, Any] = None) -> Any:
        """使用pandas进行数据清洗"""
        if cleaning_rules is None:
            cleaning_rules = {}

        # 默认清洗规则
        default_rules = {
            'drop_duplicates': True,
            'fillna_strategy': 'mean',  # 'mean', 'median', 'mode', 'zero', 'ffill'
            'remove_outliers': False,
            'convert_dtypes': True
        }
        default_rules.update(cleaning_rules)
        rules = default_rules

        cleaned_df = df.copy()

        # 删除重复行
        if rules['drop_duplicates']:
            cleaned_df = cleaned_df.drop_duplicates()

        # 处理缺失值
        if rules['fillna_strategy']:
            strategy = rules['fillna_strategy']
            numeric_cols = cleaned_df.select_dtypes(include=[np.number]).columns

            if strategy == 'mean':
                cleaned_df[numeric_cols] = cleaned_df[numeric_cols].fillna(cleaned_df[numeric_cols].mean())
            elif strategy == 'median':
                cleaned_df[numeric_cols] = cleaned_df[numeric_cols].fillna(cleaned_df[numeric_cols].median())
            elif strategy == 'mode':
                for col in numeric_cols:
                    mode_val = cleaned_df[col].mode()
                    if not mode_val.empty:
                        cleaned_df[col] = cleaned_df[col].fillna(mode_val.iloc[0])
            elif strategy == 'zero':
                cleaned_df[numeric_cols] = cleaned_df[numeric_cols].fillna(0)
            elif strategy == 'ffill':
                cleaned_df = cleaned_df.fillna(method='ffill')

            # 非数值列用空字符串填充
            non_numeric_cols = cleaned_df.select_dtypes(exclude=[np.number]).columns
            cleaned_df[non_numeric_cols] = cleaned_df[non_numeric_cols].fillna('')

        # 转换数据类型
        if rules['convert_dtypes']:
            cleaned_df = cleaned_df.infer_objects()

        return cleaned_df

    def _clean_data_basic(self, data: List[Dict[str, Any]], cleaning_rules: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """基础数据清洗（不使用pandas）"""
        if not data:
            return data

        if cleaning_rules is None:
            cleaning_rules = {}

        cleaned_data = []
        seen_rows = set()

        for row in data:
            # 去重（基于行字符串表示）
            row_str = str(sorted(row.items()))
            if row_str in seen_rows:
                continue
            seen_rows.add(row_str)

            cleaned_row = {}
            for key, value in row.items():
                # 处理缺失值
                if value is None or value == '':
                    cleaned_row[key] = ''
                else:
                    cleaned_row[key] = value

            cleaned_data.append(cleaned_row)

        return cleaned_data

    def calculate_basic_stats(self, data: Any, numeric_columns: List[str] = None) -> Dict[str, Any]:
        """计算基本统计量

        Args:
            data: 输入数据
            numeric_columns: 需要统计的数值列名（如未指定则自动检测）

        Returns:
            统计量字典
        """
        if self.pandas_available and isinstance(data, self.pd.DataFrame):
            return self._calculate_stats_pandas(data, numeric_columns)
        else:
            return self._calculate_stats_basic(data, numeric_columns)

    def _calculate_stats_pandas(self, df, numeric_columns: List[str] = None) -> Dict[str, Any]:
        """使用pandas计算统计量"""
        if numeric_columns is None:
            numeric_columns = df.select_dtypes(include=[np.number]).columns.tolist()

        stats = {}
        for col in numeric_columns:
            if col in df.columns:
                col_data = df[col].dropna()
                if len(col_data) > 0:
                    stats[col] = {
                        'count': int(col_data.count()),
                        'mean': float(col_data.mean()),
                        'std': float(col_data.std()),
                        'min': float(col_data.min()),
                        'max': float(col_data.max()),
                        'median': float(col_data.median()),
                        'q25': float(col_data.quantile(0.25)),
                        'q75': float(col_data.quantile(0.75))
                    }

        return stats

    def _calculate_stats_basic(self, data: List[Dict[str, Any]], numeric_columns: List[str] = None) -> Dict[str, Any]:
        """基础统计量计算"""
        if not data:
            return {}

        # 自动检测数值列
        if numeric_columns is None:
            numeric_columns = []
            first_row = data[0]
            for key, value in first_row.items():
                if isinstance(value, (int, float)):
                    numeric_columns.append(key)

        # 收集每列的数据
        col_data = {col: [] for col in numeric_columns}
        for row in data:
            for col in numeric_columns:
                if col in row:
                    value = row[col]
                    if isinstance(value, (int, float)):
                        col_data[col].append(value)

        stats = {}
        for col, values in col_data.items():
            if len(values) > 0:
                values_array = np.array(values)
                stats[col] = {
                    'count': len(values),
                    'mean': float(np.mean(values_array)),
                    'std': float(np.std(values_array)),
                    'min': float(np.min(values_array)),
                    'max': float(np.max(values_array)),
                    'median': float(np.median(values_array)),
                    'q25': float(np.percentile(values_array, 25)),
                    'q75': float(np.percentile(values_array, 75))
                }

        return stats

    def derive_fields(self, data: Any, derivation_rules: Dict[str, Any] = None,
                     scenario: str = None) -> Any:
        """衍生新字段

        Args:
            data: 输入数据
            derivation_rules: 衍生规则字典
            scenario: 业务场景（如 'supermarket', 'ecommerce'）

        Returns:
            包含衍生字段的数据
        """
        if scenario:
            scenario_rules = self._get_scenario_rules(scenario)
            if derivation_rules:
                scenario_rules.update(derivation_rules)
            derivation_rules = scenario_rules

        if self.pandas_available and isinstance(data, self.pd.DataFrame):
            return self._derive_fields_pandas(data, derivation_rules)
        else:
            return self._derive_fields_basic(data, derivation_rules)

    def _get_scenario_rules(self, scenario: str) -> Dict[str, Any]:
        """获取业务场景特定的衍生规则"""
        scenario_rules = {
            'supermarket': {
                # 超市数据分析衍生字段
                'profit_margin': {
                    'formula': 'revenue - cost',
                    'description': '利润 = 收入 - 成本'
                },
                'profit_margin_rate': {
                    'formula': '(revenue - cost) / revenue * 100 if revenue > 0 else 0',
                    'description': '利润率 (%) = (收入 - 成本) / 收入 * 100'
                },
                'customer_contribution': {
                    'formula': 'revenue / customers if customers > 0 else 0',
                    'description': '客户贡献度 = 收入 / 客户数'
                },
                'basket_size': {
                    'formula': 'revenue / transactions if transactions > 0 else 0',
                    'description': '平均购物篮大小 = 收入 / 交易次数'
                },
                'sales_per_sqft': {
                    'formula': 'revenue / area if area > 0 else 0',
                    'description': '每平方英尺销售额 = 收入 / 店铺面积'
                },
                # 新增超市衍生字段
                'gross_margin': {
                    'formula': '(revenue - cost_of_goods) / revenue * 100 if revenue > 0 else 0',
                    'description': '毛利率 (%) = (收入 - 商品成本) / 收入 * 100'
                },
                'inventory_turnover': {
                    'formula': 'cost_of_goods / average_inventory if average_inventory > 0 else 0',
                    'description': '库存周转率 = 销售成本 / 平均库存'
                },
                'customer_traffic': {
                    'formula': 'customers / operating_hours if operating_hours > 0 else 0',
                    'description': '客流量 = 客户数 / 营业小时数'
                },
                'sales_per_customer': {
                    'formula': 'revenue / customers if customers > 0 else 0',
                    'description': '客单价 = 收入 / 客户数'
                },
                'promotion_effectiveness': {
                    'formula': '(promotion_revenue - baseline_revenue) / baseline_revenue * 100 if baseline_revenue > 0 else 0',
                    'description': '促销效果 (%) = (促销期收入 - 基线收入) / 基线收入 * 100'
                },
                'waste_rate': {
                    'formula': 'waste_cost / revenue * 100 if revenue > 0 else 0',
                    'description': '损耗率 (%) = 损耗成本 / 收入 * 100'
                },
                'labor_productivity': {
                    'formula': 'revenue / labor_hours if labor_hours > 0 else 0',
                    'description': '人工生产率 = 收入 / 人工工时'
                }
            },
            'ecommerce': {
                # 电商数据分析衍生字段
                'conversion_rate': {
                    'formula': 'orders / visitors * 100',
                    'description': '转化率 (%) = 订单数 / 访客数 * 100'
                },
                'average_order_value': {
                    'formula': 'revenue / orders if orders > 0 else 0',
                    'description': '平均订单价值 = 收入 / 订单数'
                },
                'customer_lifetime_value': {
                    'formula': 'revenue * repeat_rate * retention_period',
                    'description': '客户生命周期价值 = 收入 * 复购率 * 留存周期'
                },
                'bounce_rate': {
                    'formula': 'bounced_sessions / total_sessions * 100',
                    'description': '跳出率 (%) = 跳出会话数 / 总会话数 * 100'
                }
            },
            'financial': {
                # 财务数据分析衍生字段
                'gross_profit_margin': {
                    'formula': '(revenue - cogs) / revenue * 100',
                    'description': '毛利率 (%) = (收入 - 销售成本) / 收入 * 100'
                },
                'net_profit_margin': {
                    'formula': 'net_income / revenue * 100',
                    'description': '净利率 (%) = 净利润 / 收入 * 100'
                },
                'return_on_assets': {
                    'formula': 'net_income / total_assets * 100',
                    'description': '资产回报率 (%) = 净利润 / 总资产 * 100'
                },
                'current_ratio': {
                    'formula': 'current_assets / current_liabilities',
                    'description': '流动比率 = 流动资产 / 流动负债'
                }
            }
        }

        return scenario_rules.get(scenario, {})

    def _derive_fields_pandas(self, df, derivation_rules: Dict[str, Any]) -> Any:
        """使用pandas衍生字段"""
        if derivation_rules is None:
            return df

        derived_df = df.copy()

        for field_name, rule in derivation_rules.items():
            formula = rule.get('formula', '')
            description = rule.get('description', '')

            # 简单的公式求值（实际应用中可能需要更复杂的解析）
            try:
                # 这里使用pandas的eval函数，但要注意安全性
                # 对于简单公式，可以手动解析
                derived_df[field_name] = self._evaluate_formula_pandas(derived_df, formula)
                if 'description' not in derived_df.attrs:
                    derived_df.attrs['description'] = {}
                derived_df.attrs['description'][field_name] = description
            except Exception as e:
                print(f"衍生字段 '{field_name}' 计算失败: {e}")

        return derived_df

    def _evaluate_formula_pandas(self, df, formula: str):
        """公式求值（支持基本算术和条件）"""
        # 尝试使用pandas的eval（更安全且功能更强大）
        try:
            import pandas as pd
            import numpy as np

            # 清理公式，移除多余空格
            formula = formula.strip()

            # 处理条件表达式 if...else...
            if ' if ' in formula and ' else ' in formula:
                # 使用正则表达式匹配条件表达式模式
                import re
                # 匹配模式: expression if condition else default
                # 支持括号和嵌套，但这里处理简单情况
                pattern = r'^(.+?) if (.+?) else (.+?)$'
                match = re.match(pattern, formula)
                if match:
                    expr = match.group(1).strip()
                    condition = match.group(2).strip()
                    default_expr = match.group(3).strip()

                    try:
                        # 创建包含Series的局部变量字典
                        local_dict = {col: df[col] for col in df.columns}

                        # 评估条件
                        # 使用pd.eval，将DataFrame列作为Series传递
                        condition_result = pd.eval(condition, local_dict=local_dict)

                        # 评估表达式
                        expr_result = pd.eval(expr, local_dict=local_dict)

                        # 评估默认表达式
                        try:
                            default_result = pd.eval(default_expr, local_dict=local_dict)
                        except:
                            # 尝试解析为数值常量
                            try:
                                default_result = float(default_expr)
                            except:
                                default_result = 0

                        # 使用numpy.where应用条件
                        result = pd.Series(np.where(condition_result, expr_result, default_result), index=df.index)
                        return result
                    except Exception as e:
                        print(f"条件表达式求值失败 {formula}: {e}")
                        # 继续尝试其他方法

            # 尝试直接使用pandas eval
            # 对于包含列名的简单算术表达式，pd.eval可以处理
            # 创建包含Series的局部变量字典
            local_dict = {col: df[col] for col in df.columns}
            try:
                result = pd.eval(formula, local_dict=local_dict)
                return result
            except Exception as e1:
                # 如果失败，尝试使用df.to_dict('list')作为备选
                try:
                    result = pd.eval(formula, local_dict=df.to_dict('list'))
                    return result
                except:
                    # 继续尝试其他方法
                    pass

        except Exception as e:
            # 如果pandas eval失败，回退到简单解析
            print(f"pandas eval失败 {formula}: {e}")
            pass

        # 回退到简单解析（处理基本算术）
        # 移除所有空格
        formula_simple = formula.replace(' ', '')

        # 检查是否是简单列名
        if formula_simple in df.columns:
            return df[formula_simple]

        # 尝试解析基本算术运算
        # 支持 +, -, *, / 操作，假设格式为 A op B
        import re

        # 匹配 pattern: column1+column2, column1-column2 等
        # 使用正则表达式匹配操作符
        if re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*[+\-*/][a-zA-Z_][a-zA-Z0-9_]*$', formula_simple):
            if '+' in formula_simple:
                parts = formula_simple.split('+')
                if len(parts) == 2 and parts[0] in df.columns and parts[1] in df.columns:
                    return df[parts[0]] + df[parts[1]]
            elif '-' in formula_simple:
                parts = formula_simple.split('-')
                if len(parts) == 2 and parts[0] in df.columns and parts[1] in df.columns:
                    return df[parts[0]] - df[parts[1]]
            elif '*' in formula_simple:
                parts = formula_simple.split('*')
                if len(parts) == 2 and parts[0] in df.columns and parts[1] in df.columns:
                    return df[parts[0]] * df[parts[1]]
            elif '/' in formula_simple:
                parts = formula_simple.split('/')
                if len(parts) == 2 and parts[0] in df.columns and parts[1] in df.columns:
                    # 避免除零错误
                    denominator = df[parts[1]].replace(0, np.nan)
                    return df[parts[0]] / denominator

        # 尝试作为数值常量
        try:
            # 移除可能的括号
            const_formula = formula_simple.replace('(', '').replace(')', '')
            return float(const_formula)
        except:
            pass

        # 默认返回0
        print(f"警告：无法求值公式 '{formula}'，返回0")
        import pandas as pd
        return pd.Series([0] * len(df), index=df.index)

    def _derive_fields_basic(self, data: List[Dict[str, Any]], derivation_rules: Dict[str, Any]) -> List[Dict[str, Any]]:
        """基础衍生字段计算"""
        if derivation_rules is None:
            return data

        derived_data = []

        for row in data:
            derived_row = row.copy()

            for field_name, rule in derivation_rules.items():
                formula = rule.get('formula', '')
                description = rule.get('description', '')

                try:
                    derived_row[field_name] = self._evaluate_formula_basic(derived_row, formula)
                    # 存储字段描述（在实际行中可能不存储）
                except Exception as e:
                    print(f"衍生字段 '{field_name}' 计算失败: {e}")
                    derived_row[field_name] = None

            derived_data.append(derived_row)

        return derived_data

    def _evaluate_formula_basic(self, row: Dict[str, Any], formula: str):
        """基础公式求值"""
        # 先尝试直接作为Python表达式求值（注意安全性）
        try:
            # 替换列名为row中的值
            local_vars = row.copy()
            # 添加数学函数
            import math
            local_vars.update({k: getattr(math, k) for k in dir(math) if not k.startswith('_')})

            # 添加安全函数
            local_vars.update({
                'max': max,
                'min': min,
                'sum': sum,
                'len': len,
                'abs': abs,
                'round': round
            })

            # 简单的安全检查
            allowed_chars = set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._+-*/()<>!=% ')
            if all(c in allowed_chars for c in formula):
                # 使用安全的eval
                result = eval(formula, {"__builtins__": {}}, local_vars)
                # 处理可能的除零错误
                if isinstance(result, (int, float)) and (result == float('inf') or result == float('-inf')):
                    return 0
                return result
        except ZeroDivisionError:
            return 0
        except Exception as e:
            # 如果eval失败，尝试移除空格后再试
            try:
                formula_no_spaces = formula.replace(' ', '')
                if all(c in allowed_chars for c in formula_no_spaces):
                    return eval(formula_no_spaces, {"__builtins__": {}}, local_vars)
            except:
                pass

        # 回退到简单解析
        formula_simple = formula.replace(' ', '')

        # 处理条件表达式 if...else...
        if 'if' in formula_simple and 'else' in formula_simple:
            # 简单条件表达式解析
            try:
                # 格式: expression if condition else default
                # 找到if和else的位置
                if_pos = formula_simple.find('if')
                else_pos = formula_simple.find('else')

                expr = formula_simple[:if_pos]
                condition = formula_simple[if_pos+2:else_pos]
                default = formula_simple[else_pos+4:]

                # 评估条件
                condition_result = self._evaluate_condition_basic(row, condition)

                if condition_result:
                    return self._evaluate_formula_basic(row, expr)
                else:
                    return self._evaluate_formula_basic(row, default)
            except:
                pass

        # 基本算术运算
        if '+' in formula_simple and formula_simple.count('+') == 1:
            parts = formula_simple.split('+')
            if len(parts) == 2:
                left = self._evaluate_formula_basic(row, parts[0])
                right = self._evaluate_formula_basic(row, parts[1])
                return float(left) + float(right)
        elif '-' in formula_simple and formula_simple.count('-') == 1:
            parts = formula_simple.split('-')
            if len(parts) == 2:
                left = self._evaluate_formula_basic(row, parts[0])
                right = self._evaluate_formula_basic(row, parts[1])
                return float(left) - float(right)
        elif '*' in formula_simple and formula_simple.count('*') == 1:
            parts = formula_simple.split('*')
            if len(parts) == 2:
                left = self._evaluate_formula_basic(row, parts[0])
                right = self._evaluate_formula_basic(row, parts[1])
                return float(left) * float(right)
        elif '/' in formula_simple and formula_simple.count('/') == 1:
            parts = formula_simple.split('/')
            if len(parts) == 2:
                left = self._evaluate_formula_basic(row, parts[0])
                right = self._evaluate_formula_basic(row, parts[1])
                if float(right) == 0:
                    return 0
                return float(left) / float(right)

        # 如果公式就是一个列名，直接返回值
        if formula in row:
            return row[formula]

        # 尝试作为数值字面量
        try:
            return float(formula)
        except:
            return 0

    def _evaluate_condition_basic(self, row: Dict[str, Any], condition: str) -> bool:
        """评估条件表达式"""
        condition = condition.replace(' ', '')

        # 简单条件解析
        if '>' in condition:
            parts = condition.split('>')
            if len(parts) == 2:
                left = self._evaluate_formula_basic(row, parts[0])
                right = self._evaluate_formula_basic(row, parts[1])
                return float(left) > float(right)
        elif '<' in condition:
            parts = condition.split('<')
            if len(parts) == 2:
                left = self._evaluate_formula_basic(row, parts[0])
                right = self._evaluate_formula_basic(row, parts[1])
                return float(left) < float(right)
        elif '>=' in condition:
            parts = condition.split('>=')
            if len(parts) == 2:
                left = self._evaluate_formula_basic(row, parts[0])
                right = self._evaluate_formula_basic(row, parts[1])
                return float(left) >= float(right)
        elif '<=' in condition:
            parts = condition.split('<=')
            if len(parts) == 2:
                left = self._evaluate_formula_basic(row, parts[0])
                right = self._evaluate_formula_basic(row, parts[1])
                return float(left) <= float(right)
        elif '==' in condition:
            parts = condition.split('==')
            if len(parts) == 2:
                left = self._evaluate_formula_basic(row, parts[0])
                right = self._evaluate_formula_basic(row, parts[1])
                return float(left) == float(right)
        elif '!=' in condition:
            parts = condition.split('!=')
            if len(parts) == 2:
                left = self._evaluate_formula_basic(row, parts[0])
                right = self._evaluate_formula_basic(row, parts[1])
                return float(left) != float(right)

        # 默认尝试作为布尔表达式求值
        try:
            local_vars = row.copy()
            result = eval(condition, {"__builtins__": {}}, local_vars)
            return bool(result)
        except:
            return False

    def prepare_chart_data(self, data: Any, chart_type: str,
                          x_column: str = None, y_columns: List[str] = None,
                          **kwargs) -> Dict[str, Any]:
        """为特定图表类型准备数据

        Args:
            data: 输入数据
            chart_type: 图表类型
            x_column: X轴列名
            y_columns: Y轴列名列表
            **kwargs: 其他参数

        Returns:
            适合图表函数的数据字典
        """
        if self.pandas_available and isinstance(data, self.pd.DataFrame):
            return self._prepare_chart_data_pandas(data, chart_type, x_column, y_columns, **kwargs)
        else:
            return self._prepare_chart_data_basic(data, chart_type, x_column, y_columns, **kwargs)

    def _prepare_chart_data_pandas(self, df, chart_type: str,
                                  x_column: str = None, y_columns: List[str] = None,
                                  **kwargs) -> Dict[str, Any]:
        """使用pandas准备图表数据"""
        result = {}

        if chart_type in ['bar_chart', 'pie_chart', 'pareto_chart']:
            # 需要类别和数值
            if x_column is None:
                # 使用第一个非数值列作为类别
                non_numeric_cols = df.select_dtypes(exclude=[np.number]).columns
                x_column = non_numeric_cols[0] if len(non_numeric_cols) > 0 else df.columns[0]

            if y_columns is None:
                # 使用第一个数值列作为数值
                numeric_cols = df.select_dtypes(include=[np.number]).columns
                y_columns = [numeric_cols[0]] if len(numeric_cols) > 0 else [df.columns[1]]

            result['categories'] = df[x_column].tolist()
            result['values'] = df[y_columns[0]].tolist()

            if chart_type == 'pareto_chart':
                # 帕累托图需要排序
                sorted_indices = np.argsort(result['values'])[::-1]
                result['categories'] = [result['categories'][i] for i in sorted_indices]
                result['values'] = [result['values'][i] for i in sorted_indices]

        elif chart_type == 'line_chart':
            if x_column is None:
                # 使用索引或第一个列作为X轴
                x_column = df.columns[0]

            if y_columns is None:
                # 使用所有数值列作为Y轴
                y_columns = df.select_dtypes(include=[np.number]).columns.tolist()

            result['x_data'] = df[x_column].tolist()
            result['y_data_list'] = [df[col].tolist() for col in y_columns]
            result['labels'] = y_columns

        elif chart_type == 'scatter_plot':
            if x_column is None or y_columns is None:
                # 使用前两个数值列
                numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
                if len(numeric_cols) >= 2:
                    x_column = numeric_cols[0]
                    y_columns = [numeric_cols[1]]

            result['x_data'] = df[x_column].tolist()
            result['y_data'] = df[y_columns[0]].tolist()

            # 可选的颜色和大小
            if 'color_column' in kwargs:
                result['colors'] = df[kwargs['color_column']].tolist()
            if 'size_column' in kwargs:
                result['sizes'] = df[kwargs['size_column']].tolist()

        elif chart_type == 'heatmap':
            # 热力图需要矩阵数据
            if 'matrix_data' in kwargs:
                result['data'] = kwargs['matrix_data']
            else:
                # 从数据框创建相关性矩阵
                numeric_df = df.select_dtypes(include=[np.number])
                if len(numeric_df.columns) > 1:
                    result['data'] = numeric_df.corr().values
                else:
                    raise ValueError("热力图需要至少两个数值列")

        elif chart_type == 'multi_column_bar':
            if x_column is None:
                non_numeric_cols = df.select_dtypes(exclude=[np.number]).columns
                x_column = non_numeric_cols[0] if len(non_numeric_cols) > 0 else df.columns[0]

            if y_columns is None:
                y_columns = df.select_dtypes(include=[np.number]).columns.tolist()[:3]  # 取前3个数值列

            result['categories'] = df[x_column].tolist()
            result['data_dict'] = {col: df[col].tolist() for col in y_columns}

        elif chart_type == 'stacked_bar':
            if x_column is None:
                non_numeric_cols = df.select_dtypes(exclude=[np.number]).columns
                x_column = non_numeric_cols[0] if len(non_numeric_cols) > 0 else df.columns[0]

            if y_columns is None:
                y_columns = df.select_dtypes(include=[np.number]).columns.tolist()[:3]

            result['categories'] = df[x_column].tolist()
            result['data_layers'] = [df[col].tolist() for col in y_columns]
            result['layer_names'] = y_columns

        elif chart_type == 'bubble_chart':
            if x_column is None or y_columns is None:
                numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
                if len(numeric_cols) >= 3:
                    x_column = numeric_cols[0]
                    y_columns = [numeric_cols[1]]
                    size_column = numeric_cols[2]

            result['x_data'] = df[x_column].tolist()
            result['y_data'] = df[y_columns[0]].tolist()
            result['sizes'] = df[size_column].tolist()

        return result

    def _prepare_chart_data_basic(self, data: List[Dict[str, Any]], chart_type: str,
                                 x_column: str = None, y_columns: List[str] = None,
                                 **kwargs) -> Dict[str, Any]:
        """基础图表数据准备"""
        if not data:
            return {}

        result = {}
        first_row = data[0]

        if chart_type in ['bar_chart', 'pie_chart', 'pareto_chart']:
            if x_column is None:
                # 使用第一个字符串类型的键
                x_column = next((k for k, v in first_row.items() if isinstance(v, str)), list(first_row.keys())[0])

            if y_columns is None:
                # 使用第一个数值类型的键
                y_columns = [next((k for k, v in first_row.items() if isinstance(v, (int, float))), list(first_row.keys())[1])]

            categories = []
            values = []
            for row in data:
                if x_column in row and y_columns[0] in row:
                    categories.append(str(row[x_column]))
                    values.append(float(row[y_columns[0]]))

            result['categories'] = categories
            result['values'] = values

            if chart_type == 'pareto_chart':
                # 排序
                sorted_indices = np.argsort(values)[::-1]
                result['categories'] = [categories[i] for i in sorted_indices]
                result['values'] = [values[i] for i in sorted_indices]

        elif chart_type == 'line_chart':
            if x_column is None:
                x_column = list(first_row.keys())[0]

            if y_columns is None:
                y_columns = [k for k, v in first_row.items() if isinstance(v, (int, float))]
                if not y_columns:
                    y_columns = [list(first_row.keys())[1]]

            x_data = []
            y_data_dict = {col: [] for col in y_columns}

            for row in data:
                if x_column in row:
                    x_data.append(row[x_column])
                    for col in y_columns:
                        if col in row:
                            y_data_dict[col].append(float(row[col]))
                        else:
                            y_data_dict[col].append(0)

            result['x_data'] = x_data
            result['y_data_list'] = [y_data_dict[col] for col in y_columns]
            result['labels'] = y_columns

        return result

    def generate_data_summary_report(self, data: Any, output_format: str = 'markdown') -> str:
        """生成数据摘要报告

        Args:
            data: 输入数据
            output_format: 输出格式 ('markdown' 或 'html')

        Returns:
            数据摘要报告
        """
        if self.pandas_available and isinstance(data, self.pd.DataFrame):
            return self._generate_summary_pandas(data, output_format)
        else:
            return self._generate_summary_basic(data, output_format)

    def _generate_summary_pandas(self, df, output_format: str) -> str:
        """使用pandas生成数据摘要"""
        report_lines = []

        report_lines.append("# 数据摘要报告")
        report_lines.append(f"**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report_lines.append(f"**数据形状**: {df.shape[0]} 行 × {df.shape[1]} 列")
        report_lines.append("")

        report_lines.append("## 1. 数据概览")
        report_lines.append("### 前5行数据")
        report_lines.append(df.head().to_markdown())
        report_lines.append("")

        report_lines.append("### 数据类型")
        dtypes_df = df.dtypes.reset_index()
        dtypes_df.columns = ['列名', '数据类型']
        report_lines.append(dtypes_df.to_markdown(index=False))
        report_lines.append("")

        report_lines.append("## 2. 基本统计")
        report_lines.append("### 数值列统计摘要")
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 0:
            report_lines.append(df[numeric_cols].describe().to_markdown())
        else:
            report_lines.append("无数值列")
        report_lines.append("")

        report_lines.append("### 缺失值统计")
        missing_df = df.isnull().sum().reset_index()
        missing_df.columns = ['列名', '缺失值数量']
        missing_df['缺失比例%'] = (missing_df['缺失值数量'] / len(df) * 100).round(2)
        report_lines.append(missing_df.to_markdown(index=False))
        report_lines.append("")

        report_lines.append("## 3. 数据质量评估")
        # 简单质量评估
        quality_metrics = {
            '完整性': f"{((1 - df.isnull().sum().sum() / (df.shape[0] * df.shape[1])) * 100):.1f}%",
            '唯一性': f"{(df.nunique().sum() / (df.shape[0] * df.shape[1]) * 100):.1f}%",
            '数据类型一致性': "良好" if df.dtypes.nunique() <= 5 else "需检查"
        }

        for metric, value in quality_metrics.items():
            report_lines.append(f"- **{metric}**: {value}")

        return "\n".join(report_lines)

    def _generate_summary_basic(self, data: List[Dict[str, Any]], output_format: str) -> str:
        """基础数据摘要生成"""
        if not data:
            return "# 数据摘要报告\n\n数据为空"

        report_lines = []
        first_row = data[0]

        report_lines.append("# 数据摘要报告")
        report_lines.append(f"**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report_lines.append(f"**数据行数**: {len(data)} 行")
        report_lines.append(f"**数据列数**: {len(first_row)} 列")
        report_lines.append("")

        report_lines.append("## 1. 数据概览")
        report_lines.append("### 前5行数据")
        report_lines.append("| " + " | ".join(first_row.keys()) + " |")
        report_lines.append("|" + "|".join(["---"] * len(first_row)) + "|")

        for i, row in enumerate(data[:5]):
            values = [str(row.get(key, '')) for key in first_row.keys()]
            report_lines.append("| " + " | ".join(values) + " |")
        report_lines.append("")

        report_lines.append("### 列信息")
        report_lines.append("| 列名 | 数据类型 | 示例值 |")
        report_lines.append("|---|---|---|")

        for key in first_row.keys():
            value = first_row[key]
            dtype = type(value).__name__
            sample = str(value)[:50] + "..." if len(str(value)) > 50 else str(value)
            report_lines.append(f"| {key} | {dtype} | {sample} |")
        report_lines.append("")

        report_lines.append("## 2. 基本统计")
        # 计算数值列的统计
        numeric_keys = [k for k, v in first_row.items() if isinstance(v, (int, float))]

        if numeric_keys:
            report_lines.append("### 数值列统计摘要")
            report_lines.append("| 列名 | 最小值 | 最大值 | 平均值 | 中位数 |")
            report_lines.append("|---|---|---|---|---|")

            for key in numeric_keys:
                values = [float(row[key]) for row in data if key in row and isinstance(row[key], (int, float))]
                if values:
                    report_lines.append(f"| {key} | {min(values):.2f} | {max(values):.2f} | {np.mean(values):.2f} | {np.median(values):.2f} |")
        else:
            report_lines.append("无数值列")

        return "\n".join(report_lines)

    def export_data(self, data: Any, filepath: str, **kwargs) -> str:
        """导出数据到文件

        Args:
            data: 要导出的数据
            filepath: 输出文件路径
            **kwargs: 导出参数

        Returns:
            导出文件路径
        """
        ext = os.path.splitext(filepath)[1].lower()

        if self.pandas_available and isinstance(data, self.pd.DataFrame):
            import pandas as pd

            if ext == '.csv':
                data.to_csv(filepath, index=False, **kwargs)
            elif ext in ['.xlsx', '.xls']:
                data.to_excel(filepath, index=False, **kwargs)
            elif ext == '.json':
                data.to_json(filepath, orient='records', **kwargs)
            else:
                raise ValueError(f"不支持的导出格式: {ext}")
        else:
            # 基础导出
            if ext == '.csv':
                self._export_csv_basic(data, filepath, **kwargs)
            elif ext == '.json':
                self._export_json_basic(data, filepath, **kwargs)
            else:
                raise ValueError(f"基础模式不支持的导出格式: {ext}")

        return filepath

    def _export_csv_basic(self, data: List[Dict[str, Any]], filepath: str, **kwargs):
        """基础CSV导出"""
        import csv

        if not data:
            return

        with open(filepath, 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)

    def _export_json_basic(self, data: List[Dict[str, Any]], filepath: str, **kwargs):
        """基础JSON导出"""
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2, **kwargs)


# 使用示例
if __name__ == "__main__":
    # 创建数据处理器
    processor = DataProcessor()

    # 示例数据
    example_data = [
        {'product': 'A', 'revenue': 1000, 'cost': 600, 'customers': 50},
        {'product': 'B', 'revenue': 1500, 'cost': 800, 'customers': 60},
        {'product': 'C', 'revenue': 800, 'cost': 400, 'customers': 40}
    ]

    print("=== 数据处理器示例 ===")

    # 衍生字段（超市场景）
    derived_data = processor.derive_fields(example_data, scenario='supermarket')
    print("衍生字段后的数据:", derived_data)

    # 计算统计
    stats = processor.calculate_basic_stats(example_data)
    print("基本统计:", stats)

    # 准备图表数据
    chart_data = processor.prepare_chart_data(example_data, 'bar_chart', x_column='product', y_columns=['revenue'])
    print("图表数据:", chart_data)

    # 生成摘要报告
    summary = processor.generate_data_summary_report(example_data)
    print("\n数据摘要报告:")
    print(summary[:500], "...")