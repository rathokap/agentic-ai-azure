# Azure Resources Cleanup Script
# Use this to delete all Azure resources created for the support agent

param(
    [Parameter(Mandatory=$false)]
    [string]$ResourceGroup = "rg-support-agent"
)

Write-Host "========================================" -ForegroundColor Yellow
Write-Host "Azure Resources Cleanup" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Yellow
Write-Host ""

Write-Host "This will DELETE the following:" -ForegroundColor Red
Write-Host "  • Resource Group: $ResourceGroup" -ForegroundColor White
Write-Host "  • All resources within the group" -ForegroundColor White
Write-Host "  • All data and configurations" -ForegroundColor White
Write-Host ""
Write-Host "⚠️  This action CANNOT be undone!" -ForegroundColor Red
Write-Host ""

$confirm = Read-Host "Type 'DELETE' to confirm deletion"

if ($confirm -ne "DELETE") {
    Write-Host "Cleanup cancelled." -ForegroundColor Green
    exit 0
}

Write-Host "`nDeleting resource group..." -ForegroundColor Yellow

try {
    az group delete --name $ResourceGroup --yes --no-wait
    Write-Host "✓ Deletion initiated. This may take several minutes." -ForegroundColor Green
    Write-Host ""
    Write-Host "Monitor deletion status:" -ForegroundColor Cyan
    Write-Host "  az group show --name $ResourceGroup" -ForegroundColor White
    Write-Host ""
} catch {
    Write-Host "❌ Failed to delete resource group" -ForegroundColor Red
    Write-Host "Error: $_" -ForegroundColor Red
}
