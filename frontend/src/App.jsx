import { useState, useEffect } from 'react'
import { fetchGoals, fetchRecommendations, getCurrentPosition } from './api'
import './App.css'

const GOAL_LABELS = {
  gain_muscle: 'Gain muscle',
  lose_weight: 'Lose weight',
  maintain: 'Maintain',
}

function MacroPill({ label, value, unit = 'g' }) {
  return (
    <span className="macro-pill">
      <strong>{value}{unit}</strong> {label}
    </span>
  )
}

function RestaurantCard({ option, budget }) {
  return (
    <article className="result-card restaurant">
      <div className="card-badge">Restaurant</div>
      <h3>{option.chain}</h3>
      <p className="location">{option.name} · {option.distance_miles} mi</p>
      <p className="address">{option.address}</p>
      <div className="order-box">
        <p className="order-label">Your order</p>
        <p className="order-text">{option.order}</p>
      </div>
      <div className="price-row">
        <span className="price">${option.price_with_tax.toFixed(2)}</span>
        <span className="price-note">incl. tax · ${(budget - option.price_with_tax).toFixed(2)} left</span>
      </div>
      <div className="macros">
        <MacroPill label="protein" value={option.protein_g} />
        <MacroPill label="cal" value={option.calories} unit="" />
        <MacroPill label="carbs" value={option.carbs_g} />
        <MacroPill label="fat" value={option.fat_g} />
      </div>
    </article>
  )
}

function GroceryCard({ option, budget }) {
  return (
    <article className="result-card grocery">
      <div className="card-badge heb">H-E-B</div>
      <h3>{option.store_chain}</h3>
      <p className="location">{option.store} · {option.distance_miles} mi</p>
      <p className="address">{option.address}</p>
      <div className="order-box">
        <p className="order-label">Shopping list</p>
        <ul className="item-list">
          {option.items.map((item) => (
            <li key={item}>{item}</li>
          ))}
        </ul>
        <p className="recipe">{option.recipe}</p>
        <p className="prep-time">~{option.prep_minutes} min prep</p>
      </div>
      <div className="price-row">
        <span className="price">${option.price_with_tax.toFixed(2)}</span>
        <span className="price-note">incl. tax · save vs restaurant</span>
      </div>
      <div className="macros">
        <MacroPill label="protein" value={option.protein_g} />
        <MacroPill label="cal" value={option.calories} unit="" />
        <MacroPill label="carbs" value={option.carbs_g} />
        <MacroPill label="fat" value={option.fat_g} />
      </div>
    </article>
  )
}

export default function App() {
  const [budget, setBudget] = useState(8)
  const [goal, setGoal] = useState('gain_muscle')
  const [goals, setGoals] = useState([])
  const [location, setLocation] = useState(null)
  const [locationStatus, setLocationStatus] = useState('idle')
  const [results, setResults] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  useEffect(() => {
    fetchGoals()
      .then(setGoals)
      .catch(() => {
        setGoals([
          { id: 'gain_muscle', label: 'Gain muscle' },
          { id: 'lose_weight', label: 'Lose weight' },
          { id: 'maintain', label: 'Maintain' },
        ])
      })
  }, [])

  async function handleUseLocation() {
    setLocationStatus('loading')
    setError(null)
    try {
      const pos = await getCurrentPosition()
      setLocation(pos)
      setLocationStatus('ok')
    } catch {
      setLocationStatus('error')
      setError('Could not get location — using downtown San Antonio as default.')
    }
  }

  async function handleSubmit(e) {
    e.preventDefault()
    setLoading(true)
    setError(null)
    setResults(null)

    try {
      const data = await fetchRecommendations({
        budget,
        goal,
        lat: location?.lat,
        lng: location?.lng,
      })
      setResults(data)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="app">
      <header className="hero">
        <div className="hero-content">
          <p className="eyebrow">San Antonio · H-E-B powered</p>
          <h1>Bite Budget</h1>
          <p className="tagline">
            Tell us your budget. We tell you exactly what to eat — restaurant order or H-E-B fix — right now.
          </p>
        </div>
      </header>

      <main className="main">
        <form className="search-form" onSubmit={handleSubmit}>
          <div className="form-row">
            <label className="field">
              <span>Cash in wallet</span>
              <div className="budget-input">
                <span className="dollar">$</span>
                <input
                  type="number"
                  min="1"
                  max="100"
                  step="0.50"
                  value={budget}
                  onChange={(e) => setBudget(Number(e.target.value))}
                  required
                />
              </div>
            </label>

            <label className="field">
              <span>Health goal</span>
              <select value={goal} onChange={(e) => setGoal(e.target.value)}>
                {(goals.length ? goals : Object.entries(GOAL_LABELS).map(([id, label]) => ({ id, label }))).map(
                  (g) => (
                    <option key={g.id} value={g.id}>{g.label}</option>
                  ),
                )}
              </select>
            </label>
          </div>

          <div className="location-row">
            <button
              type="button"
              className="location-btn"
              onClick={handleUseLocation}
              disabled={locationStatus === 'loading'}
            >
              {locationStatus === 'loading' ? 'Finding you…' : locationStatus === 'ok' ? '📍 Location set' : '📍 Use my location'}
            </button>
            {locationStatus === 'ok' && (
              <span className="location-hint">Searching near you in San Antonio</span>
            )}
          </div>

          <button type="submit" className="submit-btn" disabled={loading}>
            {loading ? 'Searching…' : 'Find my meals'}
          </button>
        </form>

        {error && <p className="error">{error}</p>}

        {results && (
          <section className="results">
            {results.message && <p className="results-message">{results.message}</p>}

            <div className="results-grid">
              {results.restaurant && (
                <RestaurantCard option={results.restaurant} budget={results.budget} />
              )}
              {results.grocery && (
                <GroceryCard option={results.grocery} budget={results.budget} />
              )}
            </div>

            {!results.restaurant && !results.grocery && (
              <p className="empty-state">Nothing under ${results.budget.toFixed(2)} — try $10 or switch goals.</p>
            )}

            <p className="disclaimer">
              Prices include ~8.25% SA sales tax. MVP uses curated estimates — always verify at the register.
            </p>
          </section>
        )}
      </main>

      <footer className="footer">
        <p>Built for San Antonio · Chipotle · Whataburger · Panda · Torchy's · H-E-B</p>
      </footer>
    </div>
  )
}
