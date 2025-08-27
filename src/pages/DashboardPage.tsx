
import { useState, useEffect } from 'react'
import styled from 'styled-components'
import { motion } from 'framer-motion'
import { Container, Card, Button } from '../styles/GlobalStyle'
import { Copy, Key, Activity, Database, TrendingUp } from 'lucide-react'

interface ApiKeyData {
  key: string
  plan: string
  usage_count: number
  monthly_limit: number
  usage_percentage: number
}

const DashboardPage = () => {
  const [apiKeyData, setApiKeyData] = useState<ApiKeyData | null>(null)
  const [loading, setLoading] = useState(true)
  const [copied, setCopied] = useState(false)

  useEffect(() => {
    fetchApiKeyData()
  }, [])

  const fetchApiKeyData = async () => {
    // Mock data for demo
    setTimeout(() => {
      setApiKeyData({
        key: 'mapi_dev_1234567890abcdef1234567890abcdef',
        plan: 'free',
        usage_count: 247,
        monthly_limit: 1000,
        usage_percentage: 24.7
      })
      setLoading(false)
    }, 1000)
  }

  const copyApiKey = () => {
    if (apiKeyData) {
      navigator.clipboard.writeText(apiKeyData.key)
      setCopied(true)
      setTimeout(() => setCopied(false), 2000)
    }
  }

  if (loading) {
    return (
      <DashboardContainer>
        <Container>
          <LoadingSpinner>Loading dashboard...</LoadingSpinner>
        </Container>
      </DashboardContainer>
    )
  }

  return (
    <DashboardContainer>
      <Container>
        <Header>
          <HeaderContent>
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6 }}
            >
              <Title>Developer Dashboard</Title>
              <Subtitle>Monitor your API usage and manage your integration</Subtitle>
            </motion.div>
          </HeaderContent>
        </Header>

        <StatsGrid>
          <StatCard
            as={motion.div}
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.5, delay: 0.1 }}
          >
            <StatIcon style={{ color: '#10b981' }}>
              <Key size={24} />
            </StatIcon>
            <StatTitle>API Key</StatTitle>
            <StatValue>{apiKeyData?.plan.toUpperCase()} PLAN</StatValue>
          </StatCard>

          <StatCard
            as={motion.div}
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.5, delay: 0.2 }}
          >
            <StatIcon style={{ color: '#10b981' }}>
              <Activity size={24} />
            </StatIcon>
            <StatTitle>Requests This Month</StatTitle>
            <StatValue>{apiKeyData?.usage_count.toLocaleString()}</StatValue>
          </StatCard>

          <StatCard
            as={motion.div}
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.5, delay: 0.3 }}
          >
            <StatIcon style={{ color: '#10b981' }}>
              <TrendingUp size={24} />
            </StatIcon>
            <StatTitle>Usage Percentage</StatTitle>
            <StatValue>{apiKeyData?.usage_percentage.toFixed(1)}%</StatValue>
          </StatCard>

          <StatCard
            as={motion.div}
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.5, delay: 0.4 }}
          >
            <StatIcon style={{ color: '#10b981' }}>
              <Database size={24} />
            </StatIcon>
            <StatTitle>Monthly Limit</StatTitle>
            <StatValue>{apiKeyData?.monthly_limit.toLocaleString()}</StatValue>
          </StatCard>
        </StatsGrid>

        <MainContent>
          <ApiKeySection
            as={motion.div}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.5 }}
          >
            <SectionTitle>Your API Key</SectionTitle>
            <ApiKeyCard>
              <ApiKeyDisplay>
                <KeyLabel>API Key</KeyLabel>
                <KeyValue>{apiKeyData?.key}</KeyValue>
              </ApiKeyDisplay>
              <CopyButton onClick={copyApiKey}>
                <Copy size={16} />
                {copied ? 'Copied!' : 'Copy'}
              </CopyButton>
            </ApiKeyCard>
            <UsageBar>
              <UsageProgress 
                progress={apiKeyData?.usage_percentage || 0}
                style={{ width: `${apiKeyData?.usage_percentage}%` }}
              />
            </UsageBar>
            <UsageText>
              {apiKeyData?.usage_count} / {apiKeyData?.monthly_limit} requests used this month
            </UsageText>
          </ApiKeySection>

          <QuickStartSection
            as={motion.div}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.6 }}
          >
            <SectionTitle>Quick Start</SectionTitle>
            <CodeBlock>
              <CodeTitle>Example API Request</CodeTitle>
              <CodeContent>
                {`curl -X GET "https://your-app.repl.co/movies" \\
  -H "X-API-KEY: ${apiKeyData?.key}"`}
              </CodeContent>
            </CodeBlock>
            <ActionButtons>
              <Button>View Documentation</Button>
              <Button variant="secondary">Download SDK</Button>
            </ActionButtons>
          </QuickStartSection>
        </MainContent>
      </Container>
    </DashboardContainer>
  )
}

