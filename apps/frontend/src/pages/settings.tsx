import { useState, useEffect } from 'react';
import Layout from '../components/Layout';
import { api } from '../services/api';
import toast from 'react-hot-toast';

interface Settings {
  overleaf_api_key: string;
  overleaf_projects: {
    PO: string;
    PM: string;
    TPM: string;
  };
  chrome_user_data_dir: string;
  profile_fields: {
    name: string;
    email: string;
    phone: string;
  };
  tracker_path: string;
  apply_pack_dir: string;
  resume_dir: string;
}

export default function SettingsPage() {
  const [settings, setSettings] = useState<Settings>({
    overleaf_api_key: '',
    overleaf_projects: {
      PO: '',
      PM: '',
      TPM: ''
    },
    chrome_user_data_dir: '',
    profile_fields: {
      name: '',
      email: '',
      phone: ''
    },
    tracker_path: '',
    apply_pack_dir: '',
    resume_dir: ''
  });
  const [loading, setLoading] = useState(false);
  const [testing, setTesting] = useState<string | null>(null);

  useEffect(() => {
    fetchSettings();
  }, []);

  const fetchSettings = async () => {
    try {
      const response = await api.settings.get();
      setSettings(response.data);
    } catch (error) {
      toast.error('Failed to fetch settings');
      console.error('Error fetching settings:', error);
    }
  };

  const handleSaveSettings = async () => {
    setLoading(true);
    try {
      await api.settings.update(settings);
      toast.success('Settings saved successfully');
    } catch (error) {
      toast.error('Failed to save settings');
      console.error('Error saving settings:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleTestOverleaf = async () => {
    setTesting('overleaf');
    try {
      const response = await api.settings.testOverleaf();
      if (response.data.success) {
        toast.success('Overleaf connection successful');
      } else {
        toast.error('Overleaf connection failed');
      }
    } catch (error) {
      toast.error('Failed to test Overleaf connection');
      console.error('Error testing Overleaf:', error);
    } finally {
      setTesting(null);
    }
  };

  const handleTestChrome = async () => {
    setTesting('chrome');
    try {
      const response = await api.settings.testChrome();
      if (response.data.success) {
        toast.success('Chrome profile accessible');
      } else {
        toast.error('Chrome profile not accessible');
      }
    } catch (error) {
      toast.error('Failed to test Chrome profile');
      console.error('Error testing Chrome:', error);
    } finally {
      setTesting(null);
    }
  };

  const handleTestLaTeX = async () => {
    setTesting('latex');
    try {
      const response = await api.settings.testLaTeX();
      if (response.data.success) {
        toast.success('LaTeX build successful');
      } else {
        toast.error('LaTeX build failed');
      }
    } catch (error) {
      toast.error('Failed to test LaTeX build');
      console.error('Error testing LaTeX:', error);
    } finally {
      setTesting(null);
    }
  };

  return (
    <Layout>
      <div>
        <h1 className="text-2xl font-bold text-gray-900 mb-6">Settings</h1>

        <div className="space-y-6">
          {/* Overleaf Settings */}
          <div className="card">
            <h2 className="text-lg font-semibold mb-4">Overleaf Configuration</h2>
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  API Key
                </label>
                <input
                  type="password"
                  value={settings.overleaf_api_key}
                  onChange={(e) => setSettings({...settings, overleaf_api_key: e.target.value})}
                  className="input-field"
                  placeholder="Enter your Overleaf API key"
                />
              </div>
              
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    PO Project ID
                  </label>
                  <input
                    type="text"
                    value={settings.overleaf_projects.PO}
                    onChange={(e) => setSettings({
                      ...settings, 
                      overleaf_projects: {...settings.overleaf_projects, PO: e.target.value}
                    })}
                    className="input-field"
                    placeholder="Project ID"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    PM Project ID
                  </label>
                  <input
                    type="text"
                    value={settings.overleaf_projects.PM}
                    onChange={(e) => setSettings({
                      ...settings, 
                      overleaf_projects: {...settings.overleaf_projects, PM: e.target.value}
                    })}
                    className="input-field"
                    placeholder="Project ID"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    TPM Project ID
                  </label>
                  <input
                    type="text"
                    value={settings.overleaf_projects.TPM}
                    onChange={(e) => setSettings({
                      ...settings, 
                      overleaf_projects: {...settings.overleaf_projects, TPM: e.target.value}
                    })}
                    className="input-field"
                    placeholder="Project ID"
                  />
                </div>
              </div>
              
              <button
                onClick={handleTestOverleaf}
                disabled={testing === 'overleaf'}
                className="btn-secondary"
              >
                {testing === 'overleaf' ? 'Testing...' : 'Test Overleaf Connection'}
              </button>
            </div>
          </div>

          {/* Chrome Profile Settings */}
          <div className="card">
            <h2 className="text-lg font-semibold mb-4">Chrome Profile Configuration</h2>
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  User Data Directory
                </label>
                <input
                  type="text"
                  value={settings.chrome_user_data_dir}
                  onChange={(e) => setSettings({...settings, chrome_user_data_dir: e.target.value})}
                  className="input-field"
                  placeholder="/Users/username/Library/Application Support/Google/Chrome"
                />
              </div>
              
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Name
                  </label>
                  <input
                    type="text"
                    value={settings.profile_fields.name}
                    onChange={(e) => setSettings({
                      ...settings, 
                      profile_fields: {...settings.profile_fields, name: e.target.value}
                    })}
                    className="input-field"
                    placeholder="Your name"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Email
                  </label>
                  <input
                    type="email"
                    value={settings.profile_fields.email}
                    onChange={(e) => setSettings({
                      ...settings, 
                      profile_fields: {...settings.profile_fields, email: e.target.value}
                    })}
                    className="input-field"
                    placeholder="your@email.com"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Phone
                  </label>
                  <input
                    type="tel"
                    value={settings.profile_fields.phone}
                    onChange={(e) => setSettings({
                      ...settings, 
                      profile_fields: {...settings.profile_fields, phone: e.target.value}
                    })}
                    className="input-field"
                    placeholder="+1 (555) 123-4567"
                  />
                </div>
              </div>
              
              <button
                onClick={handleTestChrome}
                disabled={testing === 'chrome'}
                className="btn-secondary"
              >
                {testing === 'chrome' ? 'Testing...' : 'Test Chrome Profile'}
              </button>
            </div>
          </div>

          {/* File Paths */}
          <div className="card">
            <h2 className="text-lg font-semibold mb-4">File Paths</h2>
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Tracker Path
                </label>
                <input
                  type="text"
                  value={settings.tracker_path}
                  onChange={(e) => setSettings({...settings, tracker_path: e.target.value})}
                  className="input-field"
                  placeholder="/path/to/career_autopilot_tracker.xlsx"
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Apply Pack Directory
                </label>
                <input
                  type="text"
                  value={settings.apply_pack_dir}
                  onChange={(e) => setSettings({...settings, apply_pack_dir: e.target.value})}
                  className="input-field"
                  placeholder="/path/to/applications"
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Resume Directory
                </label>
                <input
                  type="text"
                  value={settings.resume_dir}
                  onChange={(e) => setSettings({...settings, resume_dir: e.target.value})}
                  className="input-field"
                  placeholder="/path/to/resumes"
                />
              </div>
            </div>
          </div>

          {/* LaTeX Build Test */}
          <div className="card">
            <h2 className="text-lg font-semibold mb-4">LaTeX Build Test</h2>
            <p className="text-sm text-gray-600 mb-4">
              Test the LaTeX build process to ensure PDF generation works correctly.
            </p>
            <button
              onClick={handleTestLaTeX}
              disabled={testing === 'latex'}
              className="btn-secondary"
            >
              {testing === 'latex' ? 'Testing...' : 'Test LaTeX Build'}
            </button>
          </div>

          {/* Save Button */}
          <div className="card">
            <div className="flex justify-between items-center">
              <div>
                <h2 className="text-lg font-semibold">Save Settings</h2>
                <p className="text-sm text-gray-600">Save all configuration changes</p>
              </div>
              <button
                onClick={handleSaveSettings}
                disabled={loading}
                className="btn-primary"
              >
                {loading ? 'Saving...' : 'Save Settings'}
              </button>
            </div>
          </div>
        </div>
      </div>
    </Layout>
  );
}
