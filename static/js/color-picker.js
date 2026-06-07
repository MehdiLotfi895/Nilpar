document.addEventListener("DOMContentLoaded", function () {
    
    // ═══════════════════════════════════════
    // المنت‌ها
    // ═══════════════════════════════════════
    const container = document.getElementById('circlesContainer');
    if (!container) return; // اگه المنت نبود، کار نکن

    const circles = container.querySelectorAll('.color-circle');
    const selectedSpan = document.getElementById('selectedColorValue');
    const hiddenInput = document.getElementById('hiddenColorInput');

    // ═══════════════════════════════════════
    // تابع محاسبه روشنایی رنگ (برای رنگ تیک)
    // ═══════════════════════════════════════
    function getBrightness(hexColor) {
        const hex = hexColor.replace('#', '');
        if (hex.length !== 6) return 150; // پیش‌فرض
        const r = parseInt(hex.substr(0, 2), 16);
        const g = parseInt(hex.substr(2, 2), 16);
        const b = parseInt(hex.substr(4, 2), 16);
        return (r * 299 + g * 587 + b * 114) / 1000;
    }

    // ═══════════════════════════════════════
    // اعمال رنگ‌ها و استایل‌ها به دایره‌ها
    // ═══════════════════════════════════════
    circles.forEach((circle, index) => {
        // 1. گرفتن کد رنگ از HTML
        const colorCode = circle.getAttribute('data-color-code');
        
        if (colorCode) {
            circle.style.backgroundColor = colorCode;
        } else {
            // اگه کد رنگ تو دیتابیس خالی بود، یه رنگ پیش‌فرض
            circle.style.backgroundColor = '#CCCCCC';
        }

        // 2. تنظیم حاشیه (Border) بر اساس روشنایی
        const brightness = getBrightness(colorCode || '#CCCCCC');
        
        if (brightness > 180) {
            // رنگ روشن -> حاشیه تیره
            circle.style.border = '2px solid #999';
        } else {
            // رنگ تیره -> حاشیه روشن یا شفاف
            circle.style.border = '2px solid transparent';
        }

        // 3. تنظیم رنگ تیک (Checkmark)
        const checkmark = circle.querySelector('.checkmark');
        if (checkmark) {
            checkmark.style.color = brightness > 150 ? '#333' : '#fff';
            checkmark.style.textShadow = brightness > 150 
                ? '0 0 3px rgba(0,0,0,0.3)' 
                : '0 0 4px rgba(0,0,0,0.8)';
        }
    });

    // ═══════════════════════════════════════
    // تابع انتخاب رنگ
    // ═══════════════════════════════════════
    function selectColor(circleElement) {
        const colorName = circleElement.getAttribute('data-color-name');
        const colorCode = circleElement.getAttribute('data-color-code');
        
        // 1. حذف کلاس active از همه
        circles.forEach(c => c.classList.remove('active'));
        
        // 2. اضافه کردن به دایره کلیک شده
        circleElement.classList.add('active');
        
        // 3. به‌روزرسانی متن نمایشی
        if (selectedSpan) {
            selectedSpan.textContent = colorName;
            // اگه خواستی کد رنگ هم نمایش داده بشه:
            // selectedSpan.textContent = `${colorName} (${colorCode})`;
        }
        
        // 4. به‌روزرسانی اینپوت مخفی (مهم برای فرم)
        if (hiddenInput) {
            hiddenInput.value = colorName; 
        }
    }

    // ═══════════════════════════════════════
    // اضافه کردن رویداد کلیک
    // ═══════════════════════════════════════
    circles.forEach((circle) => {
        circle.addEventListener('click', function () {
            selectColor(this);
        });

        // دسترسی‌پذیری با کیبورد
        circle.setAttribute('tabindex', '0');
        circle.setAttribute('role', 'radio');
        
        circle.addEventListener('keydown', function (e) {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                selectColor(this);
            }
        });
    });

    // ═══════════════════════════════════════
    // اطمینان از اینکه همیشه یک دایره فعال هست
    // ═══════════════════════════════════════
    const activeCircles = document.querySelectorAll('.color-circle.active');
    if (activeCircles.length === 0 && circles.length > 0) {
        // اگه هیچکدوم active نبود (مثلاً اگه کلاس active رو از HTML حذف کردی)،
        // دایره اول رو فعال کن
        circles[0].classList.add('active');
        const firstColorName = circles[0].getAttribute('data-color-name');
        if (selectedSpan) selectedSpan.textContent = firstColorName;
        if (hiddenInput) hiddenInput.value = firstColorName;
    }
});



const plusBtn = document.querySelector('.plus-btn');
const minusBtn = document.querySelector('.minus-btn');
const counterSpan = document.getElementById('order-number_detail');
const hiddenInput = document.getElementById('hidden-quantity');
const counterContainer = document.querySelector('.counter-container');

// گرفتن حداکثر تعداد از attribute داده شده
const maxNumber = parseInt(counterContainer.getAttribute('data-max') || 10);

let currentNumber = 1;

// آپدیت کردن نمایش و فیلد مخفی
function updateCounter() {
    counterSpan.textContent = currentNumber;
    hiddenInput.value = currentNumber;
}

// دکمه مثبت
plusBtn.addEventListener('click', function() {
    if (currentNumber < maxNumber) {
        currentNumber++;
        updateCounter();
    } else {
        alert('تعداد سفارش نمی‌تواند بیشتر از ' + maxNumber + ' باشد');
    }
});

// دکمه منفی
minusBtn.addEventListener('click', function() {
    if (currentNumber > 1) {
        currentNumber--;
        updateCounter();
    }
    else{
        alert('تعداد سفارش نمیتواند کمتر از 1 باشد')
    }
});



