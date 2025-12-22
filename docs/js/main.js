// 主JavaScript文件
document.addEventListener('DOMContentLoaded', function() {
    // 初始化页面
    initPage();
    
    // 加载数据
    loadData();
});

function initPage() {
    // 设置最后更新时间
    document.getElementById('last-update').textContent = new Date().toLocaleString();
    
    // 初始化搜索框
    const searchInput = document.getElementById('search-item');
    if (searchInput) {
        searchInput.addEventListener('input', debounce(searchItems, 300));
    }
}

function loadData() {
    // 加载统计数据
    fetch('/api/stats.json')
        .then(response => response.json())
        .then(data => {
            updateStats(data);
            loadItems(data.items);
            initCharts(data);
        })
        .catch(error => {
            console.error('加载数据失败:', error);
            // 使用模拟数据
            useMockData();
        });
}

function updateStats(data) {
    document.getElementById('item-count').textContent = data.itemCount || 0;
    document.getElementById('match-count').textContent = data.matchCount || 0;
    document.getElementById('data-size').textContent = data.totalSize || '0';
}

function loadItems(items) {
    const container = document.getElementById('items-container');
    if (!container) return;
    
    if (items && items.length > 0) {
        let html = '<table class="table table-striped"><thead><tr>';
        html += '<th>名称</th><th>价格</th><th>攻击力</th><th>法强</th><th>详情</th></tr></thead><tbody>';
        
        items.slice(0, 10).forEach(item => {
            html += `<tr>
                <td>${item.name || '未知'}</td>
                <td><span class="badge bg-warning">${item.price || 0}</span></td>
                <td>${item.ad || 0}</td>
                <td>${item.ap || 0}</td>
                <td><button class="btn btn-sm btn-info" onclick="showItemDetail('${item.id || item.name}')">查看</button></td>
            </tr>`;
        });
        
        html += '</tbody></table>';
        container.innerHTML = html;
    } else {
        container.innerHTML = '<p class="text-center text-muted">暂无装备数据</p>';
    }
}

function initCharts(data) {
    // 初始化图表
    const itemCtx = document.getElementById('item-chart');
    if (itemCtx) {
        new Chart(itemCtx.getContext('2d'), {
            type: 'bar',
            data: {
                labels: ['攻击', '法强', '生命', '护甲', '魔抗'],
                datasets: [{
                    label: '平均属性值',
                    data: [
                        data.avgAD || 0,
                        data.avgAP || 0, 
                        data.avgHealth || 0,
                        data.avgArmor || 0,
                        data.avgMR || 0
                    ],
                    backgroundColor: [
                        '#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF'
                    ]
                }]
            }
        });
    }
}

function searchItems() {
    const query = document.getElementById('search-item').value.toLowerCase();
    const items = window.itemsData || [];
    
    const filtered = items.filter(item => 
        item.name.toLowerCase().includes(query)
    );
    
    renderItems(filtered);
}

function renderItems(items) {
    // 渲染物品列表
    console.log('显示物品:', items.length);
}

function showItemDetail(itemId) {
    // 显示物品详情
    alert('物品详情功能: ' + itemId);
}

function analyzeByPrice() {
    document.getElementById('analysis-result').innerHTML = 
        '<div class="alert alert-success">价格分析完成！平均价格: 2500金币</div>';
}

function analyzeByStats() {
    document.getElementById('analysis-result').innerHTML = 
        '<div class="alert alert-info">属性分析完成！攻击型装备占比: 45%</div>';
}

function generateReport() {
    document.getElementById('analysis-result').innerHTML = 
        '<div class="alert alert-warning">报告生成完成！<a href="#" class="alert-link">下载报告</a></div>';
}

// 工具函数
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

function useMockData() {
    // 模拟数据
    const mockData = {
        itemCount: 156,
        matchCount: 1245,
        totalSize: '2.4MB',
        items: [
            {name: '无尽之刃', price: 3400, ad: 70, ap: 0, id: '1'},
            {name: '灭世者的死亡之帽', price: 3600, ad: 0, ap: 120, id: '2'},
            {name: '兰顿之兆', price: 2700, ad: 0, ap: 0, health: 400, id: '3'}
        ],
        avgAD: 45.6,
        avgAP: 32.1,
        avgHealth: 280.3,
        avgArmor: 35.2,
        avgMR: 28.7
    };
    
    updateStats(mockData);
    loadItems(mockData.items);
    initCharts(mockData);
    
    // 存储数据供其他函数使用
    window.itemsData = mockData.items;
}