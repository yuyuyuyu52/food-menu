/**
 * 移动端增强脚本
 * 用于提供更好的移动端交互体验
 */

document.addEventListener('DOMContentLoaded', function() {
    // 检测是否为移动设备
    const isMobile = window.innerWidth < 640;
    
    // 移动端图片优化处理
    enhanceMobileImages();
    
    // 添加移动端触摸反馈效果
    addTouchFeedback();
    
    // 优化分类页面交互
    enhanceCategoryInteraction();
    
    // 添加表单元素交互优化
    enhanceMobileForms();
    
    // 添加下拉刷新功能
    if (isMobile) {
        setupPullToRefresh();
    }
    
    // 修复底部导航栏边距
    adjustBottomNavBarSpace();
    
    // 如果有图片加载问题，尝试重新加载
    setTimeout(checkImagesLoading, 3000);
});

/**
 * 为触摸设备添加触摸反馈效果
 */
function addTouchFeedback() {
    // 为可点击元素添加触摸效果
    const touchableElements = document.querySelectorAll(
        'a, button, .cursor-pointer, [role="button"], .touch-target'
    );
    
    touchableElements.forEach(elem => {
        // 添加触摸开始效果
        elem.addEventListener('touchstart', function() {
            this.classList.add('active-touch');
            
            // 对于卡片式元素，添加特定效果
            if (this.classList.contains('card') || 
                this.classList.contains('bg-white') || 
                this.closest('.bg-white')) {
                this.style.backgroundColor = 'rgba(243, 244, 246, 0.8)';
            }
        }, { passive: true });
        
        // 添加触摸结束效果
        elem.addEventListener('touchend', function() {
            this.classList.remove('active-touch');
            this.style.backgroundColor = '';
        }, { passive: true });
        
        // 如果触摸被取消也移除效果
        elem.addEventListener('touchcancel', function() {
            this.classList.remove('active-touch');
            this.style.backgroundColor = '';
        }, { passive: true });
    });
}

/**
 * 优化分类页面交互
 */
function enhanceCategoryInteraction() {
    // 使分类卡片内的按钮点击不触发卡片点击
    const categoryCards = document.querySelectorAll('.p-3, .p-4');
    if (categoryCards.length) {
        categoryCards.forEach(card => {
            const buttons = card.querySelectorAll('a, button');
            buttons.forEach(btn => {
                btn.addEventListener('click', function(e) {
                    e.stopPropagation();
                });
            });
        });
    }
}

/**
 * 移动端图片优化处理
 */
function enhanceMobileImages() {
    // 找到所有图片元素
    const images = document.querySelectorAll('img');
    
    images.forEach(img => {
        // 添加错误处理
        if (!img.hasAttribute('onerror')) {
            img.onerror = function() {
                // 设置一个默认图标来替代加载失败的图片
                const parent = this.parentElement;
                if (parent) {
                    parent.innerHTML = '<div class="w-full h-full flex items-center justify-center"><i class="fas fa-utensils text-gray-400 text-2xl"></i></div>';
                }
            };
        }
        
        // 添加加载完成处理
        img.onload = function() {
            // 移除任何加载中的占位符
            const loadingIndicator = img.closest('.img-container')?.querySelector('.loading-indicator');
            if (loadingIndicator) {
                loadingIndicator.remove();
            }
        };
    });
}

/**
 * 设置下拉刷新功能
 */
