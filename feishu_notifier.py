# -*- coding: utf-8 -*-
import os
import sys
import json
import argparse
import requests
from xml.etree import ElementTree as ET
import time
import hmac
import hashlib
import base64

# ---------- 签名计算函数 ----------
def gen_sign(timestamp, secret):
    """生成飞书机器人签名"""
    string_to_sign = '{}\n{}'.format(timestamp, secret)
    hmac_code = hmac.new(
        string_to_sign.encode('utf-8'),
        digestmod=hashlib.sha256
    ).digest()
    sign = base64.b64encode(hmac_code).decode('utf-8')
    return sign

def parse_junit_xml(xml_file):
    """解析 JUnit XML 文件，提取测试结果统计及失败详情"""
    if not os.path.exists(xml_file):
        print(f"错误: 未找到报告文件 {xml_file}")
        sys.exit(1)

    tree = ET.parse(xml_file)
    root = tree.getroot()

    total = 0
    failures = 0
    errors = 0
    skipped = 0
    failed_cases = []

    for suite in root.findall('testsuite'):
        total += int(suite.get('tests', 0))
        failures += int(suite.get('failures', 0))
        errors += int(suite.get('errors', 0))
        skipped += int(suite.get('skipped', 0))

        for case in suite.findall('testcase'):
            failure_elem = case.find('failure')
            error_elem = case.find('error')
            if failure_elem is not None or error_elem is not None:
                classname = case.get('classname', '')
                name = case.get('name', '')
                failure_type = 'failure' if failure_elem is not None else 'error'

                # 安全获取 message
                if failure_elem is not None:
                    message = failure_elem.get('message', '无详细信息')
                elif error_elem is not None:
                    message = error_elem.get('message', '无详细信息')
                else:
                    message = '无详细信息'

                # 添加到 failed_cases 列表（你之前漏掉了这一部分）
                failed_cases.append({
                    'name': f"{classname}.{name}" if classname else name,
                    'type': failure_type,
                    'message': message
                })


    passed = total - failures - errors - skipped
    return {
        'total': total,
        'passed': passed,
        'failures': failures,
        'errors': errors,
        'skipped': skipped,
        'failed_cases': failed_cases
    }

def send_feishu_message(webhook_url, secret, stats, report_url=""):
    """发送带签名的结构化卡片消息到飞书"""
    if not webhook_url:
        print("未配置飞书 Webhook URL，跳过通知")
        return

    timestamp = str(int(time.time()))
    sign = gen_sign(timestamp, secret)

    status_color = "green" if stats['failures'] == 0 and stats['errors'] == 0 else "red"
    status_text = "✅ 测试全部通过" if status_color == "green" else "❌ 测试未完全通过"

    elements = [
        {
            "tag": "div",
            "text": {
                "tag": "lark_md",
                "content": f"**总数:** {stats['total']}  |  **✅ 通过:** {stats['passed']}  |  **❌ 失败:** {stats['failures']}  |  **⚠️ 错误:** {stats['errors']}  |  **⏭️ 跳过:** {stats['skipped']}"
            }
        },
        {"tag": "hr"}
    ]

    if stats['failed_cases']:
        failed_text = ""
        for case in stats['failed_cases']:
            msg = case['message'][:200] + "..." if len(case['message']) > 200 else case['message']
            failed_text += f"**{case['name']}** ({case['type']})\n{msg}\n\n"
            if len(failed_text) > 1500:
                failed_text += "...(内容过多已截断)"
                break
        elements.append({
            "tag": "div",
            "text": {
                "tag": "lark_md",
                "content": f"**失败用例详情**\n{failed_text}"
            }
        })

    if report_url:
        elements.append({
            "tag": "action",
            "actions": [
                {
                    "tag": "button",
                    "text": {"tag": "plain_text", "content": "📊 查看完整报告"},
                    "type": "primary",
                    "url": report_url
                }
            ]
        })

    # 关键修正：在根对象中包含 timestamp 和 sign
    payload = {
        "timestamp": timestamp,
        "sign": sign,
        "msg_type": "interactive",
        "card": {
            "config": {"wide_screen_mode": True},
            "header": {
                "title": {"tag": "plain_text", "content": status_text},
                "template": status_color
            },
            "elements": elements
        }
    }

    try:
        response = requests.post(webhook_url, json=payload, timeout=10)
        response.raise_for_status()
        print("飞书通知发送成功")
    except Exception as e:
        print(f"发送飞书通知失败: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Pytest 结果通知到飞书')
    parser.add_argument('--report', default='report.xml', help='JUnit XML 报告路径')
    parser.add_argument('--webhook', required=True, help='飞书机器人 Webhook URL')
    parser.add_argument('--secret', required=True, help='飞书机器人签名密钥')
    parser.add_argument('--report-url', default='', help='Allure 报告完整访问地址')
    args = parser.parse_args()

    stats = parse_junit_xml(args.report)
    print(f"测试统计: 总数={stats['total']}, 失败={stats['failures']}, 错误={stats['errors']}, 跳过={stats['skipped']}")

    # 修正：将 secret 作为第四个参数传入
    send_feishu_message(args.webhook, args.secret, stats, args.report_url)