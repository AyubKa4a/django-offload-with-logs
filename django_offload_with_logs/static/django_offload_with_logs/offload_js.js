// django_offload_with_logs/static/django_offload_with_logs/offload_js.js

(function () {
    let displayedTaskIds = new Set();

    if (typeof OFFLOAD_TASK_IDS === 'undefined') return;
    if (!Array.isArray(OFFLOAD_TASK_IDS)) return;
    if (typeof OFFLOAD_BASE_URL === 'undefined') return;

    const POLL_INTERVAL = 3000;

    function checkTasks() {
        OFFLOAD_TASK_IDS.forEach(function (taskId, idx) {
            fetch(OFFLOAD_BASE_URL + "task-status/" + taskId + "/")
                .then(response => response.json())
                .then(data => {
                    let status = data.status;
                    if (status === 'SUCCESS' || status === 'FAILURE' || status === 'NOT_FOUND') {
                        
                        // Pull out messages
                        let successMsg = data.success_message || 'Task finished successfully.';
                        let failMsg = data.fail_message || 'Task failed or not found.';
                        let duration = data.message_duration || 4000;
                        let colorCode = data.color_code; // might be null
                        let position = data.toast_position; // might be null

                        let message = (status === 'SUCCESS') ? successMsg : failMsg;

                        showOffloadToast(taskId, status, message, duration, position, colorCode);

                        // remove from array
                        OFFLOAD_TASK_IDS.splice(idx, 1);
                        updateSessionTasks(OFFLOAD_TASK_IDS);
                    }
                })
                .catch(err => console.error(err));
        });
    }

    setInterval(checkTasks, POLL_INTERVAL);

    function showOffloadToast(taskId, status, message, duration, position, colorCode) {
        if (displayedTaskIds.has(taskId)) {
            return;
        }
        displayedTaskIds.add(taskId);

        injectToastCSS();

        // Decide container position
        // If user didn't pass position, default to 'top-right'
        let finalPosition = position || 'top-right';
        let containerId = 'offload-toast-container-' + finalPosition;

        let container = document.getElementById(containerId);
        if (!container) {
            container = document.createElement('div');
            container.id = containerId;
            container.style.position = 'fixed';
            container.style.zIndex = '9999';
            container.style.display = 'flex';
            container.style.flexDirection = 'column';
            container.style.gap = '10px';

            // Basic logic for position
            if (finalPosition === 'bottom-left') {
                container.style.bottom = '20px';
                container.style.left = '20px';
            } else if (finalPosition === 'bottom-right') {
                container.style.bottom = '20px';
                container.style.right = '20px';
            } else if (finalPosition === 'top-left') {
                container.style.top = '20px';
                container.style.left = '20px';
            } else {
                // Default top-right
                container.style.top = '20px';
                container.style.right = '20px';
            }

            document.body.appendChild(container);
        }

        // Decide color
        let defaultColor = (status === 'SUCCESS') ? '#4CAF50' : '#f44336';
        let backgroundColor = colorCode || defaultColor;

        // Build the toast
        const toast = document.createElement('div');
        toast.className = 'offload-toast';
        toast.dataset.taskId = taskId;
        toast.style.backgroundColor = backgroundColor;
        toast.style.padding = '16px 50px 16px 16px';
        toast.style.width = '360px';
        toast.style.minHeight = '60px';
        toast.style.color = '#fff';
        toast.style.fontSize = '16px';
        toast.style.borderRadius = '6px';
        toast.style.boxShadow = '0 2px 8px rgba(0,0,0,0.2)';
        toast.style.position = 'relative';
        toast.style.animation = 'fadeInToast 0.3s ease forwards';
        toast.textContent = message;

        container.appendChild(toast);

        // Hover to pause
        let hover = false;
        toast.addEventListener('mouseenter', () => hover = true);
        toast.addEventListener('mouseleave', () => hover = false);

        // Close button
        const closeBtn = document.createElement('button');
        closeBtn.innerHTML = '&times;';
        closeBtn.setAttribute('aria-label', 'Close');
        closeBtn.style.position = 'absolute';
        closeBtn.style.top = '8px';
        closeBtn.style.right = '12px';
        closeBtn.style.border = 'none';
        closeBtn.style.background = 'transparent';
        closeBtn.style.color = '#fff';
        closeBtn.style.fontWeight = 'bold';
        closeBtn.style.fontSize = '20px';
        closeBtn.style.cursor = 'pointer';
        closeBtn.style.padding = '0';
        closeBtn.style.lineHeight = '1';
        closeBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            removeToast(toast);
        });
        toast.appendChild(closeBtn);

        // Auto-close
        let autoCloseTimer = setTimeout(() => {
            if (!hover) {
                removeToast(toast);
            }
        }, duration);

        // Fallback forced close after extra 16s
        let forcedTimer = setTimeout(() => {
            removeToast(toast);
        }, duration + 16000);

        toast.dataset.autoCloseTimer = autoCloseTimer;
        toast.dataset.forcedTimer = forcedTimer;
    }

    function removeToast(toast) {
        toast.style.animation = 'fadeOutToast 0.3s ease forwards';

        const taskId = toast.dataset.taskId;
        const autoCloseTimer = toast.dataset.autoCloseTimer;
        const forcedTimer = toast.dataset.forcedTimer;

        if (autoCloseTimer) {
            clearTimeout(autoCloseTimer);
        }
        if (forcedTimer) {
            clearTimeout(forcedTimer);
        }

        setTimeout(() => {
            if (toast.parentNode) {
                toast.parentNode.removeChild(toast);
            }
            if (taskId) {
                displayedTaskIds.delete(taskId);
            }
        }, 300);
    }

    function injectToastCSS() {
        if (document.getElementById('toast-animation-styles')) return;
        const style = document.createElement('style');
        style.id = 'toast-animation-styles';
        style.innerHTML = `
            @keyframes fadeInToast {
                0% { opacity: 0; transform: translateY(-5px); }
                100% { opacity: 1; transform: translateY(0); }
            }
            @keyframes fadeOutToast {
                0% { opacity: 1; transform: translateY(0); }
                100% { opacity: 0; transform: translateY(-5px); }
            }
            .offload-toast:hover {
                opacity: 0.95;
            }
        `;
        document.head.appendChild(style);
    }

    function updateSessionTasks(newTaskIds) {
        fetch(OFFLOAD_BASE_URL + 'clear-tasks/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({ task_ids: newTaskIds })
        })
        .then(r => r.json())
        .then(data => {
            console.log("Offload tasks updated:", data);
        })
        .catch(err => {
            console.error("Error updating offload tasks:", err);
        });
    }

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

})();
