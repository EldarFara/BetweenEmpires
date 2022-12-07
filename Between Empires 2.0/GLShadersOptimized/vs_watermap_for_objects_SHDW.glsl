uniform vec4 vLightDiffuse[4];
uniform vec4 vMaterialColor;
uniform vec4 vSpecularColor;
uniform vec4 vSunDir;
uniform vec4 vSunColor;
uniform vec4 vAmbientColor;
uniform vec4 vSkyLightDir;
uniform vec4 vSkyLightColor;
uniform float fMaterialPower;
uniform float fFogDensity;
uniform float spec_coef;
uniform int iLightPointCount;
uniform int iLightIndices[4];
uniform bool bUseMotionBlur;
uniform mat4 matWorldViewProj;
uniform mat4 matWorldView;
uniform mat4 matWorld;
uniform mat4 matMotionBlur;
uniform mat4 matSunViewProj;
uniform mat4 matViewProj;
uniform vec4 vLightPosDir[4];
uniform vec4 vCameraPos;
attribute vec3 inPosition;
attribute vec3 inNormal;
attribute vec4 inColor0;
attribute vec2 inTexCoord;
varying float Fog;
varying vec4 Color;
varying vec4 Tex0;
varying vec4 SunLight;
varying vec4 ShadowTexCoord;
varying vec3 vSpecular;
void main ()
{
  vec4 tmpvar_1;
  tmpvar_1.w = 1.0;
  tmpvar_1.xyz = inPosition;
  vec4 vColor_2;
  vColor_2 = inColor0;
  vec4 diffuse_light_3;
  vec4 vWorldPos_4;
  vec4 tmpvar_5;
  vec4 tmpvar_6;
  vec4 tmpvar_7;
  vec3 tmpvar_8;
  vec4 tmpvar_9;
  tmpvar_9 = (matWorld * tmpvar_1);
  vWorldPos_4 = tmpvar_9;
  vec4 tmpvar_10;
  tmpvar_10.w = 0.0;
  tmpvar_10.xyz = inNormal;
  vec3 tmpvar_11;
  tmpvar_11 = normalize((matWorld * tmpvar_10).xyz);
  if (bUseMotionBlur) {
    vec4 vWorldPos1_12;
    vec4 tmpvar_13;
    tmpvar_13 = (matMotionBlur * tmpvar_1);
    vWorldPos1_12 = tmpvar_13;
    vec3 tmpvar_14;
    tmpvar_14 = (tmpvar_13 - tmpvar_9).xyz;
    float tmpvar_15;
    tmpvar_15 = sqrt(dot (tmpvar_14, tmpvar_14));
    vec3 tmpvar_16;
    tmpvar_16 = (tmpvar_14 / tmpvar_15);
    if ((tmpvar_15 > 0.25)) {
      vWorldPos1_12.xyz = (tmpvar_9.xyz + (tmpvar_14 * 0.25));
    };
    float tmpvar_17;
    tmpvar_17 = dot (tmpvar_11, tmpvar_16);
    float tmpvar_18;
    if ((tmpvar_17 > 0.12)) {
      tmpvar_18 = 1.0;
    } else {
      tmpvar_18 = 0.0;
    };
    vec4 tmpvar_19;
    tmpvar_19 = mix (tmpvar_9, vWorldPos1_12, (tmpvar_18 * clamp (
      (inPosition.y + 0.15)
    , 0.0, 1.0)));
    vWorldPos_4 = tmpvar_19;
    vColor_2.w = ((clamp (
      (0.5 - inPosition.y)
    , 0.0, 1.0) + clamp (
      mix (1.1, -0.6999999, clamp ((dot (tmpvar_11, tmpvar_16) + 0.5), 0.0, 1.0))
    , 0.0, 1.0)) + 0.25);
    tmpvar_5 = (matViewProj * tmpvar_19);
  } else {
    tmpvar_5 = (matWorldViewProj * tmpvar_1);
  };
  tmpvar_6.xy = inTexCoord;
  vec4 tmpvar_20;
  tmpvar_20 = normalize((vCameraPos - vWorldPos_4));
  vec4 tmpvar_21;
  tmpvar_21.w = 1.0;
  tmpvar_21.xyz = vSunColor.xyz;
  vec4 tmpvar_22;
  tmpvar_22.w = 1.0;
  tmpvar_22.xyz = vSpecularColor.xyz;
  tmpvar_8 = (((
    (spec_coef * tmpvar_21)
   * tmpvar_22) * pow (
    clamp (dot (normalize((tmpvar_20.xyz - vSunDir.xyz)), tmpvar_11), 0.0, 1.0)
  , fMaterialPower)).xyz * inColor0.zyx);
  tmpvar_6.zw = ((tmpvar_20.xyz - tmpvar_11).yz + 1.0);
  diffuse_light_3.w = vAmbientColor.w;
  diffuse_light_3.xyz = (vAmbientColor.xyz + (clamp (
    dot (tmpvar_11, -(vSkyLightDir.xyz))
  , 0.0, 1.0) * vSkyLightColor.xyz));
  vec4 vWorldPos_23;
  vWorldPos_23 = vWorldPos_4;
  vec3 vWorldN_24;
  vWorldN_24 = tmpvar_11;
  vec4 total_26;
  total_26 = vec4(0.0, 0.0, 0.0, 0.0);
  for (int j_25 = 0; j_25 < iLightPointCount; j_25++) {
    int tmpvar_27;
    tmpvar_27 = iLightIndices[j_25];
    vec3 tmpvar_28;
    tmpvar_28 = (vLightPosDir[tmpvar_27].xyz - vWorldPos_23.xyz);
    total_26 = (total_26 + ((
      clamp (dot (vWorldN_24, normalize(tmpvar_28)), 0.0, 1.0)
     * vLightDiffuse[tmpvar_27]) * (1.0/(
      dot (tmpvar_28, tmpvar_28)
    ))));
  };
  diffuse_light_3 = (diffuse_light_3 + total_26);
  vec4 tmpvar_29;
  tmpvar_29.w = 1.0;
  tmpvar_29.xyz = vSunColor.xyz;
  tmpvar_7.xyz = (((
    max (-0.0001, dot (tmpvar_11, -(vSunDir.xyz)))
   * tmpvar_29) * vMaterialColor) * vColor_2.zyxw).xyz;
  tmpvar_7.w = vColor_2.w;
  vec3 tmpvar_30;
  tmpvar_30 = (matWorldView * tmpvar_1).xyz;
  gl_Position = tmpvar_5;
  Fog = (1.0/(exp2((
    sqrt(dot (tmpvar_30, tmpvar_30))
   * fFogDensity))));
  Color = ((vMaterialColor * vColor_2.zyxw) * diffuse_light_3);
  Tex0 = tmpvar_6;
  SunLight = tmpvar_7;
  ShadowTexCoord = (matSunViewProj * vWorldPos_4);
  vSpecular = tmpvar_8;
}

