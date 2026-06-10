import { AnimatePresence, motion } from 'framer-motion';
import { useMemo, useState } from 'react';
import { formatWon, priorityLabel, osLabel } from '../utils/format.js';

const steps = ['회원 정보', '학과 선택', '예산 설정', '추천 기준', '운영체제'];
const priorityOptions = [
  { id: 'price', title: '가격', icon: '💰', desc: '예산 안에서 가성비를 우선합니다.' },
  { id: 'performance', title: '성능', icon: '🚀', desc: 'CPU·GPU·RAM 점수를 강하게 반영합니다.' },
  { id: 'weight', title: '휴대성', icon: '⚡', desc: '강의실 이동과 통학 무게를 고려합니다.' },
];
const osOptions = [
  { id: 'windows', title: 'Windows', icon: '🪟', desc: '대부분의 전공 소프트웨어 호환' },
  { id: 'macos', title: 'macOS', icon: '🍎', desc: '디자인·영상·개발 환경에 강점' },
  { id: 'freedos', title: 'FreeDOS', icon: '🛠️', desc: '직접 OS 설치 가능 제품만 탐색' },
  { id: 'any', title: '상관없음', icon: '🌐', desc: '모든 OS 후보를 함께 비교' },
];

function SelectCard({ active, icon, title, desc, onClick }) {
  return (
    <button type="button" className={`select-card ${active ? 'active' : ''}`} onClick={onClick}>
      <span className="select-icon">{icon}</span>
      <strong>{title}</strong>
      <small>{desc}</small>
      {active && <span className="checkmark">✓</span>}
    </button>
  );
}

