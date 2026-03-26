import pandas as pd
import numpy as np
import re
from datetime import datetime

def load_data(file_path):
    """加载CSV数据"""
    df = pd.read_csv(file_path, encoding='utf-8')
    print(f"原始数据形状: {df.shape}")
    print("\n原始数据前5行:")
    print(df.head())
    print("\n原始数据信息:")
    print(df.info())
    print("\n原始数据缺失值统计:")
    print(df.isnull().sum())
    return df

def clean_employee_id(df):
    """清洗员工ID列：去除重复行"""
    # 记录原始行数
    original_rows = len(df)
    # 去除完全重复的行（基于所有列）
    df = df.drop_duplicates(keep='first')
    # 检查员工ID重复（可能其他列不同）
    duplicate_ids = df[df.duplicated(subset=['员工ID'], keep=False)]
    if not duplicate_ids.empty:
        print(f"发现员工ID重复的行: {len(duplicate_ids)}")
        # 保留第一个出现的记录，删除后续重复
        df = df.drop_duplicates(subset=['员工ID'], keep='first')
    print(f"去除重复后行数: {len(df)} (删除了 {original_rows - len(df)} 行)")
    return df

def clean_name(df):
    """清洗姓名列：去除空格，处理特殊字符，统一格式"""
    # 确保为字符串类型
    df['姓名'] = df['姓名'].astype(str)
    # 去除前后空格
    df['姓名'] = df['姓名'].str.strip()
    # 将NaN重新设为空字符串
    df['姓名'] = df['姓名'].replace('nan', '', regex=False)
    df['姓名'] = df['姓名'].replace('NaN', '', regex=False)
    # 处理特殊字符：保留中文字符和点号（如·），移除其他特殊字符
    # 姓名中可能包含·作为分隔符，保留它
    df['姓名'] = df['姓名'].apply(lambda x: re.sub(r'[^a-zA-Z\u4e00-\u9fff·\s]', '', x))
    # 统一格式：首字母大写（针对英文名），中文名保持不变
    df['姓名'] = df['姓名'].apply(lambda x: x.title() if x and any(c.isalpha() for c in x) else x)
    # 将空字符串重新设为NaN
    df['姓名'] = df['姓名'].replace('', np.nan)
    print("姓名列清洗完成")
    return df

def clean_age(df):
    """清洗年龄列：转换为数值，处理异常值"""
    # 将字符串数字转换为数值
    df['年龄'] = pd.to_numeric(df['年龄'], errors='coerce')
    # 处理异常值：年龄应在18-70之间（合理工作年龄）
    # 将小于18或大于70的值设为NaN
    df['年龄'] = df['年龄'].apply(lambda x: x if pd.isna(x) or (18 <= x <= 70) else np.nan)
    print("年龄列清洗完成")
    return df

def clean_salary(df):
    """清洗工资列：处理'k'后缀，转换为数值，处理异常值"""
    # 复制列用于处理
    salary_series = df['工资(元)'].copy()

    # 定义转换函数
    def convert_salary(val):
        if pd.isna(val):
            return np.nan
        # 如果是字符串
        if isinstance(val, str):
            # 去除空格
            val = val.strip()
            # 处理'k'或'K'后缀
            if val.lower().endswith('k'):
                try:
                    num = float(val[:-1].strip())
                    return num * 1000
                except:
                    return np.nan
            # 尝试直接转换为数字
            try:
                return float(val)
            except:
                return np.nan
        # 如果是数值
        try:
            return float(val)
        except:
            return np.nan

    df['工资(元)'] = salary_series.apply(convert_salary)
    # 处理异常值：工资应在0-1000000之间（假设最高100万）
    df['工资(元)'] = df['工资(元)'].apply(lambda x: x if pd.isna(x) or (0 <= x <= 1000000) else np.nan)
    print("工资列清洗完成")
    return df

def clean_join_date(df):
    """清洗入职日期列：统一格式为YYYY-MM-DD"""
    def parse_date(date_str):
        if pd.isna(date_str):
            return np.nan
        # 如果是字符串
        if isinstance(date_str, str):
            date_str = str(date_str).strip()
            # 处理无效日期
            if date_str in ['0000-00-00', 'invalid', 'Invalid', 'INVALID']:
                return np.nan
            # 尝试多种格式解析
            formats = [
                '%Y-%m-%d',  # 2023-02-15
                '%Y/%m/%d',  # 2023/02/15
                '%d-%m-%Y',  # 15-02-2023
                '%d/%m/%Y',  # 15/02/2023
                '%d.%m.%Y',  # 15.02.2023
                '%Y年%m月%d日',  # 2023年02月15日
                '%Y%m%d',    # 20230215
            ]
            for fmt in formats:
                try:
                    return datetime.strptime(date_str, fmt).strftime('%Y-%m-%d')
                except:
                    continue
            # 如果所有格式都失败，返回NaN
            return np.nan
        # 如果不是字符串，返回NaN
        return np.nan

    df['入职日期'] = df['入职日期'].apply(parse_date)
    print("入职日期列清洗完成")
    return df

def clean_email(df):
    """清洗邮箱列：验证格式，处理不完整邮箱"""
    def validate_email(email):
        if pd.isna(email):
            return np.nan
        email = str(email).strip()
        # 基本邮箱格式验证
        if '@' not in email or '.' not in email:
            return np.nan
        # 检查是否以@开头或@.结尾等无效格式
        if email.startswith('@') or email.endswith('@') or '@.' in email:
            return np.nan
        # 简单正则验证
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if re.match(pattern, email):
            return email
        return np.nan

    df['邮箱'] = df['邮箱'].apply(validate_email)
    print("邮箱列清洗完成")
    return df

