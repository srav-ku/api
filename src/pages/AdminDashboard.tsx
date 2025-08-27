
import { useState, useEffect } from 'react'
import styled from 'styled-components'
import { Container, Card, Button } from '../styles/GlobalStyle'
import { Users, Key, Activity, Database, Settings } from 'lucide-react'

const AdminDashboard = () => {
  const [stats, setStats] = useState({
    totalUsers: 0,
    totalApiKeys: 0,
    totalRequests: 0,
    totalMovies: 0
  })

  useEffect(() => {
    fetchStats()
  }, [])

  const fetchStats = async () => {
    // Mock data for demo
    setTimeout(() => {
      setStats({
        totalUsers: 156,
        totalApiKeys: 134,
        totalRequests: 45678,
        totalMovies: 10547
      })
      
    }, 1000)
  }

  return (
    <AdminContainer>
      <Container>
        <Header>
          <Title>Admin Dashboard</Title>
          <Subtitle>System overview and management</Subtitle>
        </Header>

        <StatsGrid>
          <StatCard>
            <StatIcon style={{ color: '#6b46c1' }}>
              <Users size={24} />
            </StatIcon>
            <StatTitle>Total Users</StatTitle>
            <StatValue>{stats.totalUsers.toLocaleString()}</StatValue>
          </StatCard>

          <StatCard>
            <StatIcon style={{ color: '#6b46c1' }}>
              <Key size={24} />
            </StatIcon>
            <StatTitle>API Keys</StatTitle>
            <StatValue>{stats.totalApiKeys.toLocaleString()}</StatValue>
          </StatCard>

          <StatCard>
            <StatIcon style={{ color: '#6b46c1' }}>
              <Activity size={24} />
            </StatIcon>
            <StatTitle>Total Requests</StatTitle>
            <StatValue>{stats.totalRequests.toLocaleString()}</StatValue>
          </StatCard>

          <StatCard>
            <StatIcon style={{ color: '#6b46c1' }}>
              <Database size={24} />
            </StatIcon>
            <StatTitle>Movies</StatTitle>
            <StatValue>{stats.totalMovies.toLocaleString()}</StatValue>
          </StatCard>
        </StatsGrid>

        <ActionsSection>
          <ActionCard>
            <ActionTitle>User Management</ActionTitle>
            <ActionDescription>Manage user accounts and permissions</ActionDescription>
            <Button>
              <Users size={16} />
              Manage Users
            </Button>
          </ActionCard>

          <ActionCard>
            <ActionTitle>API Keys</ActionTitle>
            <ActionDescription>View and manage all API keys</ActionDescription>
            <Button>
              <Key size={16} />
              Manage Keys
            </Button>
          </ActionCard>

          <ActionCard>
            <ActionTitle>System Settings</ActionTitle>
            <ActionDescription>Configure system parameters</ActionDescription>
            <Button>
              <Settings size={16} />
              Settings
            </Button>
          </ActionCard>
        </ActionsSection>
      </Container>
    </AdminContainer>
  )
}

const AdminContainer = styled.div`
  min-height: 100vh;
  background: linear-gradient(135deg, rgba(107, 70, 193, 0.1), rgba(139, 92, 246, 0.1));
  padding-top: 2rem;
`

const Header = styled.header`
  text-align: center;
  margin-bottom: 3rem;
`

const Title = styled.h1`
  font-size: 2.5rem;
  font-weight: 700;
  margin-bottom: 0.5rem;
  color: #6b46c1;
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
  background: rgba(107, 70, 193, 0.1);
  border: 1px solid rgba(107, 70, 193, 0.2);
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
  color: #6b46c1;
`

const ActionsSection = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1.5rem;
`

const ActionCard = styled(Card)`
  background: rgba(107, 70, 193, 0.05);
  border: 1px solid rgba(107, 70, 193, 0.2);
  text-align: center;
  padding: 2rem;
`

const ActionTitle = styled.h3`
  font-size: 1.25rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
  color: #6b46c1;
`

const ActionDescription = styled.p`
  color: #a1a1aa;
  margin-bottom: 1.5rem;
`

export default AdminDashboard
