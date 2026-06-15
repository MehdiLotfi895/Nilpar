// ═══════════════════════════════════════════════════════════════
// SMART HEADER - مخفی شدن nav-content بعد از 100px اسکرول پایین
// ═══════════════════════════════════════════════════════════════
(function() {
    let lastScrollY = window.scrollY;
    let ticking = false;

    function handleScroll() {
        // اگر منوها باز هستند، کدهای حرکتی هدر نباید اجرا شوند تا تداخل پیش نیاید
        if (document.body.classList.contains('scroll-locked')) {
            ticking = false;
            return;
        }

        const currentScrollY = window.scrollY;
        const navContent = document.querySelector('.nav-content');

        if (!navContent) return;

        if (currentScrollY > 100) {
            if (currentScrollY > lastScrollY) {
                navContent.classList.add('nav-hidden');
            } else {
                navContent.classList.remove('nav-hidden');
            }
        } else {
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
// SEARCH TOGGLE - رفع باگ جابجایی + قفل اسکرول هوشمند
// ═══════════════════════════════════════════════════════════════
function toggleSearch() {
    const dropdown = document.getElementById('searchDropdown');
    const overlay = document.getElementById('darkOverlay');
    const categoriesDropdown = document.getElementById('categoriesDropdown');
    const profileDropdown = document.getElementById('profileDropdown');
    const profileBtn = document.getElementById('userProfileBtn');

    if (categoriesDropdown) categoriesDropdown.classList.remove('active');
    if (profileDropdown) profileDropdown.classList.remove('active');
    if (profileBtn) profileBtn.classList.remove('active');

    const isOpening = !dropdown.classList.contains('active');
    dropdown.classList.toggle('active');

    if (isOpening) {
        overlay.classList.add('active');
        overlay.classList.add('search-overlay-active');
        lockScroll(); // فعال‌سازی پکیج جدید قفل اسکرول
        document.body.classList.add('search-open');

        setTimeout(() => {
            const searchInput = document.getElementById('searchInput');
            if (searchInput) searchInput.focus();
        }, 300);
    } else {
        overlay.classList.remove('active');
        overlay.classList.remove('search-overlay-active');
        unlockScroll(); // باز کردن اسکرول
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

    if (searchDropdown) {
        searchDropdown.classList.remove('active');
        unlockScroll();
        document.body.classList.remove('search-open');
    }
    if (profileDropdown) profileDropdown.classList.remove('active');
    if (profileBtn) profileBtn.classList.remove('active');
    overlay.classList.remove('search-overlay-active');

    if (show) {
        dropdown.classList.add('active');
        overlay.classList.add('active');
        lockScroll();
    } else {
        dropdown.classList.remove('active');
        if (!profileDropdown || !profileDropdown.classList.contains('active')) {
            overlay.classList.remove('active');
        }
        unlockScroll();
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
// MEGA MENU HOVER LOGIC - مدیریت بدون اختلال هاور دسته‌بندی‌ها
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
            lockScroll();
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
                unlockScroll();
            }
        }, 200);
    });
}

if (categoriesDropdown) {
    categoriesDropdown.addEventListener('mouseenter', () => {
        clearTimeout(megaMenuTimeout);
        categoriesDropdown.classList.add('active');
        lockScroll();
    });

    categoriesDropdown.addEventListener('mouseleave', () => {
        megaMenuTimeout = setTimeout(() => {
            categoriesDropdown.classList.remove('active');
            const profileDropdown = document.getElementById('profileDropdown');
            if (!profileDropdown || !profileDropdown.classList.contains('active')) {
                document.getElementById('darkOverlay').classList.remove('active');
            }
            unlockScroll();
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
    unlockScroll();
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

    if (searchDropdown) {
        searchDropdown.classList.remove('active');
        unlockScroll();
        document.body.classList.remove('search-open');
    }
    if (categoriesDropdown) categoriesDropdown.classList.remove('active');
    overlay.classList.remove('active');
    overlay.classList.remove('search-overlay-active');
    unlockScroll();

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


// // ═══════════════════════════════════════════════════════════════
// // SMART NAVIGATION - هماهنگ با هدر استیکی و بدون لگ
// // ═══════════════════════════════════════════════════════════════
// (function() {
//     const nav = document.querySelector('.main-nav');
//     if (!nav) return;

//     let lastScrollS = window.pageYOffset || document.documentElement.scrollTop;
//     let ticking = false;

//     function updateNav() {
//         if (document.body.classList.contains('scroll-locked')) {
//             ticking = false;
//             return;
//         }

//         const currentScrollY = window.pageYOffset || document.documentElement.scrollTop;

//         if (currentScrollY < 100) {
//             nav.classList.remove('nav-hidden');
//         } 
//         else if (Math.abs(currentScrollY - lastScrollS) > 5) {
//             if (currentScrollY > lastScrollS) {
//                 nav.classList.add('nav-hidden');
//             } else {
//                 nav.classList.remove('nav-hidden');
//             }
//         }

//         lastScrollS = currentScrollY;
//         ticking = false;
//     }

//     window.addEventListener('scroll', function() {
//         if (!ticking) {
//             window.requestAnimationFrame(updateNav);
//             ticking = true;
//         }
//     }, { passive: true });
// })();


// ═══════════════════════════════════════════════════════════════
// پکیج فوق‌پیشرفته و هوشمند قفل اسکرول (پشتیبانی کامل از منو، پنل‌ها و محصولات)
// ═══════════════════════════════════════════════════════════════
// ═══════════════════════════════════════════════════════════════
// پکیج هوشمند قفل اسکرول (رفع کامل باگ با تمرکز روی products-grid-mega)
// ═══════════════════════════════════════════════════════════════
const preventKeys = {32:1, 33:1, 34:1, 35:1, 36:1, 37:1, 38:1, 39:1, 40:1};

function freezeEvent(e) {
    // بررسی اینکه آیا هدف در بخش‌های مجاز (منوی دسکتاپ یا منوی موبایل) قرار دارد
    const isInsideAllowedArea = e.target.closest('#categoriesDropdown') || 
                                e.target.closest('.products-panel.active') || 
                                e.target.closest('.products-grid-mega') || 
                                e.target.closest('.mega-menu-category') ||
                                e.target.closest('#mobileCategoriesLayer') ||          // خود لایه موبایل
                                e.target.closest('.mobile-categories-content') ||     // محتوای اسکرول‌شونده
                                e.target.closest('.mobile-subcategory-panel') ||      // پنل زیرمجموعه‌ها
                                e.target.closest('.mobile-categories-inner');          // کل محفظه لایه
    
    if (isInsideAllowedArea) {
        return;  // اسکرول آزاد باشد
    }
    e.preventDefault();
}

function freezeKeyEvent(e) {
    if (preventKeys[e.keyCode]) {
        const isInsideDropdown = e.target.closest('#categoriesDropdown') || 
                                 e.target.closest('#searchDropdown') || 
                                 e.target.closest('.products-panel.active') ||
                                 e.target.closest('.products-grid-mega') ||
                                 e.target.closest('.mega-menu-category');
        if (isInsideDropdown) {
            return;
        }
        freezeEvent(e);
        return false;
    }
}

function lockScroll() {
    if (document.body.classList.contains('scroll-locked')) return;
    
    window.addEventListener('DOMMouseScroll', freezeEvent, false);
    window.addEventListener('wheel', freezeEvent, { passive: false });
    window.addEventListener('touchmove', freezeEvent, { passive: false });
    window.addEventListener('keydown', freezeKeyEvent, false);
    
    document.body.classList.add('scroll-locked');
}

function unlockScroll() {
    if (!document.body.classList.contains('scroll-locked')) return;
    
    window.removeEventListener('DOMMouseScroll', freezeEvent, false);
    window.removeEventListener('wheel', freezeEvent, { passive: false });
    window.removeEventListener('touchmove', freezeEvent, { passive: false });
    window.removeEventListener('keydown', freezeKeyEvent, false);
    
    document.body.classList.remove('scroll-locked');
}










document.addEventListener("DOMContentLoaded", () => {
    const consultBox = document.getElementById("consultBox");
    const closeBtn = document.getElementById("closeConsult");

    if (!consultBox || !closeBtn) return;

    let isClosing = false;

    closeBtn.addEventListener("click", () => {
        if (isClosing) return;

        isClosing = true;

        consultBox.classList.add("closing");

        consultBox.addEventListener(
            "animationend",
            () => {
                consultBox.remove();
            },
            { once: true }
        );
    });
});






// // ═══════════════════════════════════════════════════════════════
// // SMART MOBILE HEADER
// // ═══════════════════════════════════════════════════════════════
// (function () {

//     const mobileHeader = document.querySelector('.mobile-header-wrapper');

//     if (!mobileHeader) return;

//     let lastScrollY = window.pageYOffset || document.documentElement.scrollTop;
//     let ticking = false;

//     function updateHeader() {

//         if (document.body.classList.contains('scroll-locked')) {
//             lastScrollY = window.pageYOffset || document.documentElement.scrollTop;
//             ticking = false;
//             return;
//         }

//         const currentScrollY =
//             window.pageYOffset || document.documentElement.scrollTop;

//         const diff = currentScrollY - lastScrollY;

//         //  بالای صفحه همیشه نمایش داده شود
//          if (currentScrollY < 100) {
//              mobileHeader.classList.remove('mobile-nav-hidden');
//         }

//         // جلوگیری از لرزش روی اسکرول‌های ریز
//         else if (Math.abs(diff) > 5) {

//             // اسکرول به پایین
//             if (diff > 0) {
//                 mobileHeader.classList.add('mobile-nav-hidden');
//             }

//             // اسکرول به بالا
//             else {
//                 mobileHeader.classList.remove('mobile-nav-hidden');
//             }
//         }

//         lastScrollY = currentScrollY;
//         ticking = false;
//     }

//     window.addEventListener('scroll', function () {

//         if (!ticking) {
//             requestAnimationFrame(updateHeader);
//             ticking = true;
//         }

//     }, { passive: true });

// })();







document.addEventListener("DOMContentLoaded", () => {

    document.querySelectorAll(".alert").forEach(alert => {

        setTimeout(() => {

            alert.classList.add("hide");

            alert.addEventListener("animationend", () => {
                alert.remove();
            });

        }, 10000); // 10 ثانیه

    });

});

// ========== کد مربوط به سرچ لایه تمام صفحه (فقط باز و بسته شدن) ==========
(function() {
    const fullLayer = document.getElementById('fullscreenLayer');
    const openBtn = document.getElementById('magicOpenBtn');
    const closeBtn = document.getElementById('closeLayerBtn');

    // باز کردن لایه
    function openLayer() {
        if (fullLayer) {
            fullLayer.classList.add('active');
            document.body.classList.add('no-scroll');
        }
    }

    // بستن لایه
    function closeLayer() {
        if (fullLayer) {
            fullLayer.classList.remove('active');
            document.body.classList.remove('no-scroll');
        }
    }

    // رویداد باز کردن
    if (openBtn) {
        openBtn.addEventListener('click', openLayer);
    }

    // رویداد بستن
    if (closeBtn) {
        closeBtn.addEventListener('click', closeLayer);
    }

    // بستن با کلیک روی پس‌زمینه لایه
    if (fullLayer) {
        fullLayer.addEventListener('click', function(e) {
            if (e.target === fullLayer) {
                closeLayer();
            }
        });
    }

    // بستن با دکمه Escape
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && fullLayer && fullLayer.classList.contains('active')) {
            closeLayer();
        }
    });
})();

// ========== کد مربوط به منوی کناری (سایدبار) ==========
(function() {
    const menuBtn = document.getElementById('menuToggleBtn');
    const drawer = document.getElementById('drawerSidebar');
    const closeBtn = document.getElementById('closeDrawerBtn');
    const overlay = document.getElementById('drawerOverlay');

    function openDrawer() {
        if (drawer) drawer.classList.add('open');
        if (overlay) overlay.classList.add('active');
        document.body.classList.add('no-scroll');
    }

    function closeDrawer() {
        if (drawer) drawer.classList.remove('open');
        if (overlay) overlay.classList.remove('active');
        document.body.classList.remove('no-scroll');
    }

    // باز کردن
    if (menuBtn) {
        menuBtn.addEventListener('click', openDrawer);
    }

    // بستن با دکمه ضربدر
    if (closeBtn) {
        closeBtn.addEventListener('click', closeDrawer);
    }

    // بستن با کلیک روی اوورلی
    if (overlay) {
        overlay.addEventListener('click', closeDrawer);
    }

    // بستن با Escape
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && drawer && drawer.classList.contains('open')) {
            closeDrawer();
        }
    });
})();



