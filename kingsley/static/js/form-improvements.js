/* ==================================================
   FORM UX IMPROVEMENTS - JAVASCRIPT
   Elite Wealth Capital
   ================================================== */

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    initFormImprovements();
});

function initFormImprovements() {
    // Add loading states to all forms
    addFormLoadingStates();
    
    // Add real-time validation
    addRealTimeValidation();
    
    // Auto-hide messages after 5 seconds
    autoHideMessages();
    
    // Prevent double-submit
    preventDoubleSubmit();
}

/* ==================================================
   LOADING STATES
   ================================================== */

function addFormLoadingStates() {
    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const submitBtn = form.querySelector('button[type="submit"]');
            
            if (submitBtn && !submitBtn.classList.contains('btn-loading')) {
                // Add loading state
                submitBtn.classList.add('btn-loading');
                submitBtn.disabled = true;
                
                // Store original text
                submitBtn.dataset.originalText = submitBtn.innerHTML;
                
                // Change button text
                const loadingText = submitBtn.dataset.loadingText || 'Processing...';
                submitBtn.innerHTML = `<span class="me-2">${loadingText}</span>`;
            }
        });
    });
}

/* ==================================================
   REAL-TIME VALIDATION
   ================================================== */

function addRealTimeValidation() {
    // Email validation
    const emailInputs = document.querySelectorAll('input[type="email"]');
    emailInputs.forEach(input => {
        input.addEventListener('blur', function() {
            validateEmail(this);
        });
    });
    
    // Password validation
    const passwordInputs = document.querySelectorAll('input[type="password"]');
    passwordInputs.forEach(input => {
        // Only validate on signup/register forms
        if (input.closest('form').action.includes('signup') || 
            input.closest('form').action.includes('register')) {
            input.addEventListener('input', function() {
                validatePassword(this);
            });
        }
    });
    
    // Amount validation (for investment/withdrawal forms)
    const amountInputs = document.querySelectorAll('input[name="amount"], input[name*="amount"]');
    amountInputs.forEach(input => {
        input.addEventListener('blur', function() {
            validateAmount(this);
        });
    });
}

function validateEmail(input) {
    const email = input.value.trim();
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    
    clearValidation(input);
    
    if (email === '') {
        return; // Don't validate empty (let required attribute handle it)
    }
    
    if (!emailRegex.test(email)) {
        showInvalid(input, 'Please enter a valid email address');
    } else {
        showValid(input, 'Email looks good!');
    }
}

function validatePassword(input) {
    const password = input.value;
    
    clearValidation(input);
    
    if (password === '') {
        return;
    }
    
    const errors = [];
    
    if (password.length < 8) {
        errors.push('at least 8 characters');
    }
    if (!/[A-Z]/.test(password)) {
        errors.push('one uppercase letter');
    }
    if (!/[a-z]/.test(password)) {
        errors.push('one lowercase letter');
    }
    if (!/[0-9]/.test(password)) {
        errors.push('one number');
    }
    
    if (errors.length > 0) {
        showInvalid(input, `Password needs: ${errors.join(', ')}`);
    } else {
        showValid(input, 'Strong password!');
    }
}

function validateAmount(input) {
    const amount = parseFloat(input.value);
    const min = parseFloat(input.min) || 0;
    const max = parseFloat(input.max) || Infinity;
    
    clearValidation(input);
    
    if (isNaN(amount) || amount <= 0) {
        showInvalid(input, 'Please enter a valid amount');
    } else if (amount < min) {
        showInvalid(input, `Minimum amount is $${min.toFixed(2)}`);
    } else if (amount > max) {
        showInvalid(input, `Maximum amount is $${max.toFixed(2)}`);
    } else {
        showValid(input, 'Amount is valid');
    }
}

function showInvalid(input, message) {
    input.classList.add('is-invalid-custom');
    input.classList.remove('is-valid-custom');
    
    let feedback = input.nextElementSibling;
    if (!feedback || !feedback.classList.contains('invalid-feedback-custom')) {
        feedback = document.createElement('div');
        feedback.className = 'invalid-feedback-custom';
        input.parentNode.insertBefore(feedback, input.nextSibling);
    }
    feedback.textContent = message;
}

