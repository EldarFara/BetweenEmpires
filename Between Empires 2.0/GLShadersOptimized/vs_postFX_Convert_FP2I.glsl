uniform vec4 g_HalfPixel_ViewportSizeInv;
attribute vec3 inPosition;
varying vec2 texCoord0;
varying vec2 texCoord1;
varying vec2 texCoord2;
varying vec2 texCoord3;
void main ()
{
  vec4 tmpvar_1;
  tmpvar_1.w = 1.0;
  tmpvar_1.xyz = inPosition;
  gl_Position = tmpvar_1;
  vec2 tmpvar_2;
  tmpvar_2 = ((inPosition.xy * 0.5) + 0.5);
  texCoord0 = (tmpvar_2 + (vec2(-1.0, 1.0) * g_HalfPixel_ViewportSizeInv.xy));
  texCoord1 = (tmpvar_2 + g_HalfPixel_ViewportSizeInv.xy);
  texCoord2 = (tmpvar_2 + (vec2(1.0, -1.0) * g_HalfPixel_ViewportSizeInv.xy));
  texCoord3 = (tmpvar_2 - g_HalfPixel_ViewportSizeInv.xy);
}