document.addEventListener('DOMContentLoaded', function() {

    const form = document.getElementById('searchFormMobile');
    const input = document.getElementById('searchInputMobile');
    const recentList = document.getElementById('recentTagList');

    // نمایش جستجوهای ذخیره شده
    renderRecentSearches();

    form.addEventListener('submit', function() {

        const searchTerm = input.value.trim();

        if (!searchTerm) return;

        let searches = JSON.parse(localStorage.getItem('recentSearches')) || [];

        // حذف تکراری
        searches = searches.filter(item => item !== searchTerm);

        // اضافه کردن به اول لیست
        searches.unshift(searchTerm);

        // فقط 10 مورد آخر
        searches = searches.slice(0, 10);

        localStorage.setItem('recentSearches', JSON.stringify(searches));
    });

    function renderRecentSearches() {

        const searches = JSON.parse(localStorage.getItem('recentSearches')) || [];

        recentList.innerHTML = '';

        searches.forEach(term => {

            const span = document.createElement('span');

            span.className = 'recent-tag-item';
            span.textContent = term;

            span.addEventListener('click', function() {
                input.value = term;
                input.focus();
            });

            recentList.appendChild(span);
        });
    }

});

document.getElementById('clearRecentSearches').addEventListener('click', function() {
    localStorage.removeItem('recentSearches');
    document.getElementById('recentTagList').innerHTML = '';
});






