uniform vec4 vLightDiffuse[4];
uniform vec4 vMaterialColor;
uniform float fMaterialPower;
uniform float fFogDensity;
uniform int iLightPointCount;
uniform int iLightIndices[4];
uniform mat4 matWorldViewProj;
uniform mat4 matWorldView;
uniform mat4 matWorld;
uniform mat4 matWorldArray[32];
uniform mat4 matSunViewProj;
uniform vec4 vLightPosDir[4];
uniform vec4 vCameraPos;
attribute vec3 inPosition;
attribute vec3 inNormal;
attribute vec4 inColor0;
attribute vec2 inTexCoord;
attribute vec4 inBlendWeight;
attribute vec4 inBlendIndices;
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
  vec4 vObjectPos_2;
  vec4 tmpvar_3;
  vec4 tmpvar_4;
  vec3 tmpvar_5;
  vec4 tmpvar_6;
  vObjectPos_2 = (((
    ((matWorldArray[int(inBlendIndices.x)] * tmpvar_1) * inBlendWeight.x)
   + 
    ((matWorldArray[int(inBlendIndices.y)] * tmpvar_1) * inBlendWeight.y)
  ) + (
    (matWorldArray[int(inBlendIndices.z)] * tmpvar_1)
   * inBlendWeight.z)) + ((matWorldArray[
    int(inBlendIndices.w)
  ] * tmpvar_1) * inBlendWeight.w));
  vec4 tmpvar_7;
  tmpvar_7 = (matWorld * vObjectPos_2);
  vec4 tmpvar_8;
  tmpvar_8.w = 0.0;
  tmpvar_8.xyz = inNormal;
  vec3 tmpvar_9;
  tmpvar_9 = normalize((matWorld * tmpvar_8).xyz);
  tmpvar_3 = (matWorldViewProj * vObjectPos_2);
  tmpvar_4 = inColor0.zyxw;
  vec4 vWorldPos_10;
  vWorldPos_10 = tmpvar_7;
  vec3 vWorldN_11;
  vWorldN_11 = tmpvar_9;
  vec4 total_13;
  total_13 = vec4(0.0, 0.0, 0.0, 0.0);
  for (int j_12 = 0; j_12 < iLightPointCount; j_12++) {
    int tmpvar_14;
    tmpvar_14 = iLightIndices[j_12];
    vec3 tmpvar_15;
    tmpvar_15 = (vLightPosDir[tmpvar_14].xyz - vWorldPos_10.xyz);
    total_13 = (total_13 + ((
      clamp (dot (vWorldN_11, normalize(tmpvar_15)), 0.0, 1.0)
     * vLightDiffuse[tmpvar_14]) * (1.0/(
      dot (tmpvar_15, tmpvar_15)
    ))));
  };
  tmpvar_5 = total_13.xyz;
  vec3 tmpvar_16;
  tmpvar_16 = normalize((vCameraPos.xyz - tmpvar_7.xyz));
  vec3 vWorldPos_17;
  vWorldPos_17 = tmpvar_7.xyz;
  vec3 vWorldN_18;
  vWorldN_18 = tmpvar_9;
  vec3 vWorldView_19;
  vWorldView_19 = tmpvar_16;
  vec4 total_21;
  total_21 = vec4(0.0, 0.0, 0.0, 0.0);
  for (int i_20 = 0; i_20 < iLightPointCount; i_20++) {
    vec3 tmpvar_22;
    tmpvar_22 = (vLightPosDir[i_20].xyz - vWorldPos_17);
    total_21 = (total_21 + ((
      (1.0/(dot (tmpvar_22, tmpvar_22)))
     * vLightDiffuse[i_20]) * pow (
      clamp (dot (normalize((vWorldView_19 + 
        normalize(tmpvar_22)
      )), vWorldN_18), 0.0, 1.0)
    , fMaterialPower)));
  };
  tmpvar_4.w = (inColor0.w * vMaterialColor.w);
  vec3 tmpvar_23;
  tmpvar_23 = (matWorldView * vObjectPos_2).xyz;
  gl_Position = tmpvar_3;
  Fog = (1.0/(exp2((
    sqrt(dot (tmpvar_23, tmpvar_23))
   * fFogDensity))));
  VertexColor = tmpvar_4;
  VertexLighting = tmpvar_5;
  Tex0 = inTexCoord;
  SunLightDir = tmpvar_9;
  SkyLightDir = total_21.xyz;
  PointLightDir = tmpvar_6;
  ShadowTexCoord = (matSunViewProj * tmpvar_7);
  ViewDir = tmpvar_16;
}

