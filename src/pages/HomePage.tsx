
import { useEffect, useRef } from 'react'
import styled from 'styled-components'
import { motion } from 'framer-motion'
import { useNavigate } from 'react-router-dom'
import { Container, Button } from '../styles/GlobalStyle'
import { Code, Database, Shield, Zap, Users, TrendingUp } from 'lucide-react'

const HomePage = () => {
  const navigate = useNavigate()
  const canvasRef = useRef<HTMLCanvasElement>(null)

  useEffect(() => {
    // Matrix rain effect
    const canvas = canvasRef.current
    if (!canvas) return

    const ctx = canvas.getContext('2d')
    if (!ctx) return

    canvas.width = window.innerWidth
    canvas.height = window.innerHeight

    const matrix = "ABCDEFGHIJKLMNOPQRSTUVWXYZ123456789@#$%^&*()*&^%+-/~{[|`]}0123456789"
    const matrixArray = matrix.split("")

    const fontSize = 10
    const columns = canvas.width / fontSize

    const drops: number[] = []
    for (let x = 0; x < columns; x++) {
      drops[x] = 1
    }

    function draw() {
      if (!ctx || !canvas) return
      
      ctx.fillStyle = 'rgba(0, 0, 0, 0.04)'
      ctx.fillRect(0, 0, canvas.width, canvas.height)

      ctx.fillStyle = '#00ff41'
      ctx.font = fontSize + 'px monospace'

      for (let i = 0; i < drops.length; i++) {
        const text = matrixArray[Math.floor(Math.random() * matrixArray.length)]
        ctx.fillText(text, i * fontSize, drops[i] * fontSize)

        if (drops[i] * fontSize > canvas.height && Math.random() > 0.975) {
          drops[i] = 0
        }
        drops[i]++
      }
    }

    const interval = setInterval(draw, 35)

    return () => clearInterval(interval)
  }, [])

  return (
    <HomeContainer>
      <MatrixCanvas ref={canvasRef} />
      
      <Header>
        <Container>
          <Nav>
            <Logo>
              <span className="matrix-text">THE MATRIX</span>
            </Logo>
            <NavButtons>
              <Button variant="ghost" onClick={() => navigate('/login')}>
                Login
              </Button>
              <Button onClick={() => navigate('/register')}>
                Get Started
              </Button>
            </NavButtons>
          </Nav>
        </Container>
      </Header>

      <HeroSection>
        <Container>
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
          >
            <HeroContent>
              <HeroTitle>
                Enter <span className="matrix-text">THE MATRIX</span>
                <br />
                Ultimate Movie API Platform
              </HeroTitle>
              <HeroSubtitle>
                Access 10,000+ movies with enterprise-grade security and lightning-fast performance. 
                Built for developers who demand excellence.
              </HeroSubtitle>
              <HeroButtons>
                <Button onClick={() => navigate('/register')}>
                  Start Building
                </Button>
                <Button variant="secondary" onClick={() => navigate('/docs')}>
                  View Documentation
                </Button>
              </HeroButtons>
            </HeroContent>
          </motion.div>
        </Container>
      </HeroSection>

      <FeaturesSection>
        <Container>
          <SectionTitle>Why Choose The Matrix?</SectionTitle>
          <FeaturesGrid>
            <FeatureCard>
              <FeatureIcon>
                <Database size={32} />
              </FeatureIcon>
              <FeatureTitle>Massive Database</FeatureTitle>
              <FeatureDescription>
                Access over 10,000 movies with detailed metadata, ratings, and poster images.
              </FeatureDescription>
            </FeatureCard>

            <FeatureCard>
              <FeatureIcon>
                <Shield size={32} />
              </FeatureIcon>
              <FeatureTitle>Enterprise Security</FeatureTitle>
              <FeatureDescription>
                Advanced API key management with rate limiting and usage analytics.
              </FeatureDescription>
            </FeatureCard>

            <FeatureCard>
              <FeatureIcon>
                <Zap size={32} />
              </FeatureIcon>
              <FeatureTitle>Lightning Fast</FeatureTitle>
              <FeatureDescription>
                Optimized PostgreSQL queries with sub-100ms response times.
              </FeatureDescription>
            </FeatureCard>

            <FeatureCard>
              <FeatureIcon>
                <Code size={32} />
              </FeatureIcon>
              <FeatureTitle>Developer Friendly</FeatureTitle>
              <FeatureDescription>
                RESTful API with comprehensive documentation and code examples.
              </FeatureDescription>
            </FeatureCard>

            <FeatureCard>
              <FeatureIcon>
                <Users size={32} />
              </FeatureIcon>
              <FeatureTitle>Multi-tenant</FeatureTitle>
              <FeatureDescription>
                Separate developer accounts with individual API keys and usage tracking.
              </FeatureDescription>
            </FeatureCard>

            <FeatureCard>
              <FeatureIcon>
                <TrendingUp size={32} />
              </FeatureIcon>
              <FeatureTitle>Analytics</FeatureTitle>
              <FeatureDescription>
                Real-time usage statistics and performance monitoring dashboard.
              </FeatureDescription>
            </FeatureCard>
          </FeaturesGrid>
        </Container>
      </FeaturesSection>

      <CTASection>
        <Container>
          <CTAContent>
            <CTATitle>Ready to Enter The Matrix?</CTATitle>
            <CTASubtitle>
              Join thousands of developers building amazing applications with our Movie API
            </CTASubtitle>
            <Button onClick={() => navigate('/register')}>
              Get Your API Key
            </Button>
          </CTAContent>
        </Container>
      </CTASection>
    </HomeContainer>
  )
}

