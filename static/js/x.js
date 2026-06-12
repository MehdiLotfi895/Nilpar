(function() {
  const images = document.querySelectorAll('.slider-image');
  const prevBtn = document.getElementById('sliderPrevBtn');
  const nextBtn = document.getElementById('sliderNextBtn');
  const dots = document.querySelectorAll('.dot');
  let currentIndex = 0;
  const totalSlides = images.length;
  let autoSlideInterval;
  const slideLinks = document.querySelectorAll('.image-slider-wrapper a');
  // تابع نمایش اسلاید مشخص
  function showSlide(index) {
    // normalize index
    if (index < 0) index = totalSlides - 1;
    if (index >= totalSlides) index = 0;
    
    // مخفی کردن همه اسلایدها
    images.forEach(img => img.classList.remove('active'));
    dots.forEach(dot => dot.classList.remove('active'));
    
    // نمایش اسلاید جدید
    images[index].classList.add('active');
    if (dots[index]) dots[index].classList.add('active');
    
    currentIndex = index;
  }

  // حرکت به اسلاید بعدی (برای تایمر خودکار)
  function nextSlide() {
    showSlide(currentIndex + 1);
  }

  // شروع تایمر خودکار
  function startAutoSlide() {
    if (autoSlideInterval) clearInterval(autoSlideInterval);
    autoSlideInterval = setInterval(nextSlide, 5000); 
  }
  
  // توقف تایمر خودکار (و راه‌اندازی مجدد بعد از کلیک)
  function resetAutoSlide() {
    startAutoSlide();
  }

  // رویداد دکمه قبلی
  if (prevBtn) {
    prevBtn.addEventListener('click', () => {
      showSlide(currentIndex - 1);
      resetAutoSlide();
    });
  }
  
  // رویداد دکمه بعدی
  if (nextBtn) {
    nextBtn.addEventListener('click', () => {
      showSlide(currentIndex + 1);
      resetAutoSlide();
    });
  }
  
  // رویداد کلیک روی هر دایره
  dots.forEach((dot, idx) => {
    dot.addEventListener('click', () => {
      showSlide(idx);
      resetAutoSlide();
    });
  });
  
  // قابلیت کیبورد (فلش چپ/راست)
  document.addEventListener('keydown', (e) => {
    const activeTag = document.activeElement?.tagName;
    if (activeTag === 'INPUT' || activeTag === 'TEXTAREA') return;
    if (e.key === 'ArrowRight') {
      e.preventDefault();
      showSlide(currentIndex + 1);
      resetAutoSlide();
    } else if (e.key === 'ArrowLeft') {
      e.preventDefault();
      showSlide(currentIndex - 1);
      resetAutoSlide();
    }
  });
  
  
  
  // نمایش اولین اسلاید و شروع خودکار
  if (!document.querySelector('.slider-image.active')) {
    showSlide(0);
  }
  startAutoSlide();
})();


// const cont = document.getElementById('scrollContainer');
// const leftBtn = document.getElementById('scrollLeftBtn');
// const rightBtn = document.getElementById('scrollRightBtn');

// leftBtn.onclick = () => cont.scrollLeft -= 300;
// rightBtn.onclick = () => cont.scrollLeft += 300;

// rightBtn.disabled = false;
// leftBtn.disabled = true;


// const cont = document.getElementById('scrollContainer');
// const leftBtn = document.getElementById('scrollLeftBtn'); // دکمه‌ای که به چپ می‌برد (برای رفتن به انتها)
// const rightBtn = document.getElementById('scrollRightBtn'); // دکمه‌ای که به راست می‌برد (برای برگشتن به شروع)

// // تابع به‌روزرسانی وضعیت دکمه‌ها
// function updateButtons() {
//   // در حالت RTL:
//   // scrollLeft <= 0 یعنی در ابتدای محتوا (سمت راست) هستیم.
//   // scrollLeft >= maxScroll یعنی در انتهای محتوا (سمت چپ) هستیم.
  
//   const maxScroll = cont.scrollWidth - cont.clientWidth;
//   const currentScroll = cont.scrollLeft;

//   // اگر در ابتدای محتوا (سمت راست) هستیم:
//   if (currentScroll <= 0) {
//     // دکمه‌ای که به راست می‌رود (برگشت به شروع) غیرفعال است
//     rightBtn.disabled = true;
//     // دکمه‌ای که به چپ می‌رود (به سمت انتها) فعال است
//     leftBtn.disabled = false;
//   } 
//   // اگر در انتهای محتوا (سمت چپ) هستیم:
//   else if (currentScroll >= maxScroll - 2) { // -2 برای دقت بیشتر
//     // دکمه‌ای که به چپ می‌رود (به سمت انتها) غیرفعال است
//     leftBtn.disabled = true;
//     // دکمه‌ای که به راست می‌رود (برگشت به شروع) فعال است
//     rightBtn.disabled = false;
//   } 
//   // در حالت وسط:
//   else {
//     leftBtn.disabled = false;
//     rightBtn.disabled = false;
//   }
// }