// تابع نمایش پیام کپی شد
function showCopyMessage() {
    const copyMessage = document.getElementById('copyMessage');
    copyMessage.classList.add('show');
    
    // پنهان کردن پیام بعد از 2 ثانیه
    setTimeout(() => {
        copyMessage.classList.remove('show');
    }, 2000);
}

// تابع کپی کردن لینک
async function copyToClipboard(text) {
    try {
        await navigator.clipboard.writeText(text);
        showCopyMessage();
    } catch (err) {
        console.error('خطا در کپی لینک:', err);
        // روش جایگزین برای مرورگرهای قدیمی
        const textarea = document.createElement('textarea');
        textarea.value = text;
        document.body.appendChild(textarea);
        textarea.select();
        document.execCommand('copy');
        document.body.removeChild(textarea);
        showCopyMessage();
    }
}

// اضافه کردن event listener به دکمه اشتراک‌گذاری
document.addEventListener('DOMContentLoaded', function() {
    const shareButton = document.querySelector('.action-icon[data-share-link]');
    
    if (shareButton) {
        shareButton.addEventListener('click', async function(e) {
            e.preventDefault();
            const shareLink = this.getAttribute('data-share-link');
            
            // روش اول: استفاده از Web Share API (در موبایل)
            if (navigator.share) {
                try {
                    await navigator.share({
                        title: 'اشتراک‌گذاری محصول',
                        text: 'این محصول را ببینید!',
                        url: shareLink
                    });
                } catch (err) {
                    if (err.name !== 'AbortError') {
                        // اگر اشتراک‌گذاری موبایل کار نکرد، لینک را کپی کنیم
                        copyToClipboard(shareLink);
                    }
                }
            } else {
                // روش دوم: کپی لینک در دسکتاپ
                copyToClipboard(shareLink);
            }
        });
    }
});




document.addEventListener('DOMContentLoaded', function() {
    const img = document.getElementById('mainImage');
    const container = document.querySelector('.product-main-image');
    const zoomIcon = document.getElementById('zoomIcon');
    
    if (!img || !container || !zoomIcon) return;
    
    let zoomLevel = 2;
    let isZoomActive = false;
    
    // تابع فعال‌سازی زوم
    function enableZoom() {
        isZoomActive = true;
        container.classList.add('zoomed');
        zoomIcon.style.backgroundColor = 'rgba(0, 0, 0, 0.9)';
    }
    
    // تابع غیرفعال‌سازی زوم
    function disableZoom() {
        isZoomActive = false;
        container.classList.remove('zoomed');
        img.style.transform = 'scale(1)';
        img.style.transformOrigin = 'center center';
        zoomIcon.style.backgroundColor = 'rgba(0, 0, 0, 0.6)';
    }
    
    // کلیک روی آیکون ذره‌بین
    zoomIcon.addEventListener('click', function(e) {
        e.stopPropagation();
        if (isZoomActive) {
            disableZoom();
        } else {
            enableZoom();
        }
    });
    
    // حرکت موس برای زوم (فقط زمانی که زوم فعال باشد)
    container.addEventListener('mousemove', function(e) {
        if (!isZoomActive) return;
        
        const rect = container.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
        
        // اطمینان از مقادیر بین 0 تا 100
        const percentX = Math.min(Math.max((x / rect.width) * 100, 0), 100);
        const percentY = Math.min(Math.max((y / rect.height) * 100, 0), 100);
        
        img.style.transformOrigin = `${percentX}% ${percentY}%`;
        img.style.transform = `scale(${zoomLevel})`;
    });
    
    // خروج موس از کانتینر
    container.addEventListener('mouseleave', function() {
        if (isZoomActive) {
            img.style.transform = 'scale(1)';
            img.style.transformOrigin = 'center center';
        }
    });
    
    // ورود مجدد موس به کانتینر (برای حفظ زوم)
    container.addEventListener('mouseenter', function() {
        if (isZoomActive) {
            // موقعیت پیش‌فرض برای شروع زوم
            img.style.transformOrigin = 'center center';
            img.style.transform = `scale(${zoomLevel})`;
        }
    });
});


// تکراری

const cont = document.getElementById('scrollContainerDetail');
const leftBtn = document.getElementById('scrollLeftBtnDetail');   // دکمه چپ (رفتن به انتها)
const rightBtn = document.getElementById('scrollRightBtnDetail'); // دکمه راست (برگشت به شروع)

function updateButtons() {
  const maxScroll = cont.scrollWidth - cont.clientWidth;
  const currentScroll = Math.abs(cont.scrollLeft); // مقدار مطلق برای مقایسه راحت‌تر
  
  // اگر در ابتدای محتوا (سمت راست) هستیم: scrollLeft = 0
  if (currentScroll <= 1) {
    rightBtn.disabled = true;  // دکمه برگشت به شروع غیرفعال
    leftBtn.disabled = false;  // دکمه رفتن به انتها فعال
  } 
  // اگر در انتهای محتوا (سمت چپ) هستیم: |scrollLeft| = maxScroll
  else if (currentScroll >= maxScroll - 2) {
    leftBtn.disabled = true;   // دکمه رفتن به انتها غیرفعال
    rightBtn.disabled = false; // دکمه برگشت به شروع فعال
  } 
  // در حالت وسط
  else {
    leftBtn.disabled = false;
    rightBtn.disabled = false;
  }
}

// اسکرول با دکمه‌ها (در RTL، scrollLeft منفی است)
leftBtn.onclick = () => {
  cont.scrollLeft -= 287;  // حرکت به چپ = کاهش scrollLeft = رفتن به انتها
};

rightBtn.onclick = () => {
  cont.scrollLeft += 287;  // حرکت به راست = افزایش scrollLeft = برگشت به شروع
};

cont.addEventListener('scroll', updateButtons);
updateButtons();


