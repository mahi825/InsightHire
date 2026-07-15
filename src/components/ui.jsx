import { Link } from 'react-router-dom'

export function Button({ children, variant = 'primary', className = '', ...props }) {
  return <button className={`button button--${variant} ${className}`} {...props}>{children}</button>
}

export function LinkButton({ to, children, variant = 'primary', className = '' }) {
  return <Link to={to} className={`button button--${variant} ${className}`}>{children}</Link>
}

export function Card({ children, className = '' }) {
  return <section className={`card ${className}`}>{children}</section>
}

export function PageHeader({ eyebrow, title, description, action }) {
  return <header className="page-header">
    <div>{eyebrow && <p className="eyebrow">{eyebrow}</p>}<h1>{title}</h1><p>{description}</p></div>
    {action}
  </header>
}

export function Progress({ value, label }) {
  return <div className="progress-wrap"><div className="progress-label"><span>{label}</span><strong>{value}%</strong></div><div className="progress"><span style={{ width: `${value}%` }} /></div></div>
}
