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
  vec3 tmpvar_4;
  tmpvar_4 = (matWorldView * tmpvar_1).xyz;
  tmpvar_2.xyz = (inColor0.zyxw * vAmbientColor).xyz;
  vec4 tmpvar_5;
  tmpvar_5.w = 1.0;
  tmpvar_5.xyz = vSunColor.xyz;
  float tmpvar_6;
  tmpvar_6 = sqrt(dot (tmpvar_4, tmpvar_4));
  tmpvar_2.w = min (1.0, ((1.0 - 
    (tmpvar_6 / 50.0)
  ) * 2.0));
  gl_Position = (matWorldViewProj * tmpvar_1);
  Fog = (1.0/(exp2((tmpvar_6 * fFogDensity))));
  Color = tmpvar_2;
  Tex0 = inTexCoord;
  SunLight = ((tmpvar_5 * 0.5) * inColor0.zyxw);
  ShadowTexCoord = tmpvar_3;
}

