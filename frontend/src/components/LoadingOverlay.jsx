import { motion, AnimatePresence } from 'framer-motion';

export default function LoadingOverlay({ show }) {
  return (
    <AnimatePresence>
      {show && (
        <motion.div className="loading-overlay" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}>
          <div className="scanner">
            <span />
          </div>
          <strong>추천 데이터를 분석하고 있습니다</strong>
          <p>학과 기준 · 예산 · OS · 노트북 후보 점수 계산 중</p>
        </motion.div>
      )}
    </AnimatePresence>
  );
}
