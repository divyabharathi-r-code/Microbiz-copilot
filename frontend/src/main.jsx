import { Component, StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import App from './App'
import './styles.css'

class StartupBoundary extends Component {
  state = { error: null }

  static getDerivedStateFromError(error) {
    return { error }
  }

  render() {
    if (this.state.error) {
      return <main className="loading"><h1>MicroBiz couldn’t start</h1><p>{this.state.error.message || 'An unexpected frontend error occurred.'}</p><p>Open the browser console for details, then refresh after correcting the issue.</p></main>
    }
    return this.props.children
  }
}

createRoot(document.getElementById('root')).render(
  <StrictMode><StartupBoundary><App /></StartupBoundary></StrictMode>,
)
