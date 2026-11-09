import { useEffect, useMemo, useState } from 'react'
import { api } from './services/api'

const money = value => new Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR', maximumFractionDigits: 0 }).format((value || 0) / 100)
const compact = value => new Intl.NumberFormat('en-IN', { notation: 'compact', maximumFractionDigits: 1 }).format((value || 0) / 100)
const Icon = ({ children }) => <span className="icon" aria-hidden="true">{children}</span>

function Metric({ label, value, note, tone = 'blue' }) {
  return <section className="metric"><div className={`metric-icon ${tone}`}><Icon>{tone === 'green' ? '↗' : tone === 'amber' ? '◷' : tone === 'red' ? '↩' : '₹'}</Icon></div><div><p>{label}</p><h2>{value}</h2><small>{note}</small></div></section>
}

function SalesChart({ points }) {
  const max = Math.max(...points.map(p => p.amount_paise), 1)
  return <div className="chart" aria-label="Seven day captured sales chart">{points.map((point, index) => <div className="bar-wrap" key={point.date}><span className="bar-value">{point.amount_paise ? compact(point.amount_paise) : ''}</span><div className="bar" style={{ height: `${Math.max(5, point.amount_paise / max * 100)}%` }} /><span>{index === 0 ? 'Mon' : index === 1 ? 'Tue' : index === 2 ? 'Wed' : index === 3 ? 'Thu' : index === 4 ? 'Fri' : index === 5 ? 'Sat' : 'Sun'}</span></div>)}</div>
}

function Copilot({ onNavigate }) {
  const [messages, setMessages] = useState([{ role: 'assistant', text: 'Hi! I can explain the numbers behind your business—try asking about sales or orders that need attention.' }])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const ask = async question => {
    if (!question.trim() || loading) return
    setMessages(items => [...items, { role: 'user', text: question }]); setInput(''); setLoading(true)
    try { const result = await api.chat(question); setMessages(items => [...items, { role: 'assistant', text: result.answer, tool: result.tool }]) }
    catch (error) { setMessages(items => [...items, { role: 'assistant', text: `I couldn't determine that right now: ${error.message}`, error: true }]) }
    finally { setLoading(false) }
  }
  return <section className="copilot-card"><div className="copilot-head"><div><span className="eyebrow">MICROBIZ COPILOT</span><h2>Ask about your business</h2></div><span className="live"><i />Grounded data</span></div><div className="messages">{messages.map((message, i) => <div className={`message ${message.role}`} key={i}><div className="avatar">{message.role === 'assistant' ? '✦' : 'YO'}</div><div><p>{message.text}</p>{message.tool && <small className="source">Verified via {message.tool}</small>}</div></div>)}{loading && <div className="message assistant"><div className="avatar">✦</div><p className="typing">Checking your records<span>.</span><span>.</span><span>.</span></p></div>}</div><div className="suggestions"><button onClick={() => ask('Compare this week with last week')}>Compare this week</button><button onClick={() => ask('Which orders need attention?')}>Orders needing attention</button></div><form onSubmit={e => { e.preventDefault(); ask(input) }}><input value={input} onChange={e => setInput(e.target.value)} placeholder="Ask a question about your business…" aria-label="Copilot question"/><button className="send" aria-label="Send question">↑</button></form><p className="disclaimer">Numbers are calculated from your payment records. The Copilot cannot move money or send messages.</p></section>
}

