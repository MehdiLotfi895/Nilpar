// ═══════════════════════════════════════════════════════════════
// SMART HEADER - مخفی شدن nav-content بعد از 100px اسکرول پایین
// ═══════════════════════════════════════════════════════════════
(function() {
    let lastScrollY = window.scrollY;
    let ticking = false;

    function handleScroll() {
        const currentScrollY = window.scrollY;
        const navContent = document.querySelector('.nav-content');

        if (!navContent) return;

        if (currentScrollY > 100) {
            // اسکرول کرده پایین بیش از 100px
            if (currentScrollY > lastScrollY) {
                // داره پایین میره → nav-content مخفی بشه
                navContent.classList.add('nav-hidden');
            } else {
                // داره بالا میاد → nav-content نمایش داده بشه
                navContent.classList.remove('nav-hidden');
            }
        } else {
            // کمتر از 100px → همیشه نمایش
            navContent.classList.remove('nav-hidden');
        }

        lastScrollY = currentScrollY;
        ticking = false;
    }

    window.addEventListener('scroll', function() {
        if (!ticking) {
            requestAnimationFrame(handleScroll);
            ticking = true;
        }
    }, { passive: true });
})();


// ═══════════════════════════════════════════════════════════════
// SEARCH TOGGLE - رفع باگ + قفل اسکرول
// ═══════════════════════════════════════════════════════════════
function toggleSearch() {
    const dropdown = document.getElementById('searchDropdown');
    const overlay = document.getElementById('darkOverlay');
    const categoriesDropdown = document.getElementById('categoriesDropdown');
    const profileDropdown = document.getElementById('profileDropdown');
    const profileBtn = document.getElementById('userProfileBtn');

    // بستن دسته‌بندی و پروفایل
    if (categoriesDropdown) categoriesDropdown.classList.remove('active');
    if (profileDropdown) profileDropdown.classList.remove('active');
    if (profileBtn) profileBtn.classList.remove('active');

    const isOpening = !dropdown.classList.contains('active');
    dropdown.classList.toggle('active');

    if (isOpening) {
        // باز کردن سرچ
        overlay.classList.add('active');
        overlay.classList.add('search-overlay-active');
        document.body.classList.add('scroll-locked');
        document.body.classList.add('search-open');

        setTimeout(() => {
            const searchInput = document.getElementById('searchInput');
            if (searchInput) searchInput.focus();
        }, 300);
    } else {
        // بستن سرچ
        overlay.classList.remove('active');
        overlay.classList.remove('search-overlay-active');
        document.body.classList.remove('scroll-locked');
        document.body.classList.remove('search-open');
    }
}


// ═══════════════════════════════════════════════════════════════
// CATEGORIES TOGGLE - رفع تداخل overlay
// ═══════════════════════════════════════════════════════════════
function toggleCategories(show) {
    const dropdown = document.getElementById('categoriesDropdown');
    const searchDropdown = document.getElementById('searchDropdown');
    const profileDropdown = document.getElementById('profileDropdown');
    const profileBtn = document.getElementById('userProfileBtn');
    const overlay = document.getElementById('darkOverlay');

    if (!dropdown) return;

    // بستن سرچ و پروفایل
    if (searchDropdown) {
        searchDropdown.classList.remove('active');
        document.body.classList.remove('scroll-locked');
        document.body.classList.remove('search-open');
    }
    if (profileDropdown) profileDropdown.classList.remove('active');
    if (profileBtn) profileBtn.classList.remove('active');
    overlay.classList.remove('search-overlay-active');

    if (show) {
        dropdown.classList.add('active');
        overlay.classList.add('active');
        document.body.classList.add('scroll-locked');
    } else {
        dropdown.classList.remove('active');
        // فقط اگه پروفایل هم بسته باشه overlay رو ببند
        if (!profileDropdown || !profileDropdown.classList.contains('active')) {
            overlay.classList.remove('active');
        }
        document.body.classList.remove('scroll-locked');
    }
}


// ═══════════════════════════════════════════════════════════════
// MEGA MENU - تغییر پنل با هاور
// ═══════════════════════════════════════════════════════════════
const categoryItems = document.querySelectorAll('.mega-category-item');
const productsPanels = document.querySelectorAll('.products-panel');

categoryItems.forEach(item => {
    item.addEventListener('mouseenter', function() {
        categoryItems.forEach(cat => cat.classList.remove('active'));
        this.classList.add('active');
        productsPanels.forEach(panel => panel.classList.remove('active'));
        const categoryId = this.getAttribute('data-category');
        const targetPanel = document.getElementById(`panel-${categoryId}`);
        if (targetPanel) targetPanel.classList.add('active');
    });
});


