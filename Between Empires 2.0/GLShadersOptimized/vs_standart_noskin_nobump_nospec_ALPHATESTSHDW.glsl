uniform vec4 vLightDiffuse[4];
uniform vec4 vMaterialColor;
uniform float fMaterialPower;
uniform float fFogDensity;
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
varying vec4 VertexColor;
varying vec3 VertexLighting;
varying vec2 Tex0;
varying vec3 SunLightDir;
varying vec3 SkyLightDir;
varying vec4 PointLightDir;
varying vec4 ShadowTexCoord;
varying vec3 ViewDir;
void main ()
{
  vec4 tmpvar_1;
  tmpvar_1.w = 1.0;
  tmpvar_1.xyz = inPosition;
  vec4 vVertexColor_2;
  vVertexColor_2 = inColor0;
  vec4 vWorldPos_3;
  vec4 tmpvar_4;
  vec4 tmpvar_5;
  vec3 tmpvar_6;
  vec4 tmpvar_7;
  vec4 tmpvar_8;
  tmpvar_8 = (matWorld * tmpvar_1);
  vWorldPos_3 = tmpvar_8;
  vec4 tmpvar_9;
  tmpvar_9.w = 0.0;
  tmpvar_9.xyz = inNormal;
  vec3 tmpvar_10;
  tmpvar_10 = normalize((matWorld * tmpvar_9).xyz);
  if (bUseMotionBlur) {
    vec4 tmpvar_11;
    tmpvar_11 = (matMotionBlur * tmpvar_1);
    vec4 tmpvar_12;
    tmpvar_12 = normalize((tmpvar_11 - tmpvar_8));
    float tmpvar_13;
    tmpvar_13 = dot (tmpvar_10, tmpvar_12.xyz);
    float tmpvar_14;
    if ((tmpvar_13 > 0.1)) {
      tmpvar_14 = 1.0;
    } else {
      tmpvar_14 = 0.0;
    };
    vWorldPos_3 = mix (tmpvar_8, tmpvar_11, (tmpvar_14 * clamp (
      (inPosition.y + 0.15)
    , 0.0, 1.0)));
    vVertexColor_2.w = ((clamp (
      (0.5 - inPosition.y)
    , 0.0, 1.0) + clamp (
      mix (1.1, -0.6999999, clamp ((dot (tmpvar_10, tmpvar_12.xyz) + 0.5), 0.0, 1.0))
    , 0.0, 1.0)) + 0.25);
  };
  if (bUseMotionBlur) {
    tmpvar_4 = (matViewProj * vWorldPos_3);
  } else {
    tmpvar_4 = (matWorldViewProj * tmpvar_1);
  };
  tmpvar_5 = vVertexColor_2.zyxw;
  vec4 vWorldPos_15;
  vWorldPos_15 = vWorldPos_3;
  vec3 vWorldN_16;
  vWorldN_16 = tmpvar_10;
  vec4 total_18;
  total_18 = vec4(0.0, 0.0, 0.0, 0.0);
  for (int j_17 = 0; j_17 < iLightPointCount; j_17++) {
    int tmpvar_19;
    tmpvar_19 = iLightIndices[j_17];
    vec3 tmpvar_20;
    tmpvar_20 = (vLightPosDir[tmpvar_19].xyz - vWorldPos_15.xyz);
    total_18 = (total_18 + ((
      clamp (dot (vWorldN_16, normalize(tmpvar_20)), 0.0, 1.0)
     * vLightDiffuse[tmpvar_19]) * (1.0/(
      dot (tmpvar_20, tmpvar_20)
    ))));
  };
  tmpvar_6 = total_18.xyz;
  vec3 tmpvar_21;
  tmpvar_21 = normalize((vCameraPos.xyz - vWorldPos_3.xyz));
  vec3 vWorldPos_22;
  vWorldPos_22 = vWorldPos_3.xyz;
  vec3 vWorldN_23;
  vWorldN_23 = tmpvar_10;
  vec3 vWorldView_24;
  vWorldView_24 = tmpvar_21;
  vec4 total_26;
  total_26 = vec4(0.0, 0.0, 0.0, 0.0);
  for (int i_25 = 0; i_25 < iLightPointCount; i_25++) {
    vec3 tmpvar_27;
    tmpvar_27 = (vLightPosDir[i_25].xyz - vWorldPos_22);
    total_26 = (total_26 + ((
      (1.0/(dot (tmpvar_27, tmpvar_27)))
     * vLightDiffuse[i_25]) * pow (
      clamp (dot (normalize((vWorldView_24 + 
        normalize(tmpvar_27)
      )), vWorldN_23), 0.0, 1.0)
    , fMaterialPower)));
  };
  tmpvar_5.w = (vVertexColor_2.w * vMaterialColor.w);
  vec3 tmpvar_28;
  tmpvar_28 = (matWorldView * tmpvar_1).xyz;
  gl_Position = tmpvar_4;
  Fog = (1.0/(exp2((
    sqrt(dot (tmpvar_28, tmpvar_28))
   * fFogDensity))));
  VertexColor = tmpvar_5;
  VertexLighting = tmpvar_6;
  Tex0 = inTexCoord;
  SunLightDir = tmpvar_10;
  SkyLightDir = total_26.xyz;
  PointLightDir = tmpvar_7;
  ShadowTexCoord = (matSunViewProj * vWorldPos_3);
  ViewDir = tmpvar_21;
}

