import json
import os
from datetime import datetime
# 数据文件路径
DATA_FILE = "data.txt"
CONFIG_FILE = "config.txt"
# 全局变量存储数据
records = []
config = {}

def load_data():
    global records, config
    try:
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                records = json.load(f)
        else:
            records = []
    except:
        records = []
    try:
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                config = json.load(f)
        else:
            config = {"categories": ["餐饮", "交通", "购物", "娱乐", "其他"],"budget": 3000}
    except:
        config = {"categories": ["餐饮", "交通", "购物", "娱乐", "其他"],"budget": 3000}

def save_data():
    try:
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(records, f, ensure_ascii=False, indent=2)
        return True
    except:
        return False

def save_config():
    try:
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
        return True
    except:
        return False

def add_record():
    print("\n--- 添加消费记录 ---")
    date = input("日期(YYYY-MM-DD，直接回车使用今天): ")
    if date == "":
        today = datetime.now()
        date = today.strftime("%Y-%m-%d")
    print("\n可选类别:")
    for i in range(len(config["categories"])):
        print(f"{i+1}. {config['categories'][i]}")
    try:
        choice = int(input("选择类别(输入数字): "))
        if 1 <= choice <= len(config["categories"]):
            category = config["categories"][choice-1]
        else:
            category = input("输入自定义类别: ")
    except:
        category = input("输入类别: ")
    try:
        amount = float(input("金额: "))
    except:
        print("金额输入错误！")
        return
    desc = input("描述(可选): ")
    if len(records) == 0:
        new_id = 1
    else:
        max_id = 0
        for r in records:
            if r["id"] > max_id:
                max_id = r["id"]
        new_id = max_id + 1
    new_record = {"id": new_id,"date": date,"category": category,"amount": amount,"desc": desc}
    records.append(new_record)
    if save_data():
        print(f"记录添加成功！ID: {new_id}")
    else:
        print("保存失败！")

def show_all_records():
    print("\n--- 所有消费记录 ---")
    if len(records) == 0:
        print("暂无记录")
        return
    total = 0
    for r in records:
        total += r["amount"]
    print(f"总记录数: {len(records)}条")
    print(f"总消费金额: {total:.2f}元")
    print("-" * 50)
    print("ID   日期    类别    金额     描述")
    print("-" * 50)
    for r in records:
        print(f"{r['id']:<4} {r['date']:<11} {r['category']:<6} "f"{r['amount']:<8.2f} {r['desc']}")

def search_records():
    print("\n--- 查找记录 ---")
    print("1. 按日期查找")
    print("2. 按类别查找")
    print("3. 按金额范围查找")
    choice = input("请选择: ")
    if choice == "1":
        date = input("请输入日期(YYYY-MM-DD): ")
        found = []
        total = 0
        for r in records:
            if r["date"] == date:
                found.append(r)
                total += r["amount"]
        if len(found) == 0:
            print("没有找到记录")
        else:
            print(f"\n找到{len(found)}条记录，总金额: {total:.2f}元")
            print("-" * 50)
            for r in found:
                print(f"{r['id']:<4} {r['date']:<11} {r['category']:<6} "f"{r['amount']:<8.2f} {r['desc']}")
    elif choice == "2":
        print("\n可选类别:")
        for i in range(len(config["categories"])):
            print(f"{i+1}. {config['categories'][i]}")
        category_choice = input("输入类别编号或名称: ")
        try:
            idx = int(category_choice) - 1
            if 0 <= idx < len(config["categories"]):
                category = config["categories"][idx]
            else:
                category = category_choice
        except:
            category = category_choice
        found = []
        total = 0
        for r in records:
            if r["category"] == category:
                found.append(r)
                total += r["amount"]
        if len(found) == 0:
            print("没有找到记录")
        else:
            print(f"\n找到{len(found)}条记录，总金额: {total:.2f}元")
            print("-" * 50)
            for r in found:
                print(f"{r['id']:<4} {r['date']:<11} {r['category']:<6} "f"{r['amount']:<8.2f} {r['desc']}")
    elif choice == "3":
        try:
            min_amount = float(input("最小金额: "))
            max_amount = float(input("最大金额: "))
        except:
            print("金额输入错误！")
            return
        found = []
        total = 0
        for r in records:
            if min_amount <= r["amount"] <= max_amount:
                found.append(r)
                total += r["amount"]
        if len(found) == 0:
            print("没有找到记录")
        else:
            print(f"\n找到{len(found)}条记录，总金额: {total:.2f}元")
            print("-" * 50)
            for r in found:
                print(f"{r['id']:<4} {r['date']:<11} {r['category']:<6} "f"{r['amount']:<8.2f} {r['desc']}")