// ═══════════════════════════════════════════════════════════════
// MEGA MENU HOVER LOGIC
// ═══════════════════════════════════════════════════════════════
const categoriesDropdown = document.getElementById('categoriesDropdown');
const navCategories = document.querySelector('.nav-categories');
let megaMenuTimeout;

if (navCategories) {
    navCategories.addEventListener('mouseenter', () => {
        clearTimeout(megaMenuTimeout);
        if (categoriesDropdown) {
            categoriesDropdown.classList.add('active');
            document.getElementById('darkOverlay').classList.add('active');
            document.body.classList.add('scroll-locked');
        }
    });

    navCategories.addEventListener('mouseleave', () => {
        megaMenuTimeout = setTimeout(() => {
            if (categoriesDropdown) {
                categoriesDropdown.classList.remove('active');
                const profileDropdown = document.getElementById('profileDropdown');
                if (!profileDropdown || !profileDropdown.classList.contains('active')) {
                    document.getElementById('darkOverlay').classList.remove('active');
                }
                document.body.classList.remove('scroll-locked');
            }
        }, 200);
    });
}

if (categoriesDropdown) {
    categoriesDropdown.addEventListener('mouseenter', () => {
        clearTimeout(megaMenuTimeout);
        categoriesDropdown.classList.add('active');
    });

    categoriesDropdown.addEventListener('mouseleave', () => {
        megaMenuTimeout = setTimeout(() => {
            categoriesDropdown.classList.remove('active');
            const profileDropdown = document.getElementById('profileDropdown');
            if (!profileDropdown || !profileDropdown.classList.contains('active')) {
                document.getElementById('darkOverlay').classList.remove('active');
            }
            document.body.classList.remove('scroll-locked');
            // ریست به حالت اول
            categoryItems.forEach(cat => cat.classList.remove('active'));
            if (categoryItems.length > 0) categoryItems[0].classList.add('active');
            productsPanels.forEach(panel => panel.classList.remove('active'));
            if (productsPanels.length > 0) productsPanels[0].classList.add('active');
        }, 200);
    });
}


// ═══════════════════════════════════════════════════════════════
// CLOSE ALL
// ═══════════════════════════════════════════════════════════════
function closeAll() {
    const searchDropdown = document.getElementById('searchDropdown');
    const categoriesDropdown = document.getElementById('categoriesDropdown');
    const profileDropdown = document.getElementById('profileDropdown');
    const profileBtn = document.getElementById('userProfileBtn');
    const overlay = document.getElementById('darkOverlay');

    if (searchDropdown) searchDropdown.classList.remove('active');
    if (categoriesDropdown) categoriesDropdown.classList.remove('active');
    if (profileDropdown) profileDropdown.classList.remove('active');
    if (profileBtn) profileBtn.classList.remove('active');
    if (overlay) {
        overlay.classList.remove('active');
        overlay.classList.remove('search-overlay-active');
    }
    document.body.classList.remove('scroll-locked');
    document.body.classList.remove('search-open');
}


// ═══════════════════════════════════════════════════════════════
// OVERLAY CLICK - بستن با کلیک بیرون
// ═══════════════════════════════════════════════════════════════
document.getElementById('darkOverlay').addEventListener('click', function() {
    closeAll();
});


// ═══════════════════════════════════════════════════════════════
// PROFILE TOGGLE - بدون overlay
// ═══════════════════════════════════════════════════════════════
function toggleProfile() {
    const profileBtn = document.getElementById('userProfileBtn');
    const profileDropdown = document.getElementById('profileDropdown');
    const searchDropdown = document.getElementById('searchDropdown');
    const categoriesDropdown = document.getElementById('categoriesDropdown');
    const overlay = document.getElementById('darkOverlay');

    // بستن سرچ و دسته‌بندی
    if (searchDropdown) {
        searchDropdown.classList.remove('active');
        document.body.classList.remove('scroll-locked');
        document.body.classList.remove('search-open');
    }
    if (categoriesDropdown) categoriesDropdown.classList.remove('active');
    overlay.classList.remove('active');
    overlay.classList.remove('search-overlay-active');
    document.body.classList.remove('scroll-locked');

    // باز/بستن پروفایل (بدون overlay)
    profileBtn.classList.toggle('active');
    profileDropdown.classList.toggle('active');
}


// ═══════════════════════════════════════════════════════════════
// PROFILE CLOSE با کلیک بیرون
// ═══════════════════════════════════════════════════════════════
document.addEventListener('click', function(e) {
    const profileWrapper = document.getElementById('userProfileWrapper');
    const profileDropdown = document.getElementById('profileDropdown');
    const profileBtn = document.getElementById('userProfileBtn');

    if (profileWrapper && profileDropdown && profileBtn) {
        if (!profileWrapper.contains(e.target)) {
            profileDropdown.classList.remove('active');
            profileBtn.classList.remove('active');
        }
    }
});


