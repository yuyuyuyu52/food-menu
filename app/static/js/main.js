/**
 * 主要JavaScript文件 - Tailwind CSS 版本
 */

document.addEventListener('DOMContentLoaded', function() {    
    // 自动关闭闪现消息
    const alerts = document.querySelectorAll('.mb-4.p-4.rounded.border-l-4');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            const closeButton = alert.querySelector('button');
            if (closeButton) {
                closeButton.click();
            } else {
                alert.style.opacity = '0';
                alert.style.transition = 'opacity 0.5s ease';
                setTimeout(() => {
                    alert.remove();
                }, 500);
            }
        }, 5000);
    });
    
    // 为确认删除添加事件监听器
    const confirmDeleteButtons = document.querySelectorAll('[data-confirm-delete]');
    confirmDeleteButtons.forEach(function(button) {
        button.addEventListener('click', function(event) {
            if (!confirm('确定要删除吗？此操作不可恢复！')) {
                event.preventDefault();
            }
        });
    });
    
    // 为平滑滚动添加事件监听
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            if (href && href.startsWith('#') && href.length > 1) {
                e.preventDefault();
                const targetId = href.substring(1);
                const targetElement = document.getElementById(targetId);
                
                if (targetElement) {
                    const offsetTop = targetElement.getBoundingClientRect().top + window.pageYOffset;
                    window.scrollTo({
                        top: offsetTop - 20, // 顶部偏移量
                        behavior: 'smooth'
                    });
                }
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

/**
 * 切换菜单项的展开/收起状态
 * @param {string} id - 要切换的元素ID
 */
function toggleMenu(id) {
    const menu = document.getElementById(id);
    if (menu) {
        menu.classList.toggle('hidden');
    }
}

/**
 * 切换移动端导航菜单
 */
function toggleMobileMenu() {
    const menu = document.getElementById('mobile-menu');
    if (menu) {
        menu.classList.toggle('hidden');
    }
}

/**
 * 滚动到页面特定位置
 * @param {string} elementId - 目标元素ID
 * @param {number} offset - 顶部偏移量，默认为20px
 */
function scrollToElement(elementId, offset = 20) {
    const element = document.getElementById(elementId);
    if (element) {
        const elementRect = element.getBoundingClientRect();
        const absoluteElementTop = elementRect.top + window.pageYOffset;
        const targetPosition = absoluteElementTop - offset;
        window.scrollTo({
            top: targetPosition,
            behavior: 'smooth'
        });
    }
}

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

/**
 * 初始化Tailwind UI效果和交互
 */
function initTailwindEffects() {
    // 关闭警告提示框
    const alertCloseButtons = document.querySelectorAll('.alert-close');
    alertCloseButtons.forEach(button => {
        button.addEventListener('click', function() {
            const alert = this.closest('[role="alert"]');
            if (alert) {
                alert.style.opacity = '0';
                setTimeout(() => {
                    alert.style.display = 'none';
                }, 300);
            }
        });
    });
    
    // 初始化下拉菜单
    const dropdownButtons = document.querySelectorAll('[data-dropdown-toggle]');
    dropdownButtons.forEach(button => {
        button.addEventListener('click', function() {
            const targetId = this.getAttribute('data-dropdown-toggle');
            const dropdown = document.getElementById(targetId);
            if (dropdown) {
                dropdown.classList.toggle('hidden');
            }
        });
    });
}

/**
 * 滚动到页面特定位置
 * @param {string} elementId - 目标元素ID
 * @param {number} offset - 顶部偏移量，默认为20px
 */
function scrollToElement(elementId, offset = 20) {
    const element = document.getElementById(elementId);
    if (element) {
        const elementRect = element.getBoundingClientRect();
        const absoluteElementTop = elementRect.top + window.pageYOffset;
        const middle = absoluteElementTop - offset;
        window.scrollTo({
            top: middle,
            behavior: 'smooth'
        });
    }
}

/**
 * 选择菜品功能 - 特别用于点菜页面
 */
function initDishSelection() {
    const checkboxes = document.querySelectorAll('.dish-checkbox');
    const selectedCountElement = document.getElementById('selected-count');
    
    if (!checkboxes.length || !selectedCountElement) return;
    
    // 更新已选计数
    function updateSelectedCount() {
        const selectedCount = Array.from(checkboxes).filter(checkbox => checkbox.checked).length;
        selectedCountElement.textContent = selectedCount;
        
        // 更新菜品卡片样式
        checkboxes.forEach(function(checkbox) {
            const card = checkbox.closest('.p-4');
            if (card) {
                if (checkbox.checked) {
                    card.classList.add('bg-blue-50');
                    card.classList.add('border-blue-200');
                } else {
                    card.classList.remove('bg-blue-50');
                    card.classList.remove('border-blue-200');
                }
            }
        });
    }
    
    // 为所有复选框添加事件
    checkboxes.forEach(function(checkbox) {
        checkbox.addEventListener('change', updateSelectedCount);
        
        // 确保点击事件不被阻止
        checkbox.addEventListener('click', function(e) {
            e.stopPropagation();
        });
    });
    
    // 初始状态更新
    updateSelectedCount();
    
    console.log('点菜选择功能已初始化');
}

// 在页面加载时初始化点菜选择功能
document.addEventListener('DOMContentLoaded', function() {
    initDishSelection();
});
