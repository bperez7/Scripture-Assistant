import { useEffect, useMemo, useState } from 'react'
import './App.css'
import { askQuestion, getBooks, getChapter, getChapters, getVolumes, searchScriptures } from './api'

const Icon = ({ name, size = 20 }) => {
  const paths = {
    book: <><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2Z"/></>,
    search: <><circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/></>,
    sparkle: <path d="m12 3-1.3 3.5A6.5 6.5 0 0 1 7 10.2L3.5 11.5 7 12.8a6.5 6.5 0 0 1 3.7 3.7L12 20l1.3-3.5a6.5 6.5 0 0 1 3.7-3.7l3.5-1.3-3.5-1.3a6.5 6.5 0 0 1-3.7-3.7L12 3Z"/>,
    arrow: <><path d="M5 12h14"/><path d="m13 6 6 6-6 6"/></>,
    close: <><path d="m18 6-12 12"/><path d="m6 6 12 12"/></>,
  }
  return <svg className="icon" width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">{paths[name]}</svg>
}

function VerseCard({ verse }) {
  return <article className="verse-card"><span className="verse-number">{verse.verse}</span><div><strong>{verse.reference}</strong><p>{verse.text}</p></div></article>
}

function App() {
  const [view, setView] = useState('ask')
  const [question, setQuestion] = useState('')
  const [answer, setAnswer] = useState(null)
  const [askLoading, setAskLoading] = useState(false)
  const [error, setError] = useState('')
  const [query, setQuery] = useState('')
  const [results, setResults] = useState([])
  const [searchLoading, setSearchLoading] = useState(false)
  const [volumes, setVolumes] = useState([])
  const [books, setBooks] = useState([])
  const [chapters, setChapters] = useState([])
  const [selection, setSelection] = useState({ volume: '', book: '', chapter: '' })
  const [verses, setVerses] = useState([])
  const [browseLoading, setBrowseLoading] = useState(false)

  useEffect(() => {
    getVolumes().then(setVolumes).catch(() => setError('Could not connect to the scripture library. Is the API running?'))
  }, [])
  useEffect(() => {
    if (!selection.volume) return
    setBooks([]); setChapters([]); setVerses([])
    getBooks(selection.volume).then(setBooks).catch(() => setError('Unable to load books.'))
  }, [selection.volume])
  useEffect(() => {
    if (!selection.book) return
    setChapters([]); setVerses([])
    getChapters(selection.book).then(setChapters).catch(() => setError('Unable to load chapters.'))
  }, [selection.book])
  useEffect(() => {
    if (!selection.book || !selection.chapter) return
    setBrowseLoading(true); setVerses([])
    getChapter(selection.book, selection.chapter).then(setVerses).catch(() => setError('Unable to load this chapter.')).finally(() => setBrowseLoading(false))
  }, [selection.book, selection.chapter])

  const bookLabel = useMemo(() => selection.book && selection.chapter ? `${selection.book} ${selection.chapter}` : 'Choose a chapter', [selection])

  async function handleAsk(event) {
    event.preventDefault()
    if (!question.trim() || askLoading) return
    setAskLoading(true); setError(''); setAnswer(null)
    try { setAnswer(await askQuestion(question.trim())) }
    catch { setError('The study assistant could not answer right now. Check that the API and OpenAI key are available.') }
    finally { setAskLoading(false) }
  }
  async function handleSearch(event) {
    event.preventDefault()
    if (!query.trim() || searchLoading) return
    setSearchLoading(true); setError(''); setResults([])
    try { setResults(await searchScriptures(query.trim())) }
    catch { setError('Search is unavailable. Check that the API is running.') }
    finally { setSearchLoading(false) }
  }
  function changeView(next) { setView(next); setError('') }

  return <div className="app-shell">
    <header className="site-header">
      <button className="brand" onClick={() => changeView('ask')}><span className="brand-mark"><Icon name="book" size={23}/></span><span><b>Scripture Study</b><small>Gospel Library Assistant</small></span></button>
      <nav aria-label="Main navigation">
        <button className={view === 'ask' ? 'active' : ''} onClick={() => changeView('ask')}>Ask</button>
        <button className={view === 'search' ? 'active' : ''} onClick={() => changeView('search')}>Search</button>
        <button className={view === 'browse' ? 'active' : ''} onClick={() => changeView('browse')}>Browse</button>
      </nav>
    </header>
    <main>
      {error && <div className="error-banner" role="alert"><span>{error}</span><button aria-label="Dismiss" onClick={() => setError('')}><Icon name="close" size={17}/></button></div>}
      {view === 'ask' && <section className="ask-view">
        <div className="eyebrow"><Icon name="sparkle" size={16}/> Scripture-guided answers</div>
        <h1>What would you like<br/>to study today?</h1>
        <p className="lede">Ask a gospel question and explore an answer grounded in scripture.</p>
        <form className="ask-box" onSubmit={handleAsk}>
          <textarea value={question} onChange={e => setQuestion(e.target.value)} placeholder="Ask about faith, hope, prayer, or a scripture passage…" rows="4" />
          <div className="ask-actions"><span>Answers include scripture references</span><button className="primary-button" disabled={!question.trim() || askLoading}>{askLoading ? <span className="spinner"/> : <Icon name="sparkle" size={17}/>} {askLoading ? 'Studying…' : 'Ask question'}</button></div>
        </form>
        {!answer && !askLoading && <div className="suggestions"><span>Try asking</span><div>{['How can faith help during trials?', 'What do the scriptures teach about prayer?', 'How can I find more peace?'].map(item => <button key={item} onClick={() => setQuestion(item)}>{item}<Icon name="arrow" size={16}/></button>)}</div></div>}
        {answer && <div className="answer-wrap"><article className="answer-card"><div className="answer-heading"><span><Icon name="sparkle" size={18}/></span><h2>Study answer</h2></div><p>{answer.answer}</p></article>{answer.citations?.length > 0 && <section className="citations"><h3>Scriptures referenced</h3><div className="citation-grid">{answer.citations.map((citation, index) => <article key={`${citation.reference}-${index}`}><strong>{citation.reference}</strong><p>{citation.text}</p></article>)}</div></section>}</div>}
      </section>}
      {view === 'search' && <section className="content-view">
        <div className="section-heading"><span className="section-icon"><Icon name="search" size={23}/></span><div><h1>Search the scriptures</h1><p>Find verses containing a word or phrase.</p></div></div>
        <form className="search-form" onSubmit={handleSearch}><Icon name="search" size={20}/><input value={query} onChange={e => setQuery(e.target.value)} placeholder="Search for faith, charity, peace…"/><button className="primary-button" disabled={!query.trim() || searchLoading}>{searchLoading ? 'Searching…' : 'Search'}</button></form>
        <div className="results-header">{results.length > 0 && <><h2>Results for “{query}”</h2><span>{results.length} verses</span></>}</div>
        {!searchLoading && results.length === 0 && query && <div className="empty-state"><Icon name="search" size={28}/><p>No results yet. Enter a phrase and start your search.</p></div>}
        <div className="verse-list">{results.map(verse => <VerseCard verse={verse} key={verse.id}/>)}</div>
      </section>}
      {view === 'browse' && <section className="content-view">
        <div className="section-heading"><span className="section-icon"><Icon name="book" size={23}/></span><div><h1>Browse the scriptures</h1><p>Choose a volume, book, and chapter to begin reading.</p></div></div>
        <div className="browse-controls">
          <label><span>Volume</span><select value={selection.volume} onChange={e => setSelection({ volume: e.target.value, book: '', chapter: '' })}><option value="">Select a volume</option>{volumes.map(v => <option key={v}>{v}</option>)}</select></label>
          <label><span>Book</span><select disabled={!selection.volume} value={selection.book} onChange={e => setSelection(s => ({ ...s, book: e.target.value, chapter: '' }))}><option value="">Select a book</option>{books.map(b => <option key={`${b.volume}-${b.name}`}>{b.name}</option>)}</select></label>
          <label><span>Chapter</span><select disabled={!selection.book} value={selection.chapter} onChange={e => setSelection(s => ({ ...s, chapter: e.target.value }))}><option value="">Select a chapter</option>{chapters.map(c => <option key={c}>{c}</option>)}</select></label>
        </div>
        <div className="chapter-heading"><div><span>{selection.volume || 'Scripture library'}</span><h2>{bookLabel}</h2></div>{verses.length > 0 && <small>{verses.length} verses</small>}</div>
        {browseLoading && <div className="loading-row"><span className="spinner dark"/> Loading chapter…</div>}
        {!browseLoading && verses.length === 0 && <div className="empty-state"><Icon name="book" size={30}/><p>Select a volume, book, and chapter above.</p></div>}
        <div className="verse-list">{verses.map(verse => <VerseCard verse={verse} key={verse.id}/>)}</div>
      </section>}
    </main>
    <footer><span>Built for thoughtful scripture study.</span><span>AI responses should complement personal study.</span></footer>
  </div>
}

export default App
