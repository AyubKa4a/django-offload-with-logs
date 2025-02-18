(function () {
    // Track active toast IDs to prevent duplicates
    let displayedTaskIds = new Set();

    if (typeof OFFLOAD_TASK_IDS === 'undefined') return;
    if (!Array.isArray(OFFLOAD_TASK_IDS)) return;
    if (typeof OFFLOAD_BASE_URL === 'undefined') return;

    const POLL_INTERVAL = 3000;

    // Poll the status for each task ID in the session
    function checkTasks() {
        OFFLOAD_TASK_IDS.forEach(function (taskId, idx) {
            fetch(OFFLOAD_BASE_URL + "task-status/" + taskId + "/")
                .then(response => response.json())
                .then(data => {
                    let status = data.status;
                    if (status === 'SUCCESS' || status === 'FAILURE' || status === 'NOT_FOUND') {

                        // Defaults
                        let message = 'The task finished successfully.';
                        let duration = 4000; // default auto-close time

                        // If not success, use a fail message
                        if (status !== 'SUCCESS') {
                            message = 'The task failed or was not found.';
                        }

                        // Custom messages from backend?
                        if (status === 'SUCCESS' && data.success_message) {
                            message = data.success_message;
                        } else if ((status === 'FAILURE' || status === 'NOT_FOUND') && data.fail_message) {
                            message = data.fail_message;
                        }

                        if (data.message_duration) {
                            duration = data.message_duration;
                        }

                        // Show the toast (with ID to prevent duplicates)
                        showOffloadToast(taskId, status, message, duration);

                        // Remove taskId from the array after scheduling
                        OFFLOAD_TASK_IDS.splice(idx, 1);

                        // Update server session
                        updateSessionTasks(OFFLOAD_TASK_IDS);
                    }
                })
                .catch(err => console.error(err));
        });
    }

    setInterval(checkTasks, POLL_INTERVAL);

    /**
     * Create & show a toast (skipping duplicates),
     * hover pauses auto-close, but forced fallback ensures it won't stay forever.
     */
    function showOffloadToast(taskId, status, message, duration) {
        // 1) Avoid duplicates for the same task
        if (displayedTaskIds.has(taskId)) {
            return;
        }
        displayedTaskIds.add(taskId);

        injectToastCSS();

        // 2) Ensure container for stacking
        let container = document.getElementById('offload-toast-container');
        if (!container) {
            container = document.createElement('div');
            container.id = 'offload-toast-container';
            container.style.position = 'fixed';
            container.style.top = '20px';
            container.style.right = '20px';
            container.style.zIndex = '9999';
            container.style.display = 'flex';
            container.style.flexDirection = 'column';
            container.style.gap = '10px';
            document.body.appendChild(container);
        }

        // 3) Pick success/failure styling
        let backgroundColor = '#4CAF50'; // green
        if (status !== 'SUCCESS') {
            backgroundColor = '#f44336'; // red
        }

        // 4) Build the toast element
        const toast = document.createElement('div');
        toast.className = 'offload-toast';
        toast.dataset.taskId = taskId;
        toast.style.backgroundColor = backgroundColor;
        toast.style.padding = '16px 50px 16px 16px'; // extra right padding for close button
        toast.style.width = '360px';
        toast.style.minHeight = '60px';
        toast.style.color = '#fff';
        toast.style.fontSize = '16px';
        toast.style.borderRadius = '6px';
        toast.style.boxShadow = '0 2px 8px rgba(0,0,0,0.2)';
        toast.style.position = 'relative'; // for absolutely positioned close button
        toast.style.animation = 'fadeInToast 0.3s ease forwards';
        toast.textContent = message;

        // 4a) Insert into container
        container.appendChild(toast);

        // 5) Hover logic to pause auto-close
        let hover = false;
        toast.addEventListener('mouseenter', () => (hover = true));
        toast.addEventListener('mouseleave', () => (hover = false));

        // 6) Add close button in top-right
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

        // 7) Main auto-close after "duration" ms if not hovered
        let autoCloseTimer = setTimeout(() => {
            if (!hover) {
                removeToast(toast);
            }
        }, duration || 4000);

        // 8) Fallback forced close:
        // If user hovers indefinitely, toast auto-hides anyway after 20s
        let forcedTimer = setTimeout(() => {
            removeToast(toast);
        }, (duration || 4000) + 16000); // 16s buffer

        // Store timers on toast element
        toast.dataset.autoCloseTimer = autoCloseTimer;
        toast.dataset.forcedTimer = forcedTimer;
    }

    /**
     * Remove toast with fadeOut, free the task ID, clear timers
     */
    function removeToast(toast) {
        // fade out
        toast.style.animation = 'fadeOutToast 0.3s ease forwards';

        const taskId = toast.dataset.taskId;
        const autoCloseTimer = toast.dataset.autoCloseTimer;
        const forcedTimer = toast.dataset.forcedTimer;

        // Clear any timers
        if (autoCloseTimer) {
            clearTimeout(autoCloseTimer);
        }
        if (forcedTimer) {
            clearTimeout(forcedTimer);
        }

        setTimeout(() => {
            // Remove from DOM
            if (toast.parentNode) {
                toast.parentNode.removeChild(toast);
            }
            // Free up the ID
            if (taskId) {
                displayedTaskIds.delete(taskId);
            }
        }, 300);
    }

    /**
     * Inject fade in/out keyframes once
     */
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

    /**
     * Update server session with current task IDs
     */
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

    /**
     * Standard Django CSRF token retrieval
     */
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