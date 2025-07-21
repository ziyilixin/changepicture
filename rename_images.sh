#!/bin/bash

# 图片重命名工具 - Shell 版本
# 使用方法: ./rename_images.sh <项目名称> <Assets.xcassets路径> [项目根目录]

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 打印带颜色的消息
print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 显示帮助信息
show_help() {
    echo "图片重命名工具 - Shell 版本"
    echo ""
    echo "使用方法:"
    echo "  $0 <项目名称> <Assets.xcassets路径> [项目根目录]"
    echo ""
    echo "参数说明:"
    echo "  项目名称        用作图片前缀的名称（如 novi、myapp 等）"
    echo "  Assets.xcassets路径  Assets.xcassets 文件夹的完整路径"
    echo "  项目根目录      可选，用于更新代码中的图片引用"
    echo ""
    echo "示例:"
    echo "  $0 novi /Users/wcf/Desktop/Novv/Novi/Classes/ClearSource/Assets.xcassets"
    echo "  $0 novi /Users/wcf/Desktop/Novv/Novi/Classes/ClearSource/Assets.xcassets /Users/wcf/Desktop/Novv"
    echo ""
    echo "选项:"
    echo "  -h, --help      显示此帮助信息"
    echo "  --dry-run       预览模式，仅显示将要进行的操作"
}

