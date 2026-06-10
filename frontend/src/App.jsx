import { useEffect, useState } from 'react';
import { AnimatePresence, motion } from 'framer-motion';
import { api } from './api/client.js';
import ParticleField from './components/ParticleField.jsx';
import CursorGlow from './components/CursorGlow.jsx';
import IntroSection from './components/IntroSection.jsx';
import Wizard from './components/Wizard.jsx';
import Results from './components/Results.jsx';
import LoadingOverlay from './components/LoadingOverlay.jsx';

export default function App() {
  const [screen, setScreen] = useState('intro');
  const [departments, setDepartments] = useState([]);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    document.body.classList.toggle('intro-page', screen === 'intro');
    return () => document.body.classList.remove('intro-page');
  }, [screen]);

  useEffect(() => {
    let mounted = true;

    async function loadInitialData() {
      try {
        const departmentResponse = await api.getDepartments();
        if (!mounted) return;
        setDepartments(departmentResponse.departments || []);
      } catch (err) {
        if (!mounted) return;
        setError('백엔드 API에 연결할 수 없습니다. backend 서버를 먼저 실행해 주세요.');
      }
    }

    loadInitialData();
    return () => { mounted = false; };
  }, []);

  const handleSubmit = async payload => {
    setLoading(true);
    setError('');

    try {
      const response = await api.recommend(payload);
      setResult(response);
      setScreen('results');
      window.scrollTo({ top: 0, behavior: 'smooth' });
    } catch (err) {
      setError(err.message || '추천 요청에 실패했습니다.');
    } finally {
      setLoading(false);
    }
  };

  const reset = () => {
    setResult(null);
    setScreen('intro');
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  return (
    <div className={`app-root screen-${screen}`}>
      <ParticleField />
      <CursorGlow />
      <div className="noise-layer" />

      {error && (
        <motion.div className="api-error" initial={{ opacity: 0, y: -12 }} animate={{ opacity: 1, y: 0 }}>
          {error}
        </motion.div>
      )}

      <main className="app-main">
        <AnimatePresence mode="wait">
          {screen === 'intro' && (
            <motion.div key="intro" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0, scale: 0.98 }}>
              <IntroSection onStart={() => setScreen('wizard')} />
            </motion.div>
          )}
          {screen === 'wizard' && (
            <motion.div key="wizard" initial={{ opacity: 0, y: 24 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -24 }}>
              <Wizard departments={departments} onSubmit={handleSubmit} loading={loading} />
            </motion.div>
          )}
          {screen === 'results' && (
            <motion.div key="results" initial={{ opacity: 0, y: 24 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0 }}>
              <Results result={result} onReset={reset} />
            </motion.div>
          )}
        </AnimatePresence>
      </main>

      <LoadingOverlay show={loading} />
    </div>
  );
}
