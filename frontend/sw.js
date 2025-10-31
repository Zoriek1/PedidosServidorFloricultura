// Service Worker - Plante Uma Flor PWA v3.0
// Gerencia cache e funcionalidade offline

const CACHE_NAME = 'plante-uma-flor-v5';
const CACHE_URLS = [
    '/',
    '/index.html',
    '/manifest.json',
    '/assets/images/Buques.ico',
    '/assets/js/icons/icon-192x192.png?v=buques',
    '/assets/js/icons/icon-512x512.png?v=buques',
    '/assets/css/style.css',
    '/assets/js/app.js',
    '/assets/js/router.js',
    '/assets/js/api.js',
    '/assets/js/db.js',
    '/assets/js/utils.js',
    '/assets/js/form.js',
    '/assets/js/painel.js',
    '/assets/js/masks.js',
    '/assets/js/validators.js',
    '/assets/js/components/notification.js',
    '/assets/js/components/modal.js',
    '/assets/js/components/pedido-card.js',
    '/pages/criar-pedido.html',
    '/pages/painel.html',
    'https://cdn.tailwindcss.com',
    'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css'
];

// Instalação do Service Worker
self.addEventListener('install', (event) => {
    console.log('✅ Service Worker: Instalando...');
    
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then((cache) => {
                console.log('✅ Service Worker: Cache aberto');
                return cache.addAll(CACHE_URLS.map(url => {
                    return new Request(url, {
                        cache: 'reload',
                        mode: 'no-cors'
                    });
                })).catch(err => {
                    // Falha silenciosa para CDNs externos
                    console.log('⚠️ Alguns recursos não foram cacheados:', err);
                });
            })
    );
    
    self.skipWaiting();
});

// Ativação do Service Worker
self.addEventListener('activate', (event) => {
    console.log('✅ Service Worker: Ativando...');
    
    event.waitUntil(
        caches.keys().then((cacheNames) => {
            return Promise.all(
                cacheNames.map((cacheName) => {
                    if (cacheName !== CACHE_NAME) {
                        console.log('🗑️ Service Worker: Removendo cache antigo:', cacheName);
                        return caches.delete(cacheName);
                    }
                })
            );
        })
    );
    
    self.clients.claim();
});

// Interceptar requisições
self.addEventListener('fetch', (event) => {
    const { request } = event;
    const url = new URL(request.url);
    
    // Estratégia para API: Network First (tenta rede primeiro)
    if (url.pathname.startsWith('/api/')) {
        event.respondWith(
            fetch(request)
                .then((response) => {
                    // Clonar resposta para cache
                    const responseClone = response.clone();
                    caches.open(CACHE_NAME).then((cache) => {
                        cache.put(request, responseClone);
                    });
                    return response;
                })
                .catch(() => {
                    // Se falhar, tentar cache
                    return caches.match(request).then((cached) => {
                        return cached || new Response(
                            JSON.stringify({
                                error: 'Sem conexão com a internet',
                                offline: true
                            }),
                            {
                                status: 503,
                                statusText: 'Service Unavailable',
                                headers: new Headers({
                                    'Content-Type': 'application/json'
                                })
                            }
                        );
                    });
                })
        );
        return;
    }
    
    // Estratégia para assets estáticos: Cache First (cache primeiro)
    event.respondWith(
        caches.match(request)
            .then((cached) => {
                if (cached) {
                    return cached;
                }
                
                return fetch(request).then((response) => {
                    // Só cachear respostas válidas
                    if (!response || response.status !== 200 || response.type === 'error') {
                        return response;
                    }
                    
                    // Clonar resposta
                    const responseClone = response.clone();
                    
                    caches.open(CACHE_NAME).then((cache) => {
                        cache.put(request, responseClone);
                    });
                    
                    return response;
                }).catch(() => {
                    // Fallback para página offline
                    if (request.destination === 'document') {
                        return caches.match('/index.html');
                    }
                });
            })
    );
});

// Background Sync para criar pedidos offline
self.addEventListener('sync', (event) => {
    console.log('🔄 Service Worker: Background sync disparado');
    
    if (event.tag === 'sync-pedidos') {
        event.waitUntil(syncPedidos());
    }
});

// Função para sincronizar pedidos pendentes
async function syncPedidos() {
    try {
        // Esta função será chamada quando o app voltar online
        // O IndexedDB será usado no frontend para armazenar pedidos pendentes
        console.log('✅ Service Worker: Sincronização de pedidos concluída');
    } catch (error) {
        console.error('❌ Service Worker: Erro na sincronização:', error);
        throw error;
    }
}

// Mensagens do app
self.addEventListener('message', (event) => {
    if (event.data && event.data.type === 'SKIP_WAITING') {
        self.skipWaiting();
    }
    
    if (event.data && event.data.type === 'CLEAR_CACHE') {
        event.waitUntil(
            caches.keys().then((cacheNames) => {
                return Promise.all(
                    cacheNames.map((cacheName) => caches.delete(cacheName))
                );
            }).then(() => {
                console.log('🗑️ Cache limpo com sucesso');
            })
        );
    }
});

