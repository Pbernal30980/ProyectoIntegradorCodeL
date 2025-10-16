# Script para solucionar los errores de Java/Maven en VS Code

Write-Host "=== Solucionando errores de proyecto MQTT ===" -ForegroundColor Green

# Paso 1: Limpiar y compilar con Maven
Write-Host "`n[1/3] Limpiando y compilando el proyecto Maven..." -ForegroundColor Yellow
mvn clean install
if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Compilación exitosa" -ForegroundColor Green
} else {
    Write-Host "✗ Error en la compilación" -ForegroundColor Red
}

# Paso 2: Verificar que las dependencias se descargaron
Write-Host "`n[2/3] Verificando dependencias..." -ForegroundColor Yellow
$pahoPath = "$env:USERPROFILE\.m2\repository\org\eclipse\paho\org.eclipse.paho.client.mqttv3\1.2.5"
if (Test-Path $pahoPath) {
    Write-Host "✓ Dependencia de Eclipse Paho MQTT encontrada en:" -ForegroundColor Green
    Write-Host "  $pahoPath" -ForegroundColor Gray
} else {
    Write-Host "✗ Dependencia NO encontrada. Ejecutando mvn install..." -ForegroundColor Red
    mvn dependency:resolve
}

# Paso 3: Instrucciones para VS Code
Write-Host "`n[3/3] Pasos finales en VS Code:" -ForegroundColor Yellow
Write-Host "  1. Presiona Ctrl+Shift+P" -ForegroundColor Cyan
Write-Host "  2. Escribe: 'Java: Clean Java Language Server Workspace'" -ForegroundColor Cyan
Write-Host "  3. Selecciona 'Reload and delete'" -ForegroundColor Cyan
Write-Host "  4. Espera a que VS Code recargue" -ForegroundColor Cyan
Write-Host "`n  O simplemente:" -ForegroundColor Yellow
Write-Host "  1. Presiona Ctrl+Shift+P" -ForegroundColor Cyan
Write-Host "  2. Escribe: 'Developer: Reload Window'" -ForegroundColor Cyan

Write-Host "`n=== Los archivos correctos están en: ===" -ForegroundColor Green
Write-Host "  src\main\java\MQTTPublisher.java" -ForegroundColor White
Write-Host "  src\main\java\MQTTSubscriber.java" -ForegroundColor White

Write-Host "`n✓ Script completado. Sigue los pasos anteriores." -ForegroundColor Green
