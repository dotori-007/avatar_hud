(function () {
  // DOM Elements
  const avatarWrapper = document.getElementById('avatar-wrapper');
  const avatarImg = document.getElementById('avatar-img');
  const speechBubble = document.getElementById('speech-bubble');
  const statusBadge = document.getElementById('status-badge');
  const statusText = document.getElementById('status-text');
  const stepBadge = document.getElementById('step-badge');
  const elapsedTime = document.getElementById('elapsed-time');
  const bubbleText = document.getElementById('bubble-text');
  const btnSettings = document.getElementById('btn-settings');
  const btnChangeAvatar = document.getElementById('btn-change-avatar');
  const btnScaleUp = document.getElementById('btn-scale-up');
  const btnScaleDown = document.getElementById('btn-scale-down');
  const avatarFileInput = document.getElementById('avatar-file-input');

  let currentScale = 1.0;
  let autoHideTimer = null;

  // Dynamic Speech Bubble Positioning
  // Places the speech bubble directly above the top edge of the avatar character
  function updateBubblePosition() {
    if (!avatarImg || !speechBubble) return;
    const rect = avatarImg.getBoundingClientRect();
    if (!rect || rect.height === 0) return;

    // Distance from the bottom of viewport to the top edge of avatar image
    const avatarTopFromBottom = window.innerHeight - rect.top;
    const bubbleHeight = speechBubble.offsetHeight || 80;
    
    // Clamp so bubble never overflows outside the top or bottom of the window
    const maxBottom = window.innerHeight - bubbleHeight - 12;
    const minBottom = 16;
    const targetBottom = Math.max(minBottom, Math.min(avatarTopFromBottom + 6, maxBottom));

    speechBubble.style.top = 'auto';
    speechBubble.style.bottom = `${Math.round(targetBottom)}px`;
  }

  // 1. Scale Avatar
  function setScale(scale) {
    currentScale = Math.min(2.0, Math.max(0.5, scale));
    avatarImg.style.transform = `scale(${currentScale})`;
    avatarImg.style.transformOrigin = 'bottom center';
    requestAnimationFrame(updateBubblePosition);
  }

  avatarImg.addEventListener('load', () => {
    requestAnimationFrame(updateBubblePosition);
  });

  window.addEventListener('resize', () => {
    requestAnimationFrame(updateBubblePosition);
  });

  btnScaleUp.addEventListener('click', (e) => {
    e.stopPropagation();
    setScale(currentScale + 0.1);
  });

  btnScaleDown.addEventListener('click', (e) => {
    e.stopPropagation();
    setScale(currentScale - 0.1);
  });

  // Mouse wheel on avatar scales image
  avatarWrapper.addEventListener('wheel', (e) => {
    e.preventDefault();
    const delta = e.deltaY < 0 ? 0.05 : -0.05;
    setScale(currentScale + delta);
  }, { passive: false });

  // 2. Open Settings Window
  function openSettings() {
    fetch('/api/open_settings', { method: 'POST' }).catch(console.warn);
  }

  if (btnSettings) {
    btnSettings.addEventListener('click', (e) => {
      e.stopPropagation();
      openSettings();
    });
  }

  // Right-click on character opens settings
  avatarWrapper.addEventListener('contextmenu', (e) => {
    e.preventDefault();
    openSettings();
  });

  // 3. Quick Change Avatar File from hover camera icon
  btnChangeAvatar.addEventListener('click', (e) => {
    e.stopPropagation();
    avatarFileInput.click();
  });

  avatarFileInput.addEventListener('change', (e) => {
    const file = e.target.files[0];
    if (!file) return;

    const isImage = file.type.startsWith('image/') || /\.(png|webp|jpe?g|gif|bmp|svg|avif|tiff?|ico)$/i.test(file.name);
    if (!isImage) {
      alert('이미지 파일(PNG, WebP, JPEG, GIF, BMP, SVG, AVIF, TIFF, ICO 등)만 선택할 수 있습니다.');
      return;
    }

    const reader = new FileReader();
    reader.onload = (event) => {
      const dataUrl = event.target.result;
      avatarImg.src = dataUrl;

      // Save to server config and notify all
      fetch('/api/config', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          avatar_image: dataUrl,
          avatar_name: file.name
        })
      }).catch(console.warn);
    };
    reader.readAsDataURL(file);
  });

  // 4. Update Status UI
  function updateStatus(data) {
    const status = data.status || 'idle';
    const title = data.title || (status === 'working' ? '작업 수행 중...' : status === 'done' ? '작업 완료!' : '대기 중');
    const message = data.message || '';
    const step = data.step || '';
    const elapsed = data.elapsed != null ? `${data.elapsed}초` : '';

    // Class update for status
    speechBubble.className = `speech-bubble show status-${status}`;

    // Status map
    const statusMap = {
      working: '작업 중',
      done: '완료됨',
      error: '오류 발생',
      idle: '대기 중'
    };
    statusText.textContent = statusMap[status] || status;

    // Step badge
    if (step) {
      stepBadge.style.display = 'inline-block';
      stepBadge.textContent = step;
    } else {
      stepBadge.style.display = 'none';
    }

    // Elapsed badge
    if (elapsed) {
      elapsedTime.style.display = 'inline-block';
      elapsedTime.textContent = elapsed;
    } else {
      elapsedTime.style.display = 'none';
    }

    // Compose text
    let displayText = '';
    if (title && message) {
      displayText = `${title}\n${message}`;
    } else {
      displayText = title || message || 'AvatarHUD 준비 완료!';
    }

    bubbleText.textContent = displayText;

    // Trigger bounce animation
    speechBubble.classList.remove('show');
    void speechBubble.offsetWidth; // Force reflow
    speechBubble.classList.add('show');

    // Recalculate speech bubble position to sit directly above avatar head
    requestAnimationFrame(updateBubblePosition);
  }

  // 5. Real-time Server-Sent Events (SSE) Connection
  function connectSSE() {
    const eventSource = new EventSource('/api/stream');

    eventSource.onopen = () => {
      console.log('[AvatarHUD] SSE stream connected.');
    };

    eventSource.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        
        // Handle real-time config updates (e.g. from settings window)
        if (data.type === 'config' && data.config) {
          if (data.config.avatar_image) {
            avatarImg.src = data.config.avatar_image;
          }
          if (data.config.scale != null) {
            setScale(data.config.scale);
          }
          return;
        }

        updateStatus(data);
      } catch (err) {
        console.error('[AvatarHUD] Failed to parse SSE message:', err);
      }
    };

    eventSource.onerror = (err) => {
      console.warn('[AvatarHUD] SSE stream disconnected, reconnecting in 2s...', err);
      eventSource.close();
      setTimeout(connectSSE, 2000);
    };
  }

  // Initial Fetch of Current Status & Config
  fetch('/api/status')
    .then(res => res.json())
    .then(data => {
      updateStatus(data);
    })
    .catch(() => {
      console.log('[AvatarHUD] Initial status fetch fallback.');
    });

  fetch('/api/config')
    .then(res => res.json())
    .then(config => {
      if (config.avatar_image) {
        avatarImg.src = config.avatar_image;
      }
      if (config.scale) {
        setScale(config.scale);
      }
    })
    .catch(() => {});

  // Start SSE connection
  connectSSE();
})();
