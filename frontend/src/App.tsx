import { useEffect } from 'react'
import { useAppDispatch, useAppSelector } from './app/hooks'
import { checkAuthStatus } from './features/auth/authSlice'
import AppRouter from './routes/AppRouter'
import { Loader } from './components/ui/Loader'

function App() {
  const dispatch = useAppDispatch()
  const { isLoading } = useAppSelector((state) => state.auth)

  useEffect(() => {
    dispatch(checkAuthStatus())
  }, [dispatch])

  if (isLoading) {
    return <Loader />
  }

  return <AppRouter />
}

export default App