const HomeContainer = styled.div`
  min-height: 100vh;
  position: relative;
`

const MatrixCanvas = styled.canvas`
  position: fixed;
  top: 0;
  left: 0;
  z-index: -1;
  opacity: 0.1;
`

const Header = styled.header`
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 100;
  background: rgba(10, 10, 10, 0.8);
  backdrop-filter: blur(10px);
  border-bottom: 1px solid rgba(107, 70, 193, 0.2);
`

const Nav = styled.nav`
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 0;
`

const Logo = styled.div`
  font-size: 1.5rem;
  font-weight: 700;
  font-family: 'JetBrains Mono', monospace;
`

const NavButtons = styled.div`
  display: flex;
  gap: 1rem;
`

const HeroSection = styled.section`
  min-height: 100vh;
  display: flex;
  align-items: center;
  background: linear-gradient(135deg, rgba(107, 70, 193, 0.1), rgba(139, 92, 246, 0.1));
`

const HeroContent = styled.div`
  text-align: center;
  max-width: 800px;
  margin: 0 auto;
`

const HeroTitle = styled.h1`
  font-size: 3.5rem;
  font-weight: 700;
  margin-bottom: 1.5rem;
  line-height: 1.2;
  
  @media (max-width: 768px) {
    font-size: 2.5rem;
  }
`

const HeroSubtitle = styled.p`
  font-size: 1.25rem;
  color: #a1a1aa;
  margin-bottom: 2rem;
  max-width: 600px;
  margin-left: auto;
  margin-right: auto;
`

const HeroButtons = styled.div`
  display: flex;
  gap: 1rem;
  justify-content: center;
  flex-wrap: wrap;
`

const FeaturesSection = styled.section`
  padding: 5rem 0;
  background: rgba(26, 26, 26, 0.5);
`

const SectionTitle = styled.h2`
  font-size: 2.5rem;
  text-align: center;
  margin-bottom: 3rem;
  font-weight: 600;
`

const FeaturesGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
`

const FeatureCard = styled.div`
  background: rgba(26, 26, 26, 0.8);
  border: 1px solid rgba(107, 70, 193, 0.2);
  border-radius: 12px;
  padding: 2rem;
  text-align: center;
  transition: all 0.3s ease;
  
  &:hover {
    border-color: rgba(107, 70, 193, 0.5);
    transform: translateY(-4px);
    box-shadow: 0 8px 25px rgba(107, 70, 193, 0.2);
  }
`

const FeatureIcon = styled.div`
  color: #6b46c1;
  margin-bottom: 1rem;
  display: flex;
  justify-content: center;
`

const FeatureTitle = styled.h3`
  font-size: 1.25rem;
  font-weight: 600;
  margin-bottom: 1rem;
`

const FeatureDescription = styled.p`
  color: #a1a1aa;
  line-height: 1.6;
`

const CTASection = styled.section`
  padding: 5rem 0;
  background: linear-gradient(135deg, rgba(107, 70, 193, 0.1), rgba(139, 92, 246, 0.1));
`

const CTAContent = styled.div`
  text-align: center;
  max-width: 600px;
  margin: 0 auto;
`

const CTATitle = styled.h2`
  font-size: 2.5rem;
  font-weight: 600;
  margin-bottom: 1rem;
`

const CTASubtitle = styled.p`
  font-size: 1.125rem;
  color: #a1a1aa;
  margin-bottom: 2rem;
`

export default HomePage
