"""
CSV 文件读取工具
功能：读取测试用例 CSV 文件，自动合并多行步骤
"""
import csv
import os
from config import config


def read_test_cases():
    """
    读取并处理测试用例 CSV 文件

    核心逻辑：
    1. 读取 CSV 每一行数据
    2. 按"用例编号"分组，将同一个用例的多行步骤合并
    3. 返回结构化的测试数据列表

    比喻说明：
    就像整理菜谱，CSV 中一个菜可能占多行（主料一行、辅料一行、步骤一行），
    这个函数把它们合并成一道完整的菜。

    返回格式示例：
    [
        {
            "用例编号": "1",
            "功能模块": "首页",
            "用例名称": "进入官方网站",
            "测试步骤": ["步骤1", "步骤2"],
            "预期结果": ["结果1", "结果2"],
            "优先级": "p0"
        },
        ...
    ]
    """
    csv_file = config.CSV_FILE

    # 检查文件是否存在
    if not os.path.exists(csv_file):
        raise FileNotFoundError(f"CSV文件不存在: {csv_file}")

    # 用于存储所有测试用例
    test_cases_dict = {}

    # 打开并读取 CSV 文件
    with open(csv_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)

        for row in reader:
            # 清理数据：去除每个字段的前后空格
            case_id = row.get('用例编号', '').strip()

            # 跳过空行（没有用例编号的行）
            if not case_id:
                continue

            # 如果这个用例编号还没出现过，创建新条目
            if case_id not in test_cases_dict:
                test_cases_dict[case_id] = {
                    "用例编号": case_id,
                    "功能模块": row.get('功能模块', '').strip(),
                    "用例名称": row.get('用例名称', '').strip(),
                    "前置条件": row.get('前置条件', '').strip(),
                    "测试步骤": [],  # 用列表存储多个步骤
                    "预期结果": [],  # 用列表存储多个预期结果
                    "优先级": row.get('优先级', '').strip()
                }

            # 提取当前行的步骤和预期结果
            step = row.get('测试步骤', '').strip()
            expected = row.get('预期结果', '').strip()

            # 如果有步骤内容，添加到列表中
            if step:
                # 按换行符分割多个步骤（处理单元格内的多行文本）
                steps_list = [s.strip() for s in step.split('\n') if s.strip()]
                test_cases_dict[case_id]["测试步骤"].extend(steps_list)

            # 如果有预期结果，添加到列表中
            if expected:
                expected_list = [e.strip() for e in expected.split('\n') if e.strip()]
                test_cases_dict[case_id]["预期结果"].extend(expected_list)

    # 将字典转换为列表，并按用例编号排序
    test_cases_list = list(test_cases_dict.values())
    test_cases_list.sort(key=lambda x: int(x["用例编号"]))

    print(f"✓ 成功读取 {len(test_cases_list)} 条测试用例")
    return test_cases_list


if __name__ == "__main__":
    """测试 CSV 读取功能"""
    cases = read_test_cases()
    for case in cases[:3]:  # 打印前3条查看效果
        print(f"\n用例 {case['用例编号']}: {case['用例名称']}")
        print(f"  步骤数: {len(case['测试步骤'])}")
        print(f"  预期结果数: {len(case['预期结果'])}")
