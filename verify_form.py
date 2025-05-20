#!/usr/bin/env python3
# 文件名: verify_form.py
# 描述: 本脚本用于验证表单HTML是否正确，不需要完整运行应用

import re
import sys
import os

def check_form_html(form_path):
    """检查表单HTML是否存在可能导致submit方法被覆盖的问题"""
    try:
        with open(form_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # 检查是否有id="submit"或name="submit"的元素
        submit_id_pattern = re.compile(r'id=["\']submit["\']')
        submit_name_pattern = re.compile(r'name=["\']submit["\']')
        
        if submit_id_pattern.search(content):
            print("警告: 表单中存在id='submit'的元素，这会导致表单的submit()方法被覆盖!")
        elif submit_name_pattern.search(content):
            print("警告: 表单中存在name='submit'的元素，这会导致表单的submit()方法被覆盖!")
        else:
            print("表单元素命名正常，没有发现会覆盖submit()方法的元素。")
        
        # 检查JavaScript代码中是否有dishForm.submit()调用
        submit_call_pattern = re.compile(r'dishForm\.submit\(\)')
        submit_calls = submit_call_pattern.findall(content)
        
        if submit_calls:
            print(f"发现 {len(submit_calls)} 处dishForm.submit()调用，这可能会导致TypeError错误。")
        else:
            print("没有发现直接调用dishForm.submit()的代码，表单提交方式正确。")
            
        # 检查是否正确使用表单提交事件
        if "addEventListener('submit'" in content or 'addEventListener("submit"' in content:
            print("表单使用了正确的submit事件监听方式。")
        else:
            print("警告: 没有找到表单的submit事件监听器，可能存在问题。")
            
        # 检查提交按钮
        submit_btn_pattern = re.compile(r'{{ form\.submit\(.*?\) }}')
        if submit_btn_pattern.search(content):
            print("表单使用了Flask-WTF的submit按钮渲染方式。")
            print("注意: 这会生成一个name='submit'的元素，可能会覆盖表单的submit方法。")
            print("建议: 在Flask表单类中将submit字段改为另一个名称，如'save_button'。")
    except Exception as e:
        print(f"检查失败: {str(e)}")
        return False
    
    return True

def main():
    """主函数"""
    form_path = "/home/will/food-menu/app/templates/dishes/form.html"
    if not os.path.exists(form_path):
        print(f"表单文件不存在: {form_path}")
        return 1
        
    print(f"检查表单文件: {form_path}")
    check_form_html(form_path)
    
    # 检查新表单文件
    new_form_path = f"{form_path}.new"
    if os.path.exists(new_form_path):
        print(f"\n检查新表单文件: {new_form_path}")
        check_form_html(new_form_path)
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
