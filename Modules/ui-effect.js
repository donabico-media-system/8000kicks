// Modules/ui-effect.js
// Giả sử nút mua hàng của bạn có class là 'buy-button'
const btn = document.querySelector('.buy-button');
if (btn) {
    btn.style.transition = "transform 0.3s";
    btn.addEventListener('mouseover', () => {
        btn.style.transform = "scale(1.1)";
    });
    btn.addEventListener('mouseout', () => {
        btn.style.transform = "scale(1)";
    });
}
