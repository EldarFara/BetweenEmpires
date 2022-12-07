uniform vec4 vLightDiffuse[4];
uniform vec4 vMaterialColor;
uniform vec4 vSunDir;
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
  vec4 tmpvar_8;
  int tmpvar_9;
  tmpvar_9 = int(inBlendIndices.x);
  int tmpvar_10;
  tmpvar_10 = int(inBlendIndices.y);
  int tmpvar_11;
  tmpvar_11 = int(inBlendIndices.z);
  int tmpvar_12;
  tmpvar_12 = int(inBlendIndices.w);
  vObjectPos_3 = (((
    ((matWorldArray[tmpvar_9] * tmpvar_1) * inBlendWeight.x)
   + 
    ((matWorldArray[tmpvar_10] * tmpvar_1) * inBlendWeight.y)
  ) + (
    (matWorldArray[tmpvar_11] * tmpvar_1)
   * inBlendWeight.z)) + ((matWorldArray[tmpvar_12] * tmpvar_1) * inBlendWeight.w));
  vec4 tmpvar_13;
  tmpvar_13.w = 0.0;
  tmpvar_13.xyz = inTangent;
  vec4 tmpvar_14;
  tmpvar_14.w = 0.0;
  tmpvar_14.xyz = inTangent;
  vec4 tmpvar_15;
  tmpvar_15.w = 0.0;
  tmpvar_15.xyz = inTangent;
  vec4 tmpvar_16;
  tmpvar_16.w = 0.0;
  tmpvar_16.xyz = inTangent;
  vec3 tmpvar_17;
  tmpvar_17 = normalize(((
    (((matWorldArray[tmpvar_9] * tmpvar_13).xyz * inBlendWeight.x) + ((matWorldArray[tmpvar_10] * tmpvar_14).xyz * inBlendWeight.y))
   + 
    ((matWorldArray[tmpvar_11] * tmpvar_15).xyz * inBlendWeight.z)
  ) + (
    (matWorldArray[tmpvar_12] * tmpvar_16)
  .xyz * inBlendWeight.w)));
  vec3 tmpvar_18;
  tmpvar_18 = ((inNormal.yzx * tmpvar_17.zxy) - (inNormal.zxy * tmpvar_17.yzx));
  vObjectB_2 = tmpvar_18;
  if ((dot ((
    (inNormal.yzx * inTangent.zxy)
   - 
    (inNormal.zxy * inTangent.yzx)
  ), inBinormal) < 0.0)) {
    vObjectB_2 = -(tmpvar_18);
  };
  vec4 tmpvar_19;
  tmpvar_19 = (matWorld * vObjectPos_3);
  vec4 tmpvar_20;
  tmpvar_20.w = 0.0;
  tmpvar_20.xyz = inNormal;
  vec3 tmpvar_21;
  tmpvar_21 = normalize((matWorld * tmpvar_20).xyz);
  tmpvar_4 = (matWorldViewProj * vObjectPos_3);
  vec4 tmpvar_22;
  tmpvar_22.w = 0.0;
  tmpvar_22.xyz = vObjectB_2;
  vec3 tmpvar_23;
  tmpvar_23 = normalize((matWorld * tmpvar_22).xyz);
  vec4 tmpvar_24;
  tmpvar_24.w = 0.0;
  tmpvar_24.xyz = tmpvar_17;
  vec3 tmpvar_25;
  tmpvar_25 = normalize((matWorld * tmpvar_24).xyz);
  vec3 tmpvar_26;
  tmpvar_26.x = tmpvar_25.x;
  tmpvar_26.y = tmpvar_23.x;
  tmpvar_26.z = tmpvar_21.x;
  vec3 tmpvar_27;
  tmpvar_27.x = tmpvar_25.y;
  tmpvar_27.y = tmpvar_23.y;
  tmpvar_27.z = tmpvar_21.y;
  vec3 tmpvar_28;
  tmpvar_28.x = tmpvar_25.z;
  tmpvar_28.y = tmpvar_23.z;
  tmpvar_28.z = tmpvar_21.z;
  mat3 tmpvar_29;
  tmpvar_29[0] = tmpvar_26;
  tmpvar_29[1] = tmpvar_27;
  tmpvar_29[2] = tmpvar_28;
  tmpvar_6 = normalize((tmpvar_29 * -(vSunDir.xyz)));
  tmpvar_7 = (tmpvar_29 * vec3(0.0, 0.0, 1.0));
  tmpvar_5 = inColor0.zyxw;
  vec4 vWorldPos_30;
  vWorldPos_30 = tmpvar_19;
  vec3 vWorldN_31;
  vWorldN_31 = tmpvar_21;
  vec4 total_33;
  total_33 = vec4(0.0, 0.0, 0.0, 0.0);
  for (int j_32 = 0; j_32 < iLightPointCount; j_32++) {
    if ((j_32 != 0)) {
      int tmpvar_34;
      tmpvar_34 = iLightIndices[j_32];
      vec3 tmpvar_35;
      tmpvar_35 = (vLightPosDir[tmpvar_34].xyz - vWorldPos_30.xyz);
      total_33 = (total_33 + ((
        clamp (dot (vWorldN_31, normalize(tmpvar_35)), 0.0, 1.0)
       * vLightDiffuse[tmpvar_34]) * (1.0/(
        dot (tmpvar_35, tmpvar_35)
      ))));
    };
  };
  int tmpvar_36;
  tmpvar_36 = iLightIndices[0];
  vec3 tmpvar_37;
  tmpvar_37 = (vLightPosDir[tmpvar_36].xyz - tmpvar_19.xyz);
  tmpvar_8.xyz = (tmpvar_29 * normalize(tmpvar_37));
  tmpvar_8.w = clamp ((1.0/(dot (tmpvar_37, tmpvar_37))), 0.0, 1.0);
  tmpvar_5.w = (inColor0.w * vMaterialColor.w);
  vec3 tmpvar_38;
  tmpvar_38 = (matWorldView * vObjectPos_3).xyz;
  gl_Position = tmpvar_4;
  Fog = (1.0/(exp2((
    sqrt(dot (tmpvar_38, tmpvar_38))
   * fFogDensity))));
  VertexColor = tmpvar_5;
  VertexLighting = total_33.xyz;
  Tex0 = inTexCoord;
  SunLightDir = tmpvar_6;
  SkyLightDir = tmpvar_7;
  PointLightDir = tmpvar_8;
  ShadowTexCoord = (matSunViewProj * tmpvar_19);
  ViewDir = (tmpvar_29 * normalize((vCameraPos.xyz - tmpvar_19.xyz)));
}

