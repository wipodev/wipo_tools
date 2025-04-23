$historyDir = Join-Path $PSScriptRoot 'history'

if (!(Test-Path $historyDir)) {
    New-Item -Path $historyDir -ItemType Directory | Out-Null
}

$historyFile = Join-Path $historyDir 'history_commands.txt'

if (!(Test-Path $historyFile)) {
    New-Item -Path $historyFile -ItemType File | Out-Null
}

Set-PSReadlineOption -HistorySavePath $historyFile

Set-PSReadlineOption -HistoryNoDuplicates
Set-PSReadLineOption -HistorySaveStyle SaveIncrementally
