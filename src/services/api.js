// Future backend integration points. No real requests are made in this frontend.
const mockSuccess = (payload) => {
  console.log('API placeholder payload:', payload)
  return Promise.resolve({ success: true })
}

export const login = (payload) => mockSuccess(payload)
export const signup = (payload) => mockSuccess(payload)
export const submitResume = (payload) => mockSuccess(payload)
export const searchJobs = (payload) => mockSuccess(payload)
export const applyToJob = (payload) => mockSuccess(payload)
export const saveProfile = (payload) => mockSuccess(payload)
export const saveSettings = (payload) => mockSuccess(payload)
