const CACHE_VERSION = 'v1';
const CORE_CACHE = `quiz-core-${CACHE_VERSION}`;
const QUESTIONS_CACHE = `quiz-questions-${CACHE_VERSION}`;
const CORE_ASSETS = [
  './',
  'index.html',
  'questions.json'
];
self.addEventListener('install', e => {
  self.skipWaiting();
  e.waitUntil(
    caches.open(CORE_CACHE).then(c => c.addAll(CORE_ASSETS)).catch(()=>{})
  );
});
self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys().then(keys => Promise.all(
      keys.filter(k => ![CORE_CACHE, QUESTIONS_CACHE].includes(k)).map(k => caches.delete(k))
    )).then(()=>self.clients.claim())
  );
});
self.addEventListener('fetch', e => {
  const url = new URL(e.request.url);
  if (url.origin === location.origin) {
    if (url.pathname.endsWith('questions.json')) {
      e.respondWith(
        caches.open(QUESTIONS_CACHE).then(async c => {
          try {
            const net = await fetch(e.request);
            c.put(e.request, net.clone());
            return net;
          } catch(err) {
            const cached = await c.match(e.request);
            if (cached) return cached;
            throw err;
          }
        })
      );
      return;
    }
    if (url.pathname === '/' || url.pathname.endsWith('.html')) {
      e.respondWith(
        caches.match('index.html').then(cached => cached || fetch(e.request))
      );
      return;
    }
  }
  
  e.respondWith(
    fetch(e.request).catch(()=>caches.match(e.request))
  );
});
