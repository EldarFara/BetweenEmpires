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
uniform vec4 texture_offset;
attribute vec3 inPosition;
attribute vec3 inNormal;
attribute vec4 inColor0;
attribute vec4 inColor1;
attribute vec2 inTexCoord;
varying vec4 Color;
varying vec2 Tex0;
varying vec3 LightDir;
varying vec3 CameraDir;
varying vec4 PosWater;
varying float Fog;
void main ()
{
  vec4 tmpvar_1;
  tmpvar_1.w = 1.0;
  tmpvar_1.xyz = inPosition;
  vec4 diffuse_light_2;
  vec4 tmpvar_3;
  vec4 tmpvar_4;
  tmpvar_4.w = 0.0;
  tmpvar_4.xyz = inNormal;
  vec3 tmpvar_5;
  tmpvar_5 = normalize((matWorld * tmpvar_4).xyz);
  vec3 tmpvar_6;
  tmpvar_6 = (matWorldView * tmpvar_1).xyz;
  vec4 tmpvar_7;
  tmpvar_7 = (vAmbientColor + inColor1.zyxw);
  diffuse_light_2.w = tmpvar_7.w;
  diffuse_light_2.xyz = (tmpvar_7.xyz + (clamp (
    dot (tmpvar_5, -(vSkyLightDir.xyz))
  , 0.0, 1.0) * vSkyLightColor.xyz));
  vec3 tmpvar_8;
  tmpvar_8 = -(vSunDir.xyz);
  diffuse_light_2.xyz = (diffuse_light_2.xyz + (max (0.0001, 
    dot (tmpvar_5, tmpvar_8)
  ) * vSunColor.xyz));
  diffuse_light_2.w = 1.0;
  mat3 tmpvar_9;
  tmpvar_9[0] = vec3(1.0, 0.0, 0.0);
  tmpvar_9[1] = vec3(0.0, 1.0, 0.0);
  tmpvar_9[2] = vec3(0.0, 0.0, 1.0);
  gl_Position = (matWorldViewProj * tmpvar_1);
  Color = ((vMaterialColor * inColor0.zyxw) * diffuse_light_2);
  Tex0 = (inTexCoord + texture_offset.xy);
  LightDir = (tmpvar_9 * tmpvar_8);
  CameraDir = (tmpvar_9 * -(normalize(
    (vCameraPos.xyz - (matWorld * tmpvar_1).xyz)
  )));
  PosWater = tmpvar_3;
  Fog = (1.0/(exp2((
    sqrt(dot (tmpvar_6, tmpvar_6))
   * fFogDensity))));
}

