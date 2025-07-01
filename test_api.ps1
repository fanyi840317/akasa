$headers = @{
    'Content-Type' = 'application/json'
    'Accept' = 'text/event-stream'
}

$body = @'
{
    "messages": [{"role": "user", "content": "hello"}],
    "thread_id": "test",
    "resources": [],
    "max_plan_iterations": 3,
    "max_step_num": 10,
    "max_search_results": 5,
    "auto_accepted_plan": true,
    "interrupt_feedback": "",
    "mcp_settings": {},
    "enable_background_investigation": false,
    "report_style": "academic",
    "enable_deep_thinking": false
}
'@

try {
    Write-Host "Testing API endpoint..."
    $response = Invoke-WebRequest -Uri 'http://localhost:8000/api/chat/stream' -Method POST -Headers $headers -Body $body -TimeoutSec 10
    Write-Host "Success! Status: $($response.StatusCode)"
    Write-Host "Content-Type: $($response.Headers['Content-Type'])"
    Write-Host "Content Length: $($response.Content.Length)"
    if ($response.Content.Length -gt 0) {
        Write-Host "First 200 chars: $($response.Content.Substring(0, [Math]::Min(200, $response.Content.Length)))"
    }
} catch {
    Write-Host "Error: $($_.Exception.Message)"
    Write-Host "Status Code: $($_.Exception.Response.StatusCode)"
}