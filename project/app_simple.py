from flask import Flask, render_template, jsonify, request
import requests
import random
from datetime import datetime
import os

app = Flask(__name__)

# 你的Riot API密钥（用你自己的）
RIOT_API_KEY = "RGAPI-6a65a9f8-ebeb-47f7-aace-13d362aee1b2"

@app.route('/')
def home():
    """首页 - 完整的英雄排行榜"""
    # 获取游戏版本
    version = get_game_version()
    
    # 获取英雄数据
    champions = get_champion_data()
    
    # 添加模拟统计数据
    champions_with_stats = add_simulated_stats(champions)
    
    return render_template('index_beautiful.html',
                         champions=champions_with_stats[:30],  # 只显示前30个
                         version=version,
                         now=datetime.now().strftime("%Y-%m-%d %H:%M"),
                         total_champions=len(champions))

@app.route('/champion/<champion_name>')
def champion_detail(champion_name):
    """英雄详情页"""
    version = get_game_version()
    
    # 获取英雄详细信息
    champion = get_champion_detail(champion_name, version)
    
    return render_template('champion.html',
                         champion=champion,
                         version=version)

@app.route('/api/champions')
def api_champions():
    """API接口：获取所有英雄数据"""
    champions = get_champion_data()
    return jsonify(champions)

@app.route('/api/champion/<champion_name>')
def api_champion_detail(champion_name):
    """API接口：获取单个英雄数据"""
    version = get_game_version()
    champion = get_champion_detail(champion_name, version)
    return jsonify(champion)