// // اسکرول با دکمه‌ها
// leftBtn.onclick = () => {
//   // در RTL، اسکرول به چپ یعنی کاهش scrollLeft
//   cont.scrollLeft -= 300;
// };

// rightBtn.onclick = () => {
//   // در RTL، اسکرول به راست یعنی افزایش scrollLeft
//   cont.scrollLeft += 300;
// };

// // گوش دادن به رویداد اسکرول برای به‌روز کردن دکمه‌ها
// cont.addEventListener('scroll', updateButtons);

// // تنظیم اولیه وضعیت دکمه‌ها (در بارگذاری صفحه، ما در ابتدای لیست هستیم)
// updateButtons();

const cont = document.getElementById('scrollContainer');
const leftBtn = document.getElementById('scrollLeftBtn');   // دکمه چپ (رفتن به انتها)
const rightBtn = document.getElementById('scrollRightBtn'); // دکمه راست (برگشت به شروع)

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
  cont.scrollLeft -= 250;  // حرکت به چپ = کاهش scrollLeft = رفتن به انتها
};

rightBtn.onclick = () => {
  cont.scrollLeft += 250;  // حرکت به راست = افزایش scrollLeft = برگشت به شروع
};

cont.addEventListener('scroll', updateButtons);
updateButtons();




const contlast = document.getElementById('scrollWrapper');
const leftBtnlast = document.getElementById('scrollLeftBtnLast');   // دکمه چپ (رفتن به انتها)
const rightBtnlast = document.getElementById('scrollRightBtnLast'); // دکمه راست (برگشت به شروع)

function updateButtonsLast() {
  const maxScroll = contlast.scrollWidth - contlast.clientWidth;
  const currentScroll = Math.abs(contlast.scrollLeft); // مقدار مطلق برای مقایسه راحت‌تر
  
  // اگر در ابتدای محتوا (سمت راست) هستیم: scrollLeft = 0
  if (currentScroll <= 1) {
    rightBtnlast.disabled = true;  // دکمه برگشت به شروع غیرفعال
    leftBtnlast.disabled = false;  // دکمه رفتن به انتها فعال
  } 
  // اگر در انتهای محتوا (سمت چپ) هستیم: |scrollLeft| = maxScroll
  else if (currentScroll >= maxScroll - 2) {
    leftBtnlast.disabled = true;   // دکمه رفتن به انتها غیرفعال
    rightBtnlast.disabled = false; // دکمه برگشت به شروع فعال
  } 
  // در حالت وسط
  else {
    leftBtnlast.disabled = false;
    rightBtnlast.disabled = false;
  }
}

// اسکرول با دکمه‌ها (در RTL، scrollLeft منفی است)
leftBtnlast.onclick = () => {
  contlast.scrollLeft -=287;  // حرکت به چپ = کاهش scrollLeft = رفتن به انتها
};

rightBtnlast.onclick = () => {
  contlast.scrollLeft += 287;  // حرکت به راست = افزایش scrollLeft = برگشت به شروع
};

contlast.addEventListener('scroll', updateButtonsLast);
updateButtonsLast();









const cont1 = document.getElementById('offerScrollWrapper');
const leftBtn1 = document.getElementById('scrollLeftBtnOffer');   // دکمه چپ (رفتن به انتها)
const rightBtn1 = document.getElementById('scrollRightBtnOffer'); // دکمه راست (برگشت به شروع)

function updateButtonsOffer() {
  const maxScroll = cont1.scrollWidth - cont1.clientWidth;
  const currentScroll = Math.abs(cont1.scrollLeft); // مقدار مطلق برای مقایسه راحت‌تر
  
  // اگر در ابتدای محتوا (سمت راست) هستیم: scrollLeft = 0
  if (currentScroll <= 1) {
    rightBtn1.disabled = true;  // دکمه برگشت به شروع غیرفعال
    leftBtn1.disabled = false;  // دکمه رفتن به انتها فعال
  } 
  // اگر در انتهای محتوا (سمت چپ) هستیم: |scrollLeft| = maxScroll
  else if (currentScroll >= maxScroll - 2) {
    leftBtn1.disabled = true;   // دکمه رفتن به انتها غیرفعال
    rightBtn1.disabled = false; // دکمه برگشت به شروع فعال
  } 
  // در حالت وسط
  else {
    leftBtn1.disabled = false;
    rightBtn1.disabled = false;
  }
}

