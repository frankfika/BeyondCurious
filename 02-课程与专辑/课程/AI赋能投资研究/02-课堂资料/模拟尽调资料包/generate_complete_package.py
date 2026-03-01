#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""模拟尽调资料包全面升级脚本 - 生成完整的14文件夹结构"""

import os
import sys
import shutil
import importlib

BASE_DIR = "/Users/fangchen/Desktop/测试数据/模拟尽调资料包"

FOLDERS = [
    "01 公司基本信息", "02 公司历史沿革", "03 公司治理",
    "04 人力资源情况", "05 子分公司情况", "06 市场和行业分析",
    "07 产品和技术", "08 供应商分析", "09 客户分析",
    "10 财务分析", "11 合规法律分析", "12 盈利预测",
    "13 资本市场分析和规划", "14 其他"
]

# PDF迁移映射: 旧路径 -> 新路径 (相对于BASE_DIR)
OLD_TO_NEW = {
    "01_公司情况/1-01_营业执照.pdf": "01 公司基本信息/营业执照.pdf",
    "01_公司情况/1-01_工商变更登记表.pdf": "01 公司基本信息/工商变更登记表.pdf",
    "01_公司情况/1-02_验资报告.pdf": "01 公司基本信息/验资报告.pdf",
    "01_公司情况/1-03_实缴资本出资凭证.pdf": "01 公司基本信息/实缴资本出资凭证.pdf",
    "01_公司情况/1-03_公司章程修正案.pdf": "01 公司基本信息/公司章程修正案.pdf",
    "01_公司情况/1-11_股权结构图.pdf": "01 公司基本信息/股权结构图.pdf",
    "01_公司情况/1-10_实际控制人控制框架图.pdf": "01 公司基本信息/实际控制人控制框架图.pdf",
    "01_公司情况/1-09_实际控制人身份证.pdf": "01 公司基本信息/实际控制人身份证.pdf",
    "01_公司情况/1-01_工商基本情况表.txt": "01 公司基本信息/工商基本情况表.txt",
    "01_公司情况/1-03_公司章程.txt": "01 公司基本信息/公司章程.txt",
    "01_公司情况/1-02_工商变更登记记录表.txt": "02 公司历史沿革/工商变更登记记录表.txt",
    "01_公司情况/1-17_股东会决议.pdf": "03 公司治理/股东会决议.pdf",
    "01_公司情况/1-17_董事会决议.pdf": "03 公司治理/董事会决议.pdf",
    "01_公司情况/1-12_内部控制制度清单.pdf": "03 公司治理/内部控制制度清单.pdf",
    "01_公司情况/1-07_员工统计表.pdf": "04 人力资源情况/员工统计表.pdf",
    "01_公司情况/1-07_员工名册.pdf": "04 人力资源情况/员工名册.pdf",
    "01_公司情况/1-09_高管简历.pdf": "04 人力资源情况/高管简历.pdf",
    "01_公司情况/1-11_组织结构图.pdf": "05 子分公司情况/组织结构图.pdf",
    "01_公司情况/1-14_公司业务介绍.pdf": "07 产品和技术/公司业务介绍.pdf",
    "01_公司情况/1-18_产品手册.pdf": "07 产品和技术/产品手册.pdf",
    "01_公司情况/1-18_主要产品生产流程.pdf": "07 产品和技术/主要产品生产流程.pdf",
    "01_公司情况/1-16_知识产权证书.pdf": "07 产品和技术/知识产权证书.pdf",
    "02_财务情况/2-10_审计报告.pdf": "10 财务分析/审计报告.pdf",
    "02_财务情况/2-10_财务报表.pdf": "10 财务分析/财务报表.pdf",
    "02_财务情况/2-10_三年一期财务对比.pdf": "10 财务分析/三年一期财务对比.pdf",
    "02_财务情况/2-23_固定资产明细表.pdf": "10 财务分析/固定资产明细表.pdf",
    "02_财务情况/2-24_无形资产明细表.pdf": "10 财务分析/无形资产明细表.pdf",
    "02_财务情况/2-07_成本构成表.pdf": "10 财务分析/成本构成表.pdf",
    "02_财务情况/2-26_期间费用明细表.pdf": "10 财务分析/期间费用明细表.pdf",
    "02_财务情况/2-26_研发费用明细表.pdf": "10 财务分析/研发费用明细表.pdf",
    "02_财务情况/2-06_分地区收入统计表.pdf": "10 财务分析/分地区收入统计表.pdf",
    "02_财务情况/2-06_分产品收入统计表.pdf": "10 财务分析/分产品收入统计表.pdf",
    "02_财务情况/2-14_政府补贴明细.pdf": "10 财务分析/政府补贴明细.pdf",
    "02_财务情况/2-16_银行对账单.pdf": "10 财务分析/银行对账单.pdf",
    "02_财务情况/2-18_借款合同台账.pdf": "10 财务分析/借款合同台账.pdf",
    "02_财务情况/2-25_存货收发存报表.pdf": "10 财务分析/存货收发存报表.pdf",
    "02_财务情况/2-22_企业征信报告.pdf": "10 财务分析/企业征信报告.pdf",
    "02_财务情况/2-01_房产证.pdf": "10 财务分析/房产证.pdf",
    "02_财务情况/2-02_办公场所租赁合同.pdf": "10 财务分析/办公场所租赁合同.pdf",
    "02_财务情况/2-04_前五大供应商详细资料.pdf": "08 供应商分析/前五大供应商详细资料.pdf",
    "02_财务情况/2-05_前五大客户详细资料.pdf": "09 客户分析/前五大客户详细资料.pdf",
    "02_财务情况/2-05_主要客户供应商清单.pdf": "09 客户分析/主要客户供应商清单.pdf",
    "02_财务情况/2-20_销售合同样本.pdf": "09 客户分析/销售合同样本.pdf",
    "02_财务情况/2-21_重大合同清单.pdf": "09 客户分析/重大合同清单.pdf",
    "02_财务情况/2-23_盈利预测报告.pdf": "12 盈利预测/盈利预测报告.pdf",
    "03_税务情况/3-01_税收优惠文件.pdf": "11 合规法律分析/税收优惠文件.pdf",
    "03_税务情况/3-03_所得税汇算清缴报告.pdf": "11 合规法律分析/所得税汇算清缴报告.pdf",
    "03_税务情况/3-04_纳税申报表.pdf": "11 合规法律分析/纳税申报表.pdf",
    "03_税务情况/3-04_完税证明.pdf": "11 合规法律分析/完税证明.pdf",
    "04_其他/4-01_行业分析报告.pdf": "06 市场和行业分析/行业分析报告.pdf",
    "04_其他/4-07_诉讼仲裁情况说明.pdf": "11 合规法律分析/诉讼仲裁情况说明.pdf",
    "04_其他/4-08_行政处罚记录说明.pdf": "11 合规法律分析/行政处罚记录说明.pdf",
    "04_其他/4-02_增资协议.pdf": "13 资本市场分析和规划/增资协议.pdf",
    "04_其他/4-03_战略合作协议.pdf": "13 资本市场分析和规划/战略合作协议.pdf",
    "04_其他/4-01_未来发展规划.pdf": "14 其他/未来发展规划.pdf",
    "04_其他/4-06_风险因素说明.pdf": "14 其他/风险因素说明.pdf",
    "04_其他/4-05_委托研发合同.pdf": "14 其他/委托研发合同.pdf",
    "04_其他/4-09_环评报告.pdf": "14 其他/环评报告.pdf",
    "附件/附件二_社保公积金缴纳统计.pdf": "04 人力资源情况/社保公积金缴纳统计.pdf",
    "附件/附件三_关联方调查问卷.pdf": "14 其他/关联方调查问卷.pdf",
    "附件/附件五_承诺函.pdf": "14 其他/承诺函.pdf",
    "附件/附件四_无形资产统计表.pdf": "10 财务分析/scan001.pdf",
}

