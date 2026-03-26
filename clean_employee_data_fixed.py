import csv
import re
from datetime import datetime
import sys

def read_csv_file(file_path):
    """读取CSV文件，返回标题行和数据行（处理BOM）"""
    with open(file_path, 'r', encoding='utf-8-sig') as f:
        reader = csv.reader(f)
        header = next(reader)  # 读取标题行
        data = list(reader)
    print(f"原始数据行数: {len(data)}")
    print(f"标题: {header}")
    return header, data

def write_csv_file(file_path, header, data):
    """写入CSV文件"""
    with open(file_path, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(data)
    print(f"数据已保存到: {file_path}")

def clean_employee_id(data):
    """清洗员工ID：去除重复行（基于员工ID）"""
    seen_ids = set()
    cleaned_data = []
    duplicate_count = 0

    for row in data:
        emp_id = row[0]  # 员工ID在第一列
        if emp_id not in seen_ids:
            seen_ids.add(emp_id)
            cleaned_data.append(row)
        else:
            duplicate_count += 1

    print(f"去除重复行: 删除了 {duplicate_count} 个重复行")
    return cleaned_data

def clean_name(name):
    """清洗姓名"""
    if not name or name.lower() == 'nan':
        return ''
    # 去除前后空格
    name = name.strip()
    # 去除特殊字符，保留中文、英文、点和空格
    name = re.sub(r'[^a-zA-Z\u4e00-\u9fff·\s]', '', name)
    # 如果名称为空，返回空字符串
    if not name:
        return ''
    return name

def clean_age(age):
    """清洗年龄"""
    if not age or age.lower() == 'nan':
        return ''
    # 尝试转换为整数
    try:
        age_int = int(age)
        # 检查合理范围
        if 18 <= age_int <= 70:
            return str(age_int)
    except ValueError:
        # 如果不是数字，尝试处理字符串
        # 这里可以添加更多逻辑，比如"二十"转20
        # 简单起见，返回空
        pass
    return ''

def clean_salary(salary):
    """清洗工资"""
    if not salary or salary.lower() == 'nan':
        return ''

    salary_str = str(salary).strip()

    # 处理'k'后缀
    if salary_str.lower().endswith('k'):
        try:
            num = float(salary_str[:-1].strip())
            return str(int(num * 1000))
        except:
            return ''

    # 尝试转换为整数
    try:
        salary_int = int(float(salary_str))
        # 检查合理范围
        if 0 <= salary_int <= 1000000:
            return str(salary_int)
    except:
        pass

    return ''

def clean_join_date(date_str):
    """清洗入职日期"""
    if not date_str or date_str.lower() == 'nan':
        return ''

    date_str = str(date_str).strip()

    # 处理无效日期
    invalid_dates = ['0000-00-00', 'invalid', 'Invalid', 'INVALID']
    if date_str in invalid_dates:
        return ''

    # 尝试多种格式解析
    date_formats = [
        '%Y-%m-%d',    # 2023-02-15
        '%Y/%m/%d',    # 2023/02/15
        '%d-%m-%Y',    # 15-02-2023
        '%d/%m/%Y',    # 15/02/2023
        '%d.%m.%Y',    # 15.02.2023
        '%Y年%m月%d日', # 2023年02月15日
        '%Y%m%d',      # 20230215
    ]

    for fmt in date_formats:
        try:
            dt = datetime.strptime(date_str, fmt)
            return dt.strftime('%Y-%m-%d')
        except:
            continue

    return ''

def clean_email(email):
    """清洗邮箱"""
    if not email or email.lower() == 'nan':
        return ''

    email = str(email).strip()

    # 基本验证
    if '@' not in email or '.' not in email:
        return ''
    if email.startswith('@') or email.endswith('@') or '@.' in email:
        return ''

    # 简单正则验证
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if re.match(pattern, email):
        return email

    return ''

def clean_department(dept):
    """清洗部门"""
    if not dept or dept.lower() == 'nan':
        return ''

    dept = str(dept).strip()

    # 部门映射
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
    }

    if dept in dept_mapping:
        return dept_mapping[dept]

    # 检查是否已经是标准中文部门
    standard_depts = ['技术部', '销售部', '市场部', '人力资源部', '财务部', '行政部']
    if dept in standard_depts:
        return dept

    return ''

def clean_status(status):
    """清洗状态"""
    if not status or status.lower() == 'nan':
        return ''

    status = str(status).strip()

    # 状态映射
    status_mapping = {
        'In Service': '在职',
        'Resigned': '离职',
        'Probation': '试用期',
        'On Leave': '休假中',
        '在职 ': '在职',
        ' 离职': '离职',
        '离职 ': '离职',
        '试用期 ': '试用期',
        '休假中 ': '休假中',
    }

    if status in status_mapping:
        return status_mapping[status]

    # 标准状态
    standard_statuses = ['在职', '离职', '试用期', '休假中']
    if status in standard_statuses:
        return status

    return ''

def clean_performance(rating):
    """清洗绩效评分"""
    if not rating or rating.lower() == 'nan':
        return ''

    try:
        rating_int = int(float(rating))
        if 1 <= rating_int <= 10:
            return str(rating_int)
    except:
        pass

    return ''

def clean_remark(remark):
    """清洗备注"""
    if not remark or remark.lower() == 'nan':
        return ''

    remark = str(remark)

    # 去除垃圾字符
    remark = re.sub(r'[!@#$%^&*()_+=`~\[\]\{\}\\\|;:\'",<>/?]+', '', remark)
    # 去除连续的点
    remark = re.sub(r'\.{2,}', '', remark)
    # 截断超长文本
    if len(remark) > 100:
        remark = remark[:100] + '...'

    return remark.strip()

