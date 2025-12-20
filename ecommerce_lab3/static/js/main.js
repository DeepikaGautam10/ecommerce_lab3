// static/js/main.js

// Auto-dismiss alerts after 5 seconds
document.addEventListener('DOMContentLoaded', function() {
    // Auto-hide alerts
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });
    
    // Add fade-in animation to cards
    const cards = document.querySelectorAll('.card');
    cards.forEach(function(card, index) {
        setTimeout(function() {
            card.classList.add('fade-in');
        }, index * 100);
    });
    
    // Product card hover effects
    const productCards = document.querySelectorAll('.product-card');
    productCards.forEach(function(card) {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-10px)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });
    
    // Form validation
    const forms = document.querySelectorAll('.needs-validation');
    forms.forEach(function(form) {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        });
    });
    
    // Auto-generate slug from name
    const nameInput = document.querySelector('input[name="name"]');
    const slugInput = document.querySelector('input[name="slug"]');
    
    if (nameInput && slugInput) {
        nameInput.addEventListener('input', function() {
            const slug = this.value
                .toLowerCase()
                .replace(/[^a-z0-9\s-]/g, '')
                .replace(/\s+/g, '-')
                .replace(/-+/g, '-')
                .trim();
            slugInput.value = slug;
        });
    }
    
    // Confirm delete actions
    const deleteButtons = document.querySelectorAll('[data-confirm-delete]');
    deleteButtons.forEach(function(button) {
        button.addEventListener('click', function(event) {
            const confirmed = confirm('Are you sure you want to delete this item?');
            if (!confirmed) {
                event.preventDefault();
            }
        });
    });
    
    // Image preview for file uploads
    const imageInputs = document.querySelectorAll('input[type="file"][accept*="image"]');
    imageInputs.forEach(function(input) {
        input.addEventListener('change', function(e) {
            const file = e.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function(event) {
                    // Create or update preview
                    let preview = input.parentElement.querySelector('.image-preview');
                    if (!preview) {
                        preview = document.createElement('img');
                        preview.className = 'image-preview mt-2 img-thumbnail';
                        preview.style.maxWidth = '200px';
                        input.parentElement.appendChild(preview);
                    }
                    preview.src = event.target.result;
                };
                reader.readAsDataURL(file);
            }
        });
    });
    
    // Search functionality
    const searchInput = document.querySelector('input[name="q"]');
    if (searchInput) {
        searchInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                this.form.submit();
            }
        });
    }
    
    // Quantity controls
    window.updateQuantity = function(itemId, action, maxStock) {
        const input = document.getElementById('qty-' + itemId);
        let value = parseInt(input.value);
        
        if (action === 'increase' && value < maxStock) {
            input.value = value + 1;
        } else if (action === 'decrease' && value > 1) {
            input.value = value - 1;
        }
    };
    
    // Smooth scroll to top
    const scrollTopBtn = document.createElement('button');
    scrollTopBtn.innerHTML = '<i class="fas fa-arrow-up"></i>';
    scrollTopBtn.className = 'btn btn-primary btn-scroll-top';
    scrollTopBtn.style.cssText = `
        position: fixed;
        bottom: 20px;
        right: 20px;
        display: none;
        z-index: 1000;
        border-radius: 50%;
        width: 50px;
        height: 50px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    `;
    document.body.appendChild(scrollTopBtn);
    
    window.addEventListener('scroll', function() {
        if (window.pageYOffset > 300) {
            scrollTopBtn.style.display = 'block';
        } else {
            scrollTopBtn.style.display = 'none';
        }
    });
    
    scrollTopBtn.addEventListener('click', function() {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });
    
    // Loading indicator for forms
    const submitButtons = document.querySelectorAll('form button[type="submit"]');
    submitButtons.forEach(function(button) {
        const form = button.closest('form');
        if (form) {
            form.addEventListener('submit', function() {
                button.disabled = true;
                const originalText = button.innerHTML;
                button.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Processing...';
                
                // Re-enable after 5 seconds (safety measure)
                setTimeout(function() {
                    button.disabled = false;
                    button.innerHTML = originalText;
                }, 5000);
            });
        }
    });
    
    // Category filter animation
    const categoryLinks = document.querySelectorAll('.list-group-item');
    categoryLinks.forEach(function(link) {
        link.addEventListener('click', function() {
            categoryLinks.forEach(function(l) {
                l.classList.remove('active');
            });
            this.classList.add('active');
        });
    });
    
    // Price formatter
    window.formatPrice = function(price) {
        return 'NPR ' + parseFloat(price).toFixed(2);
    };
    
    // Cart count updater
    window.updateCartCount = function() {
        const cartBadge = document.querySelector('.badge.bg-danger');
        if (cartBadge) {
            fetch('/cart/count/')
                .then(response => response.json())
                .then(data => {
                    cartBadge.textContent = data.count;
                })
                .catch(error => console.error('Error:', error));
        }
    };
    
    // Toast notifications
    window.showToast = function(message, type = 'success') {
        const toastContainer = document.querySelector('.toast-container') || createToastContainer();
        
        const toast = document.createElement('div');
        toast.className = `toast align-items-center text-white bg-${type} border-0`;
        toast.setAttribute('role', 'alert');
        toast.setAttribute('aria-live', 'assertive');
        toast.setAttribute('aria-atomic', 'true');
        
        toast.innerHTML = `
            <div class="d-flex">
                <div class="toast-body">
                    ${message}
                </div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
            </div>
        `;
        
        toastContainer.appendChild(toast);
        const bsToast = new bootstrap.Toast(toast);
        bsToast.show();
        
        // Remove toast after hidden
        toast.addEventListener('hidden.bs.toast', function() {
            toast.remove();
        });
    };
    
    function createToastContainer() {
        const container = document.createElement('div');
        container.className = 'toast-container position-fixed bottom-0 end-0 p-3';
        document.body.appendChild(container);
        return container;
    }
    
    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Initialize popovers
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function(popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
    
    // Local storage for cart (optional enhancement)
    window.saveCartToLocal = function() {
        const cart = {
            items: [],
            timestamp: Date.now()
        };
        
        document.querySelectorAll('.cart-item').forEach(function(item) {
            const id = item.dataset.productId;
            const quantity = item.querySelector('input[name="quantity"]').value;
            cart.items.push({ id, quantity });
        });
        
        localStorage.setItem('cart', JSON.stringify(cart));
    };
    
    // Dark mode toggle (bonus feature)
    window.toggleDarkMode = function() {
        document.body.classList.toggle('dark-mode');
        const isDark = document.body.classList.contains('dark-mode');
        localStorage.setItem('darkMode', isDark);
    };
    
    // Load dark mode preference
    if (localStorage.getItem('darkMode') === 'true') {
        document.body.classList.add('dark-mode');
    }
    
    console.log('E-Commerce Lab 3 - JavaScript Initialized');
});

// Utility functions
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

// CSRF token for AJAX requests
const csrftoken = getCookie('csrftoken');

// AJAX helper function
function ajaxRequest(url, method, data) {
    return fetch(url, {
        method: method,
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .catch(error => {
        console.error('Error:', error);
        throw error;
    });
}

// Export functions for use in templates
window.ajaxRequest = ajaxRequest;
window.getCookie = getCookie;