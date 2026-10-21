/* Apply before paint; preferences stay on this device. */
(()=>{try{const theme=localStorage.getItem('atlas-theme')||'light';if(['light','jade','blue','dark'].includes(theme))document.documentElement.dataset.theme=theme;document.documentElement.dataset.motion=localStorage.getItem('atlas-motion')||'on'}catch{}})();
