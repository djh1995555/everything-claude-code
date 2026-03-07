#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
完整批量翻译所有 skills 文件
"""

import os
import re
import shutil
from pathlib import Path

# 基础翻译映射
TRANSLATIONS = {
    # 常用标题
    "When to Activate": "何时激活",
    "When to Use": "何时使用",
    "Core Principles": "核心原则",
    "Core Concepts": "核心概念",
    "Best Practices": "最佳实践",
    "Code Examples": "代码示例",
    "Quick Reference": "快速参考",
    "Anti-Patterns": "反模式",
    "Common Patterns": "常见模式",
    "Error Handling": "错误处理",
    "Performance": "性能",
    "Security": "安全",
    "Testing": "测试",
    "References": "参考",
    "Related": "相关",
    "Overview": "概述",
    "Summary": "摘要",
    "Description": "描述",
    "Example": "示例",
    "Note": "注意",
    "Warning": "警告",
    "Important": "重要",
    "Tip": "提示",
    
    # 技术术语
    "Repository": "仓库",
    "Pattern": "模式",
    "Service": "服务",
    "Component": "组件",
    "Function": "函数",
    "Method": "方法",
    "Class": "类",
    "Interface": "接口",
    "Type": "类型",
    "Variable": "变量",
    "Constant": "常量",
    "Parameter": "参数",
    "Return": "返回",
    "Callback": "回调",
    "Async": "异步",
    "Await": "等待",
    "State": "状态",
    "Props": "属性",
    "Context": "上下文",
    "Event": "事件",
    "Handler": "处理器",
    "Request": "请求",
    "Response": "响应",
    "Endpoint": "端点",
    "Route": "路由",
    "Controller": "控制器",
    "Model": "模型",
    "View": "视图",
    "Template": "模板",
    "Database": "数据库",
    "Query": "查询",
    "Migration": "迁移",
    "Schema": "模式",
    "Table": "表",
    "Column": "列",
    "Index": "索引",
    "Transaction": "事务",
    "Connection": "连接",
    "Cache": "缓存",
    "Session": "会话",
    "Token": "令牌",
    "Authentication": "认证",
    "Authorization": "授权",
    "Permission": "权限",
    "Role": "角色",
    "User": "用户",
    "Client": "客户端",
    "Server": "服务器",
    "API": "API",
    "REST": "REST",
    "JSON": "JSON",
    "HTML": "HTML",
    "CSS": "CSS",
    "SQL": "SQL",
    "Docker": "Docker",
    "Container": "容器",
    "Image": "镜像",
    "Volume": "卷",
    "Network": "网络",
    "Deployment": "部署",
    "Pipeline": "流水线",
    "Build": "构建",
    "Test": "测试",
    "Deploy": "部署",
    "Version": "版本",
    "Branch": "分支",
    "Commit": "提交",
    "Merge": "合并",
    "Unit Test": "单元测试",
    "Integration Test": "集成测试",
    "E2E Test": "端到端测试",
    "Mock": "Mock",
    "Coverage": "覆盖率",
    "Assertion": "断言",
    "Error": "错误",
    "Exception": "异常",
    "Debug": "调试",
    "Log": "日志",
    "Console": "控制台",
}

def translate_content(content):
    """翻译内容"""
    # 保存代码块
    code_blocks = []
    counter = [0]
    
    def save_code(match):
        code_blocks.append(match.group(0))
        idx = counter[0]
        counter[0] += 1
        return f"<<<CODE{idx}>>>"
    
    # 保护代码块
    content = re.sub(r'```[\s\S]*?```', save_code, content)
    content = re.sub(r'`[^`]+`', save_code, content)
    
    # 翻译标题和常用短语
    for en, cn in sorted(TRANSLATIONS.items(), key=lambda x: len(x[0]), reverse=True):
        # 标题
        content = re.sub(r'(^|\n)(#+\s*)' + re.escape(en) + r'(\s*$|\n)', 
                        r'\1\2' + cn + r'\3', content, flags=re.IGNORECASE)
        # 列表项
        content = re.sub(r'(^|\n)(\s*[-*]\s*)' + re.escape(en) + r'(:|\s)', 
                        r'\1\2' + cn + r'\3', content, flags=re.IGNORECASE)
    
    # 恢复代码块
    for i, block in enumerate(code_blocks):
        content = content.replace(f"<<<CODE{i}>>>", block)
    
    return content

def translate_file(src_path, dst_path):
    """翻译单个文件"""
    try:
        with open(src_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        translated = translate_content(content)
        
        # 确保目录存在
        dst_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(dst_path, 'w', encoding='utf-8') as f:
            f.write(translated)
        
        return True
    except Exception as e:
        print(f"  错误: {e}")
        return False

def main():
    base_dir = Path("c:/Users/DJH/Desktop/vibe coding/everything-claude-code")
    skills_src = base_dir / "skills"
    skills_dst = base_dir / "translate" / "skills"
    
    # 获取所有源文件
    src_files = list(skills_src.glob("*/SKILL.md"))
    
    print(f"找到 {len(src_files)} 个源文件")
    print("=" * 60)
    
    success = 0
    failed = 0
    
    for src_file in sorted(src_files):
        skill_name = src_file.parent.name
        dst_file = skills_dst / skill_name / "SKILL.md"
        
        print(f"翻译: {skill_name}...", end=" ")
        
        if translate_file(src_file, dst_file):
            print("✓")
            success += 1
        else:
            print("✗")
            failed += 1
    
    print("=" * 60)
    print(f"完成: 成功 {success}, 失败 {failed}")
    print(f"总计: {success}/{len(src_files)}")
    
    # 验证文件数量和结构
    print("\n验证文件结构:")
    print("=" * 60)
    
    dst_files = list(skills_dst.glob("*/SKILL.md"))
    print(f"源文件数量: {len(src_files)}")
    print(f"翻译文件数量: {len(dst_files)}")
    
    if len(src_files) == len(dst_files):
        print("✅ 文件数量匹配!")
    else:
        print("❌ 文件数量不匹配!")
        print(f"  缺少 {len(src_files) - len(dst_files)} 个文件")
    
    # 检查结构
    src_dirs = set(p.parent.name for p in src_files)
    dst_dirs = set(p.parent.name for p in dst_files)
    
    missing_dirs = src_dirs - dst_dirs
    extra_dirs = dst_dirs - src_dirs
    
    if missing_dirs:
        print(f"\n❌ 缺少目录: {missing_dirs}")
    if extra_dirs:
        print(f"\n❌ 多余目录: {extra_dirs}")
    if not missing_dirs and not extra_dirs:
        print("\n✅ 目录结构匹配!")

if __name__ == "__main__":
    main()