function setupPullToRefresh() {
    let touchStartY = 0;
    let touchMoveY = 0;
    const threshold = 80; // 触发刷新需要的下拉距离
    
    // 创建下拉指示器
    const indicator = document.createElement('div');
    indicator.className = 'pull-refresh-indicator';
    indicator.innerHTML = '<div class="spinner"></div><span>下拉刷新...</span>';
    indicator.style.cssText = 'position: absolute; top: -60px; left: 0; right: 0; height: 60px; display: flex; justify-content: center; align-items: center; transition: transform 0.3s ease;';
    document.body.insertBefore(indicator, document.body.firstChild);
    
    document.addEventListener('touchstart', function(e) {
        // 只在顶部区域启用下拉刷新
        if (window.scrollY <= 5) {
            touchStartY = e.touches[0].clientY;
        }
    }, { passive: true });
    
    document.addEventListener('touchmove', function(e) {
        if (touchStartY > 0 && window.scrollY <= 0) {
            touchMoveY = e.touches[0].clientY;
            const pullDistance = touchMoveY - touchStartY;
            
            if (pullDistance > 0) {
                indicator.style.transform = `translateY(${Math.min(pullDistance / 2, threshold)}px)`;
                if (pullDistance > threshold) {
                    indicator.querySelector('span').textContent = '释放刷新...';
                } else {
                    indicator.querySelector('span').textContent = '下拉刷新...';
                }
            }
        }
    }, { passive: true });
    
    document.addEventListener('touchend', function() {
        if (touchStartY > 0 && touchMoveY > 0) {
            const pullDistance = touchMoveY - touchStartY;
            
            if (pullDistance > threshold) {
                // 显示加载动画
                indicator.querySelector('span').textContent = '加载中...';
                indicator.querySelector('.spinner').classList.add('active');
                
                // 等待一段时间后刷新页面
                setTimeout(() => {
                    window.location.reload();
                }, 1000);
            } else {
                // 重置指示器位置
                indicator.style.transform = 'translateY(0)';
            }
            
            // 重置触摸坐标
            touchStartY = 0;
            touchMoveY = 0;
        }
    }, { passive: true });
}

/**
 * 为表单元素添加移动端优化
 */
function enhanceMobileForms() {
    // 处理表单字段交互
    const formFields = document.querySelectorAll('.form-field');
    formFields.forEach(field => {
        const input = field.querySelector('input, textarea, select');
        const label = field.querySelector('label');
        
        if (input && label) {
            // 输入框获得焦点时，标签高亮
            input.addEventListener('focus', function() {
                label.classList.add('text-blue-600');
                field.classList.add('focused');
            });
            
            // 输入框失去焦点时，移除高亮
            input.addEventListener('blur', function() {
                label.classList.remove('text-blue-600');
                field.classList.remove('focused');
            });
        }
    });
    
    // 优化文本区域自动调整高度
    const textareas = document.querySelectorAll('textarea');
    textareas.forEach(textarea => {
        textarea.addEventListener('input', function() {
            this.style.height = 'auto';
            this.style.height = (this.scrollHeight) + 'px';
        });
        
        // 初始调整
        setTimeout(() => {
            textarea.dispatchEvent(new Event('input'));
        }, 100);
    });
    
    // 美化自定义文件上传
    const fileInputs = document.querySelectorAll('input[type="file"]');
    fileInputs.forEach(input => {
        const wrapper = input.closest('.custom-file-upload');
        if (wrapper) {
            // 添加拖放功能
            wrapper.addEventListener('dragover', function(e) {
                e.preventDefault();
                this.classList.add('border-blue-500', 'bg-blue-50');
            });
            
            wrapper.addEventListener('dragleave', function(e) {
                e.preventDefault();
                this.classList.remove('border-blue-500', 'bg-blue-50');
            });
            
            wrapper.addEventListener('drop', function(e) {
                e.preventDefault();
                this.classList.remove('border-blue-500', 'bg-blue-50');
                
                if (e.dataTransfer.files.length) {
                    input.files = e.dataTransfer.files;
                    input.dispatchEvent(new Event('change'));
                }
            });
        }
    });
}

/**
 * 调整底部导航栏的空间
 */
function adjustBottomNavBarSpace() {
    // 检查底部导航栏
    const bottomNav = document.querySelector('nav.fixed.bottom-0');
    const mainContent = document.querySelector('main');
    
    if (bottomNav && mainContent) {
        // 获取底部导航栏高度
        const navHeight = bottomNav.offsetHeight;
        // 设置主内容底部边距
        mainContent.style.marginBottom = (navHeight + 10) + 'px';
    }
}

/**
 * 检查图片是否正确加载
 */
function checkImagesLoading() {
    const images = document.querySelectorAll('img');
    console.log(`检查 ${images.length} 张图片加载状态`);
    
    images.forEach(img => {
        // 如果图片未加载成功或没有显示
        if (!img.complete || img.naturalHeight === 0 || !img.src || img.src === 'data:,') {
            console.warn('发现未加载的图片，尝试重新加载', img.src);
            
            // 如果有data-src属性，尝试使用它
            if (img.dataset.src) {
                img.src = img.dataset.src;
            }
            // 如果图片来源是缩略图路径，尝试加载原图
            else if (img.src && img.src.includes('thumb_')) {
                const originalSrc = img.src.replace('thumb_', '');
                img.src = originalSrc;
            }
        }
    });
}
