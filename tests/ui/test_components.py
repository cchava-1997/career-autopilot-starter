import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import Layout from '../../apps/frontend/src/components/Layout';

// Mock Next.js router
jest.mock('next/router', () => ({
  useRouter: () => ({
    pathname: '/',
  }),
}));

describe('Layout Component', () => {
  it('renders navigation items', () => {
    render(
      <Layout>
        <div>Test content</div>
      </Layout>
    );
    
    expect(screen.getByText('Career Autopilot')).toBeInTheDocument();
    expect(screen.getByText('Dashboard')).toBeInTheDocument();
    expect(screen.getByText('Resumes')).toBeInTheDocument();
    expect(screen.getByText('Jobs')).toBeInTheDocument();
  });
  
  it('renders children content', () => {
    render(
      <Layout>
        <div data-testid="test-content">Test content</div>
      </Layout>
    );
    
    expect(screen.getByTestId('test-content')).toBeInTheDocument();
  });
});
