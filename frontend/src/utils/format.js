export function formatWon(value) {
  const numeric = Number(value || 0);
  if (numeric >= 100000000) return `${(numeric / 100000000).toFixed(1)}억원`;
  return `${Math.round(numeric / 10000).toLocaleString()}만원`;
}

export function formatFullWon(value) {
  return `${Number(value || 0).toLocaleString()}원`;
}

export function priorityLabel(priority) {
  return {
    price: '가격',
    performance: '성능',
    weight: '휴대성',
  }[priority] || priority;
}

export function osLabel(os) {
  return {
    windows: 'Windows',
    macos: 'macOS',
    freedos: 'FreeDOS',
    any: '상관없음',
  }[os] || os;
}