def update_record():
    print("\n--- 修改记录 ---")
    try:
        record_id = int(input("请输入要修改的记录ID: "))
    except:
        print("ID必须是数字！")
        return
    found_record = None
    for r in records:
        if r["id"] == record_id:
            found_record = r
            break
    if found_record is None:
        print(f"未找到ID为{record_id}的记录")
        return
    print(f"\n找到记录:")
    print(f"ID: {found_record['id']}")
    print(f"日期: {found_record['date']}")
    print(f"类别: {found_record['category']}")
    print(f"金额: {found_record['amount']}")
    print(f"描述: {found_record['desc']}")
    print("-" * 30)
    print("请选择要修改的内容:")
    print("1. 日期")
    print("2. 类别")
    print("3. 金额")
    print("4. 描述")
    print("5. 全部修改")
    choice = input("请选择(1-5): ")
    if choice == "1":
        new_date = input("新日期(YYYY-MM-DD): ")
        found_record["date"] = new_date
    elif choice == "2":
        print("\n可选类别:")
        for i in range(len(config["categories"])):
            print(f"{i+1}. {config['categories'][i]}")
        cat_choice = input("选择类别编号或输入自定义类别: ")
        try:
            idx = int(cat_choice) - 1
            if 0 <= idx < len(config["categories"]):
                found_record["category"] = config["categories"][idx]
            else:
                found_record["category"] = cat_choice
        except:
            found_record["category"] = cat_choice
    elif choice == "3":
        try:
            new_amount = float(input("新金额: "))
            found_record["amount"] = new_amount
        except:
            print("金额输入错误！")
            return
    elif choice == "4":
        new_desc = input("新描述: ")
        found_record["desc"] = new_desc
    elif choice == "5":
        new_date = input("新日期(YYYY-MM-DD): ")
        found_record["date"] = new_date
        print("\n可选类别:")
        for i in range(len(config["categories"])):
            print(f"{i+1}. {config['categories'][i]}")
        cat_choice = input("选择类别编号或输入自定义类别: ")
        try:
            idx = int(cat_choice) - 1
            if 0 <= idx < len(config["categories"]):
                found_record["category"] = config["categories"][idx]
            else:
                found_record["category"] = cat_choice
        except:
            found_record["category"] = cat_choice
        try:
            new_amount = float(input("新金额: "))
            found_record["amount"] = new_amount
        except:
            print("金额输入错误！")
            return
        new_desc = input("新描述: ")
        found_record["desc"] = new_desc
    else:
        print("无效选择")
        return
    if save_data():
        print("记录修改成功！")
    else:
        print("保存失败！")

def delete_record():
    print("\n--- 删除记录 ---")
    print("1. 按ID删除")
    print("2. 删除所有记录")
    choice = input("请选择: ")
    if choice == "1":
        try:
            record_id = int(input("请输入要删除的记录ID: "))
        except:
            print("ID必须是数字！")
            return
        found_index = -1
        for i in range(len(records)):
            if records[i]["id"] == record_id:
                found_index = i
                break
        if found_index == -1:
            print(f"未找到ID为{record_id}的记录")
            return
        print(f"\n找到记录:")
        print(f"ID: {records[found_index]['id']}")
        print(f"日期: {records[found_index]['date']}")
        print(f"类别: {records[found_index]['category']}")
        print(f"金额: {records[found_index]['amount']}")
        confirm = input("确认删除？(y/N): ")
        if confirm.lower() == "y":
            deleted_record = records.pop(found_index)
            if save_data():
                print(f"记录{deleted_record['id']}已删除")
            else:
                print("保存失败！")
        else:
            print("取消删除")
    elif choice == "2":
        confirm = input("确认删除所有记录？(输入'YES'确认): ")
        if confirm == "YES":
            records.clear()
            if save_data():
                print("所有记录已删除")
            else:
                print("保存失败！")
        else:
            print("取消删除")

