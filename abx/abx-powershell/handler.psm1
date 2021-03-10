function handler {
  Param($context, $inputs)
  $inputsString = $inputs | ConvertTo-Json -Compress
  $DebugPreference = "Continue"

  $proxyString = "http://" + $context.proxy.host + ":" + $context.proxy.port
  $Env:HTTP_PROXY = $proxyString
  $Env:HTTPS_PROXY = $proxyString

  Write-Host $proxyString
  $proxyUri = new-object System.Uri($proxyString)
  [System.Net.WebRequest]::DefaultWebProxy = new-object System.Net.WebProxy ($proxyUri)
  Write-Host "Inputs were $inputsString"
  # From this point it is my script making calls to MS Azure
