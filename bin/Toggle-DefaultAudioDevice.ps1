$soundcard="Speakers (Creative SB X-Fi)"
$hdmi="27EA73-1 (NVIDIA High Definition Audio)"
$current_device=Get-DefaultAudioDevice
if ($current_device.DeviceFriendlyName -eq $hdmi)
{
 Set-DefaultAudioDevice $soundcard
}
if ($current_device.DeviceFriendlyName -eq $soundcard)
{
 Set-DefaultAudioDevice $hdmi
}
