# Set the path to the executable relative to the script's location
$exePath = Join-Path $PSScriptRoot "DidMyGamesUpdate.exe"

# Generate the XML task definition
$xmlDefinition = @"
<?xml version="1.0" encoding="UTF-16"?>
<Task version="1.2" xmlns="http://schemas.microsoft.com/windows/2004/02/mit/task">
  <RegistrationInfo>
    <Date>$((Get-Date).ToString("yyyy-MM-ddTHH:mm:ss"))</Date>
    <Author>$($env:USERDOMAIN)\$($env:USERNAME)</Author>
    <URI>\DidMyGamesUpdate</URI>
  </RegistrationInfo>
  <Triggers>
    <CalendarTrigger>
      <StartBoundary>$((Get-Date).ToString("yyyy-MM-ddTHH:mm:ss"))</StartBoundary>
      <Enabled>true</Enabled>
      <ScheduleByDay>
        <DaysInterval>1</DaysInterval>
      </ScheduleByDay>
    </CalendarTrigger>
  </Triggers>
  <Principals>
    <Principal id="Author">
      <UserId>$($env:USERDOMAIN)\$($env:USERNAME)</UserId>
      <LogonType>InteractiveToken</LogonType>
      <RunLevel>LeastPrivilege</RunLevel>
    </Principal>
  </Principals>
  <Settings>
    <MultipleInstancesPolicy>IgnoreNew</MultipleInstancesPolicy>
    <DisallowStartIfOnBatteries>false</DisallowStartIfOnBatteries>
    <StopIfGoingOnBatteries>true</StopIfGoingOnBatteries>
    <AllowHardTerminate>true</AllowHardTerminate>
    <StartWhenAvailable>true</StartWhenAvailable>
    <RunOnlyIfNetworkAvailable>true</RunOnlyIfNetworkAvailable>
    <IdleSettings>
      <StopOnIdleEnd>true</StopOnIdleEnd>
      <RestartOnIdle>false</RestartOnIdle>
    </IdleSettings>
    <AllowStartOnDemand>true</AllowStartOnDemand>
    <Enabled>true</Enabled>
    <Hidden>false</Hidden>
    <RunOnlyIfIdle>false</RunOnlyIfIdle>
    <WakeToRun>false</WakeToRun>
    <ExecutionTimeLimit>PT4H</ExecutionTimeLimit>
    <Priority>7</Priority>
    <RestartOnFailure>
      <Interval>PT1M</Interval>
      <Count>3</Count>
    </RestartOnFailure>
  </Settings>
  <Actions Context="Author">
    <Exec>
      <Command>$exePath</Command>
      <WorkingDirectory>$($PSScriptRoot)</WorkingDirectory>
    </Exec>
  </Actions>
</Task>
"@

# Import the task definition into the Windows Task Scheduler
$taskName = "DidMyGamesUpdate"
$action = New-ScheduledTaskAction -Execute $exePath -WorkingDirectory $PSScriptRoot
$trigger = New-ScheduledTaskTrigger -Daily -At 3:04am
Register-ScheduledTask -TaskName $taskName -Xml $xmlDefinition -Force