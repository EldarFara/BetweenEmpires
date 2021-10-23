@echo off
fxc /D PS_2_X=ps_2_a /T fx_2_0 /Fo mb_2a.fxo mb.fx
fxc /D PS_2_X=ps_2_b /T fx_2_0 /Fo mb_2b.fxo mb.fx


echo Script processing has ended.
echo Press any key to exit. . .
pause>nul