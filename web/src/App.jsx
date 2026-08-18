import { useState } from "react";

const API_URL = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";

const examples = [
  "所有成功人士每天都早起，所以每天早起一定会成功。",
  "我认识的三个程序员都喜欢游戏，所以程序员都喜欢游戏。",
  "想要成功必须每天早起。",
];

function value(value) {
  if (value === true) return "是";
  if (value === false) return "否";
  if (value === null || value === undefined || value === "") return "—";
  return String(value);
}

function Section({ title, children, className = "" }) {
  return (
    <section className={`card ${className}`}>
      <div className="card-title">{title}</div>
      {children}
    </section>
  );
}

function EmptyState() {
  return (
    <div className="empty-state">
      <div className="empty-icon">⌁</div>
      <h2>等待分析</h2>
      <p>输入一条陈述，Logic Agent 会从命题结构、反例、逻辑谬误和认知偏差四个角度进行分析。</p>
    </div>
  );
}

function Result({ result }) {
  const claim = result.claim || {};
  const counterexample = result.counterexample;
  const factCheck = result.fact_check;
  const fallacy = result.fallacy || {};
  const bias = result.bias || {};

  const statusLabel = {
    accurate: "准确",
    inaccurate: "不准确",
    outdated: "已过时",
    partially_accurate: "部分准确",
    unverifiable: "无法核实",
  };

  return (
    <div className="results">
      <div className="input-preview">
        <span>分析对象</span>
        <strong>{result.input}</strong>
      </div>

      <Section title="核心判断">
        <div className="tag-row">
          <span className="tag primary">{value(claim.type)}</span>
          {claim.direction && <span className="tag">{claim.direction}</span>}
        </div>
        <div className="claim-flow">
          <div><small>主体</small><strong>{value(claim.subject)}</strong></div>
          <div className="arrow">→</div>
          <div><small>结论</small><strong>{value(claim.predicate)}</strong></div>
        </div>
        <p className="reason">{value(claim.reason)}</p>
        <div className="facts">
          <div><span>包含数据</span><b>{value(claim.has_data)}</b></div>
          <div><span>绝对命题</span><b>{value(claim.is_absolute)}</b></div>
          <div><span>需要反例</span><b>{value(claim.requires_counterexample)}</b></div>
        </div>
      </Section>

      {counterexample ? (
        <Section title="反例分析">
          <div className="counterexample">{value(counterexample.counterexample)}</div>
          <div className="facts two">
            <div><span>逻辑有效</span><b>{value(counterexample.logically_valid)}</b></div>
            <div><span>前提满足</span><b>{value(counterexample.premise_satisfied)}</b></div>
            <div><span>结论违反</span><b>{value(counterexample.conclusion_violated)}</b></div>
            <div><span>反例强度</span><b>{value(counterexample.strength)}</b></div>
            <div><span>可信度</span><b>{value(counterexample.confidence)}</b></div>
            <div><span>证据类型</span><b>{value(counterexample.evidence_type)}</b></div>
          </div>
          <p className="reason">{value(counterexample.reason)}</p>
          {counterexample.limitations && (
            <p className="muted">局限：{counterexample.limitations}</p>
          )}
        </Section>
      ) : (
        <Section title="反例分析">
          <div className="not-applicable">当前命题不要求生成反例。</div>
        </Section>
      )}

      {factCheck && (
        <Section title="事实核查">
          <div className="tag-row">
            <span className={`tag ${factCheck.verification_status === "accurate" ? "primary" : "warning"}`}>
              {statusLabel[factCheck.verification_status] || value(factCheck.verification_status)}
            </span>
          </div>
          <div className="claim-flow">
            <div><small>陈述数据</small><strong>{value(factCheck.reported_value)}</strong></div>
            <div className="arrow">→</div>
            <div><small>核实结果</small><strong>{value(factCheck.verified_value)}</strong></div>
          </div>
          <div className="facts two">
            <div><span>可信度</span><b>{value(factCheck.confidence)}</b></div>
          </div>
          <p className="reason">{value(factCheck.reason)}</p>
          {factCheck.note && (
            <p className="muted">说明：{factCheck.note}</p>
          )}
          {factCheck.evidence_sources && factCheck.evidence_sources.length > 0 && (
            <div className="sources">
              <span>信息来源</span>
              <ul>
                {factCheck.evidence_sources.map((url) => (
                  <li key={url}>
                    <a href={url} target="_blank" rel="noreferrer">{url}</a>
                  </li>
                ))}
              </ul>
            </div>
          )}
        </Section>
      )}

      <div className="grid-two">
        <Section title="逻辑谬误">
          <div className={`result-name ${fallacy.name === "none" ? "none" : "warning"}`}>
            {value(fallacy.name)}
          </div>
          <p className="reason">{value(fallacy.reason)}</p>
        </Section>
        <Section title="认知偏差">
          <div className={`result-name ${bias.name === "none" ? "none" : "warning"}`}>
            {value(bias.name)}
          </div>
          <p className="reason">{value(bias.reason)}</p>
        </Section>
      </div>
    </div>
  );
}

export default function App() {
  const [text, setText] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function analyze() {
    const input = text.trim();
    if (!input || loading) return;

    setLoading(true);
    setError("");
    setResult(null);

    try {
      const response = await fetch(`${API_URL}/api/analyze`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text: input }),
      });

      const data = await response.json();
      if (!response.ok) {
        throw new Error(data.detail || "服务器返回错误。");
      }
      setResult(data);
    } catch (err) {
      setError(
        `${err.message}。请确认 Python API 已启动（http://127.0.0.1:8000）。`
      );
    } finally {
      setLoading(false);
    }
  }

  function onKeyDown(event) {
    if ((event.ctrlKey || event.metaKey) && event.key === "Enter") {
      analyze();
    }
  }

  return (
    <main className="app-shell">
      <header className="topbar">
        <div className="brand">
          <div className="logo">L</div>
          <div>
            <div className="brand-name">Logic Agent</div>
            <div className="brand-subtitle">Structured reasoning analysis</div>
          </div>
        </div>
        <div className="status"><span /> API Ready</div>
      </header>

      <div className="content">
        <section className="hero">
          <p className="eyebrow">LOGICAL REASONING ENGINE</p>
          <h1>拆解一句话，看看它的逻辑。</h1>
          <p className="hero-copy">
            从命题结构出发，检查反例、逻辑谬误与认知偏差。结果由你的 Python LogicAgent 统一返回。
          </p>
        </section>

        <section className="composer card">
          <textarea
            value={text}
            onChange={(event) => setText(event.target.value)}
            onKeyDown={onKeyDown}
            placeholder="输入一句需要分析的陈述……"
            rows={5}
          />
          <div className="composer-footer">
            <div className="examples">
              {examples.map((example) => (
                <button key={example} onClick={() => setText(example)}>{example}</button>
              ))}
            </div>
            <button className="analyze-button" onClick={analyze} disabled={!text.trim() || loading}>
              {loading ? "分析中…" : "Analyze →"}
            </button>
          </div>
          <div className="shortcut">Ctrl / Cmd + Enter</div>
        </section>

        {error && <div className="error">{error}</div>}
        {loading && <div className="loading"><span className="spinner" /> Logic Agent 正在分析……</div>}
        {!result && !loading && !error && <EmptyState />}
        {result && !loading && <Result result={result} />}
      </div>
    </main>
  );
}
