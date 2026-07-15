import { BrowserRouter, Navigate, Route, Routes } from 'react-router-dom'
import AppShell from './layouts/AppShell'
import { AuthPage, LandingPage } from './pages/AuthPages'
import {
  AnalysisPage,
  AnalyticsPage,
  DashboardPage,
  InterviewPage,
  JobsPage,
  ProfilePage,
  ResumePage,
  SettingsPage,
} from './pages/DashboardPages'

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/login" element={<AuthPage type="login" />} />
        <Route path="/signup" element={<AuthPage type="signup" />} />
        <Route path="/forgot-password" element={<AuthPage type="forgot" />} />
        <Route path="/otp-verification" element={<AuthPage type="otp" />} />
        <Route path="/reset-password" element={<AuthPage type="reset" />} />
        <Route element={<AppShell />}>
          <Route path="/dashboard" element={<DashboardPage />} />
          <Route path="/resume" element={<ResumePage />} />
          <Route path="/upload" element={<ResumePage />} />
          <Route path="/analysis" element={<AnalysisPage />} />
          <Route path="/jobs" element={<JobsPage />} />
          <Route path="/interview" element={<InterviewPage />} />
          <Route path="/analytics" element={<AnalyticsPage />} />
          <Route path="/profile" element={<ProfilePage />} />
          <Route path="/settings" element={<SettingsPage />} />
        </Route>
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  )
}
