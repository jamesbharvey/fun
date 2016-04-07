


$candidatePaths = "C:\Program Files (x86)\Git\bin",
                  "C:\Users\James\sysinternals",
                  "C:\Program Files (x86)\ErgoEmacs\bin",
                  "C:\Users\James\projects\fun\bin",
                  "C:\Users\James\Documents\fun\bin",
                  "C:\MinGW\bin",
                  "C:\Program Files\emacs\bin",
                  "C:\Users\James\Desktop\emacs\bin",
                  "C:\rakudo\bin"

		  
                  
                  
foreach ($path in $candidatePaths) {
    if (Test-Path $path) {
        Add-PathVariable -Name Path $path
    }
}

# make this alias to make sure that we use the Pscx version of less if available
$less = "C:\Program Files (x86)\PowerShell Community Extensions\Pscx3\Pscx\Apps\less.exe" 
if (Test-Path $less) {
    New-Item -Path alias:less -Value $less | Out-Null
}

# set this so emacs knows where to look for the .emacs file
$env:HOME="C:\Users\James"
