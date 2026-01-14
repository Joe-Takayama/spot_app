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
});