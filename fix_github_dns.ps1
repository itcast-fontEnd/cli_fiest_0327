# GitHub DNS 修复脚本
# 需要以管理员身份运行 PowerShell

$hostsPath = "$env:windir\System32\drivers\etc\hosts"

# 检查是否以管理员身份运行
$currentPrincipal = New-Object Security.Principal.WindowsPrincipal([Security.Principal.WindowsIdentity]::GetCurrent())
if (-not $currentPrincipal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
    Write-Host "请以管理员身份运行此脚本！" -ForegroundColor Red
    Write-Host "右键点击 PowerShell，选择'以管理员身份运行'，然后执行此脚本。"
    pause
    exit 1
}

# 备份原始 hosts 文件
$backupPath = "$hostsPath.backup.$(Get-Date -Format 'yyyyMMddHHmmss')"
Copy-Item $hostsPath $backupPath -Force
Write-Host "已备份 hosts 文件到: $backupPath" -ForegroundColor Green

# 要添加的 GitHub 条目
$githubEntries = @(
    "# GitHub DNS 修复 - 添加于 $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')",
    "140.82.113.6    api.github.com",
    "140.82.112.6    github.com",
    "140.82.112.6    raw.githubusercontent.com",
    "140.82.113.6    uploads.github.com"
)

Write-Host "正在添加以下条目到 hosts 文件:" -ForegroundColor Yellow
$githubEntries | ForEach-Object { Write-Host "  $_" }

# 读取现有内容
$content = Get-Content $hostsPath -Raw

# 移除可能已存在的相同条目（避免重复）
$lines = Get-Content $hostsPath
$filteredLines = $lines | Where-Object {
    -not ($_ -match '^\s*140\.82\.\d+\.\d+\s+(api\.github\.com|github\.com|raw\.githubusercontent\.com|uploads\.github\.com)')
}

# 添加新条目
$newContent = $filteredLines + $githubEntries

# 写入文件
$newContent | Out-File $hostsPath -Encoding ASCII
Write-Host "`nhosts 文件已更新！" -ForegroundColor Green

# 刷新 DNS 缓存
Write-Host "正在刷新 DNS 缓存..." -ForegroundColor Yellow
ipconfig /flushdns | Out-Null

Write-Host "`n验证连接..." -ForegroundColor Yellow

# 测试连接
Write-Host "1. 测试 api.github.com 连接..."
try {
    $response = Invoke-WebRequest -Uri "https://api.github.com/zen" -TimeoutSec 10
    Write-Host "   ✓ 连接成功: $($response.Content)" -ForegroundColor Green
} catch {
    Write-Host "   ✗ 连接失败: $_" -ForegroundColor Red
}

Write-Host "`n2. 测试 github.com 连接..."
try {
    $response = Invoke-WebRequest -Uri "https://github.com" -TimeoutSec 10
    Write-Host "   ✓ 连接成功 (状态码: $($response.StatusCode))" -ForegroundColor Green
} catch {
    Write-Host "   ✗ 连接失败: $_" -ForegroundColor Red
}

Write-Host "`n3. 测试 raw.githubusercontent.com 连接..."
try {
    $response = Invoke-WebRequest -Uri "https://raw.githubusercontent.com/octocat/Hello-World/master/README" -TimeoutSec 10
    Write-Host "   ✓ 连接成功 (状态码: $($response.StatusCode))" -ForegroundColor Green
} catch {
    Write-Host "   ✗ 连接失败: $_" -ForegroundColor Red
}

Write-Host "`n==========================================" -ForegroundColor Cyan
Write-Host "GitHub DNS 修复完成！" -ForegroundColor Green
Write-Host "现在可以尝试运行: gh auth login" -ForegroundColor Yellow
Write-Host "==========================================" -ForegroundColor Cyan

pause