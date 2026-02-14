$ErrorActionPreference = 'Stop'
New-Item -ItemType Directory -Force .tools | Out-Null
New-Item -ItemType Directory -Force .android-sdk | Out-Null

# Download portable JDK 17
$jdkZip = '.tools\jdk17.zip'
if (!(Test-Path $jdkZip)) {
  Invoke-WebRequest -Uri 'https://api.adoptium.net/v3/binary/latest/17/ga/windows/x64/jdk/hotspot/normal/eclipse' -OutFile $jdkZip
}
if (!(Test-Path '.tools\jdk-17')) {
  Expand-Archive -Path $jdkZip -DestinationPath .tools -Force
  $jdkDir = Get-ChildItem .tools -Directory | Where-Object { $_.Name -like 'jdk-17*' } | Select-Object -First 1
  Rename-Item -Path $jdkDir.FullName -NewName 'jdk-17'
}

# Download Android cmdline tools
$cmdZip = '.tools\commandlinetools.zip'
if (!(Test-Path $cmdZip)) {
  Invoke-WebRequest -Uri 'https://dl.google.com/android/repository/commandlinetools-win-11076708_latest.zip' -OutFile $cmdZip
}
if (!(Test-Path '.android-sdk\cmdline-tools\latest')) {
  New-Item -ItemType Directory -Force .android-sdk\cmdline-tools\latest | Out-Null
  Expand-Archive -Path $cmdZip -DestinationPath .android-sdk\cmdline-tools\latest -Force
  if (Test-Path '.android-sdk\cmdline-tools\latest\cmdline-tools') {
    Get-ChildItem '.android-sdk\cmdline-tools\latest\cmdline-tools' | ForEach-Object {
      Move-Item $_.FullName '.android-sdk\cmdline-tools\latest' -Force
    }
    Remove-Item '.android-sdk\cmdline-tools\latest\cmdline-tools' -Recurse -Force
  }
}

# Download portable Gradle
$gradleZip = '.tools\gradle.zip'
if (!(Test-Path $gradleZip)) {
  Invoke-WebRequest -Uri 'https://services.gradle.org/distributions/gradle-8.7-bin.zip' -OutFile $gradleZip
}
if (!(Test-Path '.tools\gradle-8.7')) {
  Expand-Archive -Path $gradleZip -DestinationPath .tools -Force
}

Write-Output 'Downloaded toolchains successfully.'
