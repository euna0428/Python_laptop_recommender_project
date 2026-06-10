const API_BASE = import.meta.env.VITE_API_BASE_URL || '';

async function request(path, options = {}) {
  const response = await fetch(`${API_BASE}${path}`, {
    headers: {
      'Content-Type': 'application/json',
      ...(options.headers || {}),
    },
    ...options,
  });

  if (!response.ok) {
    let message = '요청 처리 중 오류가 발생했습니다.';
    try {
      const data = await response.json();
      message = data.detail || message;
    } catch (_) {
      message = response.statusText || message;
    }
    throw new Error(message);
  }

  return response.json();
}

export const api = {
  getDepartments: () => request('/api/departments'),
  getLaptops: () => request('/api/laptops'),
  recommend: payload => request('/api/recommend', {
    method: 'POST',
    body: JSON.stringify(payload),
  }),
};
