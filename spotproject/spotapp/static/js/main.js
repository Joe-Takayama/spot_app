document.addEventListener("DOMContentLoaded", () => {
  const slide = document.getElementById("slide");
  const items = document.querySelectorAll(".slide-item");
  const prev = document.getElementById("prev");
  const next = document.getElementById("next");
  const dots = document.querySelectorAll(".indicator .list");

  const total = items.length;
  let index = 0;
  let autoPlay;

  function updateSlide() {
    slide.style.transform = `translateX(-${index * 100}%)`;

    // ★ インジケーター更新
    dots.forEach((dot, i) => {
      dot.classList.toggle("active", i === index);
    });
  }

  function nextSlide() {
    index++;
    if (index >= total) index = 0;
    updateSlide();
  }

  function prevSlide() {
    index--;
    if (index < 0) index = total - 1;
    updateSlide();
  }

  function startAutoPlay() {
    autoPlay = setInterval(nextSlide, 3000);
  }

  function resetAutoPlay() {
    clearInterval(autoPlay);
    startAutoPlay();
  }

  next.addEventListener("click", () => {
    nextSlide();
    resetAutoPlay();
  });

  prev.addEventListener("click", () => {
    prevSlide();
    resetAutoPlay();
  });

  // ★ ぽちクリックで移動
  dots.forEach((dot, i) => {
    dot.addEventListener("click", () => {
      index = i;
      updateSlide();
      resetAutoPlay();
    });
  });

  updateSlide();   // 初期表示
  startAutoPlay();
});
