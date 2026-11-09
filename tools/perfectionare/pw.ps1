Add-Type -AssemblyName System.Drawing
Add-Type @"
using System; using System.Runtime.InteropServices;
public class PW { [DllImport("user32.dll")] public static extern bool PrintWindow(IntPtr h, IntPtr hdc, uint f);
[DllImport("user32.dll")] public static extern bool GetWindowRect(IntPtr h, out R r);
[DllImport("user32.dll")] public static extern bool SetProcessDPIAware();
[DllImport("user32.dll")] public static extern IntPtr SendMessage(IntPtr h,uint m,IntPtr w,IntPtr l);
[DllImport("user32.dll")] public static extern bool PostMessage(IntPtr h,uint m,IntPtr w,IntPtr l);
[DllImport("user32.dll")] public static extern IntPtr ChildWindowFromPointEx(IntPtr h, P p, uint f);
[DllImport("user32.dll")] public static extern bool ShowWindow(IntPtr h,int c);
public struct R { public int L,T,Rt,B; } public struct P { public int X,Y; } }
"@
[PW]::SetProcessDPIAware()|Out-Null
function WShot($h,$path){ $r=New-Object PW+R; [PW]::GetWindowRect($h,[ref]$r)|Out-Null; $w=$r.Rt-$r.L; $hh=$r.B-$r.T; $bmp=New-Object System.Drawing.Bitmap $w,$hh; $g=[System.Drawing.Graphics]::FromImage($bmp); $dc=$g.GetHdc(); [PW]::PrintWindow($h,$dc,2)|Out-Null; $g.ReleaseHdc($dc); $bmp.Save($path); "$($r.L),$($r.T) ${w}x$hh" }
