const CACHE_NAME = 'resqchain-ui-v4';
const MAP_CACHE = 'leaflet-tiles-v1';

const ASSETS = [
  './',
  './new_civ.html',
  './shelter.html',
  './tailwind-engine.js',
  './leaflet.js',
  './leaflet.css',
  './leaflet.markercluster.js',
  './leaflet-routing-machine.js',
  './leaflet-heat.js',
  './css/MarkerCluster.css',         
  './css/MarkerCluster.Default.css', 
  './css/leaflet-routing-machine.css' 
];

self.addEventListener('install', event => {
  event.waitUntil(caches.open(CACHE_NAME).then(cache => cache.addAll(ASSETS)));
});

self.addEventListener('fetch', event => {
  const url = event.request.url;

  // MAP TILES: Cache-First Strategy
  if (url.includes('tile.openstreetmap.org')) {
    event.respondWith(
      caches.open(MAP_CACHE).then(cache => {
        return cache.match(event.request).then(response => {
          // Return cached tile immediately if we have it
          if (response) return response;
          // Otherwise fetch and save for next time
          return fetch(event.request).then(netRes => {
            cache.put(event.request, netRes.clone());
            return netRes;
          });
        });
      })
    );
  } else {
    // UI ASSETS: Cache-then-Network
    event.respondWith(
      caches.match(event.request).then(res => res || fetch(event.request))
    );
  }
});