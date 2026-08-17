#!/bin/bash
# Logic Agent 一键启动脚本
# 放在 logic_agent 项目根目录下（和 api.py 同一层）

set -e

# 脚本所在目录 = 项目根目录，保证无论从哪里执行都能找对路径
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$DIR"

# 1. 加载环境变量（DEEPSEEK_API_KEY）
if [ -f ".env" ]; then
  set -a
  source .env
  set +a
else
  echo "❌ 没找到 .env 文件。"
  echo "请在 $DIR 下新建一个 .env 文件，内容为："
  echo "DEEPSEEK_API_KEY=你的key"
  exit 1
fi

if [ -z "$DEEPSEEK_API_KEY" ]; then
  echo "❌ .env 里没有设置 DEEPSEEK_API_KEY，请检查内容。"
  exit 1
fi

# 2. 启动后端 (uvicorn)
echo "🚀 启动后端 (http://127.0.0.1:8000) ..."
uvicorn api:app --reload --port 8000 &
BACKEND_PID=$!

# 3. 启动前端 (vite)
echo "🚀 启动前端 (http://127.0.0.1:5173) ..."
cd "$DIR/web"
npm run dev &
FRONTEND_PID=$!

cd "$DIR"

# 4. Ctrl+C 时同时关闭前后端
trap "echo '🛑 停止服务...'; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null" EXIT INT TERM

wait