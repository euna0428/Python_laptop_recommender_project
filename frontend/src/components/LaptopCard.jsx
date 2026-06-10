import { useState } from 'react';
import { motion } from 'framer-motion';
import { formatWon } from '../utils/format.js';

function ScoreLine({ label, value, tone = 'cyan' }) {
  const safe = Math.max(0, Math.min(100, value));
  return (
    <div className="score-line">
      <span>{label}</span>
      <div><i className={tone} style={{ width: `${safe}%` }} /></div>
      <b>{safe}</b>
    </div>
  );
}

export default function LaptopCard({ laptop, index }) {
  const [flipped, setFlipped] = useState(false);
  const rankTone = index === 0 ? 'cyan' : index === 1 ? 'violet' : 'green';
  const priceScore = Math.max(10, Math.round(100 - (laptop.priceMidKrw / 4500000) * 100));
  const weightScore = Math.max(10, Math.round(100 - (laptop.weightKg / 3.2) * 100));
  const performanceScore = Math.max(10, Math.min(100, Math.round((laptop.cpuScore + laptop.gpuScore) * 12)));

  return (
    <motion.article
      className={`laptop-card rank-${index + 1}`}
      initial={{ opacity: 0, y: 34 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.55, delay: index * 0.12 }}
    >
      <div className={`flip-card ${flipped ? 'flipped' : ''}`} onClick={() => setFlipped(current => !current)} role="button" tabIndex={0}>
        <div className="card-face card-front">
          <div className="card-topline">
            <span className={`rank-badge ${rankTone}`}>#{laptop.rank} PICK</span>
            <span className="os-chip">{laptop.osType}</span>
          </div>
          <div className="laptop-image-wrap">
            <img src={laptop.imagePath} alt={`${laptop.brand} ${laptop.model}`} loading="lazy" />
          </div>
          <p className="brand-name">{laptop.brand}</p>
          <h3>{laptop.model}</h3>
          <div className="price-row">
            <strong>{laptop.priceLabel}</strong>
            <span>{laptop.weightKg}kg</span>
          </div>
          <div className="spec-pills">
            <span>{laptop.cpu}</span>
            <span>RAM {laptop.ramGb}GB</span>
            <span>{laptop.storageLabel}</span>
          </div>
          <div className="tap-hint">클릭하여 추천 근거 보기</div>
        </div>

        <div className="card-face card-back">
          <div className="back-header">
            <strong>{laptop.score}점</strong>
            <span>추천 점수</span>
          </div>
          <ScoreLine label="가격" value={priceScore} tone="green" />
          <ScoreLine label="휴대" value={weightScore} tone="cyan" />
          <ScoreLine label="성능" value={performanceScore} tone="violet" />
          <ul className="reason-list">
            {(laptop.reasons || []).slice(0, 5).map(reason => <li key={reason}>{reason}</li>)}
          </ul>
          <a href={laptop.modelSearchLink} target="_blank" rel="noreferrer" onClick={e => e.stopPropagation()} className="buy-link">
            모델 검색 링크 열기
          </a>
        </div>
      </div>
    </motion.article>
  );
}
