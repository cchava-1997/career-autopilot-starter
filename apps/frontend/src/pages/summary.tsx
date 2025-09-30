import { useState, useEffect } from 'react';
import Layout from '../components/Layout';
import { api } from '../services/api';
import toast from 'react-hot-toast';

interface DailySummary {
  jobs_found: number;
  jobs_applied: number;
  outreach_sent: number;
  responses_received: number;
  interviews_scheduled: number;
  skills_gaps: string[];
  summary_lines: string[];
  top_priorities: string[];
}

export default function SummaryPage() {
  const [summary, setSummary] = useState<DailySummary | null>(null);
  const [loading, setLoading] = useState(false);
  const [showSummary, setShowSummary] = useState(false);

  const handleGenerateSummary = async () => {
    setLoading(true);
    try {
      const response = await api.summary.today();
      setSummary(response.data);
      setShowSummary(true);
      toast.success('Daily summary generated successfully');
    } catch (error) {
      toast.error('Failed to generate summary');
      console.error('Error generating summary:', error);
    } finally {
      setLoading(false);
    }
  };

  const handlePostToLinkedIn = () => {
    if (!summary) return;
    
    const linkedInText = summary.summary_lines.join('\n\n');
    const linkedInUrl = `https://www.linkedin.com/feed/?shareActive=true&text=${encodeURIComponent(linkedInText)}`;
    
    window.open(linkedInUrl, '_blank');
    toast.success('LinkedIn post opened');
  };

  const handleCopySummary = () => {
    if (!summary) return;
    
    const summaryText = summary.summary_lines.join('\n\n');
    navigator.clipboard.writeText(summaryText);
    toast.success('Summary copied to clipboard');
  };

  return (
    <Layout>
      <div>
        <div className="flex justify-between items-center mb-6">
          <h1 className="text-2xl font-bold text-gray-900">Daily Summary</h1>
          <button
            onClick={handleGenerateSummary}
            disabled={loading}
            className="btn-primary"
          >
            {loading ? 'Generating...' : 'Generate Today\'s Summary'}
          </button>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Summary Section */}
          <div className="space-y-6">
            {showSummary && summary && (
              <>
                {/* Summary Lines */}
                <div className="card">
                  <h2 className="text-lg font-semibold mb-4">Today's Summary</h2>
                  <div className="space-y-4">
                    {summary.summary_lines.map((line, index) => (
                      <div key={index} className="p-3 bg-gray-50 rounded-lg">
                        <p className="text-sm text-gray-900">{line}</p>
                      </div>
                    ))}
                  </div>
                  
                  <div className="mt-4 flex gap-2">
                    <button
                      onClick={handleCopySummary}
                      className="btn-secondary text-sm px-3 py-1"
                    >
                      Copy Summary
                    </button>
                    <button
                      onClick={handlePostToLinkedIn}
                      className="btn-primary text-sm px-3 py-1"
                    >
                      Post to LinkedIn
                    </button>
                  </div>
                </div>

                {/* Top Priorities */}
                <div className="card">
                  <h2 className="text-lg font-semibold mb-4">Top Priorities Tomorrow</h2>
                  <ul className="space-y-2">
                    {summary.top_priorities.map((priority, index) => (
                      <li key={index} className="flex items-start text-sm text-gray-900">
                        <span className="w-2 h-2 bg-primary-400 rounded-full mr-2 mt-2"></span>
                        {priority}
                      </li>
                    ))}
                  </ul>
                </div>
              </>
            )}

            {!showSummary && (
              <div className="card text-center py-12">
                <h3 className="text-lg font-medium text-gray-900 mb-2">Ready to Summarize</h3>
                <p className="text-gray-500 mb-4">
                  Generate your daily summary to track progress and plan tomorrow's priorities.
                </p>
                <button
                  onClick={handleGenerateSummary}
                  disabled={loading}
                  className="btn-primary"
                >
                  {loading ? 'Generating...' : 'Generate Summary'}
                </button>
              </div>
            )}
          </div>

          {/* Stats Section */}
          <div className="space-y-6">
            {showSummary && summary && (
              <>
                {/* Activity Stats */}
                <div className="card">
                  <h2 className="text-lg font-semibold mb-4">Today's Activity</h2>
                  <div className="grid grid-cols-2 gap-4">
                    <div className="text-center p-4 bg-blue-50 rounded-lg">
                      <div className="text-2xl font-bold text-blue-600">{summary.jobs_found}</div>
                      <div className="text-sm text-blue-800">Jobs Found</div>
                    </div>
                    <div className="text-center p-4 bg-green-50 rounded-lg">
                      <div className="text-2xl font-bold text-green-600">{summary.jobs_applied}</div>
                      <div className="text-sm text-green-800">Jobs Applied</div>
                    </div>
                    <div className="text-center p-4 bg-purple-50 rounded-lg">
                      <div className="text-2xl font-bold text-purple-600">{summary.outreach_sent}</div>
                      <div className="text-sm text-purple-800">Outreach Sent</div>
                    </div>
                    <div className="text-center p-4 bg-yellow-50 rounded-lg">
                      <div className="text-2xl font-bold text-yellow-600">{summary.responses_received}</div>
                      <div className="text-sm text-yellow-800">Responses</div>
                    </div>
                  </div>
                </div>

                {/* Skills Gaps */}
                <div className="card">
                  <h2 className="text-lg font-semibold mb-4">Skills Gaps</h2>
                  {summary.skills_gaps.length > 0 ? (
                    <ul className="space-y-2">
                      {summary.skills_gaps.map((gap, index) => (
                        <li key={index} className="flex items-start text-sm text-gray-600">
                          <span className="w-2 h-2 bg-red-400 rounded-full mr-2 mt-2"></span>
                          {gap}
                        </li>
                      ))}
                    </ul>
                  ) : (
                    <p className="text-sm text-gray-500">No significant skills gaps identified</p>
                  )}
                </div>

                {/* Interview Schedule */}
                <div className="card">
                  <h2 className="text-lg font-semibold mb-4">Interview Schedule</h2>
                  <div className="text-center p-4 bg-indigo-50 rounded-lg">
                    <div className="text-2xl font-bold text-indigo-600">{summary.interviews_scheduled}</div>
                    <div className="text-sm text-indigo-800">Interviews Scheduled</div>
                  </div>
                </div>
              </>
            )}

            {!showSummary && (
              <div className="card text-center py-12">
                <h3 className="text-lg font-medium text-gray-900 mb-2">Activity Tracking</h3>
                <p className="text-gray-500">
                  Your daily activity stats will appear here after generating a summary.
                </p>
              </div>
            )}
          </div>
        </div>
      </div>
    </Layout>
  );
}
