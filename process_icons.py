#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
图标处理脚本
功能：
1. 将input文件夹中的图片转换为144x144 PNG格式，输出到icon文件夹
2. 根据icon文件夹中的所有PNG文件生成/更新4个JSON文件
"""

import os
import json
from pathlib import Path
from PIL import Image
import shutil

# 配置
REPO_NAME = "silencoo/ebic"
BRANCH = "main"
ICON_SIZE = (144, 144)
INPUT_DIR = Path("input")
ICON_DIR = Path("icon")
OUTPUT_FILES = {
    "emby-icon.json": {"name": ".图标包", "description": ".", "indent": 2},
    "icon.json": {"name": ".图标包", "description": ".", "indent": 2},
    "surge.json": {"name": ".", "description": "", "indent": 2},
    "quanx.json": {"name": ".图标包", "description": ".", "indent": 4}
}

def convert_to_png(input_path, output_path, size=ICON_SIZE):
    """将图片转换为指定尺寸的PNG格式"""
    try:
        # 打开图片
        img = Image.open(input_path)
        
        # 转换为RGB模式（如果是RGBA则保留透明度）
        if img.mode not in ('RGB', 'RGBA'):
            if img.mode == 'P' and 'transparency' in img.info:
                img = img.convert('RGBA')
            else:
                img = img.convert('RGB')
        
        # 调整大小，使用高质量重采样
        img_resized = img.resize(size, Image.Resampling.LANCZOS)
        
        # 保存为PNG
        img_resized.save(output_path, 'PNG', optimize=True)
        print(f"✓ 转换成功: {input_path.name} -> {output_path.name}")
        return True
    except Exception as e:
        print(f"✗ 转换失败: {input_path.name} - {str(e)}")
        return False

def process_input_folder():
    """处理input文件夹中的图片"""
    if not INPUT_DIR.exists():
        print(f"⚠ input文件夹不存在，跳过转换步骤")
        return
    
    # 确保icon文件夹存在
    ICON_DIR.mkdir(exist_ok=True)
    
    # 支持的图片格式
    image_extensions = {'.jpg', '.jpeg', '.JPG', '.JPEG', '.png', '.PNG', '.bmp', '.BMP', '.gif', '.GIF', '.webp', '.WEBP'}
    
    converted_count = 0
    for file_path in INPUT_DIR.iterdir():
        if file_path.is_file() and file_path.suffix in image_extensions:
            # 生成输出文件名（统一为小写.png）
            output_name = file_path.stem + '.png'
            output_path = ICON_DIR / output_name
            
            # 转换图片
            if convert_to_png(file_path, output_path):
                converted_count += 1
    
    print(f"\n转换完成，共处理 {converted_count} 个文件\n")

def get_icon_name(filename):
    """从文件名提取图标名称（去掉扩展名）"""
    return Path(filename).stem

def generate_json_files():
    """根据icon文件夹中的PNG文件生成JSON文件"""
    if not ICON_DIR.exists():
        print(f"✗ icon文件夹不存在")
        return
    
    # 获取所有PNG文件
    png_files = sorted([f for f in ICON_DIR.iterdir() if f.is_file() and f.suffix.lower() == '.png'])
    
    if not png_files:
        print(f"⚠ icon文件夹中没有PNG文件")
        return
    
    print(f"找到 {len(png_files)} 个PNG图标文件\n")
    
    # 为每个输出文件生成JSON
    for json_filename, metadata in OUTPUT_FILES.items():
        icons = []
        
        for png_file in png_files:
            icon_name = get_icon_name(png_file.name)
            icon_url = f"https://raw.githubusercontent.com/{REPO_NAME}/{BRANCH}/icon/{png_file.name}"
            
            icons.append({
                "name": icon_name,
                "url": icon_url
            })
        
        # 构建JSON结构
        json_data = {
            "name": metadata["name"],
            "description": metadata["description"],
            "icons": icons
        }
        
        # 写入JSON文件
        output_path = Path(json_filename)
        # 获取该文件的缩进设置
        indent_size = metadata.get("indent", 2)
        # 先转换为JSON字符串，然后替换斜杠以保持与现有格式一致
        json_str = json.dumps(json_data, ensure_ascii=False, indent=indent_size)
        # 替换斜杠为转义的斜杠（保持与现有文件格式一致）
        json_str = json_str.replace('/', '\\/')
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(json_str)
        
        print(f"✓ 已生成: {json_filename} ({len(icons)} 个图标)")

def main():
    """主函数"""
    print("=" * 60)
    print("图标处理脚本")
    print("=" * 60)
    print()
    
    # 步骤1: 处理input文件夹
    print("步骤1: 处理input文件夹中的图片...")
    process_input_folder()
    
    # 步骤2: 生成JSON文件
    print("步骤2: 生成JSON文件...")
    generate_json_files()
    
    print()
    print("=" * 60)
    print("处理完成！")
    print("=" * 60)

if __name__ == "__main__":
    main()