export default function Wizard({ departments, onSubmit, loading }) {
  const [step, setStep] = useState(0);
  const [form, setForm] = useState({
    member: { name: '', studentId: '', grade: '' },
    department: '',
    budget: 1500000,
    priorities: ['price'],
    os: 'any',
    canInstallWindows: false,
    limit: 5,
  });

  const selectedDepartment = useMemo(
    () => departments.find(item => item.department === form.department),
    [departments, form.department],
  );

  const canGoNext = () => {
    if (step === 0) return form.member.name.trim().length > 0;
    if (step === 1) return Boolean(form.department);
    if (step === 2) return Number(form.budget) >= 300000;
    if (step === 3) return form.priorities.length > 0;
    return true;
  };

  const updateMember = (key, value) => {
    setForm(current => ({ ...current, member: { ...current.member, [key]: value } }));
  };

  const togglePriority = priority => {
    setForm(current => {
      const exists = current.priorities.includes(priority);
      const next = exists
        ? current.priorities.filter(item => item !== priority)
        : [...current.priorities, priority];
      return { ...current, priorities: next.length ? next : ['price'] };
    });
  };

  const goNext = () => {
    if (!canGoNext()) return;
    if (step === steps.length - 1) onSubmit(form);
    else setStep(current => current + 1);
  };

  return (
    <section className="wizard-section screen-shell compact-shell">
      <div className="wizard-shell glass-panel">
        <div className="wizard-progress">
          {steps.map((label, index) => (
            <div key={label} className={`wizard-step ${index <= step ? 'active' : ''}`}>
              <span>{index + 1}</span>
              <small>{label}</small>
            </div>
          ))}
        </div>

        <AnimatePresence mode="wait">
          {step === 0 && (
            <motion.div key="member" className="step-body" initial={{ opacity: 0, y: 22 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -22 }}>
              <p className="section-kicker">STEP 01</p>
              <h2>추천 결과에 표시할 회원 정보를 입력하세요</h2>
              <p className="section-desc">로그인 기능을 붙이기 전 단계에서는 입력값을 API 요청에 함께 보내는 방식으로 구성했습니다.</p>
              <div className="form-grid">
                <label className="form-field">
                  <span>이름 또는 닉네임 *</span>
                  <input value={form.member.name} onChange={e => updateMember('name', e.target.value)} placeholder="예: 이은아" />
                </label>
                <label className="form-field">
                  <span>학번 또는 구분값</span>
                  <input value={form.member.studentId} onChange={e => updateMember('studentId', e.target.value)} placeholder="예: 20261234" />
                </label>
                <label className="form-field">
                  <span>학년</span>
                  <select value={form.member.grade} onChange={e => updateMember('grade', e.target.value)}>
                    <option value="">선택 안 함</option>
                    <option value="1학년">1학년</option>
                    <option value="2학년">2학년</option>
                    <option value="3학년">3학년</option>
                    <option value="4학년">4학년</option>
                  </select>
                </label>
              </div>
            </motion.div>
          )}

          {step === 1 && (
            <motion.div key="department" className="step-body" initial={{ opacity: 0, y: 22 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -22 }}>
              <p className="section-kicker">STEP 02</p>
              <h2>학과를 선택하세요</h2>
              <p className="section-desc">학과별 권장 CPU, RAM, GPU, 예산 기준을 추천 점수에 반영합니다.</p>
              <div className="department-grid">
                {departments.map((dept, index) => (
                  <SelectCard
                    key={dept.department}
                    active={form.department === dept.department}
                    icon={['📚', '📊', '💻', '🎨', '🏗️', '🎬', '🩺', '🧪'][index] || '🎓'}
                    title={dept.department}
                    desc={dept.mainUsage}
                    onClick={() => setForm(current => ({ ...current, department: dept.department, budget: dept.avgBudgetKrw }))}
                  />
                ))}
              </div>
            </motion.div>
          )}

          {step === 2 && (
            <motion.div key="budget" className="step-body" initial={{ opacity: 0, y: 22 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -22 }}>
              <p className="section-kicker">STEP 03</p>
              <h2>구매 가능한 최대 예산을 설정하세요</h2>
              <p className="section-desc">가격을 우선순위로 선택하지 않아도 입력 예산보다 과도하게 높은 제품은 감점 처리됩니다.</p>
              <div className="budget-board">
                <strong>{formatWon(form.budget)}</strong>
                <span>{Number(form.budget).toLocaleString()}원</span>
              </div>
              <input
                className="budget-range"
                type="range"
                min="500000"
                max="4500000"
                step="50000"
                value={form.budget}
                onChange={e => setForm(current => ({ ...current, budget: Number(e.target.value) }))}
              />
              <div className="preset-row">
                {[700000, 1000000, 1500000, 2000000, 2500000, 3500000].map(value => (
                  <button key={value} type="button" className={form.budget === value ? 'active' : ''} onClick={() => setForm(current => ({ ...current, budget: value }))}>{formatWon(value)}</button>
                ))}
              </div>
              {selectedDepartment && (
                <div className="dept-spec-box">
                  <span>선택 학과 기준</span>
                  <b>평균 예산 {formatWon(selectedDepartment.avgBudgetKrw)} · RAM {selectedDepartment.minRamGb}GB 이상 · {selectedDepartment.recommendedCpu}</b>
                </div>
              )}
            </motion.div>
          )}

          {step === 3 && (
            <motion.div key="priority" className="step-body" initial={{ opacity: 0, y: 22 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -22 }}>
              <p className="section-kicker">STEP 04</p>
              <h2>중요하게 보는 기준을 선택하세요</h2>
              <p className="section-desc">두 개 이상 선택할 수 있습니다. 선택한 기준은 추천 점수의 가중치로 반영됩니다.</p>
              <div className="triple-grid">
                {priorityOptions.map(option => (
                  <SelectCard
                    key={option.id}
                    active={form.priorities.includes(option.id)}
                    icon={option.icon}
                    title={option.title}
                    desc={option.desc}
                    onClick={() => togglePriority(option.id)}
                  />
                ))}
              </div>
            </motion.div>
          )}

          {step === 4 && (
            <motion.div key="os" className="step-body" initial={{ opacity: 0, y: 22 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -22 }}>
              <p className="section-kicker">STEP 05</p>
              <h2>운영체제를 선택하세요</h2>
              <p className="section-desc">Windows 직접 설치가 가능하면 FreeDOS 제품도 Windows 후보에 포함할 수 있습니다.</p>
              <div className="os-grid">
                {osOptions.map(option => (
                  <SelectCard
                    key={option.id}
                    active={form.os === option.id}
                    icon={option.icon}
                    title={option.title}
                    desc={option.desc}
                    onClick={() => setForm(current => ({ ...current, os: option.id }))}
                  />
                ))}
              </div>
              {form.os === 'windows' && (
                <label className="install-toggle">
                  <input type="checkbox" checked={form.canInstallWindows} onChange={e => setForm(current => ({ ...current, canInstallWindows: e.target.checked }))} />
                  <span>FreeDOS 제품에 Windows를 직접 설치할 수 있습니다.</span>
                </label>
              )}
              <div className="submit-summary">
                <span>{form.member.name || '회원'} · {form.department || '학과 미선택'}</span>
                <b>{formatWon(form.budget)} · {form.priorities.map(priorityLabel).join(', ')} · {osLabel(form.os)}</b>
              </div>
            </motion.div>
          )}
        </AnimatePresence>

        <div className="wizard-actions">
          <button type="button" className="ghost-button" disabled={step === 0 || loading} onClick={() => setStep(current => current - 1)}>이전</button>
          <button type="button" className="primary-cta small" disabled={!canGoNext() || loading} onClick={goNext}>
            {step === steps.length - 1 ? (loading ? '분석 중...' : '추천 결과 보기') : '다음'}
          </button>
        </div>
      </div>
    </section>
  );
}
