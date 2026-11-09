Add-Type @"
using System; using System.Runtime.InteropServices; using System.Text;
public class CW { public delegate bool EP(IntPtr h, IntPtr l);
[DllImport("user32.dll")] public static extern bool EnumChildWindows(IntPtr p, EP cb, IntPtr l);
[DllImport("user32.dll")] public static extern int GetClassName(IntPtr h, StringBuilder s, int n);
[DllImport("user32.dll")] public static extern int GetWindowText(IntPtr h, StringBuilder s, int n);
[DllImport("user32.dll")] public static extern bool GetWindowRect(IntPtr h, out RR r); public struct RR { public int L,T,Rt,B; } }
"@
function Kids($h){ $list=New-Object System.Collections.ArrayList; [CW]::EnumChildWindows($h,{param($c,$l) $cn=New-Object Text.StringBuilder 128; $t=New-Object Text.StringBuilder 256; [CW]::GetClassName($c,$cn,128)|Out-Null; [CW]::GetWindowText($c,$t,256)|Out-Null; $r=New-Object CW+RR; [CW]::GetWindowRect($c,[ref]$r)|Out-Null; [void]$list.Add([pscustomobject]@{H=$c;Cls=$cn.ToString();Txt=$t.ToString();L=$r.L;T=$r.T;W=$r.Rt-$r.L;Hh=$r.B-$r.T}); $true },[IntPtr]::Zero)|Out-Null; $list }
function BtnClick($c){ [PW]::SendMessage($c,0x00F5,[IntPtr]::Zero,[IntPtr]::Zero)|Out-Null }
function PClick($h,$x,$y){ $lp=[IntPtr](($y -shl 16) -bor $x); [PW]::PostMessage($h,0x201,[IntPtr]1,$lp)|Out-Null; Start-Sleep -m 60; [PW]::PostMessage($h,0x202,[IntPtr]0,$lp)|Out-Null }
function PDbl($h,$x,$y){ $lp=[IntPtr](($y -shl 16) -bor $x); PClick $h $x $y; [PW]::PostMessage($h,0x203,[IntPtr]1,$lp)|Out-Null; [PW]::PostMessage($h,0x202,[IntPtr]0,$lp)|Out-Null }