// ═══════════════════════════════════════════════════════════════
// ESC KEY
// ═══════════════════════════════════════════════════════════════
document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') closeAll();
});


// ═══════════════════════════════════════════════════════════════
// BASKET DROPDOWN
// ═══════════════════════════════════════════════════════════════
const basketWrapper = document.getElementById('basketWrapper');
const basketDropdown = document.getElementById('basketDropdown');
let hideTimeout;
let showTimeout;

if (basketWrapper && basketDropdown) {
    basketWrapper.addEventListener('mouseenter', () => {
        clearTimeout(hideTimeout);
        showTimeout = setTimeout(() => {
            basketDropdown.style.display = 'block';
        }, 100);
    });

    basketWrapper.addEventListener('mouseleave', () => {
        clearTimeout(showTimeout);
        hideTimeout = setTimeout(() => {
            basketDropdown.style.display = 'none';
        }, 300);
    });

    basketDropdown.addEventListener('mouseenter', () => {
        clearTimeout(hideTimeout);
    });

    basketDropdown.addEventListener('mouseleave', () => {
        hideTimeout = setTimeout(() => {
            basketDropdown.style.display = 'none';
        }, 300);
    });
}


// ═══════════════════════════════════════════════════════════════
// REMOVE FROM BASKET (AJAX)
// ═══════════════════════════════════════════════════════════════
function removeFromBasket(productId) {
    fetch(`/basket/remove/${productId}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) updateBasketUI(data);
    })
    .catch(error => console.error('Error:', error));
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

function updateBasketUI(data) {
    const badge = document.getElementById('basketBadge');
    const itemCount = document.getElementById('itemCount');

    if (data.count > 0) {
        if (badge) { badge.style.display = 'flex'; badge.textContent = data.count; }
        if (itemCount) itemCount.textContent = data.count + ' کالا';
    } else {
        if (badge) badge.style.display = 'none';
        if (itemCount) itemCount.textContent = '0 کالا';
    }

    const dropdownBody = document.getElementById('dropdownBody');
    if (dropdownBody) dropdownBody.innerHTML = data.html;
}


// ═══════════════════════════════════════════════════════════════
// FOOTER - مشاهده بیشتر/کمتر
// ═══════════════════════════════════════════════════════════════
document.addEventListener('DOMContentLoaded', function() {
    const aboutFull = document.getElementById('aboutFull');
    const toggleBtn = document.getElementById('toggleAboutBtn');

    if (aboutFull && toggleBtn) {
        toggleBtn.addEventListener('click', function() {
            const isExpanded = aboutFull.classList.contains('show');
            if (isExpanded) {
                aboutFull.classList.remove('show');
                toggleBtn.textContent = 'مشاهده بیشتر';
            } else {
                aboutFull.classList.add('show');
                toggleBtn.textContent = 'نمایش کمتر';
            }
        });
    }
});


// ═══════════════════════════════════════════════════════════════
// NEWSLETTER
// ═══════════════════════════════════════════════════════════════
document.addEventListener('DOMContentLoaded', function() {
    const newsletterForm = document.querySelector('.newsletter-form');
    if (newsletterForm) {
        newsletterForm.addEventListener('submit', function(e) {
            e.preventDefault();
            alert('ایمیل شما با موفقیت ثبت شد!');
            this.reset();
        });
    }
});


// ═══════════════════════════════════════════════════════════════
// COLOR SELECTOR
// ═══════════════════════════════════════════════════════════════
document.addEventListener('DOMContentLoaded', function() {
    const circles = document.querySelectorAll('#multiColorSelector .color-circle');
    const hiddenInput = document.getElementById('selectedColorsInput');

    if (!circles.length || !hiddenInput) return;

    function updateSelectedColors() {
        const selectedIds = [];
        circles.forEach(circle => {
            if (circle.classList.contains('selected')) {
                const colorId = circle.getAttribute('data-color-id');
                if (colorId) selectedIds.push(colorId);
            }
        });
        hiddenInput.value = selectedIds.join(',');
    }

    circles.forEach(circle => {
        circle.addEventListener('click', function(e) {
            e.preventDefault();
            this.classList.toggle('selected');
            updateSelectedColors();
        });
    });

    const initialSelected = hiddenInput.value.split(',').filter(id => id);
    if (initialSelected.length) {
        circles.forEach(circle => {
            const id = circle.getAttribute('data-color-id');
            if (initialSelected.includes(id)) circle.classList.add('selected');
        });
    }
});















