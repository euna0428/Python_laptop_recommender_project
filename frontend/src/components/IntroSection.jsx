import { motion } from 'framer-motion';

export default function IntroSection({ onStart }) {
  return (
    <section className="intro-section screen-shell" aria-label="노트북 추천 서비스 소개 화면">
      <div className="grid-floor" />

      <motion.div
        className="intro-content"
        initial={{ opacity: 0, y: 18 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.58, ease: [0.22, 1, 0.36, 1] }}
      >
        <motion.h1
          initial={{ opacity: 0, y: 26, scale: 0.985 }}
          animate={{ opacity: 1, y: 0, scale: 1 }}
          transition={{ duration: 0.72, delay: 0.06, ease: [0.22, 1, 0.36, 1] }}
          className="hero-title hero-title-single"
        >
          나에게 "딱" 맞는 노트북을 추천 해드립니다!
        </motion.h1>

        <motion.div
          initial={{ opacity: 0, scale: 0.96, y: 18 }}
          animate={{ opacity: 1, scale: 1, y: 0 }}
          transition={{ duration: 0.64, delay: 0.2, ease: [0.22, 1, 0.36, 1] }}
          className="hero-device-stage"
        >
          <div className="laptop-fan fan-left-2" />
          <div className="laptop-fan fan-left-1" />
          <div className="laptop-fan fan-center">
            <span>SMART PICK</span>
          </div>
          <div className="laptop-fan fan-right-1" />
          <div className="laptop-fan fan-right-2" />
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 16 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.58, delay: 0.34, ease: [0.22, 1, 0.36, 1] }}
          className="intro-actions single-action"
        >
          <button type="button" className="primary-cta" onClick={onStart}>
            추천 받으러 가기
          </button>
        </motion.div>
      </motion.div>
    </section>
  );
}
