# 将 alpha 系列 JPG 图标转换为 PNG 格式
# 要求：144x144 像素

$iconPath = "c:\repo\my code\ebic\icon"

# 需要转换的文件列表
$files = @("alpha-alpha.JPG", "alpha-child.JPG", "alpha-pro.JPG")

Add-Type -AssemblyName System.Drawing

foreach ($file in $files) {
    $jpgPath = Join-Path $iconPath $file
    $pngName = $file -replace '\.JPG$', '.png'
    $pngPath = Join-Path $iconPath $pngName
    
    if (Test-Path $jpgPath) {
        try {
            # 加载 JPG 图片
            $image = [System.Drawing.Image]::FromFile($jpgPath)
            
            # 创建 144x144 的位图（如果需要调整大小）
            $bitmap = New-Object System.Drawing.Bitmap(144, 144)
            $graphics = [System.Drawing.Graphics]::FromImage($bitmap)
            $graphics.InterpolationMode = [System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
            $graphics.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::HighQuality
            $graphics.PixelOffsetMode = [System.Drawing.Drawing2D.PixelOffsetMode]::HighQuality
            
            # 绘制图片（如果尺寸不是144x144，会自动缩放）
            $graphics.DrawImage($image, 0, 0, 144, 144)
            
            # 保存为 PNG
            $bitmap.Save($pngPath, [System.Drawing.Imaging.ImageFormat]::Png)
            
            Write-Host "✓ 已转换: $file -> $pngName" -ForegroundColor Green
            
            # 清理资源
            $graphics.Dispose()
            $bitmap.Dispose()
            $image.Dispose()
        }
        catch {
            Write-Host "✗ 转换失败: $file - $($_.Exception.Message)" -ForegroundColor Red
        }
    }
    else {
        Write-Host "✗ 文件不存在: $file" -ForegroundColor Yellow
    }
}

Write-Host "`n转换完成！" -ForegroundColor Cyan

