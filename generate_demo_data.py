import json
import random
from datetime import datetime

def generate_demo():
    champions = ["Ahri", "Zed", "Jinx", "Garen", "Lux", "Yasuo"]
    data = {
        "generated_at": datetime.now().isoformat(),
        "champions": [
            {
                "name": champ,
                "win_rate": round(random.uniform(48, 55), 1),
                "pick_rate": round(random.uniform(5, 20), 1),
                "tier": random.choice(["S", "A", "B"])
            }
            for champ in champions
        ],
        "players": [
            {"name": "Faker", "region": "KR", "team": "T1"},
            {"name": "Doublelift", "region": "NA", "team": "retired"},
            {"name": "Caps", "region": "EU", "team": "G2"}
        ],
        "note": "作业项目演示数据 - 非实时"
    }
    
    os.makedirs("data", exist_ok=True)
    with open("data/demo_data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"✅ 已生成演示数据到 data/demo_data.json")

if __name__ == "__main__":
    import os
    generate_demo()
