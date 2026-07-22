// Utility for managing browser push notifications

export const requestNotificationPermission = async () => {
  if (!('Notification' in window)) {
    console.warn('This browser does not support desktop notification');
    return false;
  }
  
  if (Notification.permission === 'granted') {
    return true;
  }
  
  if (Notification.permission !== 'denied') {
    const permission = await Notification.requestPermission();
    return permission === 'granted';
  }
  
  return false;
};

export const triggerLocalPushNotification = (title, message, severity) => {
  if (!('Notification' in window)) return;

  if (Notification.permission === 'granted') {
    // If Service Workers are supported and registered, use them for rich notifications
    if ('serviceWorker' in navigator && navigator.serviceWorker.ready) {
      navigator.serviceWorker.ready.then((registration) => {
        registration.showNotification(title, {
          body: message,
          icon: '/vite.svg',
          requireInteraction: severity === 'HIGH',
          vibrate: severity === 'HIGH' ? [200, 100, 200, 100, 200] : [100, 50, 100],
        });
      });
    } else {
      // Fallback to basic Notification API
      new Notification(title, {
        body: message,
        requireInteraction: severity === 'HIGH'
      });
    }
  }
};

// Register Service Worker on boot
export const registerServiceWorker = () => {
  if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
      navigator.serviceWorker.register('/sw.js').then((registration) => {
        console.log('ServiceWorker registration successful with scope: ', registration.scope);
      }).catch((err) => {
        console.log('ServiceWorker registration failed: ', err);
      });
    });
  }
};