const DashboardContainer = styled.div`
  min-height: 100vh;
  background: linear-gradient(135deg, rgba(16, 185, 129, 0.05), rgba(34, 197, 94, 0.05));
  padding-top: 2rem;
`

const Header = styled.header`
  margin-bottom: 3rem;
`

const HeaderContent = styled.div`
  text-align: center;
`

const Title = styled.h1`
  font-size: 2.5rem;
  font-weight: 700;
  margin-bottom: 0.5rem;
  color: #10b981;
`

const Subtitle = styled.p`
  color: #a1a1aa;
  font-size: 1.125rem;
`

const StatsGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin-bottom: 3rem;
`

const StatCard = styled(Card)`
  background: rgba(16, 185, 129, 0.1);
  border: 1px solid rgba(16, 185, 129, 0.2);
  text-align: center;
  padding: 2rem;
`

const StatIcon = styled.div`
  margin-bottom: 1rem;
  display: flex;
  justify-content: center;
`

const StatTitle = styled.h3`
  font-size: 0.875rem;
  color: #a1a1aa;
  margin-bottom: 0.5rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
`

const StatValue = styled.div`
  font-size: 1.5rem;
  font-weight: 700;
  color: #10b981;
`

const MainContent = styled.div`
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
  
  @media (max-width: 768px) {
    grid-template-columns: 1fr;
  }
`

const ApiKeySection = styled(Card)`
  background: rgba(16, 185, 129, 0.05);
  border: 1px solid rgba(16, 185, 129, 0.2);
`

const SectionTitle = styled.h2`
  font-size: 1.25rem;
  font-weight: 600;
  margin-bottom: 1.5rem;
  color: #10b981;
`

const ApiKeyCard = styled.div`
  background: rgba(26, 26, 26, 0.8);
  border: 1px solid rgba(16, 185, 129, 0.3);
  border-radius: 8px;
  padding: 1rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
`

const ApiKeyDisplay = styled.div`
  flex: 1;
  margin-right: 1rem;
`

const KeyLabel = styled.div`
  font-size: 0.75rem;
  color: #a1a1aa;
  margin-bottom: 0.25rem;
`

const KeyValue = styled.div`
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.875rem;
  color: #10b981;
  word-break: break-all;
`

const CopyButton = styled(Button)`
  background: rgba(16, 185, 129, 0.2);
  border: 1px solid rgba(16, 185, 129, 0.3);
  color: #10b981;
  padding: 0.5rem 1rem;
  font-size: 0.875rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  
  &:hover {
    background: rgba(16, 185, 129, 0.3);
  }
`

const UsageBar = styled.div`
  background: rgba(26, 26, 26, 0.8);
  border-radius: 4px;
  height: 8px;
  margin-bottom: 0.5rem;
  overflow: hidden;
`

const UsageProgress = styled.div<{ progress: number }>`
  background: linear-gradient(90deg, #10b981, #34d399);
  height: 100%;
  transition: width 0.3s ease;
  border-radius: 4px;
`

const UsageText = styled.div`
  font-size: 0.875rem;
  color: #a1a1aa;
  text-align: center;
`

const QuickStartSection = styled(Card)`
  background: rgba(16, 185, 129, 0.05);
  border: 1px solid rgba(16, 185, 129, 0.2);
`

const CodeBlock = styled.div`
  background: rgba(0, 0, 0, 0.8);
  border: 1px solid rgba(16, 185, 129, 0.3);
  border-radius: 8px;
  margin-bottom: 1.5rem;
`

const CodeTitle = styled.div`
  background: rgba(16, 185, 129, 0.1);
  border-bottom: 1px solid rgba(16, 185, 129, 0.3);
  padding: 0.75rem 1rem;
  font-size: 0.875rem;
  color: #10b981;
  font-weight: 500;
`

const CodeContent = styled.pre`
  padding: 1rem;
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.875rem;
  color: #e5e5e5;
  overflow-x: auto;
  white-space: pre-wrap;
`

const ActionButtons = styled.div`
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
`

const LoadingSpinner = styled.div`
  text-align: center;
  padding: 4rem;
  font-size: 1.125rem;
  color: #a1a1aa;
`

export default DashboardPage
