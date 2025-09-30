import { useState, useEffect } from 'react';
import Layout from '../components/Layout';
import { api } from '../services/api';
import toast from 'react-hot-toast';
import { LinkIcon, CheckCircleIcon, XCircleIcon } from '@heroicons/react/24/outline';

interface Site {
  id: string;
  name: string;
  type: string;
  url: string;
  notes?: string;
  enabled: boolean;
  created_at: string;
  updated_at: string;
}

export default function SourcesPage() {
  const [sites, setSites] = useState<Site[]>([]);
  const [loading, setLoading] = useState(true);
  const [showAddForm, setShowAddForm] = useState(false);
  const [linkedinAuth, setLinkedinAuth] = useState<any>(null);
  const [linkedinJobs, setLinkedinJobs] = useState<any[]>([]);
  const [jobSearchLoading, setJobSearchLoading] = useState(false);
  const [newSite, setNewSite] = useState({
    name: '',
    type: 'board',
    url: '',
    notes: '',
    enabled: true
  });

  useEffect(() => {
    fetchSites();
    checkLinkedInAuth();
  }, []);

  const checkLinkedInAuth = async () => {
    try {
      const urlParams = new URLSearchParams(window.location.search);
      const sessionId = urlParams.get('session_id');
      
      if (sessionId) {
        const response = await fetch(`http://localhost:8000/auth/linkedin/status?session_id=${sessionId}`);
        const data = await response.json();
        
        if (data.authenticated) {
          setLinkedinAuth(data);
          // Store session ID in localStorage for future use
          localStorage.setItem('linkedin_session_id', sessionId);
        }
      } else {
        // Check for existing session
        const storedSessionId = localStorage.getItem('linkedin_session_id');
        if (storedSessionId) {
          const response = await fetch(`http://localhost:8000/auth/linkedin/status?session_id=${storedSessionId}`);
          const data = await response.json();
          
          if (data.authenticated) {
            setLinkedinAuth(data);
          } else {
            localStorage.removeItem('linkedin_session_id');
          }
        }
      }
    } catch (error) {
      console.error('Error checking LinkedIn auth:', error);
    }
  };

  const fetchSites = async () => {
    try {
      const response = await api.sources.list();
      setSites(response.data);
    } catch (error) {
      toast.error('Failed to fetch job sources');
      console.error('Error fetching sites:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleAddSite = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await api.sources.add(newSite);
      toast.success('Job source added successfully');
      setNewSite({
        name: '',
        type: 'board',
        url: '',
        notes: '',
        enabled: true
      });
      setShowAddForm(false);
      fetchSites();
    } catch (error) {
      toast.error('Failed to add job source');
      console.error('Error adding site:', error);
    }
  };

  const handleTestSite = async (siteId: string) => {
    try {
      const response = await api.sources.test(siteId);
      if (response.data.ok) {
        toast.success('Site is accessible');
      } else {
        toast.error('Site is not accessible');
      }
    } catch (error) {
      toast.error('Failed to test site');
      console.error('Error testing site:', error);
    }
  };

  const getTypeColor = (type: string) => {
    switch (type) {
      case 'board': return 'bg-blue-100 text-blue-800';
      case 'company': return 'bg-green-100 text-green-800';
      case 'ats': return 'bg-purple-100 text-purple-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const handleLinkedInLogin = async () => {
    try {
      const response = await fetch('http://localhost:8000/auth/linkedin/login');
      const data = await response.json();
      window.location.href = data.auth_url;
    } catch (error) {
      toast.error('Failed to initiate LinkedIn login');
      console.error('Error:', error);
    }
  };

  const handleLinkedInPlaywrightLogin = async () => {
    try {
      const response = await fetch('http://localhost:8000/auth/linkedin-playwright/status');
      const data = await response.json();
      
      if (data.authenticated) {
        setLinkedinAuth(data);
        toast.success('LinkedIn credentials configured');
      } else {
        toast.error('LinkedIn credentials not configured. Please update your .env file.');
      }
    } catch (error) {
      toast.error('Failed to check LinkedIn status');
      console.error('Error:', error);
    }
  };

  const handleLinkedInLogout = async () => {
    try {
      const sessionId = localStorage.getItem('linkedin_session_id');
      if (sessionId) {
        await fetch(`http://localhost:8000/auth/linkedin/logout?session_id=${sessionId}`);
        localStorage.removeItem('linkedin_session_id');
        setLinkedinAuth(null);
        setLinkedinJobs([]);
        toast.success('Logged out from LinkedIn');
      }
    } catch (error) {
      toast.error('Failed to logout from LinkedIn');
      console.error('Error:', error);
    }
  };

  const handleJobSearch = async (keywords: string, location: string = '') => {
    try {
      setJobSearchLoading(true);
      
      // Try Playwright method first (no OAuth required)
      const response = await fetch('http://localhost:8000/auth/linkedin-playwright/search-jobs', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          keywords,
          location,
          limit: 25
        })
      });

      const data = await response.json();
      
      if (data.success) {
        setLinkedinJobs(data.jobs);
        toast.success(`Found ${data.jobs.length} jobs using Playwright`);
      } else {
        toast.error(data.detail || 'Failed to search jobs');
      }
    } catch (error) {
      toast.error('Failed to search jobs');
      console.error('Error:', error);
    } finally {
      setJobSearchLoading(false);
    }
  };

  if (loading) {
    return (
      <Layout>
        <div className="animate-pulse">
          <div className="h-8 bg-gray-200 rounded w-1/4 mb-6"></div>
          <div className="space-y-4">
            {[...Array(5)].map((_, i) => (
              <div key={i} className="card">
                <div className="h-4 bg-gray-200 rounded w-3/4 mb-2"></div>
                <div className="h-4 bg-gray-200 rounded w-1/2"></div>
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
        <div className="flex justify-between items-center mb-6">
          <h1 className="text-2xl font-bold text-gray-900">Job Sources</h1>
          <div className="flex gap-3">
            {linkedinAuth ? (
              <button
                onClick={handleLinkedInLogout}
                className="btn-secondary"
              >
                Logout LinkedIn
              </button>
            ) : (
              <div className="flex gap-2">
                <button
                  onClick={handleLinkedInPlaywrightLogin}
                  className="btn-primary flex items-center gap-2"
                >
                  <LinkIcon className="h-4 w-4" />
                  LinkedIn (Playwright)
                </button>
                <button
                  onClick={handleLinkedInLogin}
                  className="btn-secondary flex items-center gap-2"
                >
                  <LinkIcon className="h-4 w-4" />
                  LinkedIn (OAuth)
                </button>
              </div>
            )}
            <button
              onClick={() => setShowAddForm(true)}
              className="btn-primary"
            >
              Add Source
            </button>
          </div>
        </div>

        {/* LinkedIn Authentication Status */}
        {linkedinAuth && (
          <div className="card mb-6">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-3">
                <CheckCircleIcon className="h-6 w-6 text-green-500" />
                <div>
                  <h3 className="font-semibold text-gray-900">
                    Connected to LinkedIn
                  </h3>
                  <p className="text-sm text-gray-600">
                    {linkedinAuth.profile?.firstName} {linkedinAuth.profile?.lastName}
                    {linkedinAuth.profile?.email && ` (${linkedinAuth.profile.email})`}
                  </p>
                </div>
              </div>
              <div className="flex gap-2">
                <button
                  onClick={() => {
                    const keywords = prompt('Enter job keywords:');
                    const location = prompt('Enter location (optional):');
                    if (keywords) {
                      handleJobSearch(keywords, location || '');
                    }
                  }}
                  disabled={jobSearchLoading}
                  className="btn-secondary"
                >
                  {jobSearchLoading ? 'Searching...' : 'Search Jobs'}
                </button>
              </div>
            </div>
          </div>
        )}

        {/* LinkedIn Job Results */}
        {linkedinJobs.length > 0 && (
          <div className="card mb-6">
            <h3 className="text-lg font-semibold mb-4">LinkedIn Job Results</h3>
            <div className="space-y-3">
              {linkedinJobs.map((job, index) => (
                <div key={index} className="border rounded-lg p-4 hover:bg-gray-50">
                  <div className="flex justify-between items-start">
                    <div className="flex-1">
                      <h4 className="font-semibold text-gray-900">{job.title}</h4>
                      <p className="text-sm text-gray-600">{job.company}</p>
                      <p className="text-sm text-gray-500">{job.location}</p>
                      {job.description && (
                        <p className="text-sm text-gray-700 mt-2 line-clamp-2">
                          {job.description.substring(0, 200)}...
                        </p>
                      )}
                    </div>
                    <div className="flex gap-2 ml-4">
                      <a
                        href={job.url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="btn-secondary text-sm"
                      >
                        View Job
                      </a>
                      <button
                        onClick={() => {
                          // TODO: Implement job application
                          toast.info('Job application feature coming soon!');
                        }}
                        className="btn-primary text-sm"
                      >
                        Apply
                      </button>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Add Source Form */}
        {showAddForm && (
          <div className="card mb-6">
            <h2 className="text-lg font-semibold mb-4">Add New Job Source</h2>
            <form onSubmit={handleAddSite} className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Name
                  </label>
                  <input
                    type="text"
                    value={newSite.name}
                    onChange={(e) => setNewSite({...newSite, name: e.target.value})}
                    className="input-field"
                    placeholder="e.g., LinkedIn Jobs"
                    required
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Type
                  </label>
                  <select
                    value={newSite.type}
                    onChange={(e) => setNewSite({...newSite, type: e.target.value})}
                    className="input-field"
                  >
                    <option value="board">Job Board</option>
                    <option value="company">Company Site</option>
                    <option value="ats">ATS Portal</option>
                  </select>
                </div>
                <div className="md:col-span-2">
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    URL
                  </label>
                  <input
                    type="url"
                    value={newSite.url}
                    onChange={(e) => setNewSite({...newSite, url: e.target.value})}
                    className="input-field"
                    placeholder="https://example.com/jobs"
                    required
                  />
                </div>
                <div className="md:col-span-2">
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Notes
                  </label>
                  <textarea
                    value={newSite.notes}
                    onChange={(e) => setNewSite({...newSite, notes: e.target.value})}
                    className="input-field"
                    rows={3}
                    placeholder="Optional notes about this source"
                  />
                </div>
                <div className="md:col-span-2">
                  <label className="flex items-center">
                    <input
                      type="checkbox"
                      checked={newSite.enabled}
                      onChange={(e) => setNewSite({...newSite, enabled: e.target.checked})}
                      className="mr-2"
                    />
                    <span className="text-sm font-medium text-gray-700">Enabled</span>
                  </label>
                </div>
              </div>
              <div className="flex gap-2">
                <button type="submit" className="btn-primary">
                  Add Source
                </button>
                <button
                  type="button"
                  onClick={() => setShowAddForm(false)}
                  className="btn-secondary"
                >
                  Cancel
                </button>
              </div>
            </form>
          </div>
        )}

        {/* Sources List */}
        <div className="space-y-4">
          {sites.length === 0 ? (
            <div className="card text-center py-12">
              <h3 className="text-lg font-medium text-gray-900 mb-2">No job sources found</h3>
              <p className="text-gray-500 mb-4">Add your first job source to start tracking opportunities.</p>
              <button
                onClick={() => setShowAddForm(true)}
                className="btn-primary"
              >
                Add Your First Source
              </button>
            </div>
          ) : (
            sites.map((site) => (
              <div key={site.id} className="card">
                <div className="flex justify-between items-start">
                  <div className="flex-1">
                    <div className="flex items-center gap-3 mb-2">
                      <h3 className="text-lg font-semibold text-gray-900">
                        {site.name}
                      </h3>
                      <span className={`px-2 py-1 rounded-full text-xs font-medium ${getTypeColor(site.type)}`}>
                        {site.type}
                      </span>
                      {!site.enabled && (
                        <span className="px-2 py-1 bg-gray-100 text-gray-800 rounded-full text-xs font-medium">
                          Disabled
                        </span>
                      )}
                    </div>
                    
                    <div className="text-sm text-gray-600 mb-2">
                      <a
                        href={site.url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="text-primary-600 hover:text-primary-800"
                      >
                        {site.url} →
                      </a>
                    </div>
                    
                    {site.notes && (
                      <p className="text-sm text-gray-600 mb-3">{site.notes}</p>
                    )}
                    
                    <div className="text-sm text-gray-600">
                      <span className="font-medium">Added:</span> {new Date(site.created_at).toLocaleDateString()} | 
                      <span className="font-medium ml-2">Updated:</span> {new Date(site.updated_at).toLocaleDateString()}
                    </div>
                  </div>
                  
                  <div className="flex flex-col gap-2">
                    <button
                      onClick={() => handleTestSite(site.id)}
                      className="btn-secondary text-sm px-3 py-1"
                    >
                      Test
                    </button>
                    
                    <a
                      href={site.url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-sm text-primary-600 hover:text-primary-800 text-center"
                    >
                      Open →
                    </a>
                  </div>
                </div>
              </div>
            ))
          )}
        </div>

        {/* Quick Add Presets */}
        <div className="card mt-8">
          <h3 className="text-lg font-semibold mb-4">Quick Add Common Sources</h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <button
              onClick={() => {
                setNewSite({
                  name: 'LinkedIn Jobs',
                  type: 'board',
                  url: 'https://www.linkedin.com/jobs/',
                  notes: 'Professional networking and job board',
                  enabled: true
                });
                setShowAddForm(true);
              }}
              className="btn-secondary text-left p-4"
            >
              <h4 className="font-medium">LinkedIn Jobs</h4>
              <p className="text-sm text-gray-600">Professional networking</p>
            </button>
            
            <button
              onClick={() => {
                setNewSite({
                  name: 'Indeed',
                  type: 'board',
                  url: 'https://www.indeed.com/',
                  notes: 'General job search engine',
                  enabled: true
                });
                setShowAddForm(true);
              }}
              className="btn-secondary text-left p-4"
            >
              <h4 className="font-medium">Indeed</h4>
              <p className="text-sm text-gray-600">Job search engine</p>
            </button>
            
            <button
              onClick={() => {
                setNewSite({
                  name: 'AngelList',
                  type: 'board',
                  url: 'https://angel.co/jobs',
                  notes: 'Startup jobs and opportunities',
                  enabled: true
                });
                setShowAddForm(true);
              }}
              className="btn-secondary text-left p-4"
            >
              <h4 className="font-medium">AngelList</h4>
              <p className="text-sm text-gray-600">Startup opportunities</p>
            </button>
          </div>
        </div>
      </div>
    </Layout>
  );
}
