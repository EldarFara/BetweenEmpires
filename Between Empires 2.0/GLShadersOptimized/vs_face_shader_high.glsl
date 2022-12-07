uniform vec4 vLightDiffuse[4];
uniform vec4 vSunDir;
uniform vec4 vSkyLightDir;
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
attribute vec4 inColor0;
attribute vec2 inTexCoord;
attribute vec3 inTangent;
attribute vec3 inBinormal;
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
  vec4 tmpvar_2;
  vec4 tmpvar_3;
  vec3 tmpvar_4;
  vec3 tmpvar_5;
  vec4 tmpvar_6;
  vec4 tmpvar_7;
  vec4 tmpvar_8;
  tmpvar_8 = (matWorld * tmpvar_1);
  tmpvar_2 = (matWorldViewProj * tmpvar_1);
  vec4 tmpvar_9;
  tmpvar_9.w = 0.0;
  tmpvar_9.xyz = inNormal;
  vec3 tmpvar_10;
  tmpvar_10 = normalize((matWorld * tmpvar_9).xyz);
  vec4 tmpvar_11;
  tmpvar_11.w = 0.0;
  tmpvar_11.xyz = inBinormal;
  vec3 tmpvar_12;
  tmpvar_12 = normalize((matWorld * tmpvar_11).xyz);
  vec4 tmpvar_13;
  tmpvar_13.w = 0.0;
  tmpvar_13.xyz = inTangent;
  vec3 tmpvar_14;
  tmpvar_14 = normalize((matWorld * tmpvar_13).xyz);
  vec3 tmpvar_15;
  tmpvar_15.x = tmpvar_14.x;
  tmpvar_15.y = tmpvar_12.x;
  tmpvar_15.z = tmpvar_10.x;
  vec3 tmpvar_16;
  tmpvar_16.x = tmpvar_14.y;
  tmpvar_16.y = tmpvar_12.y;
  tmpvar_16.z = tmpvar_10.y;
  vec3 tmpvar_17;
  tmpvar_17.x = tmpvar_14.z;
  tmpvar_17.y = tmpvar_12.z;
  tmpvar_17.z = tmpvar_10.z;
  mat3 tmpvar_18;
  tmpvar_18[0] = tmpvar_15;
  tmpvar_18[1] = tmpvar_16;
  tmpvar_18[2] = tmpvar_17;
  tmpvar_4 = normalize((tmpvar_18 * -(vSunDir.xyz)));
  tmpvar_5 = (tmpvar_18 * -(vSkyLightDir.xyz));
  tmpvar_3 = inColor0.zyxw;
  vec4 vWorldPos_19;
  vWorldPos_19 = tmpvar_8;
  vec3 vWorldN_20;
  vWorldN_20 = tmpvar_10;
  vec4 total_22;
  total_22 = vec4(0.0, 0.0, 0.0, 0.0);
  for (int j_21 = 0; j_21 < iLightPointCount; j_21++) {
    if ((j_21 != 0)) {
      int tmpvar_23;
      tmpvar_23 = iLightIndices[j_21];
      vec3 tmpvar_24;
      tmpvar_24 = (vLightPosDir[tmpvar_23].xyz - vWorldPos_19.xyz);
      float tmpvar_25;
      tmpvar_25 = dot (vWorldN_20, normalize(tmpvar_24));
      total_22 = (total_22 + ((
        max ((0.2 * (tmpvar_25 + 0.9)), tmpvar_25)
       * vLightDiffuse[tmpvar_23]) * (1.0/(
        dot (tmpvar_24, tmpvar_24)
      ))));
    };
  };
  int tmpvar_26;
  tmpvar_26 = iLightIndices[0];
  vec3 tmpvar_27;
  tmpvar_27 = (vLightPosDir[tmpvar_26].xyz - tmpvar_8.xyz);
  tmpvar_6.w = clamp ((1.0/(dot (tmpvar_27, tmpvar_27))), 0.0, 1.0);
  tmpvar_6.xyz = (tmpvar_18 * normalize(tmpvar_27));
  vec3 tmpvar_28;
  tmpvar_28 = (matWorldView * tmpvar_1).xyz;
  gl_Position = tmpvar_2;
  Fog = (1.0/(exp2((
    sqrt(dot (tmpvar_28, tmpvar_28))
   * fFogDensity))));
  VertexColor = tmpvar_3;
  VertexLighting = total_22.xyz;
  Tex0 = inTexCoord;
  SunLightDir = tmpvar_4;
  SkyLightDir = tmpvar_5;
  PointLightDir = tmpvar_6;
  ShadowTexCoord = tmpvar_7;
  ViewDir = (tmpvar_18 * normalize((vCameraPos.xyz - tmpvar_8.xyz)));
}

