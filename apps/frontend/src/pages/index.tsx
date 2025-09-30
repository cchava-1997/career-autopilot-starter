import { useState, useEffect } from 'react';
import Layout from '../components/Layout';
import { api } from '../services/api';
import toast from 'react-hot-toast';
import {
  ClipboardDocumentListIcon,
  CheckCircleIcon,
  ClockIcon,
  ChatBubbleLeftRightIcon,
  CalendarDaysIcon,
  PencilSquareIcon,
  ChartBarIcon,
} from '@heroicons/react/24/outline';

interface DashboardStats {
  total_jobs: number;
  jobs_applied: number;
  jobs_pending: number;
  outreach_sent: number;
  interviews_scheduled: number;
  recent_activity: Array<{
    type: string;
    description: string;
    timestamp: string;
  }>;
}

export default function DashboardPage() {
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Test API connection first
    console.log('API Base URL:', process.env.NEXT_PUBLIC_BACKEND_URL);
    fetchDashboardStats();
  }, []);

  const fetchDashboardStats = async () => {
    try {
      console.log('Fetching dashboard stats...');
      // Test direct fetch first
      const directResponse = await fetch('http://localhost:8000/dashboard/stats');
      console.log('Direct fetch response:', directResponse);
      const directData = await directResponse.json();
      console.log('Direct fetch data:', directData);
      
      const response = await api.dashboard.stats();
      console.log('Dashboard stats response:', response.data);
      setStats(response.data);
    } catch (error) {
      console.error('Error fetching dashboard stats:', error);
      // Show error toast for debugging
      toast.error('Failed to fetch dashboard stats: ' + error.message);
      // Don't show error toast for dashboard stats, just use default values
      setStats({
        total_jobs: 0,
        jobs_applied: 0,
        jobs_pending: 0,
        outreach_sent: 0,
        interviews_scheduled: 0,
        recent_activity: []
      });
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <Layout>
        <div className="animate-pulse">
          <div className="h-8 bg-gray-200 rounded w-1/4 mb-6"></div>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
            {[...Array(4)].map((_, i) => (
              <div key={i} className="card">
                <div className="h-4 bg-gray-200 rounded w-3/4 mb-2"></div>
                <div className="h-8 bg-gray-200 rounded w-1/2"></div>
              </div>
            ))}
          </div>
        </div>
      </Layout>
    );
  }

  return (
    <Layout>
      <div>
        <h1 className="text-2xl font-bold text-gray-900 mb-6">Dashboard</h1>
        {process.env.NODE_ENV === 'development' && (
          <div className="mb-4 p-4 bg-gray-100 rounded-lg text-sm">
            <strong>Debug Info:</strong> Stats: {JSON.stringify(stats)}
          </div>
        )}

        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow duration-200">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <div className="w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center">
                  <ClipboardDocumentListIcon className="h-5 w-5 text-blue-600" />
                </div>
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Total Jobs</p>
                <p className="text-2xl font-bold text-gray-900">{stats?.total_jobs || 0}</p>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow duration-200">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <div className="w-10 h-10 bg-green-100 rounded-lg flex items-center justify-center">
                  <CheckCircleIcon className="h-5 w-5 text-green-600" />
                </div>
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Applied</p>
                <p className="text-2xl font-bold text-gray-900">{stats?.jobs_applied || 0}</p>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow duration-200">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <div className="w-10 h-10 bg-yellow-100 rounded-lg flex items-center justify-center">
                  <ClockIcon className="h-5 w-5 text-yellow-600" />
                </div>
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Pending</p>
                <p className="text-2xl font-bold text-gray-900">{stats?.jobs_pending || 0}</p>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow duration-200">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <div className="w-10 h-10 bg-purple-100 rounded-lg flex items-center justify-center">
                  <ChatBubbleLeftRightIcon className="h-5 w-5 text-purple-600" />
                </div>
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Outreach</p>
                <p className="text-2xl font-bold text-gray-900">{stats?.outreach_sent || 0}</p>
              </div>
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Quick Actions */}
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow duration-200">
            <h2 className="text-lg font-semibold mb-4 text-gray-900">Quick Actions</h2>
            <div className="space-y-3">
              <a
                href="/jobs"
                className="flex items-center p-4 bg-gradient-to-r from-blue-50 to-blue-100 rounded-xl hover:from-blue-100 hover:to-blue-200 transition-all duration-200 border border-blue-200"
              >
                <div className="w-10 h-10 bg-blue-500 rounded-lg flex items-center justify-center mr-4">
                  <ClipboardDocumentListIcon className="h-5 w-5 text-white" />
                </div>
                <div>
                  <p className="font-semibold text-gray-900">Add New Job</p>
                  <p className="text-sm text-gray-600">Track a new job opportunity</p>
                </div>
              </a>
              
              <a
                href="/apply"
                className="flex items-center p-4 bg-gradient-to-r from-green-50 to-green-100 rounded-xl hover:from-green-100 hover:to-green-200 transition-all duration-200 border border-green-200"
              >
                <div className="w-10 h-10 bg-green-500 rounded-lg flex items-center justify-center mr-4">
                  <PencilSquareIcon className="h-5 w-5 text-white" />
                </div>
                <div>
                  <p className="font-semibold text-gray-900">Generate Apply Pack</p>
                  <p className="text-sm text-gray-600">Create bullets and cover letter</p>
                </div>
              </a>
              
              <a
                href="/outreach"
                className="flex items-center p-4 bg-gradient-to-r from-purple-50 to-purple-100 rounded-xl hover:from-purple-100 hover:to-purple-200 transition-all duration-200 border border-purple-200"
              >
                <div className="w-10 h-10 bg-purple-500 rounded-lg flex items-center justify-center mr-4">
                  <ChatBubbleLeftRightIcon className="h-5 w-5 text-white" />
                </div>
                <div>
                  <p className="font-semibold text-gray-900">Plan Outreach</p>
                  <p className="text-sm text-gray-600">Generate contact strategy</p>
                </div>
              </a>
              
              <a
                href="/summary"
                className="flex items-center p-4 bg-gradient-to-r from-orange-50 to-orange-100 rounded-xl hover:from-orange-100 hover:to-orange-200 transition-all duration-200 border border-orange-200"
              >
                <div className="w-10 h-10 bg-orange-500 rounded-lg flex items-center justify-center mr-4">
                  <ChartBarIcon className="h-5 w-5 text-white" />
                </div>
                <div>
                  <p className="font-semibold text-gray-900">Daily Summary</p>
                  <p className="text-sm text-gray-600">Generate progress report</p>
                </div>
              </a>
            </div>
          </div>

          {/* Recent Activity */}
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow duration-200">
            <h2 className="text-lg font-semibold mb-4 text-gray-900">Recent Activity</h2>
            {stats?.recent_activity && stats.recent_activity.length > 0 ? (
              <div className="space-y-3">
                {stats.recent_activity.map((activity, index) => (
                  <div key={index} className="flex items-start space-x-3 p-3 bg-gray-50 rounded-lg">
                    <div className="flex-shrink-0">
                      <div className="w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center">
                        <ClipboardDocumentListIcon className="h-4 w-4 text-blue-600" />
                      </div>
                    </div>
                    <div className="flex-1 min-w-0">
                      <p className="text-sm text-gray-900">{activity.description}</p>
                      <p className="text-xs text-gray-500 mt-1">
                        {new Date(activity.timestamp).toLocaleString()}
                      </p>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="text-center py-8 text-gray-500">
                <ClipboardDocumentListIcon className="h-12 w-12 mx-auto mb-4 text-gray-400" />
                <p>No recent activity. Start by adding a job!</p>
              </div>
            )}
          </div>
        </div>

        {/* Getting Started */}
        {(!stats || stats.total_jobs === 0) && (
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow duration-200 mt-8">
            <h2 className="text-lg font-semibold mb-4">Getting Started</h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="text-center p-4">
                <div className="w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center mx-auto mb-3">
                  <span className="text-blue-600 text-lg">1</span>
                </div>
                <h3 className="font-medium text-gray-900 mb-2">Add Job Sources</h3>
                <p className="text-sm text-gray-600 mb-3">Configure your job boards and company sites</p>
                <a href="/sources" className="bg-blue-600 text-white px-3 py-1 rounded-lg text-sm font-medium hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition-all duration-200 shadow-sm hover:shadow-md">
                  Get Started
                </a>
              </div>
              
              <div className="text-center p-4">
                <div className="w-10 h-10 bg-green-100 rounded-lg flex items-center justify-center mx-auto mb-3">
                  <span className="text-green-600 text-lg">2</span>
                </div>
                <h3 className="font-medium text-gray-900 mb-2">Set Up Resumes</h3>
                <p className="text-sm text-gray-600 mb-3">Configure your resume tracks in Overleaf</p>
                <a href="/resumes" className="bg-blue-600 text-white px-3 py-1 rounded-lg text-sm font-medium hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition-all duration-200 shadow-sm hover:shadow-md">
                  Get Started
                </a>
              </div>
              
              <div className="text-center p-4">
                <div className="w-10 h-10 bg-purple-100 rounded-lg flex items-center justify-center mx-auto mb-3">
                  <span className="text-purple-600 text-lg">3</span>
                </div>
                <h3 className="font-medium text-gray-900 mb-2">Add Your First Job</h3>
                <p className="text-sm text-gray-600 mb-3">Start tracking job opportunities</p>
                <a href="/jobs" className="bg-blue-600 text-white px-3 py-1 rounded-lg text-sm font-medium hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition-all duration-200 shadow-sm hover:shadow-md">
                  Get Started
                </a>
              </div>
            </div>
          </div>
        )}
      </div>
    </Layout>
  );
}