@app.route('/api/health')
def health_check():
    """健康检查"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'riot_api': check_riot_api(),
        'version': get_game_version()
    })

@app.route('/search')
def search():
    """搜索页面"""
    query = request.args.get('q', '')
    champions = get_champion_data()
    
    if query:
        results = [c for c in champions if query.lower() in c['name'].lower()]
    else:
        results = champions[:10]
    
    return render_template('search.html',
                         query=query,
                         results=results,
                         count=len(results))

# ---------- 数据获取函数 ----------
def get_game_version():
    """获取游戏最新版本"""
    try:
        response = requests.get("https://ddragon.leagueoflegends.com/api/versions.json", timeout=5)
        return response.json()[0]
    except:
        return "14.1.1"

def get_champion_data():
    """获取英雄数据（简化版）"""
    # 这里使用静态数据避免API调用问题
    champions = [
        {'id': '266', 'name': '亚托克斯', 'title': '暗裔剑魔', 'tags': ['战士', '坦克']},
        {'id': '103', 'name': '阿狸', 'title': '九尾妖狐', 'tags': ['法师', '刺客']},
        {'id': '84', 'name': '亚索', 'title': '疾风剑豪', 'tags': ['战士', '刺客']},
        {'id': '166', 'name': '李青', 'title': '盲僧', 'tags': ['战士', '刺客']},
        {'id': '12', 'name': '奥拉夫', 'title': '狂战士', 'tags': ['战士', '坦克']},
        {'id': '32', 'name': '阿木木', 'title': '殇之木乃伊', 'tags': ['坦克', '法师']},
        {'id': '34', 'name': '安妮', 'title': '黑暗之女', 'tags': ['法师']},
        {'id': '1', 'name': '艾希', 'title': '寒冰射手', 'tags': ['射手', '辅助']},
        {'id': '22', 'name': '厄运小姐', 'title': '赏金猎人', 'tags': ['射手']},
        {'id': '53', 'name': '布里茨', 'title': '蒸汽机器人', 'tags': ['坦克', '辅助']},
        {'id': '63', 'name': '布兰德', 'title': '复仇焰魂', 'tags': ['法师']},
        {'id': '201', 'name': '布隆', 'title': '弗雷尔卓德之心', 'tags': ['坦克', '辅助']},
        {'id': '51', 'name': '凯特琳', 'title': '皮城女警', 'tags': ['射手']},
        {'id': '164', 'name': '卡蜜尔', 'title': '青钢影', 'tags': ['战士', '坦克']},
        {'id': '69', 'name': '卡西奥佩娅', 'title': '魔蛇之拥', 'tags': ['法师']},
        {'id': '31', 'name': '赵信', 'title': '德邦总管', 'tags': ['战士', '刺客']},
        {'id': '42', 'name': '库奇', 'title': '英勇投弹手', 'tags': ['射手']},
        {'id': '122', 'name': '达瑞斯', 'title': '诺克萨斯之手', 'tags': ['战士', '坦克']},
        {'id': '131', 'name': '黛安娜', 'title': '皎月女神', 'tags': ['战士', '法师']},
        {'id': '36', 'name': '蒙多医生', 'title': '祖安狂人', 'tags': ['战士', '坦克']},
        {'id': '119', 'name': '德莱文', 'title': '荣耀行刑官', 'tags': ['射手']},
        {'id': '245', 'name': '艾克', 'title': '时间刺客', 'tags': ['刺客', '战士']},
        {'id': '60', 'name': '伊莉丝', 'title': '蜘蛛女皇', 'tags': ['法师', '战士']},
        {'id': '28', 'name': '伊芙琳', 'title': '痛苦之拥', 'tags': ['刺客', '法师']},
        {'id': '81', 'name': '伊泽瑞尔', 'title': '探险家', 'tags': ['射手', '法师']},
        {'id': '9', 'name': '费德提克', 'title': '末日使者', 'tags': ['法师', '辅助']},
        {'id': '114', 'name': '菲奥娜', 'title': '无双剑姬', 'tags': ['战士', '刺客']},
        {'id': '105', 'name': '菲兹', 'title': '潮汐海灵', 'tags': ['刺客', '战士']},
        {'id': '3', 'name': '加里奥', 'title': '正义巨像', 'tags': ['坦克', '法师']},
        {'id': '41', 'name': '盖伦', 'title': '德玛西亚之力', 'tags': ['战士', '坦克']},
        {'id': '86', 'name': '古拉加斯', 'title': '酒桶', 'tags': ['坦克', '法师']},
        {'id': '150', 'name': '纳尔', 'title': '迷失之牙', 'tags': ['战士', '坦克']},
    ]
    return champions

def add_simulated_stats(champions):
    """添加模拟统计数据"""
    for champ in champions:
        # 生成随机但合理的数据
        champ['win_rate'] = round(random.uniform(48.0, 55.0), 1)
        champ['pick_rate'] = round(random.uniform(2.0, 15.0), 1)
        champ['ban_rate'] = round(random.uniform(0.5, 30.0), 1)
        
        # 确定层级
        if champ['win_rate'] >= 53.5:
            champ['tier'] = 'S'
            champ['tier_color'] = 'danger'
        elif champ['win_rate'] >= 51.0:
            champ['tier'] = 'A'
            champ['tier_color'] = 'warning'
        elif champ['win_rate'] >= 49.0:
            champ['tier'] = 'B'
            champ['tier_color'] = 'primary'
        else:
            champ['tier'] = 'C'
            champ['tier_color'] = 'secondary'
        
        # 生成图片URL
        champ['image'] = f"https://ddragon.leagueoflegends.com/cdn/14.1.1/img/champion/{champ['name']}.png"
        champ['splash'] = f"https://ddragon.leagueoflegends.com/cdn/img/champion/splash/{champ['name']}_0.jpg"
    
    # 按胜率排序
    return sorted(champions, key=lambda x: x['win_rate'], reverse=True)

def get_champion_detail(name, version):
    """获取英雄详情"""
    try:
        # 从静态数据中查找
        all_champs = get_champion_data()
        champ_data = next((c for c in all_champs if c['name'] == name), None)
        
        if champ_data:
            # 添加更多详情
            champ_data.update({
                'lore': f"{name}是英雄联盟中的一位英雄，拥有独特的技能和玩法。",
                'stats': {
                    'hp': random.randint(580, 650),
                    'mp': random.randint(300, 400),
                    'ad': random.randint(60, 80),
                    'armor': random.randint(30, 45),
                    'mr': random.randint(30, 40)
                },
                'skills': [
                    {'name': f'{name}的Q技能', 'description': '主要伤害技能'},
                    {'name': f'{name}的W技能', 'description': '防御或辅助技能'},
                    {'name': f'{name}的E技能', 'description': '位移或控制技能'},
                    {'name': f'{name}的R技能', 'description': '终极技能'}
                ]
            })
            return champ_data
    except:
        pass
    
    # 如果找不到，返回默认数据
    return {
        'name': name,
        'title': '英雄',
        'lore': f'这是{name}的背景故事。',
        'tags': ['战士', '坦克'],
        'stats': {'hp': 600, 'mp': 350, 'ad': 65, 'armor': 35, 'mr': 32},
        'win_rate': 50.0,
        'pick_rate': 5.0,
        'tier': 'B'
    }

def check_riot_api():
    """检查Riot API状态"""
    try:
        response = requests.get(
            'https://na1.api.riotgames.com/lol/status/v4/platform-data',
            headers={'X-Riot-Token': RIOT_API_KEY},
            timeout=3
        )
        return 'connected' if response.status_code == 200 else 'disconnected'
    except:
        return 'disconnected'

if __name__ == '__main__':
    app.run(debug=True)
