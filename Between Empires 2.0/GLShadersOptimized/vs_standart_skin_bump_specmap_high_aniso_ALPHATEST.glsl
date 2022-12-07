uniform vec4 vLightDiffuse[4];
uniform vec4 vMaterialColor;
uniform vec4 vSunDir;
uniform float fMaterialPower;
uniform float fFogDensity;
uniform int iLightPointCount;
uniform int iLightIndices[4];
uniform mat4 matWorldViewProj;
uniform mat4 matWorldView;
uniform mat4 matWorld;
uniform mat4 matWorldArray[32];
uniform vec4 vLightPosDir[4];
uniform vec4 vCameraPos;
attribute vec3 inPosition;
attribute vec3 inNormal;
attribute vec4 inColor0;
attribute vec2 inTexCoord;
attribute vec3 inTangent;
attribute vec3 inBinormal;
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
  vec3 vObjectB_2;
  vec4 vObjectPos_3;
  vec4 tmpvar_4;
  vec4 tmpvar_5;
  vec3 tmpvar_6;
  vec3 tmpvar_7;
  vec3 tmpvar_8;
  vec4 tmpvar_9;
  vec3 tmpvar_10;
  int tmpvar_11;
  tmpvar_11 = int(inBlendIndices.x);
  int tmpvar_12;
  tmpvar_12 = int(inBlendIndices.y);
  int tmpvar_13;
  tmpvar_13 = int(inBlendIndices.z);
  int tmpvar_14;
  tmpvar_14 = int(inBlendIndices.w);
  vObjectPos_3 = (((
    ((matWorldArray[tmpvar_11] * tmpvar_1) * inBlendWeight.x)
   + 
    ((matWorldArray[tmpvar_12] * tmpvar_1) * inBlendWeight.y)
  ) + (
    (matWorldArray[tmpvar_13] * tmpvar_1)
   * inBlendWeight.z)) + ((matWorldArray[tmpvar_14] * tmpvar_1) * inBlendWeight.w));
  vec4 tmpvar_15;
  tmpvar_15.w = 0.0;
  tmpvar_15.xyz = inTangent;
  vec4 tmpvar_16;
  tmpvar_16.w = 0.0;
  tmpvar_16.xyz = inTangent;
  vec4 tmpvar_17;
  tmpvar_17.w = 0.0;
  tmpvar_17.xyz = inTangent;
  vec4 tmpvar_18;
  tmpvar_18.w = 0.0;
  tmpvar_18.xyz = inTangent;
  vec3 tmpvar_19;
  tmpvar_19 = normalize(((
    (((matWorldArray[tmpvar_11] * tmpvar_15).xyz * inBlendWeight.x) + ((matWorldArray[tmpvar_12] * tmpvar_16).xyz * inBlendWeight.y))
   + 
    ((matWorldArray[tmpvar_13] * tmpvar_17).xyz * inBlendWeight.z)
  ) + (
    (matWorldArray[tmpvar_14] * tmpvar_18)
  .xyz * inBlendWeight.w)));
  vec3 tmpvar_20;
  tmpvar_20 = ((inNormal.yzx * tmpvar_19.zxy) - (inNormal.zxy * tmpvar_19.yzx));
  vObjectB_2 = tmpvar_20;
  if ((dot ((
    (inNormal.yzx * inTangent.zxy)
   - 
    (inNormal.zxy * inTangent.yzx)
  ), inBinormal) < 0.0)) {
    vObjectB_2 = -(tmpvar_20);
  };
  vec4 tmpvar_21;
  tmpvar_21 = (matWorld * vObjectPos_3);
  vec4 tmpvar_22;
  tmpvar_22.w = 0.0;
  tmpvar_22.xyz = inNormal;
  vec3 tmpvar_23;
  tmpvar_23 = normalize((matWorld * tmpvar_22).xyz);
  tmpvar_4 = (matWorldViewProj * vObjectPos_3);
  vec4 tmpvar_24;
  tmpvar_24.w = 0.0;
  tmpvar_24.xyz = vObjectB_2;
  vec3 tmpvar_25;
  tmpvar_25 = normalize((matWorld * tmpvar_24).xyz);
  vec4 tmpvar_26;
  tmpvar_26.w = 0.0;
  tmpvar_26.xyz = tmpvar_19;
  vec3 tmpvar_27;
  tmpvar_27 = normalize((matWorld * tmpvar_26).xyz);
  vec3 tmpvar_28;
  tmpvar_28.x = tmpvar_27.x;
  tmpvar_28.y = tmpvar_25.x;
  tmpvar_28.z = tmpvar_23.x;
  vec3 tmpvar_29;
  tmpvar_29.x = tmpvar_27.y;
  tmpvar_29.y = tmpvar_25.y;
  tmpvar_29.z = tmpvar_23.y;
  vec3 tmpvar_30;
  tmpvar_30.x = tmpvar_27.z;
  tmpvar_30.y = tmpvar_25.z;
  tmpvar_30.z = tmpvar_23.z;
  mat3 tmpvar_31;
  tmpvar_31[0] = tmpvar_28;
  tmpvar_31[1] = tmpvar_29;
  tmpvar_31[2] = tmpvar_30;
  tmpvar_7 = normalize((tmpvar_31 * -(vSunDir.xyz)));
  tmpvar_8 = (tmpvar_31 * vec3(0.0, 0.0, 1.0));
  tmpvar_5 = inColor0.zyxw;
  vec4 vWorldPos_32;
  vWorldPos_32 = tmpvar_21;
  vec3 vWorldN_33;
  vWorldN_33 = tmpvar_23;
  vec4 total_35;
  total_35 = vec4(0.0, 0.0, 0.0, 0.0);
  for (int j_34 = 0; j_34 < iLightPointCount; j_34++) {
    if ((j_34 != 0)) {
      int tmpvar_36;
      tmpvar_36 = iLightIndices[j_34];
      vec3 tmpvar_37;
      tmpvar_37 = (vLightPosDir[tmpvar_36].xyz - vWorldPos_32.xyz);
      total_35 = (total_35 + ((
        clamp (dot (vWorldN_33, normalize(tmpvar_37)), 0.0, 1.0)
       * vLightDiffuse[tmpvar_36]) * (1.0/(
        dot (tmpvar_37, tmpvar_37)
      ))));
    };
  };
  tmpvar_6 = total_35.xyz;
  int tmpvar_38;
  tmpvar_38 = iLightIndices[0];
  vec3 tmpvar_39;
  tmpvar_39 = (vLightPosDir[tmpvar_38].xyz - tmpvar_21.xyz);
  tmpvar_9.xyz = (tmpvar_31 * normalize(tmpvar_39));
  tmpvar_9.w = clamp ((1.0/(dot (tmpvar_39, tmpvar_39))), 0.0, 1.0);
  vec3 tmpvar_40;
  tmpvar_40 = normalize((vCameraPos.xyz - tmpvar_21.xyz));
  tmpvar_10 = (tmpvar_31 * tmpvar_40);
  vec3 vWorldPos_41;
  vWorldPos_41 = tmpvar_21.xyz;
  vec3 vWorldN_42;
  vWorldN_42 = tmpvar_23;
  vec3 vWorldView_43;
  vWorldView_43 = tmpvar_40;
  vec4 total_45;
  total_45 = vec4(0.0, 0.0, 0.0, 0.0);
  for (int i_44 = 0; i_44 < iLightPointCount; i_44++) {
    vec3 tmpvar_46;
    tmpvar_46 = (vLightPosDir[i_44].xyz - vWorldPos_41);
    total_45 = (total_45 + ((
      (1.0/(dot (tmpvar_46, tmpvar_46)))
     * vLightDiffuse[i_44]) * pow (
      clamp (dot (normalize((vWorldView_43 + 
        normalize(tmpvar_46)
      )), vWorldN_42), 0.0, 1.0)
    , fMaterialPower)));
  };
  tmpvar_5.w = (inColor0.w * vMaterialColor.w);
  vec3 tmpvar_47;
  tmpvar_47 = (matWorldView * vObjectPos_3).xyz;
  gl_Position = tmpvar_4;
  Fog = (1.0/(exp2((
    sqrt(dot (tmpvar_47, tmpvar_47))
   * fFogDensity))));
  VertexColor = tmpvar_5;
  VertexLighting = tmpvar_6;
  Tex0 = inTexCoord;
  SunLightDir = tmpvar_7;
  SkyLightDir = tmpvar_8;
  PointLightDir = tmpvar_9;
  ShadowTexCoord = total_45;
  ViewDir = tmpvar_10;
}

