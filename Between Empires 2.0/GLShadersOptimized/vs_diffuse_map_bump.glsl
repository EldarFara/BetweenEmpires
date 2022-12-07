uniform vec4 vLightDiffuse[4];
uniform vec4 vMaterialColor;
uniform vec4 vSunDir;
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
attribute vec3 inPosition;
attribute vec3 inNormal;
attribute vec3 inTangent;
attribute vec3 inBinormal;
attribute vec4 inColor0;
attribute vec4 inColor1;
attribute vec2 inTexCoord;
varying vec4 Color;
varying vec2 Tex0;
varying vec4 ShadowTexCoord;
varying float Fog;
varying vec3 SunLightDir;
varying vec3 SkyLightDir;
varying vec3 ViewDir;
varying vec3 WorldNormal;
void main ()
{
  vec4 tmpvar_1;
  tmpvar_1.w = 1.0;
  tmpvar_1.xyz = inPosition;
  vec4 diffuse_light_2;
  vec4 tmpvar_3;
  vec4 tmpvar_4;
  vec4 tmpvar_5;
  vec3 tmpvar_6;
  tmpvar_3 = (matWorldViewProj * tmpvar_1);
  vec4 tmpvar_7;
  tmpvar_7 = (matWorld * tmpvar_1);
  vec4 tmpvar_8;
  tmpvar_8.w = 0.0;
  tmpvar_8.xyz = inNormal;
  vec3 tmpvar_9;
  tmpvar_9 = normalize((matWorld * tmpvar_8).xyz);
  vec4 tmpvar_10;
  tmpvar_10.w = 0.0;
  tmpvar_10.xyz = inBinormal;
  vec3 tmpvar_11;
  tmpvar_11 = normalize((matWorld * tmpvar_10).xyz);
  vec4 tmpvar_12;
  tmpvar_12.w = 0.0;
  tmpvar_12.xyz = inTangent;
  vec3 tmpvar_13;
  tmpvar_13 = normalize((matWorld * tmpvar_12).xyz);
  vec3 tmpvar_14;
  tmpvar_14.x = tmpvar_13.x;
  tmpvar_14.y = tmpvar_11.x;
  tmpvar_14.z = tmpvar_9.x;
  vec3 tmpvar_15;
  tmpvar_15.x = tmpvar_13.y;
  tmpvar_15.y = tmpvar_11.y;
  tmpvar_15.z = tmpvar_9.y;
  vec3 tmpvar_16;
  tmpvar_16.x = tmpvar_13.z;
  tmpvar_16.y = tmpvar_11.z;
  tmpvar_16.z = tmpvar_9.z;
  mat3 tmpvar_17;
  tmpvar_17[0] = tmpvar_14;
  tmpvar_17[1] = tmpvar_15;
  tmpvar_17[2] = tmpvar_16;
  diffuse_light_2 = (vAmbientColor + inColor1.zyxw);
  diffuse_light_2.xyz = (diffuse_light_2.xyz + (clamp (
    dot (tmpvar_9, -(vSkyLightDir.xyz))
  , 0.0, 1.0) * vSkyLightColor.xyz));
  vec4 vWorldPos_18;
  vWorldPos_18 = tmpvar_7;
  vec3 vWorldN_19;
  vWorldN_19 = tmpvar_9;
  vec4 total_21;
  total_21 = vec4(0.0, 0.0, 0.0, 0.0);
  for (int j_20 = 0; j_20 < iLightPointCount; j_20++) {
    int tmpvar_22;
    tmpvar_22 = iLightIndices[j_20];
    vec3 tmpvar_23;
    tmpvar_23 = (vLightPosDir[tmpvar_22].xyz - vWorldPos_18.xyz);
    total_21 = (total_21 + ((
      clamp (dot (vWorldN_19, normalize(tmpvar_23)), 0.0, 1.0)
     * vLightDiffuse[tmpvar_22]) * (1.0/(
      dot (tmpvar_23, tmpvar_23)
    ))));
  };
  diffuse_light_2 = (diffuse_light_2 + total_21);
  tmpvar_4.xyz = ((vMaterialColor * inColor0.zyxw) * diffuse_light_2).xyz;
  tmpvar_4.w = (vMaterialColor.w * inColor0.w);
  vec3 tmpvar_24;
  tmpvar_24 = (matWorldView * tmpvar_1).xyz;
  gl_Position = tmpvar_3;
  Color = tmpvar_4;
  Tex0 = inTexCoord;
  ShadowTexCoord = tmpvar_5;
  Fog = (1.0/(exp2((
    sqrt(dot (tmpvar_24, tmpvar_24))
   * fFogDensity))));
  SunLightDir = normalize((tmpvar_17 * -(vSunDir.xyz)));
  SkyLightDir = tmpvar_6;
  ViewDir = normalize((vCameraPos - tmpvar_7)).xyz;
  WorldNormal = tmpvar_9;
}

