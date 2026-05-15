"""
一键运行测试脚本
提供简单的命令行接口，方便执行测试
"""
import os
import sys
import subprocess
from config import config


def ensure_directories():
    """确保必要的目录存在"""
    os.makedirs(config.SCREENSHOTS_DIR, exist_ok=True)
    os.makedirs(config.ALLURE_RESULTS, exist_ok=True)
    os.makedirs(config.ALLURE_HTML, exist_ok=True)


def run_all_tests():
    """运行所有测试用例"""
    print("\n" + "=" * 60)
    print("开始执行所有测试用例...")
    print("=" * 60 + "\n")

    ensure_directories()

    # 构建pytest命令
    command = [
        sys.executable,  # 使用当前Python解释器
        "-m", "pytest",  # 以模块方式运行pytest
        "test_scripts/",  # 测试目录
        "-v",  # 详细输出
        "-s",  # 显示print
        "--alluredir=" + config.ALLURE_RESULTS,
        "--clean-alluredir"
    ]

    print(f"执行命令: {' '.join(command)}\n")

    # 执行命令
    result = subprocess.run(command)

    print("\n" + "=" * 60)
    if result.returncode == 0:
        print("✓ 所有测试用例执行成功！")
    else:
        print(f"⚠ 测试执行完成，但有 {result.returncode} 个用例失败")
    print("=" * 60)

    return result.returncode == 0


def run_by_priority(priority):
    """
    按优先级运行测试用例

    参数:
        priority: 优先级字符串，如 'p0', 'p1', 'p2'
    """
    print(f"\n{'=' * 60}")
    print(f"只运行 {priority.upper()} 优先级的测试用例")
    print(f"{'=' * 60}\n")

    ensure_directories()

    command = [
        sys.executable,
        "-m", "pytest",
        "test_scripts/",
        "-v",
        "-s",
        "-m", priority,  # 只运行指定标记的用例
        "--alluredir=" + config.ALLURE_RESULTS,
        "--clean-alluredir"
    ]

    result = subprocess.run(command)
    return result.returncode == 0


def run_single_test(test_name):
    """
    运行单个测试用例

    参数:
        test_name: 测试函数名，如 'test_tc001_access_homepage'
    """
    print(f"\n{'=' * 60}")
    print(f"运行单个测试用例: {test_name}")
    print(f"{'=' * 60}\n")

    ensure_directories()

    command = [
        sys.executable,
        "-m", "pytest",
        f"test_scripts/",
        "-k", test_name,
        "-v",
        "-s",
        "--alluredir=" + config.ALLURE_RESULTS,
        "--clean-alluredir"
    ]

    result = subprocess.run(command)
    return result.returncode == 0




if __name__ == "__main__":
    """
    命令行入口

    使用方法:
        python run_tests.py              # 运行所有测试
        python run_tests.py p0           # 只运行P0优先级
        python run_tests.py p1           # 只运行P1优先级
        python run_tests.py test_tc001   # 运行指定用例
    """
    if len(sys.argv) > 1:
        arg = sys.argv[1]

        if arg in ['p0', 'p1', 'p2']:
            success = run_by_priority(arg)
        elif arg.startswith('test_'):
            success = run_single_test(arg)
        else:
            print("用法:")
            print("  python run_tests.py          # 运行所有测试")
            print("  python run_tests.py p0       # 只运行P0优先级")
            print("  python run_tests.py p1       # 只运行P1优先级")
            print("  python run_tests.py test_xxx # 运行指定用例")
            sys.exit(1)
    else:
        success = run_all_tests()

    # 询问是否生成报告
    if success or input("\n是否生成Allure报告? (y/n): ").lower() == 'y':
        print("\n正在生成Allure报告...")
        generate_report_cmd = [
            "allure",
            "generate",
            config.ALLURE_RESULTS,
            "-o", config.ALLURE_HTML,
            "--clean"
        ]
        subprocess.run(generate_report_cmd)

        report_path = os.path.join(config.ALLURE_HTML, "index.html")
        print(f"\n✓ 报告已生成: {report_path}")
        print(f"在浏览器中打开: file://{os.path.abspath(report_path)}")
