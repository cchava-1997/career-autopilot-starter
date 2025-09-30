import { useState, useEffect } from 'react';
import Layout from '../components/Layout';
import { api } from '../services/api';
import toast from 'react-hot-toast';

interface Resume {
  id: string;
  track: string;
  version: string;
  notes?: string;
  is_default: boolean;
  created_at: string;
  updated_at: string;
  file_path?: string;
  overleaf_url?: string;
}

export default function ResumesPage() {
  const [resumes, setResumes] = useState<Resume[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedTrack, setSelectedTrack] = useState<string>('');

  useEffect(() => {
    fetchResumes();
  }, [selectedTrack]);

  const fetchResumes = async () => {
    try {
      const response = await api.resumes.list(selectedTrack || undefined);
      setResumes(response.data);
    } catch (error) {
      toast.error('Failed to fetch resumes');
      console.error('Error fetching resumes:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSetDefault = async (resumeId: string) => {
    try {
      await api.resumes.setDefault(resumeId);
      toast.success('Default resume updated');
      fetchResumes();
    } catch (error) {
      toast.error('Failed to set default resume');
      console.error('Error setting default resume:', error);
    }
  };

  const handleOverleafBuild = async (track: string, jobId: string) => {
    try {
      const response = await api.overleaf.build(track, jobId);
      if (response.data.success) {
        toast.success('PDF built successfully');
      } else {
        toast.error(response.data.error || 'Build failed');
      }
    } catch (error) {
      toast.error('Failed to build PDF');
      console.error('Error building PDF:', error);
    }
  };

  const handleOpenOverleaf = async (track: string) => {
    try {
      const response = await api.overleaf.openLink(`https://www.overleaf.com/project/${track}`);
      if (response.data.success) {
        toast.success('Opening Overleaf project');
      }
    } catch (error) {
      toast.error('Failed to open Overleaf');
      console.error('Error opening Overleaf:', error);
    }
  };

  const tracks = ['PO', 'PM', 'TPM'];
  const resumesByTrack = resumes.reduce((acc, resume) => {
    if (!acc[resume.track]) acc[resume.track] = [];
    acc[resume.track].push(resume);
    return acc;
  }, {} as Record<string, Resume[]>);

  if (loading) {
    return (
      <Layout>
        <div className="animate-pulse">
          <div className="h-8 bg-gray-200 rounded w-1/4 mb-6"></div>
          <div className="space-y-4">
            {[...Array(3)].map((_, i) => (
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
          <h1 className="text-2xl font-bold text-gray-900">Resume Vault</h1>
          <div className="flex gap-2">
            <select
              value={selectedTrack}
              onChange={(e) => setSelectedTrack(e.target.value)}
              className="input-field"
            >
              <option value="">All Tracks</option>
              {tracks.map(track => (
                <option key={track} value={track}>{track}</option>
              ))}
            </select>
          </div>
        </div>

        {/* Track Overview */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          {tracks.map(track => {
            const trackResumes = resumesByTrack[track] || [];
            const defaultResume = trackResumes.find(r => r.is_default);
            
            return (
              <div key={track} className="card">
                <div className="flex items-center justify-between mb-4">
                  <h3 className="text-lg font-semibold text-gray-900">{track} Track</h3>
                  <button
                    onClick={() => handleOpenOverleaf(track)}
                    className="text-sm text-primary-600 hover:text-primary-800"
                  >
                    Edit in Overleaf →
                  </button>
                </div>
                
                <div className="space-y-3">
                  <div className="text-sm text-gray-600">
                    <span className="font-medium">Versions:</span> {trackResumes.length}
                  </div>
                  
                  {defaultResume ? (
                    <div className="text-sm">
                      <span className="font-medium">Default:</span> {defaultResume.version}
                      <div className="text-xs text-gray-500 mt-1">
                        Updated: {new Date(defaultResume.updated_at).toLocaleDateString()}
                      </div>
                    </div>
                  ) : (
                    <div className="text-sm text-gray-500">No default set</div>
                  )}
                  
                  <div className="flex gap-2">
                    <button
                      onClick={() => handleOverleafBuild(track, 'demo_job')}
                      className="btn-primary text-sm px-3 py-1"
                    >
                      Build PDF
                    </button>
                  </div>
                </div>
              </div>
            );
          })}
        </div>

        {/* Resumes List */}
        <div className="space-y-4">
          {resumes.length === 0 ? (
            <div className="card text-center py-12">
              <h3 className="text-lg font-medium text-gray-900 mb-2">No resumes found</h3>
              <p className="text-gray-500 mb-4">
                {selectedTrack 
                  ? `No resumes found for ${selectedTrack} track.`
                  : 'No resumes found. Create your first resume in Overleaf.'
                }
              </p>
              <div className="space-y-2">
                {tracks.map(track => (
                  <button
                    key={track}
                    onClick={() => handleOpenOverleaf(track)}
                    className="btn-primary text-sm px-4 py-2 mr-2"
                  >
                    Create {track} Resume
                  </button>
                ))}
              </div>
            </div>
          ) : (
            resumes.map((resume) => (
              <div key={resume.id} className="card">
                <div className="flex justify-between items-start">
                  <div className="flex-1">
                    <div className="flex items-center gap-3 mb-2">
                      <h3 className="text-lg font-semibold text-gray-900">
                        {resume.track} - {resume.version}
                      </h3>
                      {resume.is_default && (
                        <span className="px-2 py-1 bg-primary-100 text-primary-800 rounded-full text-xs font-medium">
                          ⭐ Default
                        </span>
                      )}
                    </div>
                    
                    {resume.notes && (
                      <p className="text-sm text-gray-600 mb-3">{resume.notes}</p>
                    )}
                    
                    <div className="text-sm text-gray-600">
                      <span className="font-medium">Created:</span> {new Date(resume.created_at).toLocaleDateString()} | 
                      <span className="font-medium ml-2">Updated:</span> {new Date(resume.updated_at).toLocaleDateString()}
                    </div>
                    
                    {resume.file_path && (
                      <div className="text-sm text-gray-600 mt-1">
                        <span className="font-medium">File:</span> {resume.file_path.split('/').pop()}
                      </div>
                    )}
                  </div>
                  
                  <div className="flex flex-col gap-2">
                    {!resume.is_default && (
                      <button
                        onClick={() => handleSetDefault(resume.id)}
                        className="btn-secondary text-sm px-3 py-1"
                      >
                        Set Default
                      </button>
                    )}
                    
                    <button
                      onClick={() => handleOpenOverleaf(resume.track)}
                      className="text-sm text-primary-600 hover:text-primary-800"
                    >
                      Edit in Overleaf →
                    </button>
                    
                    <button
                      onClick={() => handleOverleafBuild(resume.track, 'demo_job')}
                      className="text-sm text-primary-600 hover:text-primary-800"
                    >
                      Build PDF →
                    </button>
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
