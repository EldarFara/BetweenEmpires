uniform vec4 vLightDiffuse[4];
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
  vec4 tmpvar_2;
  vec4 tmpvar_3;
  vec3 tmpvar_4;
  vec4 tmpvar_5;
  vec4 tmpvar_6;
  vec4 tmpvar_7;
  tmpvar_7 = (matWorld * tmpvar_1);
  tmpvar_2 = (matWorldViewProj * tmpvar_1);
  vec4 tmpvar_8;
  tmpvar_8.w = 0.0;
  tmpvar_8.xyz = inNormal;
  vec3 tmpvar_9;
  tmpvar_9 = normalize((matWorld * tmpvar_8).xyz);
  tmpvar_6 = (matSunViewProj * tmpvar_7);
  tmpvar_3 = inColor0.zyxw;
  vec4 vWorldPos_10;
  vWorldPos_10 = tmpvar_7;
  vec3 vWorldN_11;
  vWorldN_11 = tmpvar_9;
  vec4 total_13;
  total_13 = vec4(0.0, 0.0, 0.0, 0.0);
  for (int j_12 = 0; j_12 < iLightPointCount; j_12++) {
    if ((j_12 != 0)) {
      int tmpvar_14;
      tmpvar_14 = iLightIndices[j_12];
      vec3 tmpvar_15;
      tmpvar_15 = (vLightPosDir[tmpvar_14].xyz - vWorldPos_10.xyz);
      float tmpvar_16;
      tmpvar_16 = dot (vWorldN_11, normalize(tmpvar_15));
      total_13 = (total_13 + ((
        max ((0.2 * (tmpvar_16 + 0.9)), tmpvar_16)
       * vLightDiffuse[tmpvar_14]) * (1.0/(
        dot (tmpvar_15, tmpvar_15)
      ))));
    };
  };
  int tmpvar_17;
  tmpvar_17 = iLightIndices[0];
  vec3 tmpvar_18;
  tmpvar_18 = (vLightPosDir[tmpvar_17].xyz - tmpvar_7.xyz);
  tmpvar_5.w = clamp ((1.0/(dot (tmpvar_18, tmpvar_18))), 0.0, 1.0);
  tmpvar_5.xyz = normalize(tmpvar_18);
  vec3 tmpvar_19;
  tmpvar_19 = (matWorldView * tmpvar_1).xyz;
  gl_Position = tmpvar_2;
  Fog = (1.0/(exp2((
    sqrt(dot (tmpvar_19, tmpvar_19))
   * fFogDensity))));
  VertexColor = tmpvar_3;
  VertexLighting = total_13.xyz;
  Tex0 = inTexCoord;
  SunLightDir = tmpvar_9;
  SkyLightDir = tmpvar_4;
  PointLightDir = tmpvar_5;
  ShadowTexCoord = tmpvar_6;
  ViewDir = normalize((vCameraPos.xyz - tmpvar_7.xyz));
}