def setup_folders():
    for f in FOLDERS:
        os.makedirs(os.path.join(BASE_DIR, f), exist_ok=True)
    print(f"[OK] 创建了 {len(FOLDERS)} 个文件夹")

def migrate_files():
    count = 0
    for old, new in OLD_TO_NEW.items():
        src = os.path.join(BASE_DIR, old)
        dst = os.path.join(BASE_DIR, new)
        if os.path.exists(src):
            shutil.copy2(src, dst)
            count += 1
        else:
            print(f"[WARN] 源文件不存在: {old}")
    print(f"[OK] 迁移了 {count} 个文件")

def cleanup_old():
    old_dirs = ["01_公司情况", "02_财务情况", "03_税务情况", "04_其他", "附件"]
    for d in old_dirs:
        p = os.path.join(BASE_DIR, d)
        if os.path.exists(p):
            shutil.rmtree(p)
    old_scripts = ["generate_pdf.py", "generate_pdf_extra.py", "generate_pdf_final.py", "generate_pdf_more.py"]
    for s in old_scripts:
        p = os.path.join(BASE_DIR, s)
        if os.path.exists(p):
            os.remove(p)
    print("[OK] 清理旧文件完成")

def write_txt(folder, filename, content):
    path = os.path.join(BASE_DIR, folder, filename)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

