
import React, { useState } from 'react'
import styled from 'styled-components'
import { motion } from 'framer-motion'
import { useNavigate, Link } from 'react-router-dom'
import { Container, Card, Button, Input } from '../styles/GlobalStyle'
import { useAuth } from '../context/AuthContext'
import { Eye, EyeOff, Lock, Mail } from 'lucide-react'

const LoginPage = () => {
  const navigate = useNavigate()
  const { login } = useAuth()
  const [formData, setFormData] = useState({
    email: '',
    password: ''
  })
  const [showPassword, setShowPassword] = useState(false)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setError('')

    try {
      const success = await login(formData.email, formData.password)
      if (success) {
        navigate('/dashboard')
      } else {
        setError('Invalid email or password')
      }
    } catch (err) {
      setError('An error occurred. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData(prev => ({
      ...prev,
      [e.target.name]: e.target.value
    }))
  }

  return (
    <LoginContainer>
      <Container>
        <LoginCard
          as={motion.div}
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
        >
          <Header>
            <Logo className="matrix-text">THE MATRIX</Logo>
            <Title>Welcome Back</Title>
            <Subtitle>Enter your credentials to access your dashboard</Subtitle>
          </Header>

          <Form onSubmit={handleSubmit}>
            {error && <ErrorMessage>{error}</ErrorMessage>}
            
            <FormGroup>
              <Label>Email Address</Label>
              <InputWrapper>
                <IconWrapper>
                  <Mail size={20} />
                </IconWrapper>
                <StyledInput
                  type="email"
                  name="email"
                  placeholder="developer@example.com"
                  value={formData.email}
                  onChange={handleChange}
                  required
                />
              </InputWrapper>
            </FormGroup>

            <FormGroup>
              <Label>Password</Label>
              <InputWrapper>
                <IconWrapper>
                  <Lock size={20} />
                </IconWrapper>
                <StyledInput
                  type={showPassword ? 'text' : 'password'}
                  name="password"
                  placeholder="Enter your password"
                  value={formData.password}
                  onChange={handleChange}
                  required
                />
                <PasswordToggle
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                >
                  {showPassword ? <EyeOff size={20} /> : <Eye size={20} />}
                </PasswordToggle>
              </InputWrapper>
            </FormGroup>

            <LoginButton type="submit" disabled={loading}>
              {loading ? 'Signing In...' : 'Sign In'}
            </LoginButton>

            <ForgotPassword to="/forgot-password">
              Forgot your password?
            </ForgotPassword>
          </Form>

          <Footer>
            <span>Don't have an account?</span>
            <SignUpLink to="/register">Sign up here</SignUpLink>
          </Footer>
        </LoginCard>
      </Container>
    </LoginContainer>
  )
}

const LoginContainer = styled.div`
  min-height: 100vh;
  display: flex;
  align-items: center;
  background: linear-gradient(135deg, rgba(107, 70, 193, 0.1), rgba(139, 92, 246, 0.1));
`

const LoginCard = styled(Card)`
  max-width: 400px;
  margin: 0 auto;
  background: rgba(26, 26, 26, 0.9);
  border: 1px solid rgba(107, 70, 193, 0.3);
  backdrop-filter: blur(20px);
`

const Header = styled.div`
  text-align: center;
  margin-bottom: 2rem;
`

const Logo = styled.div`
  font-size: 1.5rem;
  font-weight: 700;
  font-family: 'JetBrains Mono', monospace;
  margin-bottom: 1rem;
`

const Title = styled.h1`
  font-size: 1.875rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
`

const Subtitle = styled.p`
  color: #a1a1aa;
  font-size: 0.875rem;
`

const Form = styled.form`
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
`

const FormGroup = styled.div`
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
`

const Label = styled.label`
  font-size: 0.875rem;
  font-weight: 500;
  color: #e5e5e5;
`

const InputWrapper = styled.div`
  position: relative;
  display: flex;
  align-items: center;
`

const IconWrapper = styled.div`
  position: absolute;
  left: 0.75rem;
  color: #a1a1aa;
  z-index: 1;
`

const StyledInput = styled(Input)`
  padding-left: 2.75rem;
  padding-right: 2.75rem;
`

const PasswordToggle = styled.button`
  position: absolute;
  right: 0.75rem;
  background: none;
  border: none;
  color: #a1a1aa;
  cursor: pointer;
  padding: 0;
  
  &:hover {
    color: #e5e5e5;
  }
`

const LoginButton = styled(Button)`
  width: 100%;
  margin-top: 0.5rem;
`

const ErrorMessage = styled.div`
  background: rgba(239, 68, 68, 0.1);
  border: 1px solid rgba(239, 68, 68, 0.3);
  color: #fca5a5;
  padding: 0.75rem;
  border-radius: 6px;
  font-size: 0.875rem;
`

const ForgotPassword = styled(Link)`
  text-align: center;
  color: #6b46c1;
  text-decoration: none;
  font-size: 0.875rem;
  
  &:hover {
    text-decoration: underline;
  }
`

const Footer = styled.div`
  text-align: center;
  margin-top: 2rem;
  padding-top: 2rem;
  border-top: 1px solid rgba(107, 70, 193, 0.2);
  font-size: 0.875rem;
  color: #a1a1aa;
`

const SignUpLink = styled(Link)`
  color: #6b46c1;
  text-decoration: none;
  margin-left: 0.5rem;
  
  &:hover {
    text-decoration: underline;
  }
`

export default LoginPage
