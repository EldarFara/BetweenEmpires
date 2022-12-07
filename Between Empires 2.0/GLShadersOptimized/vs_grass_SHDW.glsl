uniform vec4 vMaterialColor;
uniform vec4 vSunColor;
uniform vec4 vAmbientColor;
uniform float fFogDensity;
uniform mat4 matWorldViewProj;
uniform mat4 matWorldView;
uniform mat4 matWorld;
uniform mat4 matSunViewProj;
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
  vec3 tmpvar_3;
  tmpvar_3 = (matWorldView * tmpvar_1).xyz;
  tmpvar_2.xyz = (inColor0.zyxw * vAmbientColor).xyz;
  vec4 tmpvar_4;
  tmpvar_4.w = 1.0;
  tmpvar_4.xyz = vSunColor.xyz;
  float tmpvar_5;
  tmpvar_5 = sqrt(dot (tmpvar_3, tmpvar_3));
  tmpvar_2.w = min (1.0, ((1.0 - 
    (tmpvar_5 / 50.0)
  ) * 2.0));
  gl_Position = (matWorldViewProj * tmpvar_1);
  Fog = (1.0/(exp2((tmpvar_5 * fFogDensity))));
  Color = tmpvar_2;
  Tex0 = inTexCoord;
  SunLight = ((tmpvar_4 * 0.55) * (vMaterialColor * inColor0.zyxw));
  ShadowTexCoord = (matSunViewProj * (matWorld * tmpvar_1));
}

