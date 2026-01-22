document.addEventListener('DOMContentLoaded', function() {
    // すべてのドロップダウンボタンを取得
    const dropdownButtons = document.querySelectorAll('.Nav-block .Menu_btn');

    dropdownButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.stopPropagation(); // イベントの伝播を止める

            const parent = this.parentElement; // .Nav-block
            const isAlreadyActive = parent.classList.contains('active');

            // まず全部閉じる
            document.querySelectorAll('.Nav-block').forEach(item => {
                item.classList.remove('active');
            });

            // 自分が閉じてなかったら開く（トグル）
            if (!isAlreadyActive) {
                parent.classList.add('active');
            }
        });
    });

    // メニュー外をクリックしたら全部閉じる
    document.addEventListener('click', function(e) {
        if (!e.target.closest('.Nav-block')) {
            document.querySelectorAll('.Nav-block').forEach(item => {
                item.classList.remove('active');
            });
        }
    });
    const districtHidden = document.getElementById("search_district");
    const categoryHidden = document.getElementById("search_category");

    const districtBtn = document.getElementById("districtBtn");
    const categoryBtn = document.getElementById("categoryBtn");

    // 地区
    document.querySelectorAll(".district-item").forEach(a => {
        a.addEventListener("click", (e) => {
        e.preventDefault();       // ← 遷移（検索）を止める
        e.stopPropagation();

        const val = a.dataset.value || "";
        const label = a.dataset.label || "地区別";

        if (districtHidden) districtHidden.value = val;
        if (districtBtn) districtBtn.textContent = `${label} ▼`;
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
});
