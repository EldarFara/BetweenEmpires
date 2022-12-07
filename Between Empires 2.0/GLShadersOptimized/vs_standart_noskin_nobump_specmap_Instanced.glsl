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
  vec4 tmpvar_9;
  tmpvar_9 = (matWorld * tmpvar_1);
  vWorldPos_3 = tmpvar_9;
  vec4 tmpvar_10;
  tmpvar_10.w = 0.0;
  tmpvar_10.xyz = inNormal;
  vec3 tmpvar_11;
  tmpvar_11 = normalize((matWorld * tmpvar_10).xyz);
  if (bUseMotionBlur) {
    vec4 tmpvar_12;
    tmpvar_12 = (matMotionBlur * tmpvar_1);
    vec4 tmpvar_13;
    tmpvar_13 = normalize((tmpvar_12 - tmpvar_9));
    float tmpvar_14;
    tmpvar_14 = dot (tmpvar_11, tmpvar_13.xyz);
    float tmpvar_15;
    if ((tmpvar_14 > 0.1)) {
      tmpvar_15 = 1.0;
    } else {
      tmpvar_15 = 0.0;
    };
    vWorldPos_3 = mix (tmpvar_9, tmpvar_12, (tmpvar_15 * clamp (
      (inPosition.y + 0.15)
    , 0.0, 1.0)));
    vVertexColor_2.w = ((clamp (
      (0.5 - inPosition.y)
    , 0.0, 1.0) + clamp (
      mix (1.1, -0.6999999, clamp ((dot (tmpvar_11, tmpvar_13.xyz) + 0.5), 0.0, 1.0))
    , 0.0, 1.0)) + 0.25);
  };
  if (bUseMotionBlur) {
    tmpvar_4 = (matViewProj * vWorldPos_3);
  } else {
    tmpvar_4 = (matWorldViewProj * tmpvar_1);
  };
  tmpvar_5 = vVertexColor_2.zyxw;
  vec4 vWorldPos_16;
  vWorldPos_16 = vWorldPos_3;
  vec3 vWorldN_17;
  vWorldN_17 = tmpvar_11;
  vec4 total_19;
  total_19 = vec4(0.0, 0.0, 0.0, 0.0);
  for (int j_18 = 0; j_18 < iLightPointCount; j_18++) {
    int tmpvar_20;
    tmpvar_20 = iLightIndices[j_18];
    vec3 tmpvar_21;
    tmpvar_21 = (vLightPosDir[tmpvar_20].xyz - vWorldPos_16.xyz);
    total_19 = (total_19 + ((
      clamp (dot (vWorldN_17, normalize(tmpvar_21)), 0.0, 1.0)
     * vLightDiffuse[tmpvar_20]) * (1.0/(
      dot (tmpvar_21, tmpvar_21)
    ))));
  };
  tmpvar_6 = total_19.xyz;
  vec3 tmpvar_22;
  tmpvar_22 = normalize((vCameraPos.xyz - vWorldPos_3.xyz));
  vec3 vWorldPos_23;
  vWorldPos_23 = vWorldPos_3.xyz;
  vec3 vWorldN_24;
  vWorldN_24 = tmpvar_11;
  vec3 vWorldView_25;
  vWorldView_25 = tmpvar_22;
  vec4 total_27;
  total_27 = vec4(0.0, 0.0, 0.0, 0.0);
  for (int i_26 = 0; i_26 < iLightPointCount; i_26++) {
    vec3 tmpvar_28;
    tmpvar_28 = (vLightPosDir[i_26].xyz - vWorldPos_23);
    total_27 = (total_27 + ((
      (1.0/(dot (tmpvar_28, tmpvar_28)))
     * vLightDiffuse[i_26]) * pow (
      clamp (dot (normalize((vWorldView_25 + 
        normalize(tmpvar_28)
      )), vWorldN_24), 0.0, 1.0)
    , fMaterialPower)));
  };
  tmpvar_5.w = (vVertexColor_2.w * vMaterialColor.w);
  vec3 tmpvar_29;
  tmpvar_29 = (matWorldView * tmpvar_1).xyz;
  gl_Position = tmpvar_4;
  Fog = (1.0/(exp2((
    sqrt(dot (tmpvar_29, tmpvar_29))
   * fFogDensity))));
  VertexColor = tmpvar_5;
  VertexLighting = tmpvar_6;
  Tex0 = inTexCoord;
  SunLightDir = tmpvar_11;
  SkyLightDir = total_27.xyz;
  PointLightDir = tmpvar_7;
  ShadowTexCoord = tmpvar_8;
  ViewDir = tmpvar_22;
}

