/**
 * Service Worker per TauroBot 3.0 PWA
 * Gestisce cache e funzionalità offline
 */

const CACHE_NAME = 'taurobot-v1.0.0';
const urlsToCache = [
  '/',
  '/index.html',
  '/manifest.json',
  '/icons/icon-192x192.png',
  '/icons/icon-512x512.png'
];

// Installazione Service Worker
self.addEventListener('install', event => {
  console.log('[ServiceWorker] Installing...');
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => {
        console.log('[ServiceWorker] Caching app shell');
        return cache.addAll(urlsToCache);
      })
      .then(() => self.skipWaiting())
  );
});

// Attivazione Service Worker
self.addEventListener('activate', event => {
  console.log('[ServiceWorker] Activating...');
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames.map(cacheName => {
          if (cacheName !== CACHE_NAME) {
            console.log('[ServiceWorker] Removing old cache:', cacheName);
            return caches.delete(cacheName);
          }
        })
      );
    }).then(() => self.clients.claim())
  );
});

// Intercettazione richieste (strategia Cache First con timeout)
self.addEventListener('fetch', event => {
  const { request } = event;
  
  // Skip non-GET requests
  if (request.method !== 'GET') {
    return;
  }
  
  event.respondWith(
    caches.match(request)
      .then(cachedResponse => {
        // Cache hit - ritorna la risposta dalla cache
        if (cachedResponse) {
          // Stale-while-revalidate: return cache immediately, update in background
          // Use event.waitUntil to prevent fetch from being cancelled
          event.waitUntil(
            fetch(request).then(response => {
              if (response && response.status === 200 && response.type === 'basic') {
                const responseToCache = response.clone();
                return caches.open(CACHE_NAME).then(cache => {
                  return cache.put(request, responseToCache);
                });
              }
            }).catch(() => {}) // Ignore background update errors
          );
          
          return cachedResponse;
        }

        // No cache - fetch with timeout
        return fetchWithTimeout(request, 5000)
          .then(response => {
            // Verifica che la risposta sia valida
            if (!response || response.status !== 200 || response.type !== 'basic') {
              return response;
            }

            // Clone e cache della risposta
            const responseToCache = response.clone();
            caches.open(CACHE_NAME).then(cache => {
              cache.put(request, responseToCache);
            });

            return response;
          }).catch(() => {
            // Fallback offline
            return caches.match('/index.html');
          });
      })
  );
});

// Helper: fetch with timeout
function fetchWithTimeout(request, timeout = 5000) {
  return Promise.race([
    fetch(request),
    new Promise((_, reject) =>
      setTimeout(() => reject(new Error('Timeout')), timeout)
    )
  ]);
}

// Gestione messaggi dal client
self.addEventListener('message', event => {
  if (event.data && event.data.type === 'SKIP_WAITING') {
    self.skipWaiting();
  }
});

// Push notifications (per future estensioni)
self.addEventListener('push', event => {
  const options = {
    body: event.data ? event.data.text() : 'Nuovo messaggio da TauroBot',
    icon: '/icons/icon-192x192.png',
    badge: '/icons/icon-72x72.png',
    vibrate: [200, 100, 200],
    tag: 'taurobot-notification'
  };

  event.waitUntil(
    self.registration.showNotification('TauroBot 3.0', options)
  );
});

// Gestione click su notifiche
self.addEventListener('notificationclick', event => {
  event.notification.close();
  event.waitUntil(
    clients.openWindow('/')
  );
});
