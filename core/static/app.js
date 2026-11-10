(function () {
  // DOM Elements
  const avatarWrapper = document.getElementById('avatar-wrapper');
  const avatarImg = document.getElementById('avatar-img');
  const speechBubble = document.getElementById('speech-bubble');
  const statusBadge = document.getElementById('status-badge');
  const statusText = document.getElementById('status-text');
  const stepBadge = document.getElementById('step-badge');
  const bubbleTitle = document.getElementById('bubble-title');
  const bubbleMessage = document.getElementById('bubble-message');
  const elapsedTime = document.getElementById('elapsed-time');
  const timestamp = document.getElementById('timestamp');
  const btnMinimize = document.getElementById('btn-minimize-bubble');
  const btnChangeAvatar = document.getElementById('btn-change-avatar');
  const btnScaleUp = document.getElementById('btn-scale-up');
  const btnScaleDown = document.getElementById('btn-scale-down');
  const avatarFileInput = document.getElementById('avatar-file-input');

  let currentScale = 1.0;
  let isMinimized = false;
  let typingTimer = null;

  // 1. Scale Avatar
  function setScale(scale) {
    currentScale = Math.min(2.5, Math.max(0.4, scale));
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

  // 3. Minimize / Restore Bubble
  btnMinimize.addEventListener('click', (e) => {
    e.stopPropagation();
    isMinimized = !isMinimized;
    if (isMinimized) {
      speechBubble.classList.add('minimized');
      btnMinimize.textContent = '+';
    } else {
      speechBubble.classList.remove('minimized');
      btnMinimize.textContent = '✕';
    }
  });

  // Clicking a minimized bubble expands it
  speechBubble.addEventListener('click', () => {
    if (isMinimized) {
      isMinimized = false;
      speechBubble.classList.remove('minimized');
      btnMinimize.textContent = '✕';
    }
  });

  // 4. Typing Effect for Message
  function typeMessage(text, element) {
    clearTimeout(typingTimer);
    element.textContent = '';
    let index = 0;
    const speed = Math.max(8, Math.min(25, 400 / (text.length || 1)));

    function step() {
      if (index < text.length) {
        element.textContent += text.charAt(index);
        index++;
        typingTimer = setTimeout(step, speed);
      }
    }
    step();
  }

  // 5. Update Status UI
  function updateStatus(data) {
    const status = data.status || 'idle';
    const title = data.title || (status === 'working' ? '작업 수행 중...' : status === 'done' ? '작업 완료!' : '대기 중');
    const message = data.message || '';
    const step = data.step || '';
    const elapsed = data.elapsed != null ? `${data.elapsed}초 소요` : '';

    // Class update
    speechBubble.classList.remove('status-working', 'status-done', 'status-error', 'status-idle');
    speechBubble.classList.add(`status-${status}`);

    // If minimized and important event happens, restore
    if (isMinimized && (status === 'working' || status === 'done' || status === 'error')) {
      isMinimized = false;
      speechBubble.classList.remove('minimized');
      btnMinimize.textContent = '✕';
    }

    // Status text & indicator
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

    // Title & Message
    bubbleTitle.textContent = title;
    typeMessage(message, bubbleMessage);

    // Footer
    elapsedTime.textContent = elapsed;
    const now = new Date();
    timestamp.textContent = `${now.getHours().toString().padStart(2, '0')}:${now.getMinutes().toString().padStart(2, '0')}:${now.getSeconds().toString().padStart(2, '0')}`;
  }

  // 6. Real-time Server-Sent Events (SSE) Connection
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
