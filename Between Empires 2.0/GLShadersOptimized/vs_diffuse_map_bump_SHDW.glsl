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
uniform mat4 matSunViewProj;
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
  vec3 tmpvar_5;
  tmpvar_3 = (matWorldViewProj * tmpvar_1);
  vec4 tmpvar_6;
  tmpvar_6 = (matWorld * tmpvar_1);
  vec4 tmpvar_7;
  tmpvar_7.w = 0.0;
  tmpvar_7.xyz = inNormal;
  vec3 tmpvar_8;
  tmpvar_8 = normalize((matWorld * tmpvar_7).xyz);
  vec4 tmpvar_9;
  tmpvar_9.w = 0.0;
  tmpvar_9.xyz = inBinormal;
  vec3 tmpvar_10;
  tmpvar_10 = normalize((matWorld * tmpvar_9).xyz);
  vec4 tmpvar_11;
  tmpvar_11.w = 0.0;
  tmpvar_11.xyz = inTangent;
  vec3 tmpvar_12;
  tmpvar_12 = normalize((matWorld * tmpvar_11).xyz);
  vec3 tmpvar_13;
  tmpvar_13.x = tmpvar_12.x;
  tmpvar_13.y = tmpvar_10.x;
  tmpvar_13.z = tmpvar_8.x;
  vec3 tmpvar_14;
  tmpvar_14.x = tmpvar_12.y;
  tmpvar_14.y = tmpvar_10.y;
  tmpvar_14.z = tmpvar_8.y;
  vec3 tmpvar_15;
  tmpvar_15.x = tmpvar_12.z;
  tmpvar_15.y = tmpvar_10.z;
  tmpvar_15.z = tmpvar_8.z;
  mat3 tmpvar_16;
  tmpvar_16[0] = tmpvar_13;
  tmpvar_16[1] = tmpvar_14;
  tmpvar_16[2] = tmpvar_15;
  diffuse_light_2 = (vAmbientColor + inColor1.zyxw);
  diffuse_light_2.xyz = (diffuse_light_2.xyz + (clamp (
    dot (tmpvar_8, -(vSkyLightDir.xyz))
  , 0.0, 1.0) * vSkyLightColor.xyz));
  vec4 vWorldPos_17;
  vWorldPos_17 = tmpvar_6;
  vec3 vWorldN_18;
  vWorldN_18 = tmpvar_8;
  vec4 total_20;
  total_20 = vec4(0.0, 0.0, 0.0, 0.0);
  for (int j_19 = 0; j_19 < iLightPointCount; j_19++) {
    int tmpvar_21;
    tmpvar_21 = iLightIndices[j_19];
    vec3 tmpvar_22;
    tmpvar_22 = (vLightPosDir[tmpvar_21].xyz - vWorldPos_17.xyz);
    total_20 = (total_20 + ((
      clamp (dot (vWorldN_18, normalize(tmpvar_22)), 0.0, 1.0)
     * vLightDiffuse[tmpvar_21]) * (1.0/(
      dot (tmpvar_22, tmpvar_22)
    ))));
  };
  diffuse_light_2 = (diffuse_light_2 + total_20);
  tmpvar_4.xyz = ((vMaterialColor * inColor0.zyxw) * diffuse_light_2).xyz;
  tmpvar_4.w = (vMaterialColor.w * inColor0.w);
  vec3 tmpvar_23;
  tmpvar_23 = (matWorldView * tmpvar_1).xyz;
  gl_Position = tmpvar_3;
  Color = tmpvar_4;
  Tex0 = inTexCoord;
  ShadowTexCoord = (matSunViewProj * tmpvar_6);
  Fog = (1.0/(exp2((
    sqrt(dot (tmpvar_23, tmpvar_23))
   * fFogDensity))));
  SunLightDir = normalize((tmpvar_16 * -(vSunDir.xyz)));
  SkyLightDir = tmpvar_5;
  ViewDir = normalize((vCameraPos - tmpvar_6)).xyz;
  WorldNormal = tmpvar_8;
}

