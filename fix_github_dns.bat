@echo off
chcp 65001 >nul
echo ==========================================
echo GitHub DNS 修复工具
echo ==========================================
echo.

REM 检查管理员权限
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo 请以管理员身份运行此批处理文件！
    echo 右键点击此文件，选择"以管理员身份运行"
    pause
    exit /b 1
)

echo 正在备份 hosts 文件...
set hostsPath=%windir%\System32\drivers\etc\hosts
set backupPath=%hostsPath%.backup.%date:~0,4%%date:~5,2%%date:~8,2%%time:~0,2%%time:~3,2%
copy "%hostsPath%" "%backupPath%" >nul
echo 备份已创建: %backupPath%
echo.

echo 请手动编辑 hosts 文件，添加以下内容：
echo.
echo # GitHub DNS 修复 - 添加于 %date% %time%
echo 140.82.113.6    api.github.com
echo 140.82.112.6    github.com
echo 140.82.112.6    raw.githubusercontent.com
echo 140.82.113.6    uploads.github.com
echo.

echo 按任意键打开 hosts 文件进行编辑...
pause >nul

REM 以管理员身份打开 Notepad
notepad "%hostsPath%"

echo.
echo 请确保已添加上述内容，然后保存文件。
echo.
echo 正在刷新 DNS 缓存...
ipconfig /flushdns >nul

echo.
echo 正在测试连接...
echo.

echo 1. 测试 api.github.com 连接...
curl -s https://api.github.com/zen
if %errorLevel% equ 0 (
    echo ✓ 连接成功
) else (
    echo ✗ 连接失败
)

echo.
echo 2. 测试 github.com 连接...
curl -I -s https://github.com | findstr "HTTP"
if %errorLevel% equ 0 (
    echo ✓ 连接成功
) else (
    echo ✗ 连接失败
)

echo.
echo ==========================================
echo 如果连接测试成功，现在可以运行: gh auth login
echo ==========================================
pause