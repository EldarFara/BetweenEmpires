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
  vec4 tmpvar_8;
  vec3 tmpvar_9;
  vec4 tmpvar_10;
  tmpvar_10 = (matWorld * tmpvar_1);
  vWorldPos_4 = tmpvar_10;
  vec4 tmpvar_11;
  tmpvar_11.w = 0.0;
  tmpvar_11.xyz = inNormal;
  vec3 tmpvar_12;
  tmpvar_12 = normalize((matWorld * tmpvar_11).xyz);
  if (bUseMotionBlur) {
    vec4 vWorldPos1_13;
    vec4 tmpvar_14;
    tmpvar_14 = (matMotionBlur * tmpvar_1);
    vWorldPos1_13 = tmpvar_14;
    vec3 tmpvar_15;
    tmpvar_15 = (tmpvar_14 - tmpvar_10).xyz;
    float tmpvar_16;
    tmpvar_16 = sqrt(dot (tmpvar_15, tmpvar_15));
    vec3 tmpvar_17;
    tmpvar_17 = (tmpvar_15 / tmpvar_16);
    if ((tmpvar_16 > 0.25)) {
      vWorldPos1_13.xyz = (tmpvar_10.xyz + (tmpvar_15 * 0.25));
    };
    float tmpvar_18;
    tmpvar_18 = dot (tmpvar_12, tmpvar_17);
    float tmpvar_19;
    if ((tmpvar_18 > 0.12)) {
      tmpvar_19 = 1.0;
    } else {
      tmpvar_19 = 0.0;
    };
    vec4 tmpvar_20;
    tmpvar_20 = mix (tmpvar_10, vWorldPos1_13, (tmpvar_19 * clamp (
      (inPosition.y + 0.15)
    , 0.0, 1.0)));
    vWorldPos_4 = tmpvar_20;
    vColor_2.w = ((clamp (
      (0.5 - inPosition.y)
    , 0.0, 1.0) + clamp (
      mix (1.1, -0.6999999, clamp ((dot (tmpvar_12, tmpvar_17) + 0.5), 0.0, 1.0))
    , 0.0, 1.0)) + 0.25);
    tmpvar_5 = (matViewProj * tmpvar_20);
  } else {
    tmpvar_5 = (matWorldViewProj * tmpvar_1);
  };
  tmpvar_6.xy = inTexCoord;
  vec4 tmpvar_21;
  tmpvar_21 = normalize((vCameraPos - vWorldPos_4));
  vec4 tmpvar_22;
  tmpvar_22.w = 1.0;
  tmpvar_22.xyz = vSunColor.xyz;
  vec4 tmpvar_23;
  tmpvar_23.w = 1.0;
  tmpvar_23.xyz = vSpecularColor.xyz;
  tmpvar_9 = (((
    (spec_coef * tmpvar_22)
   * tmpvar_23) * pow (
    clamp (dot (normalize((tmpvar_21.xyz - vSunDir.xyz)), tmpvar_12), 0.0, 1.0)
  , fMaterialPower)).xyz * inColor0.zyx);
  tmpvar_6.zw = ((tmpvar_21.xyz - tmpvar_12).yz + 1.0);
  diffuse_light_3.w = vAmbientColor.w;
  diffuse_light_3.xyz = (vAmbientColor.xyz + (clamp (
    dot (tmpvar_12, -(vSkyLightDir.xyz))
  , 0.0, 1.0) * vSkyLightColor.xyz));
  vec4 vWorldPos_24;
  vWorldPos_24 = vWorldPos_4;
  vec3 vWorldN_25;
  vWorldN_25 = tmpvar_12;
  vec4 total_27;
  total_27 = vec4(0.0, 0.0, 0.0, 0.0);
  for (int j_26 = 0; j_26 < iLightPointCount; j_26++) {
    int tmpvar_28;
    tmpvar_28 = iLightIndices[j_26];
    vec3 tmpvar_29;
    tmpvar_29 = (vLightPosDir[tmpvar_28].xyz - vWorldPos_24.xyz);
    total_27 = (total_27 + ((
      clamp (dot (vWorldN_25, normalize(tmpvar_29)), 0.0, 1.0)
     * vLightDiffuse[tmpvar_28]) * (1.0/(
      dot (tmpvar_29, tmpvar_29)
    ))));
  };
  diffuse_light_3 = (diffuse_light_3 + total_27);
  vec4 tmpvar_30;
  tmpvar_30.w = 1.0;
  tmpvar_30.xyz = vSunColor.xyz;
  tmpvar_7.xyz = (((
    max (-0.0001, dot (tmpvar_12, -(vSunDir.xyz)))
   * tmpvar_30) * vMaterialColor) * vColor_2.zyxw).xyz;
  tmpvar_7.w = vColor_2.w;
  vec3 tmpvar_31;
  tmpvar_31 = (matWorldView * tmpvar_1).xyz;
  gl_Position = tmpvar_5;
  Fog = (1.0/(exp2((
    sqrt(dot (tmpvar_31, tmpvar_31))
   * fFogDensity))));
  Color = ((vMaterialColor * vColor_2.zyxw) * diffuse_light_3);
  Tex0 = tmpvar_6;
  SunLight = tmpvar_7;
  ShadowTexCoord = tmpvar_8;
  vSpecular = tmpvar_9;
}