function showValid(input, message) {
    input.classList.add('is-valid-custom');
    input.classList.remove('is-invalid-custom');
    
    let feedback = input.nextElementSibling;
    if (!feedback || !feedback.classList.contains('valid-feedback-custom')) {
        feedback = document.createElement('div');
        feedback.className = 'valid-feedback-custom';
        input.parentNode.insertBefore(feedback, input.nextSibling);
    }
    feedback.textContent = message;
}

function clearValidation(input) {
    input.classList.remove('is-valid-custom', 'is-invalid-custom');
    
    const feedback = input.nextElementSibling;
    if (feedback && (feedback.classList.contains('valid-feedback-custom') || 
                     feedback.classList.contains('invalid-feedback-custom'))) {
        feedback.remove();
    }
}

/* ==================================================
   AUTO-HIDE MESSAGES
   ================================================== */

function autoHideMessages() {
    const alerts = document.querySelectorAll('.alert-floating');
    
    alerts.forEach(alert => {
        // Auto-hide after 5 seconds
        setTimeout(() => {
            alert.classList.add('alert-fade-out');
            setTimeout(() => {
                alert.remove();
            }, 300);
        }, 5000);
        
        // Allow manual close
        const closeBtn = alert.querySelector('.btn-close');
        if (closeBtn) {
            closeBtn.addEventListener('click', () => {
                alert.classList.add('alert-fade-out');
                setTimeout(() => {
                    alert.remove();
                }, 300);
            });
        }
    });
}

/* ==================================================
   PREVENT DOUBLE-SUBMIT
   ================================================== */

function preventDoubleSubmit() {
    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
        let submitted = false;
        
        form.addEventListener('submit', function(e) {
            if (submitted) {
                e.preventDefault();
                return false;
            }
            
            // Mark as submitted
            submitted = true;
            
            // Re-enable after 3 seconds (in case of validation error)
            setTimeout(() => {
                submitted = false;
            }, 3000);
        });
    });
}

/* ==================================================
   SHOW SUCCESS MESSAGE
   ================================================== */

function showSuccessMessage(message, duration = 5000) {
    const alert = document.createElement('div');
    alert.className = 'alert alert-success alert-floating alert-dismissible fade show';
    alert.innerHTML = `
        <i class="fas fa-check-circle me-2"></i>
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(alert);
    
    setTimeout(() => {
        alert.classList.add('alert-fade-out');
        setTimeout(() => {
            alert.remove();
        }, 300);
    }, duration);
}

/* ==================================================
   SHOW ERROR MESSAGE
   ================================================== */

function showErrorMessage(message, duration = 5000) {
    const alert = document.createElement('div');
    alert.className = 'alert alert-danger alert-floating alert-dismissible fade show';
    alert.innerHTML = `
        <i class="fas fa-exclamation-circle me-2"></i>
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(alert);
    
    setTimeout(() => {
        alert.classList.add('alert-fade-out');
        setTimeout(() => {
            alert.remove();
        }, 300);
    }, duration);
}

/* ==================================================
   LOADING OVERLAY
   ================================================== */

function showLoadingOverlay(message = 'Processing...') {
    const overlay = document.createElement('div');
    overlay.className = 'loading-overlay';
    overlay.innerHTML = `
        <div class="text-center">
            <div class="spinner-border mb-3" role="status">
                <span class="visually-hidden">Loading...</span>
            </div>
            <p class="text-white">${message}</p>
        </div>
    `;
    
    document.body.appendChild(overlay);
    return overlay;
}

function hideLoadingOverlay(overlay) {
    if (overlay && overlay.parentNode) {
        overlay.remove();
    }
}

/* ==================================================
   EXPORT FUNCTIONS FOR GLOBAL USE
   ================================================== */

window.FormUX = {
    showSuccess: showSuccessMessage,
    showError: showErrorMessage,
    showLoading: showLoadingOverlay,
    hideLoading: hideLoadingOverlay,
    validateEmail: validateEmail,
    validatePassword: validatePassword,
    validateAmount: validateAmount
};
