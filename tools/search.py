"""
tools/search.py

给 CounterexampleGenerator 用的检索工具。

设计原则：
1. 不是每次都搜索 —— 由 LLM 先判断这次反例是否"需要事实/统计数据"支撑，
   纯逻辑反例（比如反证一个全称命题的结构性反例）不需要检索，省时间省钱。
2. 只从权威信源检索 —— 用 include_domains 白名单限定政府/统计局/权威媒体/学术机构，
   用 exclude_domains 黑名单排除知乎、小红书、微博等 UGC 平台。
3. 搜不到就如实说搜不到 —— 不强行编造，交给上层决定是否降级为理论构造反例。

依赖：Tavily Search API（对 LLM 应用场景友好，返回结构化摘要，免费额度可先跑通）。
注册地址：https://tavily.com
安装：pip install tavily-python
在 .env 里加一行：TAVILY_API_KEY=你的key
"""

import os
from tavily import TavilyClient


# ------------------------------------------------------------------
# 权威信源白名单 / 黑名单
# 按需增删，原则：官方一手数据源 > 权威媒体 > 学术机构，一律排除 UGC / 自媒体平台
# ------------------------------------------------------------------

AUTHORITATIVE_DOMAINS = [
    # 中国政府 / 官方统计
    "stats.gov.cn",       # 国家统计局
    "gov.cn",              # 中国政府网
    "people.com.cn",       # 人民日报
    "xinhuanet.com",       # 新华网
    "cctv.com",             # 央视

    # 国际权威媒体 / 通讯社
    "reuters.com",
    "apnews.com",
    "bbc.com",

    # 国际组织 / 官方数据
    "un.org",
    "who.int",
    "worldbank.org",
    "oecd.org",

    # 学术 / 研究机构
    "pewresearch.org",
    "nature.com",
    "sciencedirect.com",
    "jstor.org",
]

EXCLUDED_DOMAINS = [
    "zhihu.com",
    "xiaohongshu.com",
    "weibo.com",
    "tieba.baidu.com",
    "douban.com",
    "baijiahao.baidu.com",
    "toutiao.com",
]


class SearchTool:

    def __init__(self):
        api_key = os.environ.get("TAVILY_API_KEY")
        self.enabled = bool(api_key)
        if self.enabled:
            self.client = TavilyClient(api_key=api_key)

    def search(self, query: str, max_results: int = 5):
        """
        对权威信源做搜索，返回结构化结果列表。
        如果没配置 TAVILY_API_KEY，直接返回空列表，上层会自动降级为理论构造反例。
        """
        if not self.enabled:
            return []

        try:
            result = self.client.search(
                query=query,
                search_depth="advanced",
                include_domains=AUTHORITATIVE_DOMAINS,
                exclude_domains=EXCLUDED_DOMAINS,
                max_results=max_results,
            )
        except Exception:
            # 搜索服务本身出错（网络/额度等），不要让整个分析流程崩掉，
            # 静默降级，让上层退回理论构造反例。
            return []

        results = []
        for item in result.get("results", []):
            results.append({
                "title": item.get("title", ""),
                "url": item.get("url", ""),
                "snippet": item.get("content", "")[:300],
            })

        return results

    def format_for_prompt(self, results):
        """把搜索结果整理成可以直接塞进 LLM prompt 的文本块。"""
        if not results:
            return "（未检索到权威信源相关数据）"

        lines = []
        for i, r in enumerate(results, 1):
            lines.append(f"[{i}] {r['title']}\n来源：{r['url']}\n摘要：{r['snippet']}")

        return "\n\n".join(lines)
