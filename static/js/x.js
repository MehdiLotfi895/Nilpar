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





document.addEventListener('DOMContentLoaded', function () {
  const track = document.getElementById('offerTrack');
  const prevBtn = document.getElementById('offerPrevBtn');
  const nextBtn = document.getElementById('offerNextBtn');

  if (!track || !prevBtn || !nextBtn) return;

  let currentIndex = 0;
  let cardsPerView = getCardsPerView();
  let step = 0;
  let isRTL = false;

  // تشخیص راست‌چین بودن (RTL)
  function detectRTL() {
      const section = document.querySelector('.offer_products_section');
      if (section) {
          const direction = window.getComputedStyle(section).direction;
          isRTL = direction === 'rtl';
      } else {
          // fallback: بررسی dir روی body یا html
          isRTL = document.documentElement.getAttribute('dir') === 'rtl' ||
                  document.body.getAttribute('dir') === 'rtl';
      }
      return isRTL;
  }

  // تعداد کارت قابل نمایش بر اساس عرض صفحه (مطابق با CSS)
  function getCardsPerView() {
      const width = window.innerWidth;
      if (width >= 1500) return 4;
      if (width >= 1200) return 3;   // 1200 تا 1499 => 3 کارت
      if (width >= 900) return 3;    // 900 تا 1199 => 3 کارت
      if (width >= 600) return 2;    // 600 تا 899 => 2 کارت
      return 1;                      // 300 تا 599 => 1 کارت
  }

  // محاسبه عرض هر کارت + گپ (step)
  function getStep() {
      const firstCard = track.querySelector('.product_card_item');
      if (!firstCard) return 0;
      const cardWidth = firstCard.getBoundingClientRect().width;
      const gap = parseFloat(getComputedStyle(track).gap) || 16;
      return cardWidth + gap;
  }

  // حداکثر ایندکس ممکن
  function getMaxIndex() {
      const totalCards = track.querySelectorAll('.product_card_item').length;
      return Math.max(0, totalCards - cardsPerView);
  }

  // محدود کردن currentIndex در بازه مجاز
  function clampIndex() {
      const maxIndex = getMaxIndex();
      if (currentIndex > maxIndex) currentIndex = maxIndex;
      if (currentIndex < 0) currentIndex = 0;
  }

  // به‌روزرسانی وضعیت دکمه‌ها
  function updateButtons() {
      const maxIndex = getMaxIndex();
      prevBtn.disabled = currentIndex <= 0;
      nextBtn.disabled = currentIndex >= maxIndex;
  }

  // رندر حرکت با در نظر گرفتن RTL
  function render() {
      step = getStep();
      const translation = currentIndex * step;
      // در حالت RTL، برای رفتن به کارت بعدی باید به سمت مثبت translate کنیم
      const translateValue = isRTL ? translation : -translation;
      track.style.transform = `translateX(${translateValue}px)`;
      updateButtons();
  }

  // رویداد دکمه قبلی
  prevBtn.addEventListener('click', function () {
      currentIndex -= 1;
      clampIndex();
      render();
  });

  // رویداد دکمه بعدی
  nextBtn.addEventListener('click', function () {
      currentIndex += 1;
      clampIndex();
      render();
  });

  // هنگام تغییر اندازه صفحه
  window.addEventListener('resize', function () {
      const newCardsPerView = getCardsPerView();
      if (newCardsPerView !== cardsPerView) {
          cardsPerView = newCardsPerView;
          // پس از تغییر تعداد کارت‌ها، ایندکس فعلی را مجدداً محدود کن
          clampIndex();
      }
      // حتی اگر تعداد کارت تغییر نکرده، ممکن است عرض کارت‌ها تغییر کرده باشد
      render();
  });

  // یک بار تشخیص RTL
  detectRTL();
  // مقداردهی اولیه
  clampIndex();
  render();
});


document.addEventListener('DOMContentLoaded', function () {
  const track = document.getElementById('sliderTrack');
  const prevBtn = document.getElementById('testimonialPrev');
  const nextBtn = document.getElementById('testimonialNext');

  if (!track || !prevBtn || !nextBtn) return;

  function getGap() {
      const style = window.getComputedStyle(track);
      const gap = parseFloat(style.gap || style.columnGap || '0');
      return Number.isFinite(gap) ? gap : 0;
  }

  function getStep() {
      const card = track.querySelector('.card-item');
      if (!card) return 0;
      const cardWidth = card.getBoundingClientRect().width;
      return cardWidth + getGap();
  }

  function updateButtons() {
      const maxScrollLeft = track.scrollWidth - track.clientWidth;

      prevBtn.disabled = track.scrollLeft <= 1;
      nextBtn.disabled = track.scrollLeft >= maxScrollLeft - 1;
  }

  function scrollNext() {
      const step = getStep();
      if (!step) return;
      track.scrollBy({ left: step, behavior: 'smooth' });
  }

  function scrollPrev() {
      const step = getStep();
      if (!step) return;
      track.scrollBy({ left: -step, behavior: 'smooth' });
  }

  nextBtn.addEventListener('click', scrollNext);
  prevBtn.addEventListener('click', scrollPrev);

  track.addEventListener('scroll', updateButtons, { passive: true });
  window.addEventListener('resize', updateButtons);

  document.querySelectorAll('.product-img img, .card-item').forEach(el => {
      el.addEventListener('dragstart', e => e.preventDefault());
  });

  updateButtons();
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