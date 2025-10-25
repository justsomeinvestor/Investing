param(
  [string]$RepoRoot = (Get-Location).Path,
  [switch]$Force,          # Overwrite existing files if present
  [switch]$SkipClaudeMd    # Don't create CLAUDE.md
)

Write-Host "Configuring Claude Code write-scope at: $RepoRoot" -ForegroundColor Cyan

# 1) Create folders: toolbox and .claude
$toolboxDir = Join-Path $RepoRoot "toolbox"
$claudeDir  = Join-Path $RepoRoot ".claude"
New-Item -ItemType Directory -Path $toolboxDir -Force | Out-Null
New-Item -ItemType Directory -Path $claudeDir  -Force | Out-Null

# 2) Minimal settings.json to allow edits only under /toolbox/**
$settingsPath = Join-Path $claudeDir "settings.json"
$settingsJson = @'
{
  "permissions": {
    "allow": [
      "Read(./**)",
      "Edit(/toolbox/**)"
    ],
    "deny": [
      "Edit(/**)"
    ]
  }
}
'@

if (Test-Path $settingsPath) {
  if ($Force) {
    Write-Host "Overwriting existing .claude/settings.json (due to -Force)..." -ForegroundColor Yellow
    $settingsJson | Set-Content -Path $settingsPath -Encoding UTF8
  } else {
    Write-Host ".claude/settings.json already exists. Use -Force to overwrite. Skipping." -ForegroundColor Yellow
  }
} else {
  $settingsJson | Set-Content -Path $settingsPath -Encoding UTF8
  Write-Host "Created .claude/settings.json" -ForegroundColor Green
}

# 3) Optional: simple CLAUDE.md project rule
if (-not $SkipClaudeMd) {
  $claudeMdPath = Join-Path $RepoRoot "CLAUDE.md"
  $claudeMd = @'
# Project rule
All documentation Claude creates must go in `/toolbox/` (Markdown preferred).
'@
  if (Test-Path $claudeMdPath) {
    if ($Force) {
      Write-Host "Overwriting existing CLAUDE.md (due to -Force)..." -ForegroundColor Yellow
      $claudeMd | Set-Content -Path $claudeMdPath -Encoding UTF8
    } else {
      Write-Host "CLAUDE.md already exists. Use -Force to overwrite. Skipping." -ForegroundColor Yellow
    }
  } else {
    $claudeMd | Set-Content -Path $claudeMdPath -Encoding UTF8
    Write-Host "Created CLAUDE.md" -ForegroundColor Green
  }
} else {
  Write-Host "Skipping CLAUDE.md (per -SkipClaudeMd)" -ForegroundColor DarkYellow
}

Write-Host "`nDone. Claude Code can read the repo but will only write/edit under /toolbox/**." -ForegroundColor Cyan
Write-Host "Tip: Commit .claude/settings.json so the rule travels with the project." -ForegroundColor DarkCyan
