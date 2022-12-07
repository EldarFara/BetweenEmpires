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
attribute vec3 inPosition;
attribute vec3 inNormal;
attribute vec4 inColor0;
attribute vec4 inColor1;
attribute vec2 inTexCoord;
varying vec4 outColor0;
varying vec2 outTexCoord;
varying float outFog;
void main ()
{
  vec4 diffuse_light_1;
  vec4 tmpvar_2;
  tmpvar_2.w = 1.0;
  tmpvar_2.xyz = inPosition;
  gl_Position = (matWorldViewProj * tmpvar_2);
  vec4 tmpvar_3;
  tmpvar_3.w = 0.0;
  tmpvar_3.xyz = inNormal;
  vec3 tmpvar_4;
  tmpvar_4 = (matWorld * tmpvar_3).xyz;
  vec4 tmpvar_5;
  tmpvar_5.w = 1.0;
  tmpvar_5.xyz = inPosition;
  vec3 tmpvar_6;
  tmpvar_6 = (matWorldView * tmpvar_5).xyz;
  outTexCoord = inTexCoord;
  diffuse_light_1 = ((vAmbientColor + inColor1) + (clamp (
    dot (tmpvar_4, -(vSkyLightDir.xyz))
  , 0.0, 1.0) * vSkyLightColor));
  diffuse_light_1 = (diffuse_light_1 + (clamp (
    dot (tmpvar_4, -(vSunDir.xyz))
  , 0.0, 1.0) * vSunColor));
  outColor0 = clamp (((vMaterialColor * inColor0) * diffuse_light_1), 0.0, 1.0);
  outFog = (1.0/(exp2((
    sqrt(dot (tmpvar_6, tmpvar_6))
   * fFogDensity))));
}

