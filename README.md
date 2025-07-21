# 图片重命名工具

这是一个自动化工具，可以根据项目名称自动重命名 Assets.xcassets 中的图片并更新代码中的引用。

## 功能特性

- 🎯 自动重命名 Assets.xcassets 中的所有图片
- 🔄 同步更新代码中的图片引用
- 📝 生成详细的重命名报告
- 👀 支持预览模式，查看将要进行的操作
- 🛡️ 安全操作，避免重复重命名

## 系统要求

- Python 3.6+
- macOS/Linux/Windows

## 安装

1. 下载 `rename_images.py` 文件
2. 确保 Python 3.6+ 已安装
3. 给脚本添加执行权限（Linux/macOS）：
   ```bash
   chmod +x rename_images.py
   ```

## 使用方法

### 基本用法

```bash
python rename_images.py <项目名称> <Assets.xcassets路径>
```

### 完整用法（包含代码更新）

```bash
python rename_images.py <项目名称> <Assets.xcassets路径> --project-root <项目根目录>
```

### 参数说明

- `项目名称`: 用作图片前缀的名称（如 "novi"、"myapp" 等）
- `Assets.xcassets路径`: Assets.xcassets 文件夹的完整路径
- `--project-root`: 项目根目录路径，用于更新代码中的图片引用
- `--dry-run`: 预览模式，仅显示将要进行的操作，不实际执行

## 使用示例

### 示例 1: 基本重命名

```bash
python rename_images.py novi /Users/wcf/Desktop/Novv/Novi/Classes/ClearSource/Assets.xcassets
```

这将：
- 重命名所有图片，添加 "novi_" 前缀
- 生成重命名报告

### 示例 2: 完整重命名（包含代码更新）

```bash
python rename_images.py novi /Users/wcf/Desktop/Novv/Novi/Classes/ClearSource/Assets.xcassets --project-root /Users/wcf/Desktop/Novv
```

这将：
- 重命名所有图片，添加 "novi_" 前缀
- 更新项目中所有 .m 和 .swift 文件中的图片引用
- 生成重命名报告

### 示例 3: 预览模式

```bash
python rename_images.py novi /Users/wcf/Desktop/Novv/Novi/Classes/ClearSource/Assets.xcassets --dry-run
```

这将显示将要进行的操作，但不实际执行重命名。

## 重命名规则

工具会按照以下规则重命名图片：

1. **文件夹结构保持不变**
2. **图片名称格式**: `{项目名称}_{原图片名称}.imageset`
3. **已包含前缀的图片**: 如果图片名称已经包含项目前缀，则跳过重命名
4. **支持的图片类型**: 所有 .imageset 文件夹

### 重命名示例

```
原名称 → 新名称
common_bg.imageset → novi_common_bg.imageset
home_logo.imageset → novi_home_logo.imageset
login_button.imageset → novi_login_button.imageset
```

## 代码引用更新

工具会自动更新以下类型的代码引用：

- `ImageNamed(@"old_name")` → `ImageNamed(@"new_name")`
- `[UIImage imageNamed:@"old_name"]` → `[UIImage imageNamed:@"new_name"]`
- `setImage:[UIImage imageNamed:@"old_name"]` → `setImage:[UIImage imageNamed:@"new_name"]`
- `setBackgroundImage:[UIImage imageNamed:@"old_name"]` → `setBackgroundImage:[UIImage imageNamed:@"new_name"]`
- 字典中的图片名称引用

## 输出文件

执行完成后，工具会生成以下文件：

- `rename_report_{项目名称}.txt`: 详细的重命名报告

## 安全提示

1. **备份项目**: 在执行重命名前，建议备份整个项目
2. **预览模式**: 首次使用建议先运行 `--dry-run` 模式查看将要进行的操作
3. **版本控制**: 确保项目在版本控制系统中，以便回滚操作

## 故障排除

### 常见问题

1. **权限错误**
   ```bash
   chmod +x rename_images.py
   ```

2. **路径错误**
   - 确保 Assets.xcassets 路径正确
   - 确保项目根目录路径正确

3. **编码问题**
   - 确保文件使用 UTF-8 编码
   - 在 Windows 上可能需要设置环境变量

### 错误处理

- 工具会跳过无法访问的文件
- 重命名失败的文件会在控制台显示错误信息
- 代码更新失败的文件会在控制台显示错误信息

## 注意事项

1. **不可逆操作**: 重命名操作是不可逆的，请谨慎操作
2. **Xcode 项目**: 重命名后需要在 Xcode 中重新编译项目
3. **第三方库**: 工具会自动跳过 Pods 目录中的文件
4. **注释代码**: 工具会更新注释中的图片引用

## 许可证

MIT License

## 贡献

欢迎提交 Issue 和 Pull Request 来改进这个工具。 