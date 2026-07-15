import { Link, useNavigate } from 'react-router-dom'
import { Button, LinkButton } from '../components/ui'
import { login, signup } from '../services/api'

const copy = {
  login: ['Welcome back', 'Sign in to continue building your career profile.', 'Sign in'],
  signup: ['Create your account', 'Set up your profile and receive tailored job recommendations.', 'Create account'],
  forgot: ['Forgot your password?', 'Enter your email and we will send a reset link.', 'Send reset link'],
  otp: ['Verify your email', 'Enter the six-digit code sent to your inbox.', 'Verify code'],
  reset: ['Set a new password', 'Choose a strong password to secure your account.', 'Reset password'],
}

export function LandingPage() {
  return <div className="landing"><header><Link className="brand brand--landing" to="/"><span>IH</span><strong>InsightHire</strong></Link><div><Link to="/login">Sign in</Link><LinkButton to="/signup">Get started</LinkButton></div></header><main><section className="hero-copy"><p className="eyebrow">CAREER INTELLIGENCE, SIMPLIFIED</p><h1>Make every job application count.</h1><p>InsightHire brings your resume, applications, interview practice, and job matches into one focused workspace.</p><div className="hero-actions"><LinkButton to="/signup">Create your profile</LinkButton><LinkButton to="/login" variant="secondary">Sign in</LinkButton></div><div className="trust-row"><span>Resume insights</span><span>Job matching</span><span>Interview prep</span></div></section><section className="hero-panel"><p className="panel-label">YOUR CAREER SNAPSHOT</p><h2>Ready for your next opportunity</h2><div className="hero-score"><strong>82</strong><span>ATS score<br />+8 this month</span></div><div className="mini-bars"><i /><i /><i /><i /><i /></div><div className="mini-note"><b>3</b><span>interviews scheduled this month</span></div></section></main></div>
}

export function AuthPage({ type }) {
  const navigate = useNavigate(); const [title, description, buttonText] = copy[type]
  async function handleSubmit(event) { event.preventDefault(); const payload = Object.fromEntries(new FormData(event.currentTarget)); if (type === 'login') await login(payload); if (type === 'signup') await signup(payload); navigate(type === 'forgot' ? '/otp-verification' : type === 'otp' ? '/reset-password' : '/dashboard') }
  return <div className="auth-layout"><Link className="brand auth-brand" to="/"><span>IH</span><strong>InsightHire</strong></Link><section className="auth-card"><p className="eyebrow">CAREER WORKSPACE</p><h1>{title}</h1><p>{description}</p><form onSubmit={handleSubmit}>
    {type === 'signup' && <Field label="Full name" name="fullName" autoComplete="name" />}
    {['login', 'signup', 'forgot'].includes(type) && <Field label="Email address" name="email" type="email" autoComplete="email" />}
    {type === 'otp' && <Field label="Verification code" name="otp" inputMode="numeric" placeholder="000000" />}
    {['login', 'signup', 'reset'].includes(type) && <Field label={type === 'reset' ? 'New password' : 'Password'} name={type === 'reset' ? 'newPassword' : 'password'} type="password" autoComplete="current-password" />}
    {['signup', 'reset'].includes(type) && <Field label="Confirm password" name="confirmPassword" type="password" autoComplete="new-password" />}
    {type === 'login' && <div className="form-row"><label className="check"><input name="rememberMe" type="checkbox" />Remember me</label><Link to="/forgot-password">Forgot password?</Link></div>}
    <Button type="submit" className="full-width">{buttonText}</Button>
  </form><p className="auth-footer">{type === 'login' ? <>New to InsightHire? <Link to="/signup">Create an account</Link></> : <>Already have an account? <Link to="/login">Sign in</Link></>}</p></section></div>
}
function Field({ label, name, type = 'text', ...rest }) { return <label className="field"><span>{label}</span><input name={name} type={type} required {...rest} /></label> }
