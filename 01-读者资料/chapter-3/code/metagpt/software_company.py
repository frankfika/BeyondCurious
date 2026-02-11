"""
MetaGPT 多智能体协作示例

来源：《动手做 AI Agent：零基础玩转智能体》
章节：第3章 3.13 节「MetaGPT：多智能体协作框架」
行号：第 8800-8950 行
页码：第 XX 页

用途：展示如何使用 MetaGPT 创建软件开发生命周期

安装：
    pip install metagpt
"""

import asyncio
from metagpt.roles import (
    Architect,
    Engineer,
    ProductManager,
    ProjectManager,
    QaEngineer,
)
from metagpt.software_company import SoftwareCompany


async def software_development_example():
    """
    MetaGPT 软件开发生命周期示例

    展示如何通过 MetaGPT 创建一个虚拟软件公司，
    包含产品经理、架构师、工程师、测试工程师等角色。
    """

    # 初始化软件公司
    company = SoftwareCompany()

    # 招聘团队成员
    company.hire([
        ProductManager(),  # 产品经理
        Architect(),       # 架构师
        ProjectManager(),  # 项目经理
        Engineer(),        # 工程师
        QaEngineer(),      # 测试工程师
    ])

    # 运行开发流程
    await company.run(
        n_rounds=5,
        idea="开发一个待办事项管理应用"
    )


async def single_role_example():
    """
    单角色使用示例

    展示如何单独使用某个角色完成特定任务。
    """
    from metagpt.roles import Engineer

    engineer = Engineer()
    task = "用 Python 实现一个简单的计算器"

    result = await engineer.run(task)
    print(result)


if __name__ == "__main__":
    # 运行完整示例
    asyncio.run(software_development_example())

    # 运行单角色示例
    # asyncio.run(single_role_example())