def show_statistics():
    print("\n--- 统计信息 ---")
    if len(records) == 0:
        print("暂无记录")
        return
    total = 0
    for r in records:
        total += r["amount"]
    print(f"总消费金额: {total:.2f}元")
    print(f"总记录数: {len(records)}条")
    print("\n--- 按类别统计 ---")
    category_totals = {}
    for r in records:
        category = r["category"]
        amount = r["amount"]
        if category in category_totals:
            category_totals[category] += amount
        else:
            category_totals[category] = amount
    for category, amount in category_totals.items():
        percent = (amount / total) * 100
        print(f"{category}: {amount:.2f}元 ({percent:.1f}%)")
    print("\n--- 月度统计 ---")
    now = datetime.now()
    current_year_month = now.strftime("%Y-%m")
    month_total = 0
    for r in records:
        if r["date"].startswith(current_year_month):
            month_total += r["amount"]
    print(f"本月({current_year_month})消费: {month_total:.2f}元")
    if "budget" in config:
        budget = config["budget"]
        if month_total > budget:
            print(f"！！！！本月已超预算！超出: {month_total - budget:.2f}元")
        else:
            remaining = budget - month_total
            print(f"本月预算剩余: {remaining:.2f}元")

def manage_config():
    print("\n--- 系统配置 ---")
    print("1. 设置月度预算")
    print("2. 添加消费类别")
    print("3. 删除消费类别")
    print("4. 查看当前配置")
    choice = input("请选择: ")
    if choice == "1":
        try:
            new_budget = float(input("请输入月度预算金额: "))
            config["budget"] = new_budget
            if save_config():
                print("预算设置成功！")
            else:
                print("保存失败！")
        except:
            print("金额输入错误！")
    elif choice == "2":
        new_category = input("请输入新的消费类别: ")
        if "categories" not in config:
            config["categories"] = []
        if new_category not in config["categories"]:
            config["categories"].append(new_category)
            if save_config():
                print("类别添加成功！")
            else:
                print("保存失败！")
        else:
            print("该类别已存在！")
    elif choice == "3":
        if "categories" not in config or len(config["categories"]) == 0:
            print("当前没有可删除的消费类别！")
            return
            print("\n当前消费类别:")
        for i, category in enumerate(config["categories"]):
            print(f"{i+1}. {category}")
        try:
            delete_choice = input("请输入要删除的类别编号(输入0取消): ")
            if delete_choice == "0":
                print("操作取消")
                return
            idx = int(delete_choice) - 1
            if 0 <= idx < len(config["categories"]):
                category_to_delete = config["categories"][idx]
                confirm = input(f"确认删除类别 '{category_to_delete}'? (y/N): ")
                if confirm.lower() == "y":
                    del config["categories"][idx]
                    if save_config():
                        print("类别删除成功！")
                    else:
                        print("保存失败！")
                else:
                    print("删除操作取消")
            else:
                print("无效的类别编号！")
        except ValueError:
            print("请输入有效的数字编号！")
    elif choice == "4":
        print("\n当前配置:")
        print("-" * 30)
        if "budget" in config:
            print(f"月度预算: {config['budget']}元")
        if "categories" in config:
            print("消费类别:")
            for i, category in enumerate(config["categories"]):
                print(f"{i+1}. {category}")
    
def show_menu():
    print("="*50)
    print("1. 添加消费记录")
    print("2. 查看所有记录")
    print("3. 查找记录")
    print("4. 修改记录")
    print("5. 删除记录")
    print("6. 统计信息")
    print("7. 系统配置")
    print("8. 退出系统")
    print("="*50)

def main():
    print("正在加载数据...")
    load_data()
    print("\n欢迎使用个人记账管理系统！")
    if len(records) > 0:
        now = datetime.now()
        current_month = now.strftime("%Y-%m")
        month_total = 0
        for r in records:
            if r["date"].startswith(current_month):
                month_total += r["amount"]
        print(f"本月已消费: {month_total:.2f}元")
        if "budget" in config:
            budget = config["budget"]
            if month_total > 0:
                percent = (month_total / budget) * 100
                print(f"预算使用率: {percent:.1f}%")
                
    while True:
        show_menu()
        choice = input("请选择操作(1-8): ")
        if choice == "1":
            add_record()
        elif choice == "2":
            show_all_records()
        elif choice == "3":
            search_records()
        elif choice == "4":
            update_record()
        elif choice == "5":
            delete_record()
        elif choice == "6":
            show_statistics()
        elif choice == "7":
            manage_config()
        elif choice == "8":
            print("感谢使用，再见！")
            break
        else:
            print("无效选择，请重新输入！")
        input("\n按回车键继续...")
if __name__ == "__main__":
    main()