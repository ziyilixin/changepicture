#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复ai.json文件中的图片引用
将旧的图片名称更新为新的patalar_前缀名称
"""

import json
import os
import sys

def fix_ai_json(ai_json_path):
    """修复ai.json文件中的图片引用"""
    
    # 图片名称映射
    image_mapping = {
        "home_photo1": "patalar_home_photo1",
        "home_photo2": "patalar_home_photo2", 
        "home_photo3": "patalar_home_photo3",
        "home_photo4": "patalar_home_photo4",
        "home_photo5": "patalar_home_photo5",
        "home_photo6": "patalar_home_photo6",
        "home_big_bg1": "patalar_home_big_bg1",
        "home_big_bg2": "patalar_home_big_bg2",
        "home_big_bg3": "patalar_home_big_bg3",
        "home_big_bg4": "patalar_home_big_bg4",
        "home_big_bg5": "patalar_home_big_bg5",
        "home_big_bg6": "patalar_home_big_bg6"
    }
    
    try:
        # 读取JSON文件
        with open(ai_json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print(f"正在修复 {ai_json_path}...")
        
        # 更新alien_characters中的图片引用
        if 'alien_characters' in data:
            for character in data['alien_characters']:
                # 更新photo字段
                if 'photo' in character and character['photo'] in image_mapping:
                    old_photo = character['photo']
                    new_photo = image_mapping[old_photo]
                    character['photo'] = new_photo
                    print(f"  {character['name']}: photo {old_photo} → {new_photo}")
                
                # 更新bigBg字段
                if 'bigBg' in character and character['bigBg'] in image_mapping:
                    old_big_bg = character['bigBg']
                    new_big_bg = image_mapping[old_big_bg]
                    character['bigBg'] = new_big_bg
                    print(f"  {character['name']}: bigBg {old_big_bg} → {new_big_bg}")
        
        # 写回文件
        with open(ai_json_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        
        print(f"✅ 修复完成！")
        
    except Exception as e:
        print(f"❌ 修复失败: {e}")
        sys.exit(1)

def main():
    if len(sys.argv) != 2:
        print("使用方法: python3 fix_ai_json.py <ai.json路径>")
        print("示例: python3 fix_ai_json.py Patalar/Classes/Source/ai.json")
        sys.exit(1)
    
    ai_json_path = sys.argv[1]
    
    if not os.path.exists(ai_json_path):
        print(f"错误: 文件不存在: {ai_json_path}")
        sys.exit(1)
    
    fix_ai_json(ai_json_path)

if __name__ == "__main__":
    main() 