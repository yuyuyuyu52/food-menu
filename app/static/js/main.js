/**
 * 主要JavaScript文件
 */

document.addEventListener('DOMContentLoaded', function() {
    // 激活工具提示
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // 自动关闭闪现消息
    var alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            var closeButton = alert.querySelector('.btn-close');
            if (closeButton) {
                closeButton.click();
            } else {
                alert.style.opacity = 0;
                setTimeout(function() {
                    alert.remove();
                }, 500);
            }
        }, 5000);
    });
    
    // 为确认删除添加事件监听器
    var confirmDeleteButtons = document.querySelectorAll('[data-confirm-delete]');
    confirmDeleteButtons.forEach(function(button) {
        button.addEventListener('click', function(event) {
            if (!confirm('确定要删除吗？此操作不可恢复！')) {
                event.preventDefault();
            }
        });
    });
});

/**
 * nl2br - 将换行符转换为 <br> 标签
 * @param {string} str - 要转换的字符串
 * @return {string} - 转换后的字符串
 */
function nl2br(str) {
    if (typeof str !== 'string') return '';
    return str.replace(/\n/g, '<br>');
}

/**
 * 动态调整文本区域的高度
 * @param {HTMLElement} element - 文本区域元素
 */
function autoResize(element) {
    element.style.height = 'auto';
    element.style.height = (element.scrollHeight) + 'px';
}
