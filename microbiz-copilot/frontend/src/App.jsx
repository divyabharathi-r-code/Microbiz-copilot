import { useEffect, useState } from 'react';
import {
  Activity, ArrowDownRight, ArrowUpRight, Bot, CircleDollarSign,
  CreditCard, MessageCircle, Package, RefreshCw, Send, ShoppingBag,
  Sparkles, Wallet, Clock3
} from 'lucide-react';

const demoMetrics = [
  { label: 'Captured sales', value: '₹15,240', change: '+12.8%', up: true, icon: CircleDollarSign },
  { label: 'Completed payments', value: '38', change: '+8.2%', up: true, icon: CreditCard },
  { label: 'Pending orders', value: '7', change: 'Needs review', up: false, icon: Clock3 },
  { label: 'Refunds', value: '₹850', change: '3 transactions', up: false, icon: RefreshCw },
];

const demoOrders = [
  { id: 'MB-1048', customer: 'Aarav S.', item: 'Handmade gift box', amount: '₹1,250', status: 'Captured' },
  { id: 'MB-1047', customer: 'Meera K.', item: 'Ceramic coffee mug', amount: '₹650', status: 'Pending' },
  { id: 'MB-1046', customer: 'Rohan P.', item: 'Cotton tote bag', amount: '₹480', status: 'Captured' },
  { id: 'MB-1045', customer: 'Isha R.', item: 'Desk planter', amount: '₹920', status: 'Action needed' },
];

const prompts = [
  'Summarise my sales this week',
  'Which orders need attention?',
  'Draft a payment reminder',
];

function MetricCard({ metric }) {
  const Icon = metric.icon;
  return (
    <article className="metric-card">
      <div className="metric-top">
        <span className="metric-icon"><Icon size={19} /></span>
        <span className={metric.up ? 'trend positive' : 'trend neutral'}>
          {metric.up ? <ArrowUpRight size={14} /> : <ArrowDownRight size={14} />}
          {metric.change}
        </span>
      </div>
      <p className="metric-label">{metric.label}</p>
      <h2>{metric.value}</h2>
    </article>
  );
}

