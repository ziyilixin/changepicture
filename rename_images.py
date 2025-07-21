#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
图片重命名工具
根据项目名称自动重命名 Assets.xcassets 中的图片并更新代码中的引用

使用方法:
python rename_images.py <项目名称> <项目路径>

示例:
python rename_images.py novi /Users/wcf/Desktop/Novv/Novi/Classes/ClearSource/Assets.xcassets
"""

import os
import sys
import re
import shutil
from pathlib import Path
import argparse

class ImageRenamer:
    def __init__(self, project_name, assets_path):
        self.project_name = project_name.lower()
        self.assets_path = Path(assets_path)
        self.rename_mapping = {}
        self.old_to_new = {}
        
    def get_image_folders(self):
        """获取所有图片文件夹"""
        folders = []
        for item in self.assets_path.iterdir():
            if item.is_dir() and not item.name.startswith('.') and not item.name.endswith('.colorset'):
                folders.append(item)
        return folders
    
    def get_images_in_folder(self, folder_path):
        """获取文件夹中的所有图片"""
        images = []
        for item in folder_path.iterdir():
            if item.is_dir() and item.name.endswith('.imageset'):
                images.append(item)
        return images
    
    def generate_new_name(self, old_name, folder_name):
        """生成新的图片名称"""
        # 移除 .imageset 后缀
        base_name = old_name.replace('.imageset', '')
        
        # 如果已经包含项目前缀，直接返回
        if base_name.startswith(f"{self.project_name}_"):
            return old_name
            
        # 生成新名称
        new_name = f"{self.project_name}_{base_name}.imageset"
        return new_name
    
    def rename_images(self):
        """重命名所有图片文件夹"""
        print(f"开始重命名图片，项目前缀: {self.project_name}")
        
        folders = self.get_image_folders()
        total_renamed = 0
        
        for folder in folders:
            print(f"\n处理文件夹: {folder.name}")
            images = self.get_images_in_folder(folder)
            
            for image in images:
                old_name = image.name
                new_name = self.generate_new_name(old_name, folder.name)
                
                if old_name != new_name:
                    old_path = image
                    new_path = image.parent / new_name
                    
                    try:
                        # 重命名文件夹
                        shutil.move(str(old_path), str(new_path))
                        
                        # 记录映射关系
                        base_old = old_name.replace('.imageset', '')
                        base_new = new_name.replace('.imageset', '')
                        self.old_to_new[base_old] = base_new
                        self.rename_mapping[base_old] = base_new
                        
                        print(f"  ✓ {old_name} → {new_name}")
                        total_renamed += 1
                        
                    except Exception as e:
                        print(f"  ✗ 重命名失败 {old_name}: {e}")
                else:
                    print(f"  - {old_name} (无需重命名)")
        
        print(f"\n总共重命名了 {total_renamed} 个图片")
        return self.rename_mapping
    
    def update_code_references(self, project_root):
        """更新代码中的图片引用"""
        print(f"\n开始更新代码中的图片引用...")
        
        # 查找所有 .m 和 .swift 文件
        code_files = []
        for root, dirs, files in os.walk(project_root):
            # 跳过 Pods 目录
            if 'Pods' in root:
                continue
                
            for file in files:
                if file.endswith(('.m', '.swift')):
                    code_files.append(os.path.join(root, file))
        
        total_updated = 0
        
        for file_path in code_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                original_content = content
                file_updated = False
                
                # 更新 ImageNamed 调用
                for old_name, new_name in self.old_to_new.items():
                    # 匹配 ImageNamed(@"old_name")
                    pattern1 = f'ImageNamed\\(@"{re.escape(old_name)}"\\)'
                    replacement1 = f'ImageNamed(@"{new_name}")'
                    if re.search(pattern1, content):
                        content = re.sub(pattern1, replacement1, content)
                        file_updated = True
                    
                    # 匹配 [UIImage imageNamed:@"old_name"]
                    pattern2 = f'\\[UIImage imageNamed:@"{re.escape(old_name)}"\\]'
                    replacement2 = f'[UIImage imageNamed:@"{new_name}"]'
                    if re.search(pattern2, content):
                        content = re.sub(pattern2, replacement2, content)
                        file_updated = True
                    
                    # 匹配 setImage:[UIImage imageNamed:@"old_name"]
                    pattern3 = f'setImage:\\[UIImage imageNamed:@"{re.escape(old_name)}"\\]'
                    replacement3 = f'setImage:[UIImage imageNamed:@"{new_name}"]'
                    if re.search(pattern3, content):
                        content = re.sub(pattern3, replacement3, content)
                        file_updated = True
                    
                    # 匹配 setBackgroundImage:[UIImage imageNamed:@"old_name"]
                    pattern4 = f'setBackgroundImage:\\[UIImage imageNamed:@"{re.escape(old_name)}"\\]'
                    replacement4 = f'setBackgroundImage:[UIImage imageNamed:@"{new_name}"]'
                    if re.search(pattern4, content):
                        content = re.sub(pattern4, replacement4, content)
                        file_updated = True
                    
                    # 匹配字典中的图片名称
                    pattern5 = f'@"{re.escape(old_name)}"'
                    replacement5 = f'@"{new_name}"'
                    if re.search(pattern5, content):
                        content = re.sub(pattern5, replacement5, content)
                        file_updated = True
                
                if file_updated:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    print(f"  ✓ 更新: {os.path.relpath(file_path, project_root)}")
                    total_updated += 1
                    
            except Exception as e:
                print(f"  ✗ 更新失败 {file_path}: {e}")
        
        print(f"\n总共更新了 {total_updated} 个代码文件")
    
    def generate_report(self):
        """生成重命名报告"""
        report_path = f"rename_report_{self.project_name}.txt"
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(f"图片重命名报告 - 项目: {self.project_name}\n")
            f.write("=" * 50 + "\n\n")
            
            f.write("重命名映射:\n")
            for old_name, new_name in self.old_to_new.items():
                f.write(f"  {old_name} → {new_name}\n")
            
            f.write(f"\n总共重命名了 {len(self.old_to_new)} 个图片\n")
        
        print(f"\n重命名报告已保存到: {report_path}")

def main():
    parser = argparse.ArgumentParser(description='图片重命名工具')
    parser.add_argument('project_name', help='项目名称（用作图片前缀）')
    parser.add_argument('assets_path', help='Assets.xcassets 路径')
    parser.add_argument('--project-root', help='项目根目录路径（用于更新代码引用）')
    parser.add_argument('--dry-run', action='store_true', help='仅显示将要进行的操作，不实际执行')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.assets_path):
        print(f"错误: Assets.xcassets 路径不存在: {args.assets_path}")
        sys.exit(1)
    
    if args.dry_run:
        print("=== 预览模式 ===")
        print(f"项目名称: {args.project_name}")
        print(f"Assets 路径: {args.assets_path}")
        if args.project_root:
            print(f"项目根目录: {args.project_root}")
        print("\n将要执行的操作:")
        
        renamer = ImageRenamer(args.project_name, args.assets_path)
        folders = renamer.get_image_folders()
        
        for folder in folders:
            print(f"\n文件夹: {folder.name}")
            images = renamer.get_images_in_folder(folder)
            for image in images:
                old_name = image.name
                new_name = renamer.generate_new_name(old_name, folder.name)
                if old_name != new_name:
                    print(f"  {old_name} → {new_name}")
                else:
                    print(f"  {old_name} (无需重命名)")
        
        print("\n预览完成，使用 --dry-run 参数查看将要进行的操作")
        return
    
    # 执行重命名
    renamer = ImageRenamer(args.project_name, args.assets_path)
    
    try:
        # 重命名图片
        mapping = renamer.rename_images()
        
        # 更新代码引用
        if args.project_root and os.path.exists(args.project_root):
            renamer.update_code_references(args.project_root)
        
        # 生成报告
        renamer.generate_report()
        
        print(f"\n✅ 图片重命名完成！")
        print(f"项目前缀: {args.project_name}")
        print(f"重命名了 {len(mapping)} 个图片")
        
    except Exception as e:
        print(f"❌ 执行失败: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 