// اسکرول با دکمه‌ها (در RTL، scrollLeft منفی است)
leftBtn1.onclick = () => {
  cont1.scrollLeft -= 287;  // حرکت به چپ = کاهش scrollLeft = رفتن به انتها
};

rightBtn1.onclick = () => {
  cont1.scrollLeft += 287;  // حرکت به راست = افزایش scrollLeft = برگشت به شروع
};

cont1.addEventListener('scroll', updateButtonsOffer);
updateButtonsOffer();





document.addEventListener('DOMContentLoaded', function() {
  const wrapper = document.querySelector('.offer_products_grid_wrapper');
  
  if (!wrapper) return;
  
  let currentIndex = 0;
  let autoScrollInterval;
  let lastScrollTop = 0;
  
  // محاسبه عرض هر محصول + gap
  function getStepWidth() {
      const product = document.querySelector('.product_card_item');
      if (!product) return 235;
      const productWidth = product.offsetWidth;
      const style = window.getComputedStyle(wrapper);
      const gap = parseInt(style.gap) || 15;
      return productWidth + gap;
  }
  
  // اسکرول به محصول بعدی (در RTL به سمت چپ)
  function scrollToNext() {
      const products = document.querySelectorAll('.product_card_item');
      if (products.length === 0) return;
      
      const stepWidth = getStepWidth();
      const maxIndex = products.length - 1;
      
      if (currentIndex >= maxIndex) {
          currentIndex = 0;
          wrapper.scrollLeft = 0;
      } else {
          currentIndex++;
          wrapper.scrollLeft = -(currentIndex * stepWidth);
      }
  }
  
  // غیرفعال کردن اسکرول افقی با حفظ اسکرول عمودی
  wrapper.addEventListener('wheel', function(e) {
      // ذخیره موقعیت اسکرول عمودی فعلی
      const currentScrollTop = wrapper.scrollTop;
      
      // جلوگیری از اسکرول افقی
      if (e.deltaX !== 0) {
          e.preventDefault();
      }
      
      // اجازه اسکرول عمودی
      if (e.deltaY !== 0) {
          wrapper.scrollTop = currentScrollTop + e.deltaY;
      }
  }, { passive: false });
  
  // شروع اسکرول خودکار
  function startAutoScroll() {
      if (autoScrollInterval) clearInterval(autoScrollInterval);
      autoScrollInterval = setInterval(scrollToNext, 2000);
  }
  
  // توقف با hover
  wrapper.addEventListener('mouseenter', function() {
      if (autoScrollInterval) clearInterval(autoScrollInterval);
  });
  
  wrapper.addEventListener('mouseleave', startAutoScroll);
  
  // شروع حرکت
  startAutoScroll();
});



