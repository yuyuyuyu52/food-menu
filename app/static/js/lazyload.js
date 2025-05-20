/**
 * 图片懒加载功能
 */

// 当页面加载完成后初始化懒加载
document.addEventListener('DOMContentLoaded', function() {
    // 初始化IntersectionObserver
    const lazyImageObserver = new IntersectionObserver(function(entries, observer) {
        entries.forEach(function(entry) {
            // 当图片进入视口时
            if (entry.isIntersecting) {
                let lazyImage = entry.target;
                // 如果有data-src属性，将其设置为src
                if (lazyImage.dataset.src) {
                    console.time('图片加载: ' + lazyImage.dataset.src);
                    
                    // 创建一个新的Image对象来预加载
                    const tempImage = new Image();
                    
                    // 当图片加载成功时
                    tempImage.onload = function() {
                        lazyImage.src = lazyImage.dataset.src;
                        lazyImage.classList.remove('lazy-image');
                        lazyImage.classList.add('image-loaded');
                        console.timeEnd('图片加载: ' + lazyImage.dataset.src);
                    };
                    
                    // 当图片加载失败时
                    tempImage.onerror = function() {
                        // 设置为默认图片或保持原样
                        console.error('图片加载失败: ' + lazyImage.dataset.src);
                        // 可以设置一个默认图片
                        lazyImage.src = '/static/images/default-placeholder.jpg';
                        lazyImage.classList.remove('lazy-image');
                    };
                    
                    // 开始加载图片
                    tempImage.src = lazyImage.dataset.src;
                }
                
                // 图片已处理，不再观察
                observer.unobserve(lazyImage);
            }
        });
    }, {
        // 图片接近视口100px时开始加载
        rootMargin: '100px 0px',
        threshold: 0.01
    });
    
    // 获取所有带有lazy-image类的图片
    const lazyImages = document.querySelectorAll('.lazy-image');
    lazyImages.forEach(function(lazyImage) {
        // 观察每一个懒加载图片
        lazyImageObserver.observe(lazyImage);
    });
    
    // 添加滚动事件监听，确保在快速滚动时也能触发懒加载
    let scrollTimeout;
    window.addEventListener('scroll', function() {
        if (scrollTimeout) {
            clearTimeout(scrollTimeout);
        }
        scrollTimeout = setTimeout(function() {
            const event = new Event('scroll');
            document.dispatchEvent(event);
        }, 200);
    });
});

// 为动态添加的图片启用懒加载
function enableLazyLoad(container) {
    const lazyImageObserver = new IntersectionObserver(function(entries, observer) {
        entries.forEach(function(entry) {
            if (entry.isIntersecting) {
                let lazyImage = entry.target;
                if (lazyImage.dataset.src) {
                    lazyImage.src = lazyImage.dataset.src;
                    lazyImage.classList.remove('lazy-image');
                    lazyImage.classList.add('image-loaded');
                }
                observer.unobserve(lazyImage);
            }
        });
    }, {
        rootMargin: '100px 0px',
        threshold: 0.01
    });
    
    const lazyImages = container.querySelectorAll('.lazy-image');
    lazyImages.forEach(function(lazyImage) {
        lazyImageObserver.observe(lazyImage);
    });
}