# 检查参数
if [[ $# -eq 0 ]] || [[ "$1" == "-h" ]] || [[ "$1" == "--help" ]]; then
    show_help
    exit 0
fi

if [[ $# -lt 2 ]]; then
    print_error "参数不足！至少需要项目名称和 Assets.xcassets 路径"
    echo ""
    show_help
    exit 1
fi

PROJECT_NAME="$1"
ASSETS_PATH="$2"
PROJECT_ROOT="$3"
DRY_RUN=false

# 检查是否为预览模式
if [[ "$1" == "--dry-run" ]]; then
    DRY_RUN=true
    PROJECT_NAME="$2"
    ASSETS_PATH="$3"
    PROJECT_ROOT="$4"
fi

# 验证路径
if [[ ! -d "$ASSETS_PATH" ]]; then
    print_error "Assets.xcassets 路径不存在: $ASSETS_PATH"
    exit 1
fi

print_info "项目名称: $PROJECT_NAME"
print_info "Assets 路径: $ASSETS_PATH"
if [[ -n "$PROJECT_ROOT" ]]; then
    print_info "项目根目录: $PROJECT_ROOT"
fi
if [[ "$DRY_RUN" == true ]]; then
    print_warning "预览模式 - 不会实际执行重命名操作"
fi

echo ""

# 重命名图片函数
rename_images() {
    local total_renamed=0
    
    print_info "开始重命名图片..."
    
    # 遍历 Assets.xcassets 中的文件夹
    for folder in "$ASSETS_PATH"/*; do
        if [[ -d "$folder" ]] && [[ ! "$folder" =~ \.colorset$ ]] && [[ ! "$(basename "$folder")" =~ ^\. ]]; then
            folder_name=$(basename "$folder")
            print_info "处理文件夹: $folder_name"
            
            # 遍历文件夹中的图片
            for image in "$folder"/*.imageset; do
                if [[ -d "$image" ]]; then
                    old_name=$(basename "$image")
                    base_name="${old_name%.imageset}"
                    
                    # 检查是否已经包含项目前缀
                    if [[ "$base_name" =~ ^${PROJECT_NAME}_ ]]; then
                        print_info "  - $old_name (无需重命名)"
                        continue
                    fi
                    
                    new_name="${PROJECT_NAME}_${base_name}.imageset"
                    new_path="$(dirname "$image")/$new_name"
                    
                    if [[ "$DRY_RUN" == true ]]; then
                        print_info "  $old_name → $new_name"
                    else
                        if mv "$image" "$new_path" 2>/dev/null; then
                            print_success "  ✓ $old_name → $new_name"
                            ((total_renamed++))
                        else
                            print_error "  ✗ 重命名失败: $old_name"
                        fi
                    fi
                fi
            done
        fi
    done
    
    if [[ "$DRY_RUN" == true ]]; then
        print_info "预览完成，总共将重命名 $total_renamed 个图片"
    else
        print_success "总共重命名了 $total_renamed 个图片"
    fi
    
    return $total_renamed
}

# 更新代码引用函数
update_code_references() {
    if [[ -z "$PROJECT_ROOT" ]] || [[ ! -d "$PROJECT_ROOT" ]]; then
        print_warning "跳过代码引用更新（未提供项目根目录或路径不存在）"
        return
    fi
    
    if [[ "$DRY_RUN" == true ]]; then
        print_info "预览模式：将更新代码中的图片引用"
        return
    fi
    
    print_info "开始更新代码中的图片引用..."
    
    local total_updated=0
    
    # 查找所有 .m 和 .swift 文件
    while IFS= read -r -d '' file; do
        if [[ "$file" =~ /Pods/ ]]; then
            continue
        fi
        
        local file_updated=false
        
        # 更新 ImageNamed 调用
        if sed -i.bak -E "s/ImageNamed\\(@\"([^\"]+)\"/ImageNamed(@\"${PROJECT_NAME}_\\1\"/g" "$file" 2>/dev/null; then
            file_updated=true
        fi
        
        # 更新 [UIImage imageNamed:@"name"]
        if sed -i.bak -E "s/\\[UIImage imageNamed:@\"([^\"]+)\"\\]/[UIImage imageNamed:@\"${PROJECT_NAME}_\\1\"]/g" "$file" 2>/dev/null; then
            file_updated=true
        fi
        
        # 更新 setImage:[UIImage imageNamed:@"name"]
        if sed -i.bak -E "s/setImage:\\[UIImage imageNamed:@\"([^\"]+)\"\\]/setImage:[UIImage imageNamed:@\"${PROJECT_NAME}_\\1\"]/g" "$file" 2>/dev/null; then
            file_updated=true
        fi
        
        # 更新 setBackgroundImage:[UIImage imageNamed:@"name"]
        if sed -i.bak -E "s/setBackgroundImage:\\[UIImage imageNamed:@\"([^\"]+)\"\\]/setBackgroundImage:[UIImage imageNamed:@\"${PROJECT_NAME}_\\1\"]/g" "$file" 2>/dev/null; then
            file_updated=true
        fi
        
        # 更新字典中的图片名称
        if sed -i.bak -E "s/@\"([^\"]+)\"/@\"${PROJECT_NAME}_\\1\"/g" "$file" 2>/dev/null; then
            file_updated=true
        fi
        
        if [[ "$file_updated" == true ]]; then
            # 移除备份文件
            rm -f "$file.bak" 2>/dev/null || true
            print_success "  ✓ 更新: $(realpath --relative-to="$PROJECT_ROOT" "$file")"
            ((total_updated++))
        fi
        
    done < <(find "$PROJECT_ROOT" -type f \( -name "*.m" -o -name "*.swift" \) -print0)
    
    print_success "总共更新了 $total_updated 个代码文件"
}

# 生成报告函数
generate_report() {
    if [[ "$DRY_RUN" == true ]]; then
        print_info "预览模式：将生成重命名报告"
        return
    fi
    
    local report_file="rename_report_${PROJECT_NAME}.txt"
    
    print_info "生成重命名报告: $report_file"
    
    {
        echo "图片重命名报告 - 项目: $PROJECT_NAME"
        echo "=================================================="
        echo ""
        echo "重命名时间: $(date)"
        echo "项目名称: $PROJECT_NAME"
        echo "Assets 路径: $ASSETS_PATH"
        if [[ -n "$PROJECT_ROOT" ]]; then
            echo "项目根目录: $PROJECT_ROOT"
        fi
        echo ""
        echo "重命名映射:"
        echo "（此报告显示所有重命名的图片）"
        echo ""
        echo "注意事项:"
        echo "1. 重命名后需要在 Xcode 中重新编译项目"
        echo "2. 建议在版本控制系统中提交更改"
        echo "3. 如有问题，请检查生成的代码文件"
    } > "$report_file"
    
    print_success "重命名报告已保存到: $report_file"
}

# 主函数
main() {
    print_info "开始执行图片重命名操作..."
    echo ""
    
    # 重命名图片
    rename_images
    
    echo ""
    
    # 更新代码引用
    update_code_references
    
    echo ""
    
    # 生成报告
    generate_report
    
    echo ""
    if [[ "$DRY_RUN" == true ]]; then
        print_warning "预览模式完成！使用不带 --dry-run 参数的命令执行实际重命名"
    else
        print_success "图片重命名完成！"
        print_info "项目前缀: $PROJECT_NAME"
        print_info "请在 Xcode 中重新编译项目"
    fi
}

# 执行主函数
main "$@" 