def main():
    print("=" * 50)
    print("模拟尽调资料包全面升级")
    print("=" * 50)

    # Step 1: 创建新文件夹
    setup_folders()

    # Step 2: 迁移已有文件
    migrate_files()

    # Step 3: 清理旧结构
    cleanup_old()

    # Step 4: 生成TXT文件 (分模块)
    modules = [
        "gen_txt_01_02", "gen_txt_03_04_05",
        "gen_txt_06_07", "gen_txt_08_09_10",
        "gen_txt_11_12_13_14", "gen_txt_supplement",
    ]
    sys.path.insert(0, os.path.join(BASE_DIR, "_generators"))
    for mod_name in modules:
        print(f"  加载模块: {mod_name}")
        mod = importlib.import_module(mod_name)
        mod.generate(BASE_DIR)

    # Step 5: 生成新PDF文件
    from gen_pdf_new import generate as gen_pdf
    gen_pdf(BASE_DIR)

    # Step 6: 添加organize-files demo用的问题文件
    add_demo_files()

    # Step 7: 统计
    total = sum(len(files) for _, _, files in os.walk(BASE_DIR) if "_generators" not in _)
    print(f"\n{'=' * 50}")
    print(f"完成! 总文件数: {total}")
    for f in FOLDERS:
        p = os.path.join(BASE_DIR, f)
        n = len(os.listdir(p)) if os.path.exists(p) else 0
        print(f"  {f}: {n} 个文件")

def add_demo_files():
    """添加命名不规范和重复文件，供organize-files demo使用"""
    # 不规范命名
    src = os.path.join(BASE_DIR, "10 财务分析", "审计报告.pdf")
    if os.path.exists(src):
        shutil.copy2(src, os.path.join(BASE_DIR, "10 财务分析", "IMG_20230815.pdf"))
    # 重复文件
    src2 = os.path.join(BASE_DIR, "07 产品和技术", "产品手册.pdf")
    if os.path.exists(src2):
        shutil.copy2(src2, os.path.join(BASE_DIR, "07 产品和技术", "产品手册_副本.pdf"))
    src3 = os.path.join(BASE_DIR, "01 公司基本信息", "营业执照.pdf")
    if os.path.exists(src3):
        shutil.copy2(src3, os.path.join(BASE_DIR, "14 其他", "营业执照_扫描件.pdf"))
    print("[OK] 添加demo文件完成")

if __name__ == "__main__":
    main()
