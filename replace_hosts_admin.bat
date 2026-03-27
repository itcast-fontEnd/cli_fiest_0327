@echo off
chcp 65001 >nul
echo ==========================================
echo Hosts文件替换工具（管理员权限）
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

echo 正在备份原始hosts文件...
set hostsPath=%windir%\System32\drivers\etc\hosts
set backupPath=%hostsPath%.backup.%date:~0,4%%date:~5,2%%date:~8,2%%time:~0,2%%time:~3,2%
copy "%hostsPath%" "%backupPath%" >nul
echo 备份已创建: %backupPath%
echo.

echo 正在获取文件所有权...
takeown /f "%hostsPath%" >nul
icacls "%hostsPath%" /grant Administrators:F >nul
echo 权限已设置
echo.

echo 正在替换hosts文件内容...
type "%~dp0new_hosts.txt" > "%hostsPath%"
echo 文件已替换
echo.

echo 正在刷新DNS缓存...
ipconfig /flushdns >nul
echo DNS缓存已刷新
echo.

echo 验证新文件内容...
echo.
type "%hostsPath%" | findstr /i "github"
echo.

echo ==========================================
echo 完成！请测试GitHub连接：
echo curl.exe https://api.github.com/zen
echo ==========================================
pause