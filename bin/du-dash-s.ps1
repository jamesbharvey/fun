
gci . | 
 %{$f=$_; gci -r $_.FullName | 
  measure-object -property length -sum |
   select  @{Name="Name"; Expression={$f}} , @{Name="Sum (MB)"; Expression={  "{0:N3}" -f ($_.sum / 1MB) }}, Sum } | 
    sort Sum -desc |
     format-table -Property Name,"Sum (MB)", Sum -autosize

# based on answer by Tomalak from
# http://stackoverflow.com/questions/868264/du-in-powershell
#