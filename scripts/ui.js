/* ════════════════════════════════════════════════════════════════
   FORMAZIONE DIGITALE — ui.js
   Componenti UI globali auto-iniettati nel DOM.
   Includere con: <script src="/scripts/ui.js" defer></script>
════════════════════════════════════════════════════════════════ */

(function () {
  'use strict';

  // ── TORNA SU ────────────────────────────────────────────────────

  const CSS = `
    #back-to-top {
      position: fixed;
      bottom: 2rem;
      right: 2rem;
      z-index: 400;
      width: 44px;
      height: 44px;
      border-radius: 50%;
      background: #1F4E79;
      color: #fff;
      border: none;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      box-shadow: 0 4px 16px rgba(31,78,121,.35);
      opacity: 0;
      transform: translateY(12px);
      transition: opacity .25s ease, transform .25s ease, background .2s ease;
      pointer-events: none;
    }
    #back-to-top.visible {
      opacity: 1;
      transform: translateY(0);
      pointer-events: all;
    }
    #back-to-top:hover {
      background: #2E75B6;
      box-shadow: 0 6px 24px rgba(31,78,121,.45);
    }
    #back-to-top svg {
      width: 20px;
      height: 20px;
      stroke: #fff;
      stroke-width: 2.5;
      fill: none;
      stroke-linecap: round;
      stroke-linejoin: round;
    }
    @media (max-width: 600px) {
      #back-to-top {
        bottom: 1.25rem;
        right: 1.25rem;
        width: 40px;
        height: 40px;
      }
    }
  `;

  const HTML = `
    <button id="back-to-top" aria-label="Torna in cima alla pagina">
      <svg viewBox="0 0 24 24">
        <polyline points="18 15 12 9 6 15"/>
      </svg>
    </button>
  `;

  function init() {
    // Inietta CSS
    const style = document.createElement('style');
    style.textContent = CSS;
    document.head.appendChild(style);

    // Inietta HTML
    document.body.insertAdjacentHTML('beforeend', HTML);

    const btn = document.getElementById('back-to-top');
    if (!btn) return;

    // Mostra/nascondi in base allo scroll
    let ticking = false;
    window.addEventListener('scroll', function () {
      if (!ticking) {
        requestAnimationFrame(function () {
          if (window.scrollY > 320) {
            btn.classList.add('visible');
          } else {
            btn.classList.remove('visible');
          }
          ticking = false;
        });
        ticking = true;
      }
    }, { passive: true });

    // Click — scroll to top
    btn.addEventListener('click', function () {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  }

  // Aspetta DOM ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

})();
