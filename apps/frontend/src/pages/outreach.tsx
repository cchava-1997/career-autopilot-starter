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

interface Contact {
  name: string;
  role: string;
  company: string;
  channel: string;
  profile_url?: string;
  email?: string;
  persona: string;
}

interface OutreachPlan {
  job_id: string;
  contacts: Contact[];
  messages: Record<string, string>;
  followups: Record<string, string>;
}

export default function OutreachPage() {
  const [jobs, setJobs] = useState<Job[]>([]);
  const [selectedJob, setSelectedJob] = useState<Job | null>(null);
  const [outreachPlan, setOutreachPlan] = useState<OutreachPlan | null>(null);
  const [loading, setLoading] = useState(false);
  const [showResults, setShowResults] = useState(false);

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
    }
  };

  const handleGenerateOutreach = async () => {
    if (!selectedJob) {
      toast.error('Please select a job');
      return;
    }

    setLoading(true);
    try {
      const response = await api.outreach.plan(
        selectedJob.job_id,
        selectedJob.company,
        selectedJob.role
      );
      
      setOutreachPlan(response.data);
      setShowResults(true);
      toast.success('Outreach plan generated successfully');
    } catch (error) {
      toast.error('Failed to generate outreach plan');
      console.error('Error generating outreach plan:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleScheduleFollowups = async () => {
    if (!selectedJob) return;

    try {
      await api.followups.schedule(selectedJob.job_id);
      toast.success('Follow-ups scheduled successfully');
    } catch (error) {
      toast.error('Failed to schedule follow-ups');
      console.error('Error scheduling follow-ups:', error);
    }
  };

  const handleCreateDrafts = async () => {
    if (!selectedJob) return;

    try {
      await api.outreach.drafts(selectedJob.job_id);
      toast.success('Drafts created successfully');
    } catch (error) {
      toast.error('Failed to create drafts');
      console.error('Error creating drafts:', error);
    }
  };

  const getPersonaColor = (persona: string) => {
    switch (persona) {
      case 'peer': return 'bg-blue-100 text-blue-800';
      case 'insider': return 'bg-green-100 text-green-800';
      case 'recruiter': return 'bg-purple-100 text-purple-800';
      case 'referral': return 'bg-yellow-100 text-yellow-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const getChannelIcon = (channel: string) => {
    switch (channel) {
      case 'linkedin': return '💼';
      case 'email': return '📧';
      default: return '📱';
    }
  };

  return (
    <Layout>
      <div>
        <h1 className="text-2xl font-bold text-gray-900 mb-6">Outreach Planning</h1>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Input Section */}
          <div className="space-y-6">
            {/* Job Selection */}
            <div className="card">
              <h2 className="text-lg font-semibold mb-4">Select Job</h2>
              <select
                value={selectedJob?.job_id || ''}
                onChange={(e) => {
                  const job = jobs.find(j => j.job_id === e.target.value);
                  setSelectedJob(job || null);
                }}
                className="input-field"
              >
                <option value="">Choose a job...</option>
                {jobs.map(job => (
                  <option key={job.job_id} value={job.job_id}>
                    {job.role} at {job.company} ({job.track})
                  </option>
                ))}
              </select>
              
              {selectedJob && (
                <div className="mt-4 p-4 bg-gray-50 rounded-lg">
                  <h3 className="font-medium text-gray-900">{selectedJob.role} at {selectedJob.company}</h3>
                  <p className="text-sm text-gray-600">Track: {selectedJob.track}</p>
                  <a
                    href={selectedJob.jd_url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-sm text-primary-600 hover:text-primary-800"
                  >
                    View JD →
                  </a>
                </div>
              )}
            </div>

            {/* Generate Button */}
            <div className="card">
              <h2 className="text-lg font-semibold mb-4">Generate Outreach Plan</h2>
              <p className="text-sm text-gray-600 mb-4">
                Generate a 2+2+1 outreach strategy (2 peers, 2 insiders, 1 recruiter) with personalized messages.
              </p>
              
              <button
                onClick={handleGenerateOutreach}
                disabled={!selectedJob || loading}
                className="btn-primary w-full"
              >
                {loading ? 'Generating...' : 'Generate Outreach Plan'}
              </button>
            </div>

            {/* Actions */}
            {showResults && outreachPlan && (
              <div className="card">
                <h2 className="text-lg font-semibold mb-4">Actions</h2>
                <div className="space-y-3">
                  <button
                    onClick={handleCreateDrafts}
                    className="btn-primary w-full"
                  >
                    Create Email Drafts
                  </button>
                  
                  <button
                    onClick={handleScheduleFollowups}
                    className="btn-secondary w-full"
                  >
                    Schedule Follow-ups
                  </button>
                </div>
              </div>
            )}
          </div>

          {/* Results Section */}
          <div className="space-y-6">
            {showResults && outreachPlan && (
              <>
                {/* Contacts Overview */}
                <div className="card">
                  <h2 className="text-lg font-semibold mb-4">Outreach Contacts</h2>
                  <div className="space-y-3">
                    {outreachPlan.contacts.map((contact, index) => (
                      <div key={index} className="border border-gray-200 rounded-lg p-4">
                        <div className="flex items-center justify-between mb-2">
                          <h3 className="font-medium text-gray-900">{contact.name}</h3>
                          <div className="flex items-center gap-2">
                            <span className="text-sm">{getChannelIcon(contact.channel)}</span>
                            <span className={`px-2 py-1 rounded-full text-xs font-medium ${getPersonaColor(contact.persona)}`}>
                              {contact.persona}
                            </span>
                          </div>
                        </div>
                        <p className="text-sm text-gray-600">{contact.role} at {contact.company}</p>
                        {contact.email && (
                          <p className="text-sm text-gray-600">📧 {contact.email}</p>
                        )}
                      </div>
                    ))}
                  </div>
                </div>

                {/* Messages */}
                <div className="card">
                  <h2 className="text-lg font-semibold mb-4">Personalized Messages</h2>
                  <div className="space-y-4">
                    {outreachPlan.contacts.map((contact, index) => (
                      <div key={index} className="border border-gray-200 rounded-lg p-4">
                        <h3 className="font-medium text-gray-900 mb-2">{contact.name}</h3>
                        <div className="bg-gray-50 rounded-lg p-3">
                          <p className="text-sm text-gray-900 whitespace-pre-wrap">
                            {outreachPlan.messages[contact.name]}
                          </p>
                        </div>
                        <div className="mt-2 text-xs text-gray-500">
                          Follow-up: {new Date(outreachPlan.followups[contact.name]).toLocaleDateString()}
                        </div>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Follow-up Schedule */}
                <div className="card">
                  <h2 className="text-lg font-semibold mb-4">Follow-up Schedule</h2>
                  <div className="space-y-2">
                    {Object.entries(outreachPlan.followups).map(([name, date]) => (
                      <div key={name} className="flex justify-between items-center text-sm">
                        <span className="text-gray-900">{name}</span>
                        <span className="text-gray-600">{new Date(date).toLocaleDateString()}</span>
                      </div>
                    ))}
                  </div>
                </div>
              </>
            )}

            {!showResults && (
              <div className="card text-center py-12">
                <h3 className="text-lg font-medium text-gray-900 mb-2">Ready to Plan</h3>
                <p className="text-gray-500">
                  Select a job to generate your outreach strategy with personalized messages.
                </p>
              </div>
            )}
          </div>
        </div>
      </div>
    </Layout>
  );
}
