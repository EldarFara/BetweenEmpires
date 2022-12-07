uniform vec4 vMaterialColor;
uniform vec4 vSunDir;
uniform vec4 vSunColor;
uniform vec4 vAmbientColor;
uniform vec4 vSkyLightDir;
uniform vec4 vSkyLightColor;
uniform float fFogDensity;
uniform mat4 matWorldViewProj;
uniform mat4 matWorldView;
uniform mat4 matWorld;
uniform vec4 vCameraPos;
attribute vec3 inPosition;
attribute vec3 inNormal;
attribute vec4 inColor0;
attribute vec4 inColor1;
attribute vec2 inTexCoord;
varying float Fog;
varying vec4 Color;
varying vec2 Tex0;
varying float Map;
void main ()
{
  vec4 tmpvar_1;
  tmpvar_1.w = 1.0;
  tmpvar_1.xyz = inPosition;
  vec4 diffuse_light_2;
  vec4 tmpvar_3;
  tmpvar_3.w = 0.0;
  tmpvar_3.xyz = inNormal;
  vec3 tmpvar_4;
  tmpvar_4 = normalize((matWorld * tmpvar_3).xyz);
  vec3 tmpvar_5;
  tmpvar_5 = (matWorldView * tmpvar_1).xyz;
  vec4 tmpvar_6;
  tmpvar_6 = (vAmbientColor + inColor1.zyxw);
  diffuse_light_2.w = tmpvar_6.w;
  diffuse_light_2.xyz = (tmpvar_6.xyz + (clamp (
    dot (tmpvar_4, -(vSkyLightDir.xyz))
  , 0.0, 1.0) * vSkyLightColor.xyz));
  diffuse_light_2.xyz = (diffuse_light_2.xyz + (clamp (
    dot (tmpvar_4, -(vSunDir.xyz))
  , 0.0, 1.0) * vSunColor.xyz));
  vec3 tmpvar_7;
  tmpvar_7 = (vCameraPos.xyz - (matWorld * tmpvar_1).xyz);
  gl_Position = (matWorldViewProj * tmpvar_1);
  Fog = (1.0/(exp2((
    sqrt(dot (tmpvar_5, tmpvar_5))
   * fFogDensity))));
  Color = ((vMaterialColor * inColor0.zyxw) * diffuse_light_2);
  Tex0 = inTexCoord;
  Map = sqrt(dot (tmpvar_7, tmpvar_7));
}

