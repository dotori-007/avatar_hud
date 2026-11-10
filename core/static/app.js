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
  const btnChangeAvatar = document.getElementById('btn-change-avatar');
  const btnScaleUp = document.getElementById('btn-scale-up');
  const btnScaleDown = document.getElementById('btn-scale-down');
  const avatarFileInput = document.getElementById('avatar-file-input');

  let currentScale = 1.0;
  let typingTimer = null;
  let autoHideTimer = null;

  // 1. Scale Avatar
  function setScale(scale) {
    currentScale = Math.min(2.0, Math.max(0.5, scale));
    avatarImg.style.transform = `scale(${currentScale})`;
    avatarImg.style.transformOrigin = 'bottom center';
  }

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

  // 2. Change Avatar File
  btnChangeAvatar.addEventListener('click', (e) => {
    e.stopPropagation();
    avatarFileInput.click();
  });

  avatarFileInput.addEventListener('change', (e) => {
    const file = e.target.files[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = (event) => {
      const dataUrl = event.target.result;
      avatarImg.src = dataUrl;

      // Save to server
      fetch('/api/config', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ avatar_data: dataUrl })
      }).catch(console.warn);
    };
    reader.readAsDataURL(file);
  });

  // 3. Update Status UI
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

    // Reset bounce animation on show
    speechBubble.classList.remove('show');
    void speechBubble.offsetWidth; // Force reflow
    speechBubble.classList.add('show');

    // Auto-dim idle after timeout if needed
    clearTimeout(autoHideTimer);
    if (status === 'idle') {
      autoHideTimer = setTimeout(() => {
        // Keep visible with gentle opacity or keep shown
      }, 10000);
    }
  }

  // 4. Real-time Server-Sent Events (SSE) Connection
  function connectSSE() {
    const eventSource = new EventSource('/api/stream');

    eventSource.onopen = () => {
      console.log('[AvatarHUD] SSE stream connected.');
    };

    eventSource.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
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
      if (config.avatar_image && config.avatar_image !== 'default_avatar.png') {
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
