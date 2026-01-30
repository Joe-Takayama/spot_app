document.addEventListener("DOMContentLoaded", () => {
  // ① 全スライド取得
  let items = Array.from(document.querySelectorAll(".slide-item"));

  // ② Fisher-Yates シャッフルでランダム並び替え
  for (let i = items.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [items[i], items[j]] = [items[j], items[i]];
  }

  // ③ 先頭10枚だけ使う
  items = items.slice(0, 10);
    
  // ④ HTML の slide コンテナに10枚だけ入れ直す
  const slide = document.getElementById("slide");
  slide.innerHTML = ""; // 一旦クリア
  items.forEach(item => slide.appendChild(item));

  // ここでインジケーター調整
  const indicator = document.getElementById("indicator");
  indicator.innerHTML = ""; // 初期化

  for (let i = 0; i < items.length; i++) {
    const li = document.createElement("li");
    li.classList.add("list");
    indicator.appendChild(li);
  }

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
    autoPlay = setInterval(nextSlide, 4000);
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
