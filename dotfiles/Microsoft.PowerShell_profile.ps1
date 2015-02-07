Add-PathVariable -Name Path "C:\Program Files (x86)\Git\bin"
Add-PathVariable -Name Path "C:\Users\James\sysinternals"
Add-PathVariable -Name Path "C:\Program Files (x86)\ErgoEmacs\bin"
new-item -path alias:less -Value "C:\Program Files (x86)\PowerShell Community Extensions\Pscx3\Pscx\Apps\less.exe"

# set this so emacs knows where to look for the .emacs file
$env:HOME="C:\Users\James"
