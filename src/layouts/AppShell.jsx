import { useState } from 'react'
import { NavLink, Outlet } from 'react-router-dom'

const navItems = [
  ['Overview', '/dashboard', '▦'], ['Resume', '/resume', '▤'], ['Job matching', '/jobs', '⌕'],
  ['Resume analysis', '/analysis', '◔'], ['Interview prep', '/interview', '◌'], ['Analytics', '/analytics', '↗'],
]

export default function AppShell() {
  const [open, setOpen] = useState(false)
  const close = () => setOpen(false)
  return <div className="app-shell">
    <button className="mobile-menu" aria-label="Open navigation" onClick={() => setOpen(true)}>☰</button>
    <aside className={`sidebar ${open ? 'sidebar--open' : ''}`}>
      <div className="brand"><span>IH</span><div><strong>InsightHire</strong><small>Career workspace</small></div><button aria-label="Close navigation" onClick={close}>×</button></div>
      <nav aria-label="Main navigation">{navItems.map(([label, path, icon]) => <NavLink end={path === '/dashboard'} key={path} to={path} onClick={close}><i>{icon}</i>{label}</NavLink>)}</nav>
      <div className="sidebar-bottom"><NavLink to="/profile" onClick={close}><i>◉</i>Profile</NavLink><NavLink to="/settings" onClick={close}><i>⚙</i>Settings</NavLink><div className="user-card"><span>AK</span><div><strong>Arjun Kumar</strong><small>Job seeker</small></div></div></div>
    </aside>
    {open && <button className="sidebar-overlay" aria-label="Close navigation" onClick={close} />}
    <main className="content"><header className="topbar"><div><p>Tuesday, July 15</p><strong>Good morning, Arjun</strong></div><button className="notification" aria-label="Notifications">●</button></header><Outlet /></main>
  </div>
}
