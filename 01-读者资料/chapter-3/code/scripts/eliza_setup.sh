#!/bin/bash

###############################################################################
# ELiza 智能体环境配置脚本
#
# 来源：《动手做 AI Agent：零基础玩转智能体》
# 章节：第3章 智能体部署相关
# 行号：第 9424-9573 行
# 页码：第 XX 页
#
# 用途：一键配置智能体运行环境
###############################################################################

set -e

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo_info() { echo -e "${GREEN}[INFO]${NC} $1"; }
echo_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
echo_error() { echo -e "${RED}[ERROR]${NC} $1"; }

main() {
    echo_info "开始配置 ELiza 智能体环境..."

    # 1. 创建虚拟环境
    echo_info "创建 Python 虚拟环境..."
    python3 -m venv eliza_env

    # 2. 激活虚拟环境并安装依赖
    echo_info "安装 Python 依赖..."
    source eliza_env/bin/activate
    pip install --upgrade pip
    pip install openai anthropic python-dotenv requests

    # 3. 创建配置文件
    echo_info "创建配置文件..."
    cat > .env << 'EOF'
# OpenAI 配置
OPENAI_API_KEY=your_key_here
OPENAI_API_BASE=https://api.openai.com/v1

# DeepSeek 配置
DEEPSEEK_API_KEY=your_key_here
DEEPSEEK_API_BASE=https://api.deepseek.com/v1

# 日志级别
LOG_LEVEL=INFO
MAX_TOKENS=2000
EOF

    echo_warn "请编辑 .env 文件，填入你的 API 密钥"

    # 4. 创建项目目录
    echo_info "创建项目目录结构..."
    mkdir -p {logs,data,prompts,outputs}

    # 5. 创建启动脚本
    cat > start.sh << 'EOF'
#!/bin/bash
source eliza_env/bin/activate
python main.py
EOF
    chmod +x start.sh

    echo_info "ELiza 环境配置完成！"
    echo_info "使用方法："
    echo "  1. 编辑 .env 文件"
    echo "  2. 运行: ./start.sh"
}

main "$@"
