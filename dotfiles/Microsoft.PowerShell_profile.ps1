$candidatePaths = "C:\Users\james.harvey\go\bin",
                  "C:\Program Files (x86)\Git\bin",
                  "C:\Users\James\sysinternals",
                  "C:\Program Files\emacs\bin",
                  "C:\Program Files (x86)\ErgoEmacs\bin",
                  "C:\Users\James\projects\fun\bin",
                  "C:\Users\James\Documents\fun\bin",
                  "C:\MinGW\bin",
                  "C:\Users\James\Desktop\emacs\bin",
                  "C:\Program Files (x86)\Vim\vim80\",
                  "C:\rakudo\bin",
                  "C:\Users\james.harvey\IdeaProjects\bin\activator-dist-1.3.12\bin"

foreach ($path in $candidatePaths) {
    if (Test-Path $path) {
        Add-PathVariable -Name Path $path^M
    }
}

Set-Alias np c:\windows\notepad.exe^M
set-alias sh "C:\Program Files (x86)\Gow\bin\bash.exe"
Set-PSReadlineKeyHandler -Key Tab -Function Complete

# make this alias to make sure that we use the Pscx version of less if available
$less = "C:\Program Files (x86)\PowerShell Community Extensions\Pscx3\Pscx\Apps\less.exe" 
if (Test-Path $less) {
    New-Item -Path alias:less -Value $less | Out-Null
#set-alias -Name sh -Value "C:\Program Files (x86)\Gow\bin\bash.exe"
}

# set this so emacs knows where to look for the .emacs file
$env:HOME="C:\Users\james.harvey"
$env:GOPATH=go env GOPATH
#$env:GOPATH="C:\Users\james.harvey\IdeaProjects\go"
#$env:GOPATH="C:\Users\james.harvey\IdeaProjects\minos\src\minos"
$env:JAVA_HOME="C:\Program Files\Java\jdk1.8.0_121\"

Import-Module posh-docker^M