document.addEventListener('DOMContentLoaded', function() {
  const carouselCage = document.getElementById('carouselCage');
  if (!carouselCage) return;

  let currentIndex = 0;
  let autoScrollInterval;
  let isHovering = false;
  let isRTL = false;

  // تشخیص جهت صفحه (RTL یا LTR)
  function detectRTL() {
    const direction = window.getComputedStyle(carouselCage).direction;
    return direction === 'rtl';
  }

  // محاسبه عرض گام (عرض کارت + فاصله)
  function getStepWidth() {
    const card = document.querySelector('.card-item');
    if (!card) return 274; // 250px عرض + 24px gap تقریبی
    const cardWidth = card.getBoundingClientRect().width;
    if (cardWidth === 0) return 274;
    const track = carouselCage.querySelector('.slider-track');
    if (!track) return cardWidth + 24;
    const style = window.getComputedStyle(track);
    const gap = parseFloat(style.gap) || 0;
    return cardWidth + gap;
  }

  // حرکت به کارت بعدی
  function scrollToNext() {
    const cards = document.querySelectorAll('.card-item');
    if (cards.length === 0) return;

    const step = getStepWidth();
    const maxIndex = cards.length - 1;

    if (currentIndex >= maxIndex) {
      // رسیدیم به آخر: بدون انیمیشن به اول برگرد
      currentIndex = 0;
      carouselCage.style.scrollBehavior = 'auto';
      carouselCage.scrollLeft = 0;
      // force reflow
      void carouselCage.offsetHeight;
      carouselCage.style.scrollBehavior = 'smooth';
    } else {
      currentIndex++;
      // محاسبه مقدار اسکرول بر اساس جهت صفحه
      let scrollAmount = currentIndex * step;
      if (isRTL) {
        // در RTL، scrollLeft به سمت چپ بیشتر می‌شود، پس خود scrollAmount همان مقدار مورد نیاز است
        carouselCage.scrollLeft = scrollAmount;
      } else {
        carouselCage.scrollLeft = scrollAmount;
      }
    }
  }

  // شروع اسکرول خودکار
  function startAutoScroll() {
    if (autoScrollInterval) clearInterval(autoScrollInterval);
    autoScrollInterval = setInterval(() => {
      if (!document.hidden && !isHovering) {
        scrollToNext();
      }
    }, 2800);
  }

  // توقف با هاور
  carouselCage.addEventListener('mouseenter', () => {
    isHovering = true;
    if (autoScrollInterval) clearInterval(autoScrollInterval);
  });
  carouselCage.addEventListener('mouseleave', () => {
    isHovering = false;
    startAutoScroll();
  });

  // جلوگیری از اسکرول افقی دستی
  carouselCage.addEventListener('wheel', (e) => {
    if (Math.abs(e.deltaX) > Math.abs(e.deltaY) || e.deltaX !== 0) {
      e.preventDefault();
    }
  }, { passive: false });

  // غیرفعال کردن لمس افقی
  let touchStartX = 0;
  carouselCage.addEventListener('touchstart', (e) => {
    touchStartX = e.touches[0].clientX;
  });
  carouselCage.addEventListener('touchmove', (e) => {
    const deltaX = e.touches[0].clientX - touchStartX;
    if (Math.abs(deltaX) > 5) {
      e.preventDefault();
    }
  }, { passive: false });

  // جلوگیری از درگ تصاویر
  document.querySelectorAll('.product-img, .card-item').forEach(el => {
    el.addEventListener('dragstart', (e) => e.preventDefault());
  });

  // مقداردهی اولیه
  function init() {
    isRTL = detectRTL();
    // اطمینان از smooth scroll در CSS
    carouselCage.style.scrollBehavior = 'smooth';
    // ریست موقعیت به اول
    carouselCage.scrollLeft = 0;
    currentIndex = 0;
    startAutoScroll();
  }

  // صبر برای بارگذاری کامل تصاویر (اختیاری)
  const imgs = document.querySelectorAll('.product-img');
  if (imgs.length === 0) {
    init();
  } else {
    let loaded = 0;
    imgs.forEach(img => {
      if (img.complete) loaded++;
      else {
        img.addEventListener('load', () => { loaded++; if (loaded === imgs.length) init(); });
        img.addEventListener('error', () => { loaded++; if (loaded === imgs.length) init(); });
      }
    });
    if (loaded === imgs.length) init();
  }

  // در صورت تغییر سایز پنجره، موقعیت را تنظیم مجدد کن
  window.addEventListener('resize', () => {
    const step = getStepWidth();
    carouselCage.scrollLeft = currentIndex * step;
  });
});





document.addEventListener('DOMContentLoaded', function() {
  const adWrapper = document.querySelector('.ad-suggest-wrapper');
  if (!adWrapper) return;
  
  const adContainer = adWrapper.querySelector('.ad-suggest-container');
  const adLeftBtn = adWrapper.querySelector('.ad-scroll-left');
  const adRightBtn = adWrapper.querySelector('.ad-scroll-right');
  
  if (!adContainer || !adLeftBtn || !adRightBtn) return;
  
  // تابع برای محاسبه عرض یک باکس کامل + gap
  function getScrollAmount() {
      const boxes = adContainer.querySelectorAll('.ad-suggest-box');
      if (boxes.length === 0) return 300; // مقدار پیش‌فرض
      
      const firstBox = boxes[0];
      const boxWidth = firstBox.offsetWidth;
      
      // گرفتن gap از استایل محاسبه شده
      const containerStyle = window.getComputedStyle(adContainer);
      const gap = parseFloat(containerStyle.gap) || 0;
      
      // مقدار اسکرول = عرض باکس + gap
      return boxWidth + gap;
  }
  
  // اسکرول به چپ (به اندازه یک عکس)
  adLeftBtn.addEventListener('click', function() {
      const scrollAmount = getScrollAmount();
      adContainer.scrollBy({
          left: -scrollAmount,
          behavior: 'smooth'
      });
  });
  
  // اسکرول به راست (به اندازه یک عکس)
  adRightBtn.addEventListener('click', function() {
      const scrollAmount = getScrollAmount();
      adContainer.scrollBy({
          left: scrollAmount,
          behavior: 'smooth'
      });
  });
  
  // (اختیاری) وقتی صفحه resize بشه، دکمه‌ها به درستی کار می‌کنن
  let resizeTimer;
  window.addEventListener('resize', function() {
      clearTimeout(resizeTimer);
      resizeTimer = setTimeout(function() {
          // فقط برای رفرش کردن مقدار - کار خاصی نیاز نیست
      }, 250);
  });
});