// ========== منوی دسته‌بندی موبایل (تمام صفحه) ==========
(function() {
    const categoriesLayer = document.getElementById('mobileCategoriesLayer');
    const openBtn = document.getElementById('nav-category');  // دکمه دسته‌بندی در منوی پایین
    const closeBtn = document.getElementById('closeCategoriesLayer');

    // توابع باز و بسته کردن
    function openMobileCategories() {
        if (!categoriesLayer) return;
        categoriesLayer.classList.add('active');
        document.body.classList.add('no-scroll-categories');
        // جلوگیری از اسکرول پشت لایه (اختیاری)
        if (typeof lockScroll === 'function') {
            lockScroll();
        } else {
            document.body.style.overflow = 'hidden';
        }
    }

    function closeMobileCategories() {
        if (!categoriesLayer) return;
        categoriesLayer.classList.remove('active');
        document.body.classList.remove('no-scroll-categories');
        if (typeof unlockScroll === 'function') {
            unlockScroll();
        } else {
            document.body.style.overflow = '';
        }
        // بستن تمام پنل‌های باز (اختیاری)
        document.querySelectorAll('.mobile-category-item.expanded').forEach(item => {
            item.classList.remove('expanded');
        });
    }

    // باز کردن با کلیک روی دکمه دسته‌بندی در نوار پایین
    if (openBtn) {
        openBtn.addEventListener('click', function(e) {
            e.preventDefault();
            openMobileCategories();
        });
    }

    // بستن با دکمه ضربدر
    if (closeBtn) {
        closeBtn.addEventListener('click', closeMobileCategories);
    }

    // بستن با کلیک روی پس‌زمینه (خود لایه) – فقط اگر روی header یا close کلیک نشده باشد
    if (categoriesLayer) {
        categoriesLayer.addEventListener('click', function(e) {
            if (e.target === categoriesLayer) {
                closeMobileCategories();
            }
        });
    }

    // بستن با دکمه Escape
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && categoriesLayer && categoriesLayer.classList.contains('active')) {
            closeMobileCategories();
        }
    });

    // منطق باز/بسته شدن هر دسته (اکاردئونی)
    const categoryHeaders = document.querySelectorAll('.mobile-category-header');
    categoryHeaders.forEach(header => {
        header.addEventListener('click', function(e) {
            e.stopPropagation();
            const parentItem = this.closest('.mobile-category-item');
            if (parentItem) {
                // بستن سایر دسته‌ها (اختیاری: برای تجربه مشابه دیجی‌کالا می‌توانید فقط همین را تغییر دهید)
                // اگر می‌خواهید همزمان فقط یکی باز باشد، خط زیر را فعال کنید:
                // document.querySelectorAll('.mobile-category-item.expanded').forEach(item => {
                //     if (item !== parentItem) item.classList.remove('expanded');
                // });
                parentItem.classList.toggle('expanded');
            }
        });
    });
})();