function Orders({ orders, attention, onDraft }) {
  const [tab, setTab] = useState('Orders')
  const show = tab === 'Needs attention' ? attention : orders
  return <section className="orders-card"><div className="section-heading"><div><span className="eyebrow">OPERATIONS</span><h2>{tab === 'Orders' ? 'Recent orders' : 'Payment follow-ups'}</h2></div><button className="link" onClick={() => setTab(tab === 'Orders' ? 'Needs attention' : 'Orders')}>{tab === 'Orders' ? 'View attention queue →' : '← View orders'}</button></div><div className="tabs"><button className={tab === 'Orders' ? 'active' : ''} onClick={() => setTab('Orders')}>All orders</button><button className={tab === 'Needs attention' ? 'active' : ''} onClick={() => setTab('Needs attention')}>Needs attention <b>{attention.length}</b></button></div><div className="table-wrap"><table><thead><tr><th>ORDER</th><th>CUSTOMER</th><th>PAYMENT STATUS</th><th className="right">AMOUNT</th><th /></tr></thead><tbody>{show.slice(0, 5).map(order => <tr key={order.id}><td><strong>#{String(order.id).padStart(4, '0')}</strong><span>{new Date(order.created_at).toLocaleDateString('en-IN', { day: 'numeric', month: 'short' })}</span></td><td>{order.customer_email}</td><td><span className={`pill ${order.payment_status?.toLowerCase()}`}>{order.payment_status?.replace('_', ' ')}</span></td><td className="right"><strong>{money(order.total_paise)}</strong></td><td>{tab === 'Needs attention' && <button className="draft" onClick={() => onDraft(order.id)}>Draft reminder</button>}</td></tr>)}</tbody></table></div></section>
}

function App() {
  const [data, setData] = useState(null), [orders, setOrders] = useState([]), [attention, setAttention] = useState([]), [error, setError] = useState(''), [draft, setDraft] = useState(null)
  useEffect(() => { Promise.all([api.summary(), api.orders(), api.eligible()]).then(([summary, orderResponse, eligible]) => { setData(summary); setOrders(orderResponse.items); setAttention(eligible.items) }).catch(e => setError(e.message)) }, [])
  const totalOpen = useMemo(() => attention.reduce((sum, order) => sum + order.total_paise, 0), [attention])
  const createDraft = async id => { try { setDraft(await api.draft(id)) } catch (e) { setError(e.message) } }
  if (error && !data) return <main className="loading"><h1>MicroBiz</h1><p>Couldn’t load your workspace: {error}</p><button onClick={() => location.reload()}>Try again</button></main>
  if (!data) return <main className="loading"><div className="spinner"/><p>Loading your business pulse…</p></main>
  return <div className="app-shell"><aside><div className="brand"><span>m</span>microbiz</div><nav><a className="selected"><Icon>▦</Icon>Overview</a><a><Icon>▤</Icon>Orders</a><a><Icon>◌</Icon>Payments</a><a><Icon>◈</Icon>Products</a></nav><div className="side-bottom"><a><Icon>?</Icon>Help centre</a><div className="user"><div>RS</div><span>R. Sharma<small>Owner</small></span><b>⌄</b></div></div></aside><main><header><div><span className="eyebrow">GOOD MORNING, R. SHARMA</span><h1>Here’s your business pulse.</h1><p>Monday, 2 November · <span className="sandbox">SANDBOX DATA</span></p></div><button className="ghost">↗ Export report</button></header><div className="metrics"><Metric label="Captured sales" value={money(data.captured_sales_paise)} note="Last 7 days · captured only" tone="blue"/><Metric label="Completed payments" value={data.captured_payment_count} note="Successfully captured" tone="green"/><Metric label="Refunds" value={money(data.refunds_paise)} note="Shown separately from sales" tone="red"/><Metric label="Open to collect" value={money(totalOpen)} note={`${data.pending_orders} pending payment${data.pending_orders !== 1 ? 's' : ''}`} tone="amber"/></div><section className="sales-card"><div className="section-heading"><div><span className="eyebrow">CAPTURED REVENUE</span><h2>Sales momentum</h2></div><div className="period">Last 7 days <b>⌄</b></div></div><SalesChart points={data.daily_sales}/><footer><span><i className="dot"/>Captured payments only</span><span>Reporting period: {data.period.start} — {data.period.end}</span></footer></section><div className="lower"><Orders orders={orders} attention={attention} onDraft={createDraft}/><Copilot /></div></main>{draft && <div className="modal-backdrop" role="presentation"><div className="modal" role="dialog" aria-modal="true"><button className="close" onClick={() => setDraft(null)}>×</button><span className="eyebrow">REVIEW REQUIRED</span><h2>Payment reminder draft</h2><p>{draft.draft}</p><div className="notice">This is a draft only. No message has been sent.</div><div className="modal-actions"><button className="ghost" onClick={() => setDraft(null)}>Close</button><button className="approve" onClick={() => setDraft(null)}>Approve & send (demo)</button></div></div></div>}</div>
}
export default App