export default function App() {
  
const [metrics, setMetrics] = useState(null);
const [metricsError, setMetricsError] = useState("");

async function loadMetrics() {
  try {
    setMetricsError("");

    const response = await fetch(
      "http://127.0.0.1:8000/api/dashboard/summary"
    );

    if (!response.ok) {
      throw new Error("Failed to load dashboard metrics");
    }

    const data = await response.json();
    setMetrics(data);
  } catch (error) {
    setMetricsError(error.message);
  }
}

useEffect(() => {
  loadMetrics();
}, []);

const displayMetrics = metrics
  ? [
      {
        label: "Captured sales",
        value: new Intl.NumberFormat("en-IN", {
          style: "currency",
          currency: "INR",
          maximumFractionDigits: 0,
        }).format(metrics.captured_sales),
        change: "Live database",
        up: true,
        icon: CircleDollarSign,
      },
      {
        label: "Completed payments",
        value: String(metrics.completed_payments),
        change: "Live database",
        up: true,
        icon: CreditCard,
      },
      {
        label: "Pending orders",
        value: String(metrics.pending_orders),
        change: "Live database",
        up: false,
        icon: Clock3,
      },
      {
        label: "Refunds",
        value: new Intl.NumberFormat("en-IN", {
          style: "currency",
          currency: "INR",
          maximumFractionDigits: 0,
        }).format(metrics.refunds),
        change: "Live database",
        up: false,
        icon: RefreshCw,
      },
    ]
  : demoMetrics;

  const [apiStatus, setApiStatus] = useState('checking');
  const [question, setQuestion] = useState('');
  const [messages, setMessages] = useState([
    { role: 'assistant', text: 'Hi! I’m your MicroBiz Copilot. I can help you understand sales, review orders, and prepare payment follow-ups. These are demo figures for now.' },
  ]);

  useEffect(() => {
    fetch('http://127.0.0.1:8000/health')
      .then((response) => {
        if (!response.ok) throw new Error('API unavailable');
        return response.json();
      })
      .then((data) => setApiStatus(data.status === 'ok' ? 'connected' : 'offline'))
      .catch(() => setApiStatus('offline'));
  }, []);

  function sendQuestion(text = question) {
    const clean = text.trim();
    if (!clean) return;
    setMessages((current) => [
      ...current,
      { role: 'user', text: clean },
      { role: 'assistant', text: 'AI analysis is not connected yet. This starter UI uses demo data only. Next, we’ll connect a FastAPI endpoint that calculates answers from verified application records.' },
    ]);
    setQuestion('');
  }

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand">
          <div className="brand-mark"><Activity size={22} /></div>
          <div><strong>microbiz</strong><span> COPILOT</span></div>
        </div>
        <div className="workspace-label">WORKSPACE</div>
        <nav>
          <a className="nav-item active" href="#overview"><Activity size={18} /> Overview</a>
          <a className="nav-item" href="#orders"><ShoppingBag size={18} /> Orders <span className="nav-count">7</span></a>
          <a className="nav-item" href="#copilot"><Bot size={18} /> AI Copilot</a>
          <a className="nav-item" href="#payments"><Wallet size={18} /> Payments</a>
        </nav>
        <div className="sidebar-bottom">
          <div className="sandbox-note"><span className="pulse-dot" /> Sandbox workspace <small>Demo data only</small></div>
          <div className="profile"><div className="avatar">MB</div><div><strong>Demo Store</strong><small>Owner workspace</small></div></div>
        </div>
      </aside>

      <main className="main-content">
        <header className="topbar">
          <div><span className="eyebrow">MONDAY, OCTOBER 19</span><h1>Good morning, business owner <span>✦</span></h1><p>Here’s what’s happening with your store today.</p></div>
          <div className="topbar-actions"><span className={`api-pill ${apiStatus}`}><span className="status-dot" /> API {apiStatus}</span><button className="icon-button" aria-label="Notifications"><MessageCircle size={18} /></button><div className="avatar">MB</div></div>
        </header>

        <section className="demo-banner"><Sparkles size={18} /><div><strong>Portfolio prototype</strong><span>All displayed business figures and orders are illustrative demo data, not real transactions.</span></div></section>

        <section id="overview" className="section-block">
          <div className="section-heading"><div><h2>Business overview</h2><p>Performance snapshot · Demo reporting period</p></div><button className="outline-button" onClick={() => window.location.reload()}><RefreshCw size={15} /> Refresh</button></div>
          
<div className="metric-grid">
  {displayMetrics.map((metric) => (
    <MetricCard key={metric.label} metric={metric} />
  ))}
</div>

        </section>

        <section className="content-grid">
          <article className="panel sales-panel">
            <div className="panel-heading"><div><h3>Sales activity</h3><p>Illustrative daily captured sales</p></div><span className="tiny-tag">7 days</span></div>
            <div className="chart-area" aria-label="Illustrative sales chart">
              {[42, 65, 49, 78, 57, 88, 70].map((height, index) => <div className="bar-column" key={index}><div className="bar-track"><div className={`bar ${index === 5 ? 'highlight' : ''}`} style={{ height: `${height}%` }} /></div><span>{['Mon','Tue','Wed','Thu','Fri','Sat','Sun'][index]}</span></div>)}
            </div>
            <div className="chart-foot"><span><i className="legend-dot" /> Captured sales</span><span>Illustrative data</span></div>
          </article>

          <article id="copilot" className="panel copilot-panel">
            <div className="panel-heading"><div className="copilot-title"><span className="ai-icon"><Bot size={19} /></span><div><h3>Business Copilot</h3><p>Ask about your business</p></div></div><span className="online-label">● Demo</span></div>
            <div className="chat-messages" aria-live="polite">{messages.map((message, index) => <div className={`chat-message ${message.role}`} key={index}><span className="message-avatar">{message.role === 'assistant' ? <Sparkles size={14} /> : 'You'}</span><p>{message.text}</p></div>)}</div>
            <div className="prompt-chips">{prompts.map((prompt) => <button key={prompt} onClick={() => sendQuestion(prompt)}>{prompt}</button>)}</div>
            <form className="chat-input" onSubmit={(event) => { event.preventDefault(); sendQuestion(); }}><input value={question} onChange={(event) => setQuestion(event.target.value)} placeholder="Ask about your sales or orders…" aria-label="Ask the copilot" /><button type="submit" aria-label="Send question"><Send size={17} /></button></form>
            <p className="ai-disclaimer">Demo mode · AI answers are not connected yet</p>
          </article>
        </section>

        <section id="orders" className="section-block orders-section">
          <div className="section-heading"><div><h2>Recent orders</h2><p>Review order and payment status</p></div><button className="outline-button" onClick={() => document.getElementById('orders-table')?.scrollIntoView({ behavior: 'smooth', block: 'center' })}>View orders <Package size={15} /></button></div>
          <div className="panel table-panel"><div className="orders-table-wrap"><table id="orders-table"><thead><tr><th>ORDER</th><th>CUSTOMER</th><th>ITEM</th><th>AMOUNT</th><th>PAYMENT STATUS</th></tr></thead><tbody>{demoOrders.map((order) => <tr key={order.id}><td className="order-id">{order.id}</td><td>{order.customer}</td><td>{order.item}</td><td className="amount">{order.amount}</td><td><span className={`status-badge ${order.status.toLowerCase().replace(' ', '-')}`}>{order.status}</span></td></tr>)}</tbody></table></div></div>
        </section>

        <footer><span>MicroBiz Copilot · Portfolio starter</span><span><CreditCard size={14} /> PayPal sandbox integration planned</span></footer>
      </main>
    </div>
  );
}
