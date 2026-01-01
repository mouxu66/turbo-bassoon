// 物品管理JavaScript
let currentPage = 1;
const itemsPerPage = 10;
let allItems = [];
let filteredItems = [];

document.addEventListener('DOMContentLoaded', function() {
    loadAllItems();
    setupEventListeners();
});

function loadAllItems() {
    // 尝试从API加载
    fetch('/api/items.json')
        .then(response => response.json())
        .then(data => {
            allItems = data.items || [];
            filteredItems = [...allItems];
            renderTable();
            updatePageInfo();
        })
        .catch(() => {
            // 使用模拟数据
            generateMockItems();
        });
}

function generateMockItems() {
    const mockItems = [
        {id: 1, name: '无尽之刃', price: 3400, ad: 70, ap: 0, health: 0, armor: 0, mr: 0},
        {id: 2, name: '灭世者的死亡之帽', price: 3600, ad: 0, ap: 120, health: 0, armor: 0, mr: 0},
        {id: 3, name: '兰顿之兆', price: 2700, ad: 0, ap: 0, health: 400, armor: 60, mr: 0},
        {id: 4, name: '深渊面具', price: 2800, ad: 0, ap: 55, health: 350, armor: 0, mr: 40},
        {id: 5, name: '三相之力', price: 3333, ad: 25, ap: 0, health: 200, armor: 0, mr: 0},
        {id: 6, name: '幽梦之灵', price: 2900, ad: 60, ap: 0, health: 0, armor: 0, mr: 0},
        {id: 7, name: '卢登的回声', price: 3200, ad: 0, ap: 90, health: 0, armor: 0, mr: 0},
        {id: 8, name: '日炎圣盾', price: 2700, ad: 0, ap: 0, health: 450, armor: 35, mr: 0},
        {id: 9, name: '狂徒铠甲', price: 3000, ad: 0, ap: 0, health: 800, armor: 0, mr: 0},
        {id: 10, name: '振奋盔甲', price: 2900, ad: 0, ap: 0, health: 450, armor: 0, mr: 55}
    ];
    
    allItems = mockItems;
    filteredItems = [...mockItems];
    renderTable();
    updatePageInfo();
}

function setupEventListeners() {
    document.getElementById('search-item')?.addEventListener('input', function() {
        searchItems();
    });
}

function searchItems() {
    const nameQuery = document.getElementById('search-item')?.value.toLowerCase() || '';
    const minPrice = parseInt(document.getElementById('min-price')?.value) || 0;
    const maxPrice = parseInt(document.getElementById('max-price')?.value) || 99999;
    const minAD = parseInt(document.getElementById('min-ad')?.value) || 0;
    const minAP = parseInt(document.getElementById('min-ap')?.value) || 0;
    
    filteredItems = allItems.filter(item => {
        const nameMatch = item.name.toLowerCase().includes(nameQuery);
        const priceMatch = item.price >= minPrice && item.price <= maxPrice;
        const adMatch = item.ad >= minAD;
        const apMatch = item.ap >= minAP;
        
        return nameMatch && priceMatch && adMatch && apMatch;
    });
    
    currentPage = 1;
    renderTable();
    updatePageInfo();
}

function resetSearch() {
    document.getElementById('search-item').value = '';
    document.getElementById('min-price').value = '';
    document.getElementById('max-price').value = '';
    document.getElementById('min-ad').value = '0';
    document.getElementById('min-ap').value = '0';
    
    filteredItems = [...allItems];
    currentPage = 1;
    renderTable();
    updatePageInfo();
}

function renderTable() {
    const tbody = document.getElementById('items-table-body');
    if (!tbody) return;
    
    const start = (currentPage - 1) * itemsPerPage;
    const end = start + itemsPerPage;
    const pageItems = filteredItems.slice(start, end);
    
    let html = '';
    pageItems.forEach(item => {
        html += `<tr>
            <td><strong>${item.name}</strong></td>
            <td><span class="badge bg-warning">${item.price}</span></td>
            <td>${item.ad}</td>
            <td>${item.ap}</td>
            <td>${item.health}</td>
            <td>${item.armor}</td>
            <td>${item.mr}</td>
            <td>
                <button class="btn btn-sm btn-info" onclick="showDetail(${item.id})">
                    <i class="fas fa-eye"></i>
                </button>
            </td>
        </tr>`;
    });
    
    tbody.innerHTML = html || '<tr><td colspan="8" class="text-center">未找到匹配的装备</td></tr>';
}

function showDetail(itemId) {
    const item = allItems.find(i => i.id === itemId);
    if (!item) return;
    
    const modal = new bootstrap.Modal(document.getElementById('detailModal'));
    const content = document.getElementById('detailContent');
    
    content.innerHTML = `
        <h4>${item.name}</h4>
        <p><strong>价格:</strong> ${item.price} 金币</p>
        <hr>
        <h5>属性:</h5>
        <ul>
            <li>攻击力: ${item.ad}</li>
            <li>法术强度: ${item.ap}</li>
            <li>生命值: ${item.health}</li>
            <li>护甲: ${item.armor}</li>
            <li>魔法抗性: ${item.mr}</li>
        </ul>
        <p class="text-muted small">ID: ${item.id}</p>
    `;
    
    modal.show();
}

function prevPage() {
    if (currentPage > 1) {
        currentPage--;
        renderTable();
        updatePageInfo();
    }
}

function nextPage() {
    const totalPages = Math.ceil(filteredItems.length / itemsPerPage);
    if (currentPage < totalPages) {
        currentPage++;
        renderTable();
        updatePageInfo();
    }
}

function updatePageInfo() {
    const totalPages = Math.ceil(filteredItems.length / itemsPerPage);
    document.getElementById('page-info').textContent = 
        `第 ${currentPage} 页 / 共 ${totalPages} 页 (${filteredItems.length} 件装备)`;
}

function exportFilteredItems() {
    const dataStr = JSON.stringify(filteredItems, null, 2);
    const dataUri = 'data:application/json;charset=utf-8,'+ encodeURIComponent(dataStr);
    
    const exportFileDefaultName = `lol_items_${new Date().toISOString().split('T')[0]}.json`;
    
    const linkElement = document.createElement('a');
    linkElement.setAttribute('href', dataUri);
    linkElement.setAttribute('download', exportFileDefaultName);
    linkElement.click();
    
    alert(`已导出 ${filteredItems.length} 件装备数据`);
}