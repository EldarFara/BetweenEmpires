uniform float fFogDensity;
uniform int iLightIndices[4];
uniform mat4 matWorldViewProj;
uniform mat4 matWorldView;
uniform mat4 matWorld;
uniform vec4 vLightPosDir[4];
attribute vec3 inPosition;
attribute vec3 inNormal;
attribute vec4 inColor0;
attribute vec2 inTexCoord;
attribute vec3 inTangent;
attribute vec3 inBinormal;
varying vec4 VertexColor;
varying vec2 Tex0;
varying vec3 vec_to_light_0;
varying vec3 vec_to_light_1;
varying vec3 vec_to_light_2;
varying float Fog;
void main ()
{
  vec4 tmpvar_1;
  tmpvar_1.w = 1.0;
  tmpvar_1.xyz = inPosition;
  vec3 point_to_light_2;
  vec3 tmpvar_3;
  vec4 tmpvar_4;
  tmpvar_4 = (matWorld * tmpvar_1);
  vec4 tmpvar_5;
  tmpvar_5.w = 0.0;
  tmpvar_5.xyz = inNormal;
  vec3 tmpvar_6;
  tmpvar_6 = normalize((matWorld * tmpvar_5).xyz);
  vec4 tmpvar_7;
  tmpvar_7.w = 0.0;
  tmpvar_7.xyz = inBinormal;
  vec3 tmpvar_8;
  tmpvar_8 = normalize((matWorld * tmpvar_7).xyz);
  vec4 tmpvar_9;
  tmpvar_9.w = 0.0;
  tmpvar_9.xyz = inTangent;
  vec3 tmpvar_10;
  tmpvar_10 = normalize((matWorld * tmpvar_9).xyz);
  vec3 tmpvar_11;
  tmpvar_11.x = tmpvar_10.x;
  tmpvar_11.y = tmpvar_8.x;
  tmpvar_11.z = tmpvar_6.x;
  vec3 tmpvar_12;
  tmpvar_12.x = tmpvar_10.y;
  tmpvar_12.y = tmpvar_8.y;
  tmpvar_12.z = tmpvar_6.y;
  vec3 tmpvar_13;
  tmpvar_13.x = tmpvar_10.z;
  tmpvar_13.y = tmpvar_8.z;
  tmpvar_13.z = tmpvar_6.z;
  mat3 tmpvar_14;
  tmpvar_14[0] = tmpvar_11;
  tmpvar_14[1] = tmpvar_12;
  tmpvar_14[2] = tmpvar_13;
  point_to_light_2 = (vLightPosDir[iLightIndices[1]].xyz - tmpvar_4.xyz);
  tmpvar_3 = (tmpvar_14 * point_to_light_2);
  point_to_light_2 = (vLightPosDir[iLightIndices[2]].xyz - tmpvar_4.xyz);
  vec3 tmpvar_15;
  tmpvar_15 = (matWorldView * tmpvar_1).xyz;
  gl_Position = (matWorldViewProj * tmpvar_1);
  VertexColor = inColor0.zyxw;
  Tex0 = inTexCoord;
  vec_to_light_0 = (tmpvar_14 * (vLightPosDir[iLightIndices[0]].xyz - tmpvar_4.xyz));
  vec_to_light_1 = tmpvar_3;
  vec_to_light_2 = (tmpvar_14 * point_to_light_2);
  Fog = (1.0/(exp2((
    sqrt(dot (tmpvar_15, tmpvar_15))
   * fFogDensity))));
}

