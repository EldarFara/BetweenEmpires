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
  vec4 tmpvar_6;
  tmpvar_6 = (matWorld * tmpvar_1);
  vec3 tmpvar_7;
  tmpvar_7 = (vCameraPos.xyz - tmpvar_6.xyz);
  float tmpvar_8;
  float tmpvar_9;
  tmpvar_9 = (flora_detail * 0.75);
  tmpvar_8 = clamp ((0.5 + (
    (sqrt(dot (tmpvar_7, tmpvar_7)) - tmpvar_9)
   / 
    (flora_detail - tmpvar_9)
  )), 0.0, 1.0);
  tmpvar_3 = (matWorldViewProj * tmpvar_1);
  vec4 tmpvar_10;
  tmpvar_10.w = 0.0;
  tmpvar_10.xyz = inNormal;
  vec3 tmpvar_11;
  tmpvar_11 = normalize((matWorld * tmpvar_10).xyz);
  diffuse_light_2.w = vAmbientColor.w;
  diffuse_light_2.xyz = (vAmbientColor.xyz + (clamp (
    dot (tmpvar_11, -(vSkyLightDir.xyz))
  , 0.0, 1.0) * vSkyLightColor.xyz));
  vec4 vWorldPos_12;
  vWorldPos_12 = tmpvar_6;
  vec3 vWorldN_13;
  vWorldN_13 = tmpvar_11;
  vec4 total_15;
  total_15 = vec4(0.0, 0.0, 0.0, 0.0);
  for (int j_14 = 0; j_14 < iLightPointCount; j_14++) {
    int tmpvar_16;
    tmpvar_16 = iLightIndices[j_14];
    vec3 tmpvar_17;
    tmpvar_17 = (vLightPosDir[tmpvar_16].xyz - vWorldPos_12.xyz);
    total_15 = (total_15 + ((
      clamp (dot (vWorldN_13, normalize(tmpvar_17)), 0.0, 1.0)
     * vLightDiffuse[tmpvar_16]) * (1.0/(
      dot (tmpvar_17, tmpvar_17)
    ))));
  };
  diffuse_light_2 = (diffuse_light_2 + total_15);
  tmpvar_4 = ((vMaterialColor * inColor0.zyxw) * diffuse_light_2);
  tmpvar_4.w = (tmpvar_4.w * tmpvar_8);
  vec4 tmpvar_18;
  tmpvar_18.w = 1.0;
  tmpvar_18.xyz = vSunColor.xyz;
  vec3 tmpvar_19;
  tmpvar_19 = (matWorldView * tmpvar_1).xyz;
  gl_Position = tmpvar_3;
  Fog = (1.0/(exp2((
    sqrt(dot (tmpvar_19, tmpvar_19))
   * fFogDensity))));
  Color = tmpvar_4;
  Tex0 = inTexCoord;
  SunLight = (((
    clamp (dot (tmpvar_11, -(vSunDir.xyz)), 0.0, 1.0)
   * tmpvar_18) * vMaterialColor) * inColor0.zyxw);
  ShadowTexCoord = tmpvar_5;
}

