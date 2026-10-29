param([string]$Src = "D:\Projects\SS\SyntheticSilence2.0\review1\SyntheticSilence_RI_Review1.pptx",
      [string]$Out = "D:\Projects\SS\SyntheticSilence2.0\review1\build\render",
      [string]$Pdf = "D:\Projects\SS\SyntheticSilence2.0\review1\SyntheticSilence_RI_Review1.pdf")
if (Test-Path $Out) { Remove-Item $Out -Recurse -Force }
New-Item -ItemType Directory $Out | Out-Null
$app = New-Object -ComObject PowerPoint.Application
$p = $app.Presentations.Open($Src, $true, $false, $false)
$p.Export($Out, "PNG", 1600, 900)
$p.SaveAs($Pdf, 32)
$p.Close(); $app.Quit()
"rendered " + (Get-ChildItem $Out).Count + " slides"
