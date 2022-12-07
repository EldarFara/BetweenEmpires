uniform vec4 vMaterialColor;
uniform vec4 vSunColor;
uniform vec4 vAmbientColor;
uniform float fFogDensity;
uniform mat4 matWorldViewProj;
uniform mat4 matWorldView;
attribute vec3 inPosition;
attribute vec4 inColor0;
attribute vec2 inTexCoord;
varying float Fog;
varying vec4 Color;
varying vec2 Tex0;
varying vec4 SunLight;
varying vec4 ShadowTexCoord;
void main ()
{
  vec4 tmpvar_1;
  tmpvar_1.w = 1.0;
  tmpvar_1.xyz = inPosition;
  vec4 tmpvar_2;
  vec4 tmpvar_3;
  vec4 tmpvar_4;
  tmpvar_4.w = 1.0;
  tmpvar_4.xyz = vSunColor.xyz;
  tmpvar_2 = (inColor0.zyxw * (vAmbientColor + (tmpvar_4 * 0.06)));
  tmpvar_2.w = (tmpvar_2.w * vMaterialColor.w);
  vec4 tmpvar_5;
  tmpvar_5.w = 1.0;
  tmpvar_5.xyz = vSunColor.xyz;
  vec3 tmpvar_6;
  tmpvar_6 = (matWorldView * tmpvar_1).xyz;
  gl_Position = (matWorldViewProj * tmpvar_1);
  Fog = (1.0/(exp2((
    sqrt(dot (tmpvar_6, tmpvar_6))
   * fFogDensity))));
  Color = tmpvar_2;
  Tex0 = inTexCoord;
  SunLight = ((tmpvar_5 * 0.34) * (vMaterialColor * inColor0.zyxw));
  ShadowTexCoord = tmpvar_3;
}

