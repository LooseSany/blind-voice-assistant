# Run this in an Administrator PowerShell window.
# It enables WSL, installs Ubuntu, then gives next commands.

Write-Host "Enabling WSL + Virtual Machine Platform..."
dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart
dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart

Write-Host "Installing Ubuntu distro..."
wsl --install -d Ubuntu

Write-Host "If prompted, reboot then rerun this script."
Write-Host "After Ubuntu opens, run:"
Write-Host "  cd /mnt/c/Users/LOOSE/vsvoice"
Write-Host "  sudo apt update"
Write-Host "  sudo apt install -y git zip unzip openjdk-17-jdk python3-pip autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo6 cmake libffi-dev libssl-dev"
Write-Host "  pip install --upgrade pip"
Write-Host "  pip install buildozer cython==0.29.37"
Write-Host "  buildozer android debug"