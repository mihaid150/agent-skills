# Leagă fiecare skill din repo în ~/.claude/skills și ~/.codex/skills prin junction-uri.
# Fără -Force: sare peste folderele reale existente. Cu -Force: le mută într-un backup.
param([switch]$Force)

$repoSkills = Join-Path (Split-Path $PSScriptRoot -Parent) 'skills'
$targets = @((Join-Path $HOME '.claude\skills'), (Join-Path $HOME '.codex\skills'))
$stamp = Get-Date -Format 'yyyyMMdd-HHmmss'

foreach ($root in $targets) {
    New-Item -ItemType Directory -Force -Path $root | Out-Null
    foreach ($skill in Get-ChildItem $repoSkills -Directory) {
        $link = Join-Path $root $skill.Name
        $item = Get-Item $link -Force -ErrorAction SilentlyContinue

        if ($item -and $item.LinkType -eq 'Junction') {
            if ($item.Target -eq $skill.FullName) { Write-Host "ok      $link"; continue }
            $item.Delete()  # junction către alt loc: șterge doar legătura, nu conținutul
        }
        elseif ($item) {
            if (-not $Force) { Write-Host "SKIP    $link (folder real; rulează cu -Force)"; continue }
            $backup = "$root-backup-$stamp"
            New-Item -ItemType Directory -Force -Path $backup | Out-Null
            Move-Item $link (Join-Path $backup $skill.Name)
            Write-Host "backup  $link -> $backup"
        }

        New-Item -ItemType Junction -Path $link -Target $skill.FullName | Out-Null
        Write-Host "linked  $link"
    }
}