def clean_row(row):
    """清洗单行数据"""
    # 假设列顺序为：员工ID,姓名,年龄,工资(元),入职日期,邮箱,部门,状态,绩效评分,备注
    cleaned = list(row)

    # 清洗每一列
    cleaned[1] = clean_name(cleaned[1])  # 姓名
    cleaned[2] = clean_age(cleaned[2])   # 年龄
    cleaned[3] = clean_salary(cleaned[3]) # 工资
    cleaned[4] = clean_join_date(cleaned[4]) # 入职日期
    cleaned[5] = clean_email(cleaned[5]) # 邮箱
    cleaned[6] = clean_department(cleaned[6]) # 部门
    cleaned[7] = clean_status(cleaned[7]) # 状态
    cleaned[8] = clean_performance(cleaned[8]) # 绩效评分
    cleaned[9] = clean_remark(cleaned[9]) # 备注

    return cleaned

def remove_empty_rows(data):
    """删除所有列都为空的空行（除了员工ID）"""
    cleaned_data = []
    empty_count = 0

    for row in data:
        # 检查所有列是否都为空（除了员工ID）
        all_empty = True
        for i, cell in enumerate(row):
            # 跳过员工ID列（第0列），因为员工ID不应该为空
            if i == 0:
                if cell and cell.strip():
                    all_empty = False
                    break
            else:
                if cell and str(cell).strip() and str(cell).lower() != 'nan':
                    all_empty = False
                    break

        if not all_empty:
            cleaned_data.append(row)
        else:
            empty_count += 1

    print(f"删除空行: 删除了 {empty_count} 个空行")
    return cleaned_data

def analyze_data(header, data):
    """分析清洗后的数据（避免编码问题）"""
    print("\n" + "="*50)
    print("清洗后数据分析")
    print("="*50)
    print(f"总行数: {len(data)}")
    print(f"列数: {len(header)}")

    # 统计每列的缺失值
    print("\n缺失值统计（空值或空字符串）:")
    for i, col_name in enumerate(header):
        missing_count = sum(1 for row in data if not row[i] or str(row[i]).strip() == '')
        # 安全打印列名
        try:
            print(f"{col_name}: {missing_count} 个缺失值")
        except:
            print(f"Column {i}: {missing_count} 个缺失值")

    # 显示前5行数据（简化显示）
    print("\n前5行数据（简化）:")
    for i in range(min(5, len(data))):
        # 只显示前3列和后3列，避免过长
        row_preview = data[i][:3] + ['...'] + data[i][-3:] if len(data[i]) > 6 else data[i]
        print(f"行 {i+1}: {row_preview}")

def main():
    input_file = 'dirty_employee_data.csv'
    output_file = 'cleaned_employee_data_fixed.csv'

    print("正在加载数据...")
    header, data = read_csv_file(input_file)

    print("\n" + "="*50)
    print("开始数据清洗")
    print("="*50)

    # 清洗步骤
    data = clean_employee_id(data)

    # 清洗每一行
    cleaned_data = []
    for i, row in enumerate(data):
        cleaned_row = clean_row(row)
        cleaned_data.append(cleaned_row)

    data = cleaned_data
    data = remove_empty_rows(data)

    # 分析清洗后的数据
    analyze_data(header, data)

    # 保存清洗后的数据
    write_csv_file(output_file, header, data)

    print(f"\n数据清洗完成！清洗后的数据已保存到: {output_file}")

    # 额外检查：验证清洗是否彻底
    print("\n" + "="*50)
    print("清洗质量检查")
    print("="*50)

    # 重新读取清洗后的数据进行验证
    _, cleaned_data_check = read_csv_file(output_file)

    # 检查是否有明显的问题数据
    issues = []
    for i, row in enumerate(cleaned_data_check):
        # 检查年龄是否为数字或在合理范围
        age = row[2]
        if age and age.strip():
            try:
                age_int = int(age)
                if not (18 <= age_int <= 70):
                    issues.append(f"行 {i+1}: 年龄超出合理范围: {age_int}")
            except:
                issues.append(f"行 {i+1}: 年龄不是有效数字: {age}")

        # 检查工资是否为数字或正数
        salary = row[3]
        if salary and salary.strip():
            try:
                salary_int = int(salary)
                if salary_int < 0:
                    issues.append(f"行 {i+1}: 工资为负数: {salary_int}")
                elif salary_int > 1000000:
                    issues.append(f"行 {i+1}: 工资过高: {salary_int}")
            except:
                issues.append(f"行 {i+1}: 工资不是有效数字: {salary}")

        # 检查邮箱格式
        email = row[5]
        if email and email.strip():
            if '@' not in email or '.' not in email:
                issues.append(f"行 {i+1}: 邮箱格式无效: {email}")

        # 检查日期格式
        date_str = row[4]
        if date_str and date_str.strip():
            try:
                datetime.strptime(date_str, '%Y-%m-%d')
            except:
                issues.append(f"行 {i+1}: 日期格式无效: {date_str}")

    if issues:
        print(f"发现 {len(issues)} 个潜在问题:")
        for issue in issues[:10]:  # 最多显示10个问题
            print(f"  - {issue}")
        if len(issues) > 10:
            print(f"  ... 还有 {len(issues) - 10} 个问题未显示")
    else:
        print("数据清洗质量良好，未发现明显问题。")

    print("\n清洗完成！")

if __name__ == "__main__":
    main()