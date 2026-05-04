// ════════════════════════════════════════════════════════════════
//  FORMAZIONE DIGITALE — Service Worker  v1
//  Incrementa CACHE_VERSION ad ogni deploy significativo
//  per forzare l'aggiornamento della cache su tutti i client.
// ════════════════════════════════════════════════════════════════

const CACHE_VERSION = 'fd-v1.2';

// Risorse da precachare all'installazione (shell dell'app)
const PRECACHE = [
  '/',
  '/index.html',
  '/css/shared.css',
  '/manifest.json',
  '/mappa.html',
  '/404.html',
  '/img/formazione-digitale-logo.png',
];

// ── INSTALL — precache shell ─────────────────────────────────────
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_VERSION)
      .then(cache => cache.addAll(PRECACHE))
      .then(() => self.skipWaiting())
  );
});

// ── ACTIVATE — rimuovi cache vecchie ────────────────────────────
self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(keys =>
      Promise.all(
        keys
          .filter(key => key !== CACHE_VERSION)
          .map(key => caches.delete(key))
      )
    ).then(() => self.clients.claim())
  );
});

// ── FETCH — strategia per tipo di risorsa ───────────────────────
self.addEventListener('fetch', event => {
  const { request } = event;
  const url = new URL(request.url);

  // Ignora richieste non GET e domini esterni (GoatCounter, font Google, ecc.)
  if (request.method !== 'GET') return;
  if (url.origin !== location.origin) return;

  // Cache First per CSS, font, immagini, JSON statici
  if (
    url.pathname.startsWith('/css/') ||
    url.pathname.startsWith('/img/') ||
    url.pathname.endsWith('.css') ||
    url.pathname.endsWith('.png') ||
    url.pathname.endsWith('.jpg') ||
    url.pathname.endsWith('.svg') ||
    url.pathname.endsWith('.webp')
  ) {
    event.respondWith(cacheFirst(request));
    return;
  }

  // Network First per HTML e JSON (contenuto aggiornabile)
  event.respondWith(networkFirst(request));
});

// ── STRATEGIE ────────────────────────────────────────────────────

async function cacheFirst(request) {
  const cached = await caches.match(request);
  if (cached) return cached;
  try {
    const response = await fetch(request);
    if (response.ok) {
      const cache = await caches.open(CACHE_VERSION);
      cache.put(request, response.clone());
    }
    return response;
  } catch {
    return new Response('Risorsa non disponibile offline.', { status: 503 });
  }
}

async function networkFirst(request) {
  try {
    const response = await fetch(request);
    if (response.ok) {
      const cache = await caches.open(CACHE_VERSION);
      cache.put(request, response.clone());
    }
    return response;
  } catch {
    const cached = await caches.match(request);
    if (cached) return cached;
    // Fallback alla homepage se la pagina non è in cache
    const fallback = await caches.match('/');
    return fallback || new Response('Offline — risorsa non disponibile.', { status: 503 });
  }
}
