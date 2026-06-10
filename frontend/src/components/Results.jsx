import { motion } from 'framer-motion';
import LaptopCard from './LaptopCard.jsx';
import { formatWon, priorityLabel } from '../utils/format.js';

function CompareTable({ laptops }) {
  return (
    <div className="compare-wrap glass-panel">
      <div className="result-section-head">
        <p className="section-kicker">COMPARE</p>
        <h2>TOP 5 비교표</h2>
      </div>
      <div className="table-scroller">
        <table className="compare-table">
          <thead>
            <tr>
              <th>순위</th>
              <th>모델</th>
              <th>점수</th>
              <th>CPU</th>
              <th>RAM</th>
              <th>저장공간</th>
              <th>GPU</th>
              <th>가격</th>
              <th>무게</th>
              <th>OS</th>
            </tr>
          </thead>
          <tbody>
            {laptops.map(laptop => (
              <tr key={`${laptop.brand}-${laptop.model}`}>
                <td>#{laptop.rank}</td>
                <td>{laptop.brand} {laptop.model}</td>
                <td>{laptop.score}</td>
                <td>{laptop.cpu}</td>
                <td>{laptop.ramGb}GB</td>
                <td>{laptop.storageLabel}</td>
                <td>{laptop.gpu}</td>
                <td>{laptop.priceLabel}</td>
                <td>{laptop.weightKg}kg</td>
                <td>{laptop.osType}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default function Results({ result, onReset }) {
  const recommendations = result?.recommendations || [];
  const top = recommendations[0];
  const summary = result?.requestSummary || {};
  const member = result?.member || {};

  return (
    <section className="results-section screen-shell compact-shell">
      <motion.div
        initial={{ opacity: 0, y: 24 }}
        animate={{ opacity: 1, y: 0 }}
        className="result-hero glass-panel"
      >
        <div className="result-copy">
          <p className="section-kicker">RECOMMENDATION COMPLETE</p>
          <h1>{member.name || '사용자'}님을 위한 추천 결과</h1>
          <p>
            {summary.department} 기준으로 {formatWon(summary.budgetKrw)} 예산, {summary.priorities?.join(', ')} 우선순위를 반영했습니다.
            기존 추천 알고리즘의 학과 스펙·예산·성능·휴대성 점수를 API 응답으로 받아 화면에 표시합니다.
          </p>
          <div className="result-tags">
            <span>{summary.department}</span>
            <span>RAM {summary.minRamGb}GB 이상</span>
            <span>{summary.recommendedCpu}</span>
            <span>{summary.os}</span>
          </div>
        </div>
        {top && (
          <div className="top-pick-panel">
            <div className="top-image">
              <img src={top.imagePath} alt={`${top.brand} ${top.model}`} />
            </div>
            <div>
              <span className="rank-badge cyan">BEST PICK</span>
              <h2>{top.brand} {top.model}</h2>
              <strong>{top.score}점 · {top.priceLabel}</strong>
            </div>
          </div>
        )}
      </motion.div>

      {recommendations.length === 0 ? (
        <div className="empty-state glass-panel">
          <h2>조건에 맞는 후보가 없습니다</h2>
          <p>{result?.warning || 'OS 조건 또는 예산 범위를 넓혀 다시 시도해 주세요.'}</p>
          <button type="button" className="primary-cta small" onClick={onReset}>다시 입력하기</button>
        </div>
      ) : (
        <>
          <div className="result-section-head cards-head">
            <p className="section-kicker">TOP PICKS</p>
            <h2>추천 노트북 TOP {recommendations.length}</h2>
          </div>
          <div className="laptop-grid">
            {recommendations.map((laptop, index) => <LaptopCard key={`${laptop.brand}-${laptop.model}`} laptop={laptop} index={index} />)}
          </div>
          <CompareTable laptops={recommendations} />
          <div className="notice-box glass-panel">
            <h3>구매 전 확인 사항</h3>
            <ul>
              {(result.notice || []).map(item => <li key={item}>{item}</li>)}
              <li>실제 구매 전 모델 검색 링크에서 RAM, SSD, GPU, OS 옵션이 같은지 확인해야 합니다.</li>
            </ul>
          </div>
        </>
      )}

      <div className="bottom-actions">
        <button type="button" className="ghost-button" onClick={onReset}>처음부터 다시 추천받기</button>
      </div>
    </section>
  );
}
