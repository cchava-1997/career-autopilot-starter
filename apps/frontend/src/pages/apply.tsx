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

interface BulletRewrite {
  original: string;
  rewritten: string;
  rationale: string;
}

interface ApplyPackResponse {
  match_score: number;
  missing_skills: string[];
  rewritten_bullets: BulletRewrite[];
  cover_letter: string;
  risks: string[];
}

export default function ApplyPage() {
  const [jobs, setJobs] = useState<Job[]>([]);
  const [selectedJob, setSelectedJob] = useState<Job | null>(null);
  const [jdText, setJdText] = useState('');
  const [applyPack, setApplyPack] = useState<ApplyPackResponse | null>(null);
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

  const handlePrepareApplyPack = async () => {
    if (!selectedJob || !jdText.trim()) {
      toast.error('Please select a job and paste the job description');
      return;
    }

    setLoading(true);
    try {
      const response = await api.apply.prepare({
        job_id: selectedJob.job_id,
        company: selectedJob.company,
        role: selectedJob.role,
        track: selectedJob.track,
        jd_text: jdText
      });
      
      setApplyPack(response.data);
      setShowResults(true);
      toast.success('Apply pack generated successfully');
    } catch (error) {
      toast.error('Failed to generate apply pack');
      console.error('Error generating apply pack:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSaveApplyPack = async () => {
    if (!selectedJob || !applyPack) return;

    try {
      await api.apply.prepare({
        job_id: selectedJob.job_id,
        company: selectedJob.company,
        role: selectedJob.role,
        track: selectedJob.track,
        jd_text: jdText,
        match: applyPack
      });
      
      toast.success('Apply pack saved successfully');
    } catch (error) {
      toast.error('Failed to save apply pack');
      console.error('Error saving apply pack:', error);
    }
  };

  const getMatchColor = (score: number) => {
    if (score >= 0.8) return 'text-green-600';
    if (score >= 0.6) return 'text-yellow-600';
    return 'text-red-600';
  };

  return (
    <Layout>
      <div>
        <h1 className="text-2xl font-bold text-gray-900 mb-6">Apply Pack Generator</h1>

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

            {/* Job Description Input */}
            <div className="card">
              <h2 className="text-lg font-semibold mb-4">Job Description</h2>
              <textarea
                value={jdText}
                onChange={(e) => setJdText(e.target.value)}
                className="input-field"
                rows={12}
                placeholder="Paste the job description here..."
              />
              
              <div className="mt-4">
                <button
                  onClick={handlePrepareApplyPack}
                  disabled={!selectedJob || !jdText.trim() || loading}
                  className="btn-primary w-full"
                >
                  {loading ? 'Generating...' : 'Generate Apply Pack'}
                </button>
              </div>
            </div>
          </div>

          {/* Results Section */}
          <div className="space-y-6">
            {showResults && applyPack && (
              <>
                {/* Match Score */}
                <div className="card">
                  <h2 className="text-lg font-semibold mb-4">Match Analysis</h2>
                  <div className="text-center">
                    <div className={`text-3xl font-bold ${getMatchColor(applyPack.match_score)}`}>
                      {Math.round(applyPack.match_score * 100)}%
                    </div>
                    <p className="text-sm text-gray-600">Match Score</p>
                  </div>
                </div>

                {/* Missing Skills */}
                {applyPack.missing_skills.length > 0 && (
                  <div className="card">
                    <h2 className="text-lg font-semibold mb-4">Missing Skills</h2>
                    <ul className="space-y-2">
                      {applyPack.missing_skills.map((skill, index) => (
                        <li key={index} className="flex items-center text-sm text-gray-600">
                          <span className="w-2 h-2 bg-red-400 rounded-full mr-2"></span>
                          {skill}
                        </li>
                      ))}
                    </ul>
                  </div>
                )}

                {/* Rewritten Bullets */}
                <div className="card">
                  <h2 className="text-lg font-semibold mb-4">Rewritten Bullets</h2>
                  <div className="space-y-4">
                    {applyPack.rewritten_bullets.map((bullet, index) => (
                      <div key={index} className="border border-gray-200 rounded-lg p-4">
                        <div className="text-sm text-gray-600 mb-2">
                          <span className="font-medium">Original:</span> {bullet.original}
                        </div>
                        <div className="text-sm text-gray-900 mb-2">
                          <span className="font-medium">Rewritten:</span> {bullet.rewritten}
                        </div>
                        <div className="text-xs text-gray-500">
                          <span className="font-medium">Rationale:</span> {bullet.rationale}
                        </div>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Cover Letter */}
                <div className="card">
                  <h2 className="text-lg font-semibold mb-4">Cover Letter</h2>
                  <div className="bg-gray-50 rounded-lg p-4">
                    <p className="text-sm text-gray-900 whitespace-pre-wrap">
                      {applyPack.cover_letter}
                    </p>
                  </div>
                </div>

                {/* Risks */}
                {applyPack.risks.length > 0 && (
                  <div className="card">
                    <h2 className="text-lg font-semibold mb-4">Risks & Considerations</h2>
                    <ul className="space-y-2">
                      {applyPack.risks.map((risk, index) => (
                        <li key={index} className="flex items-start text-sm text-gray-600">
                          <span className="w-2 h-2 bg-yellow-400 rounded-full mr-2 mt-2"></span>
                          {risk}
                        </li>
                      ))}
                    </ul>
                  </div>
                )}

                {/* Actions */}
                <div className="card">
                  <h2 className="text-lg font-semibold mb-4">Actions</h2>
                  <div className="space-y-3">
                    <button
                      onClick={handleSaveApplyPack}
                      className="btn-primary w-full"
                    >
                      Save Apply Pack
                    </button>
                    
                    <button
                      onClick={() => {
                        navigator.clipboard.writeText(applyPack.cover_letter);
                        toast.success('Cover letter copied to clipboard');
                      }}
                      className="btn-secondary w-full"
                    >
                      Copy Cover Letter
                    </button>
                    
                    <button
                      onClick={() => {
                        const bullets = applyPack.rewritten_bullets.map(b => b.rewritten).join('\n');
                        navigator.clipboard.writeText(bullets);
                        toast.success('Bullets copied to clipboard');
                      }}
                      className="btn-secondary w-full"
                    >
                      Copy Bullets
                    </button>
                  </div>
                </div>
              </>
            )}

            {!showResults && (
              <div className="card text-center py-12">
                <h3 className="text-lg font-medium text-gray-900 mb-2">Ready to Generate</h3>
                <p className="text-gray-500">
                  Select a job and paste the job description to generate your apply pack.
                </p>
              </div>
            )}
          </div>
        </div>
      </div>
    </Layout>
  );
}
