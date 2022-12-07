uniform vec4 vLightDiffuse[4];
uniform vec4 vMaterialColor;
uniform vec4 vSunDir;
uniform vec4 vSunColor;
uniform vec4 vAmbientColor;
uniform vec4 vSkyLightDir;
uniform vec4 vSkyLightColor;
uniform float fFogDensity;
uniform int iLightPointCount;
uniform int iLightIndices[4];
uniform mat4 matWorldViewProj;
uniform mat4 matWorldView;
uniform mat4 matWorld;
uniform mat4 matSunViewProj;
uniform vec4 vLightPosDir[4];
uniform vec4 vCameraPos;
uniform float flora_detail;
attribute vec3 inPosition;
attribute vec3 inNormal;
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
  vec4 diffuse_light_2;
  vec4 tmpvar_3;
  vec4 tmpvar_4;
  vec4 tmpvar_5;
  tmpvar_5 = (matWorld * tmpvar_1);
  vec3 tmpvar_6;
  tmpvar_6 = (vCameraPos.xyz - tmpvar_5.xyz);
  float tmpvar_7;
  float tmpvar_8;
  tmpvar_8 = (flora_detail * 0.75);
  tmpvar_7 = clamp ((0.5 + (
    (sqrt(dot (tmpvar_6, tmpvar_6)) - tmpvar_8)
   / 
    (flora_detail - tmpvar_8)
  )), 0.0, 1.0);
  tmpvar_3 = (matWorldViewProj * tmpvar_1);
  vec4 tmpvar_9;
  tmpvar_9.w = 0.0;
  tmpvar_9.xyz = inNormal;
  vec3 tmpvar_10;
  tmpvar_10 = normalize((matWorld * tmpvar_9).xyz);
  diffuse_light_2.w = vAmbientColor.w;
  diffuse_light_2.xyz = (vAmbientColor.xyz + (clamp (
    dot (tmpvar_10, -(vSkyLightDir.xyz))
  , 0.0, 1.0) * vSkyLightColor.xyz));
  vec4 vWorldPos_11;
  vWorldPos_11 = tmpvar_5;
  vec3 vWorldN_12;
  vWorldN_12 = tmpvar_10;
  vec4 total_14;
  total_14 = vec4(0.0, 0.0, 0.0, 0.0);
  for (int j_13 = 0; j_13 < iLightPointCount; j_13++) {
    int tmpvar_15;
    tmpvar_15 = iLightIndices[j_13];
    vec3 tmpvar_16;
    tmpvar_16 = (vLightPosDir[tmpvar_15].xyz - vWorldPos_11.xyz);
    total_14 = (total_14 + ((
      clamp (dot (vWorldN_12, normalize(tmpvar_16)), 0.0, 1.0)
     * vLightDiffuse[tmpvar_15]) * (1.0/(
      dot (tmpvar_16, tmpvar_16)
    ))));
  };
  diffuse_light_2 = (diffuse_light_2 + total_14);
  tmpvar_4 = ((vMaterialColor * inColor0.zyxw) * diffuse_light_2);
  tmpvar_4.w = (tmpvar_4.w * tmpvar_7);
  vec4 tmpvar_17;
  tmpvar_17.w = 1.0;
  tmpvar_17.xyz = vSunColor.xyz;
  vec3 tmpvar_18;
  tmpvar_18 = (matWorldView * tmpvar_1).xyz;
  gl_Position = tmpvar_3;
  Fog = (1.0/(exp2((
    sqrt(dot (tmpvar_18, tmpvar_18))
   * fFogDensity))));
  Color = tmpvar_4;
  Tex0 = inTexCoord;
  SunLight = (((
    clamp (dot (tmpvar_10, -(vSunDir.xyz)), 0.0, 1.0)
   * tmpvar_17) * vMaterialColor) * inColor0.zyxw);
  ShadowTexCoord = (matSunViewProj * tmpvar_5);
}

