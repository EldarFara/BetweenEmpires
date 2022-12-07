uniform vec4 vMaterialColor;
uniform float fFogDensity;
uniform mat4 matWorldViewProj;
uniform mat4 matWorldView;
attribute vec3 inPosition;
attribute vec4 inColor0;
attribute vec2 inTexCoord;
varying float Fog;
varying vec2 Tex0;
varying vec4 Color;
varying vec4 SunLight;
varying vec4 ShadowTexCoord;
void main ()
{
  vec4 tmpvar_1;
  tmpvar_1.w = 1.0;
  tmpvar_1.xyz = inPosition;
  vec4 tmpvar_2;
  vec4 tmpvar_3;
  vec3 tmpvar_4;
  tmpvar_4 = (matWorldView * tmpvar_1).xyz;
  gl_Position = (matWorldViewProj * tmpvar_1);
  Fog = (1.0/(exp2((
    sqrt(dot (tmpvar_4, tmpvar_4))
   * fFogDensity))));
  Tex0 = inTexCoord;
  Color = (inColor0.zyxw * vMaterialColor);
  SunLight = tmpvar_2;
  ShadowTexCoord = tmpvar_3;
}

