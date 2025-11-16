/**
 * Service Worker per TauroBot 3.0 PWA
 * Gestisce cache e funzionalità offline
 */

const CACHE_NAME = 'taurobot-v3.0.0-garage';
const urlsToCache = [
  '/',
  '/index.html',
  '/manifest.json',
  '/pwa/login.html',
  '/pwa/dashboard.html',
  '/pwa/garage.html',
  '/pwa/gateway.html',
  '/android/admin.html',
  '/android/terminal.html',
  '/icons/icon-72x72.svg',
  '/icons/icon-192x192.svg',
  '/icons/icon-512x512.svg',
  '/hybrid_security/netalis/netalis_sandbox.jsx'
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

// Intercettazione richieste (strategia Cache First)
self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request)
      .then(response => {
        // Cache hit - ritorna la risposta dalla cache
        if (response) {
          return response;
        }

        // Clone della richiesta
        const fetchRequest = event.request.clone();

        return fetch(fetchRequest).then(response => {
          // Verifica che la risposta sia valida
          if (!response || response.status !== 200 || response.type !== 'basic') {
            return response;
          }

          // Clone della risposta
          const responseToCache = response.clone();

          caches.open(CACHE_NAME).then(cache => {
            cache.put(event.request, responseToCache);
          });

          return response;
        }).catch(() => {
          // Fallback offline - redirect to login
          return caches.match('/pwa/login.html');
        });
      })
  );
});

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