def clean_department(df):
    """清洗部门列：统一中文名称"""
    # 部门映射：将繁体、英文映射到简体中文
    dept_mapping = {
        '技術部': '技术部',
        '銷售部': '销售部',
        '市場部': '市场部',
        '人力資源部': '人力资源部',
        '財務部': '财务部',
        '行政部': '行政部',
        'Tech': '技术部',
        'Sales': '销售部',
        'Marketing': '市场部',
        'HR': '人力资源部',
        'Finance': '财务部',
        'Admin': '行政部',
        '技術部': '技术部',
        '銷售部': '销售部',
        '市場部': '市场部',
        '人力資源部': '人力资源部',
        '財務部': '财务部',
        '行政部': '行政部',
    }

    def standardize_dept(dept):
        if pd.isna(dept):
            return np.nan
        dept = str(dept).strip()
        # 如果部门在映射中，返回标准化名称
        if dept in dept_mapping:
            return dept_mapping[dept]
        # 否则返回原值（可能是已经标准化的中文名称）
        return dept

    df['部门'] = df['部门'].apply(standardize_dept)
    print("部门列清洗完成")
    return df

def clean_status(df):
    """清洗状态列：统一中文名称"""
    # 状态映射
    status_mapping = {
        'In Service': '在职',
        'Resigned': '离职',
        'Probation': '试用期',
        'On Leave': '休假中',
        '在职 ': '在职',
        ' 离职': '离职',
        ' 离职 ': '离职',
        '离职 ': '离职',
        '试用期 ': '试用期',
        '休假中 ': '休假中',
    }

    def standardize_status(status):
        if pd.isna(status):
            return np.nan
        status = str(status).strip()
        # 如果状态在映射中，返回标准化名称
        if status in status_mapping:
            return status_mapping[status]
        # 否则检查是否为已知状态
        known_statuses = ['在职', '离职', '试用期', '休假中']
        if status in known_statuses:
            return status
        # 未知状态设为NaN
        return np.nan

    df['状态'] = df['状态'].apply(standardize_status)
    print("状态列清洗完成")
    return df

def clean_performance(df):
    """清洗绩效评分列：转换为数值，处理异常值"""
    # 转换为数值
    df['绩效评分'] = pd.to_numeric(df['绩效评分'], errors='coerce')
    # 处理异常值：合理范围1-10，将其他值设为NaN
    df['绩效评分'] = df['绩效评分'].apply(lambda x: x if pd.isna(x) or (1 <= x <= 10) else np.nan)
    print("绩效评分列清洗完成")
    return df

def clean_remarks(df):
    """清洗备注列：去除垃圾字符，截断超长文本"""
    def clean_remark(remark):
        if pd.isna(remark):
            return np.nan
        remark = str(remark)
        # 去除垃圾字符：保留中文、英文、数字、常见标点
        # 移除!!!@@@###$$$等特殊字符
        remark = re.sub(r'[!@#$%^&*()_+=`~\[\]\{\}\\\|;:\'",<>/?]+', '', remark)
        # 移除连续的点（如......）但保留单个点
        remark = re.sub(r'\.{2,}', '', remark)
        # 截断超长文本（超过100字符）
        if len(remark) > 100:
            remark = remark[:100] + '...'
        return remark.strip()

    df['备注'] = df['备注'].apply(clean_remark)
    print("备注列清洗完成")
    return df

def remove_empty_rows(df):
    """删除所有列都为NaN或空值的行"""
    original_rows = len(df)
    # 删除所有列都为NaN的行
    df = df.dropna(how='all')
    # 删除所有列都为空的字符串的行（如果有的话）
    # 先创建副本，将空字符串替换为NaN
    df_cleaned = df.replace('', np.nan)
    # 删除所有列都为NaN的行（包括空字符串转换来的NaN）
    df_cleaned = df_cleaned.dropna(how='all')
    # 恢复原始数据（非空的字符串）
    # 但我们需要保持df的索引一致
    df = df.loc[df_cleaned.index]
    print(f"删除空行后行数: {len(df)} (删除了 {original_rows - len(df)} 行)")
    return df

def analyze_cleaned_data(df):
    """分析清洗后的数据"""
    print("\n" + "="*50)
    print("清洗后数据分析")
    print("="*50)
    print(f"数据形状: {df.shape}")
    print("\n数据前5行:")
    print(df.head())
    print("\n数据信息:")
    print(df.info())
    print("\n缺失值统计:")
    print(df.isnull().sum())
    print("\n数据类型:")
    print(df.dtypes)
    print("\n基本统计信息（数值列）:")
    print(df.describe())
    print("\n唯一值统计:")
    for col in df.columns:
        unique_count = df[col].nunique()
        print(f"{col}: {unique_count} 个唯一值")

def save_cleaned_data(df, output_path):
    """保存清洗后的数据"""
    df.to_csv(output_path, index=False, encoding='utf-8-sig')
    print(f"\n清洗后的数据已保存到: {output_path}")

def main():
    # 文件路径
    input_file = 'dirty_employee_data.csv'
    output_file = 'cleaned_employee_data.csv'

    # 加载数据
    print("正在加载数据...")
    df = load_data(input_file)

    # 执行清洗步骤
    print("\n" + "="*50)
    print("开始数据清洗")
    print("="*50)

    df = clean_employee_id(df)
    df = clean_name(df)
    df = clean_age(df)
    df = clean_salary(df)
    df = clean_join_date(df)
    df = clean_email(df)
    df = clean_department(df)
    df = clean_status(df)
    df = clean_performance(df)
    df = clean_remarks(df)
    df = remove_empty_rows(df)

    # 分析清洗后的数据
    analyze_cleaned_data(df)

    # 保存清洗后的数据
    save_cleaned_data(df, output_file)

    print("\n数据清洗完成！")

if __name__ == "__main__":
    main()