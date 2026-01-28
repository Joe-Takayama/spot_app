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

document.addEventListener("DOMContentLoaded", function () {

  // =========================
  // 地区・カテゴリ選択（検索はしない）
  // =========================
  const districtHidden = document.getElementById("search_district");
  const categoryHidden = document.getElementById("search_category");

  const districtBtn = document.getElementById("districtBtn");
  const categoryBtn = document.getElementById("categoryBtn");

  // ★ 地区ボタン色更新
  function updateDistrictColor(val) {
    if (!districtBtn) return;

    districtBtn.classList.remove("is-default");
    [...districtBtn.classList].forEach(c => {
      if (c.startsWith("d-")) districtBtn.classList.remove(c);
    });

    if (!val) {
      districtBtn.classList.add("is-default");
    } else {
      districtBtn.classList.add(`d-${val}`);
    }
  }

  // 初期状態
  updateDistrictColor(districtHidden?.value || "");

  // 地区クリック
  document.querySelectorAll(".district-item").forEach(a => {
    a.addEventListener("click", (e) => {
      e.preventDefault();
      e.stopPropagation();

      const val = a.dataset.value || "";
      const label = a.dataset.label || "地区別";

      if (districtHidden) districtHidden.value = val;
      if (districtBtn) districtBtn.textContent = `${label} ▼`;

      updateDistrictColor(val);
    });
  });

  // カテゴリ
  document.querySelectorAll(".category-item").forEach(a => {
    a.addEventListener("click", (e) => {
      e.preventDefault();
      e.stopPropagation();

      const val = a.dataset.value || "";
      const label = a.dataset.label || "カテゴリ";

      if (categoryHidden) categoryHidden.value = val;
      if (categoryBtn) categoryBtn.textContent = `${label} ▼`;
    });
  });

  // =========================
  // ナビのプルダウン開閉
  // =========================
  const navBlocks = document.querySelectorAll(".Nav-block");

  navBlocks.forEach(block => {
    const btn = block.querySelector(".Menu_btn");
    const down = block.querySelector(".menu_down");
    if (!btn || !down) return;

    btn.addEventListener("click", (e) => {
      e.preventDefault();
      e.stopPropagation();

      navBlocks.forEach(b => {
        if (b !== block) b.classList.remove("open");
      });

      block.classList.toggle("open");
    });

    down.addEventListener("click", e => e.stopPropagation());
  });

  document.addEventListener("click", () => {
    navBlocks.forEach(b => b.classList.remove("open"));
  });
});
