import { useState, useEffect } from 'react';
import Layout from '../components/Layout';
import { api } from '../services/api';
import toast from 'react-hot-toast';

interface Job {
  job_id: string;
  company: string;
  role: string;
  jd_url: string;
  track: string;
  status: string;
  apply_by: string;
  created_at: string;
  updated_at: string;
  notes?: string;
}

export default function JobsPage() {
  const [jobs, setJobs] = useState<Job[]>([]);
  const [loading, setLoading] = useState(true);
  const [showAddForm, setShowAddForm] = useState(false);
  const [newJob, setNewJob] = useState({
    job_id: '',
    company: '',
    role: '',
    jd_url: '',
    track: 'PM',
    notes: ''
  });

  useEffect(() => {
    fetchJobs();
  }, []);

  const fetchJobs = async () => {
    try {
      const response = await api.jobs.list();
      setJobs(response.data);
    } catch (error) {
      toast.error('Failed to fetch jobs');
      console.error('Error fetching jobs:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleAddJob = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await api.jobs.add(newJob);
      toast.success('Job added successfully');
      setNewJob({
        job_id: '',
        company: '',
        role: '',
        jd_url: '',
        track: 'PM',
        notes: ''
      });
      setShowAddForm(false);
      fetchJobs();
    } catch (error) {
      toast.error('Failed to add job');
      console.error('Error adding job:', error);
    }
  };

  const handleUpdateStatus = async (jobId: string, status: string) => {
    try {
      await api.jobs.updateStatus(jobId, status);
      toast.success('Status updated successfully');
      fetchJobs();
    } catch (error) {
      toast.error('Failed to update status');
      console.error('Error updating status:', error);
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'new': return 'bg-gray-100 text-gray-800';
      case 'prepared': return 'bg-blue-100 text-blue-800';
      case 'pdf_ready': return 'bg-yellow-100 text-yellow-800';
      case 'autofilled': return 'bg-purple-100 text-purple-800';
      case 'submitted': return 'bg-green-100 text-green-800';
      case 'rejected': return 'bg-red-100 text-red-800';
      case 'interview': return 'bg-indigo-100 text-indigo-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const getSLAColor = (applyBy: string) => {
    const now = new Date();
    const applyDate = new Date(applyBy);
    const diffHours = (applyDate.getTime() - now.getTime()) / (1000 * 60 * 60);
    
    if (diffHours < 0) return 'sla-overdue';
    if (diffHours < 24) return 'sla-due-today';
    return 'sla-on-track';
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
          <h1 className="text-2xl font-bold text-gray-900">Jobs</h1>
          <button
            onClick={() => setShowAddForm(true)}
            className="btn-primary"
          >
            Add Job
          </button>
        </div>

        {/* Add Job Form */}
        {showAddForm && (
          <div className="card mb-6">
            <h2 className="text-lg font-semibold mb-4">Add New Job</h2>
            <form onSubmit={handleAddJob} className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Job ID
                  </label>
                  <input
                    type="text"
                    value={newJob.job_id}
                    onChange={(e) => setNewJob({...newJob, job_id: e.target.value})}
                    className="input-field"
                    required
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Company
                  </label>
                  <input
                    type="text"
                    value={newJob.company}
                    onChange={(e) => setNewJob({...newJob, company: e.target.value})}
                    className="input-field"
                    required
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Role
                  </label>
                  <input
                    type="text"
                    value={newJob.role}
                    onChange={(e) => setNewJob({...newJob, role: e.target.value})}
                    className="input-field"
                    required
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Track
                  </label>
                  <select
                    value={newJob.track}
                    onChange={(e) => setNewJob({...newJob, track: e.target.value})}
                    className="input-field"
                  >
                    <option value="PO">PO</option>
                    <option value="PM">PM</option>
                    <option value="TPM">TPM</option>
                  </select>
                </div>
                <div className="md:col-span-2">
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    JD URL
                  </label>
                  <input
                    type="url"
                    value={newJob.jd_url}
                    onChange={(e) => setNewJob({...newJob, jd_url: e.target.value})}
                    className="input-field"
                    required
                  />
                </div>
                <div className="md:col-span-2">
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Notes
                  </label>
                  <textarea
                    value={newJob.notes}
                    onChange={(e) => setNewJob({...newJob, notes: e.target.value})}
                    className="input-field"
                    rows={3}
                  />
                </div>
              </div>
              <div className="flex gap-2">
                <button type="submit" className="btn-primary">
                  Add Job
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

        {/* Jobs List */}
        <div className="space-y-4">
          {jobs.length === 0 ? (
            <div className="card text-center py-12">
              <h3 className="text-lg font-medium text-gray-900 mb-2">No jobs found</h3>
              <p className="text-gray-500 mb-4">Get started by adding your first job opportunity.</p>
              <button
                onClick={() => setShowAddForm(true)}
                className="btn-primary"
              >
                Add Your First Job
              </button>
            </div>
          ) : (
            jobs.map((job) => (
              <div key={job.job_id} className="card">
                <div className="flex justify-between items-start">
                  <div className="flex-1">
                    <div className="flex items-center gap-3 mb-2">
                      <h3 className="text-lg font-semibold text-gray-900">
                        {job.role} at {job.company}
                      </h3>
                      <span className={`px-2 py-1 rounded-full text-xs font-medium ${getStatusColor(job.status)}`}>
                        {job.status}
                      </span>
                      <span className={`px-2 py-1 rounded-full text-xs font-medium ${getSLAColor(job.apply_by)}`}>
                        SLA: {new Date(job.apply_by).toLocaleDateString()}
                      </span>
                    </div>
                    <div className="text-sm text-gray-600 mb-2">
                      <span className="font-medium">Track:</span> {job.track} | 
                      <span className="font-medium ml-2">Job ID:</span> {job.job_id}
                    </div>
                    {job.notes && (
                      <p className="text-sm text-gray-600 mb-3">{job.notes}</p>
                    )}
                    <div className="flex gap-2">
                      <a
                        href={job.jd_url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="text-primary-600 hover:text-primary-800 text-sm"
                      >
                        View JD →
                      </a>
                    </div>
                  </div>
                  <div className="flex flex-col gap-2">
                    <select
                      value={job.status}
                      onChange={(e) => handleUpdateStatus(job.job_id, e.target.value)}
                      className="text-sm border border-gray-300 rounded px-2 py-1"
                    >
                      <option value="new">New</option>
                      <option value="prepared">Prepared</option>
                      <option value="pdf_ready">PDF Ready</option>
                      <option value="autofilled">Autofilled</option>
                      <option value="submitted">Submitted</option>
                      <option value="rejected">Rejected</option>
                      <option value="interview">Interview</option>
                    </select>
                    <div className="text-xs text-gray-500">
                      Created: {new Date(job.created_at).toLocaleDateString()}
                    </div>
                  </div>
                </div>
              </div>
            ))
          )}
        </div>
      </div>
    </Layout>
  );
}
