import { useEffect, useRef } from 'react';

function moveElement(element, x, y, opacity = '1') {
  if (!element) return;
  element.style.transform = `translate3d(${x}px, ${y}px, 0) translate(-50%, -50%)`;
  element.style.opacity = opacity;
}

export default function CursorGlow() {
  const glowRef = useRef(null);
  const ringRef = useRef(null);
  const dotRef = useRef(null);

  useEffect(() => {
    const hideCursor = () => {
      moveElement(glowRef.current, -240, -240, '0');
      moveElement(ringRef.current, -240, -240, '0');
      moveElement(dotRef.current, -240, -240, '0');
    };

    const handleMove = event => {
      const { clientX, clientY } = event;

      moveElement(dotRef.current, clientX, clientY);
      moveElement(ringRef.current, clientX, clientY);
      moveElement(glowRef.current, clientX, clientY);
    };

    const handleDown = () => {
      ringRef.current?.classList.add('is-pressed');
      dotRef.current?.classList.add('is-pressed');
      glowRef.current?.classList.add('is-pressed');
    };

    const handleUp = () => {
      ringRef.current?.classList.remove('is-pressed');
      dotRef.current?.classList.remove('is-pressed');
      glowRef.current?.classList.remove('is-pressed');
    };

    window.addEventListener('pointermove', handleMove, { passive: true });
    window.addEventListener('pointerdown', handleDown, { passive: true });
    window.addEventListener('pointerup', handleUp, { passive: true });
    document.documentElement.addEventListener('mouseleave', hideCursor);

    hideCursor();

    return () => {
      window.removeEventListener('pointermove', handleMove);
      window.removeEventListener('pointerdown', handleDown);
      window.removeEventListener('pointerup', handleUp);
      document.documentElement.removeEventListener('mouseleave', hideCursor);
    };
  }, []);

  return (
    <>
      <div ref={glowRef} className="cursor-glow" aria-hidden="true" />
      <div ref={ringRef} className="cursor-ring" aria-hidden="true" />
      <div ref={dotRef} className="cursor-dot" aria-hidden="true" />
    </>
  );
}
