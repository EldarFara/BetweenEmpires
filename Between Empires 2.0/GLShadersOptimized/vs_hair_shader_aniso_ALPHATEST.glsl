uniform vec4 vLightDiffuse[4];
uniform vec4 vAmbientColor;
uniform vec4 vSkyLightDir;
uniform vec4 vSkyLightColor;
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
attribute vec3 inBinormal;
attribute vec4 inColor0;
attribute vec2 inTexCoord;
varying vec2 Tex0;
varying vec4 VertexLighting;
varying vec3 viewVec;
varying vec3 normal;
varying vec3 tangent;
varying vec4 VertexColor;
varying vec4 ShadowTexCoord;
varying float Fog;
void main ()
{
  vec4 tmpvar_1;
  tmpvar_1.w = 1.0;
  tmpvar_1.xyz = inPosition;
  vec4 diffuse_light_2;
  vec4 tmpvar_3;
  vec4 tmpvar_4;
  tmpvar_3 = (matWorldViewProj * tmpvar_1);
  vec4 tmpvar_5;
  tmpvar_5 = (matWorld * tmpvar_1);
  vec4 tmpvar_6;
  tmpvar_6.w = 0.0;
  tmpvar_6.xyz = inNormal;
  vec3 tmpvar_7;
  tmpvar_7 = normalize((matWorld * tmpvar_6).xyz);
  vec3 tmpvar_8;
  tmpvar_8 = (matWorldView * tmpvar_1).xyz;
  diffuse_light_2.w = vAmbientColor.w;
  diffuse_light_2.xyz = (vAmbientColor.xyz + (clamp (
    dot (tmpvar_7, -(vSkyLightDir.xyz))
  , 0.0, 1.0) * vSkyLightColor.xyz));
  vec4 vWorldPos_9;
  vWorldPos_9 = tmpvar_5;
  vec3 vWorldN_10;
  vWorldN_10 = tmpvar_7;
  vec4 total_12;
  total_12 = vec4(0.0, 0.0, 0.0, 0.0);
  for (int j_11 = 0; j_11 < iLightPointCount; j_11++) {
    int tmpvar_13;
    tmpvar_13 = iLightIndices[j_11];
    vec3 tmpvar_14;
    tmpvar_14 = (vLightPosDir[tmpvar_13].xyz - vWorldPos_9.xyz);
    float tmpvar_15;
    tmpvar_15 = dot (vWorldN_10, normalize(tmpvar_14));
    total_12 = (total_12 + ((
      max ((0.2 * (tmpvar_15 + 0.9)), tmpvar_15)
     * vLightDiffuse[tmpvar_13]) * (1.0/(
      dot (tmpvar_14, tmpvar_14)
    ))));
  };
  diffuse_light_2 = (diffuse_light_2 + total_12);
  vec4 tmpvar_16;
  tmpvar_16.w = 0.0;
  tmpvar_16.xyz = inNormal;
  vec4 tmpvar_17;
  tmpvar_17.w = 0.0;
  tmpvar_17.xyz = inBinormal;
  gl_Position = tmpvar_3;
  Tex0 = inTexCoord;
  VertexLighting = clamp ((inColor0.zyxw * diffuse_light_2), 0.0, 1.0);
  viewVec = normalize((vCameraPos - tmpvar_5).xyz);
  normal = normalize((matWorld * tmpvar_16).xyz);
  tangent = normalize((matWorld * tmpvar_17).xyz);
  VertexColor = inColor0.zyxw;
  ShadowTexCoord = tmpvar_4;
  Fog = (1.0/(exp2((
    sqrt(dot (tmpvar_8, tmpvar_8))
   * fFogDensity))));
}

