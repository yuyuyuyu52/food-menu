// 计算并设置header高度
document.addEventListener('DOMContentLoaded', function() {
    // 获取和设置实际的顶部导航栏高度
    const header = document.querySelector('header');
    if (header) {
        const headerHeight = header.offsetHeight;
        document.documentElement.style.setProperty('--header-height', headerHeight + 'px');
    }
    
    // 窗口大小改变时重新计算
    window.addEventListener('resize', function() {
        if (header) {
            const headerHeight = header.offsetHeight;
            document.documentElement.style.setProperty('--header-height', headerHeight + 'px');
        }
    });
});
