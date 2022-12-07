uniform vec4 vSunDir;
uniform vec4 vSunColor;
uniform float fFogDensity;
uniform float far_clip_Inv;
uniform bool use_depth_effects;
uniform float vTimer;
uniform vec4 vWaveInfo;
uniform vec4 vWaveOrigin;
uniform mat4 matWorldViewProj;
uniform mat4 matWorldView;
uniform mat4 matWorld;
uniform mat4 matWaterWorldViewProj;
uniform vec4 vCameraPos;
uniform vec4 vDepthRT_HalfPixel_ViewportSizeInv;
attribute vec3 inPosition;
attribute vec3 inNormal;
attribute vec4 inColor0;
attribute vec2 inTexCoord;
attribute vec3 inTangent;
attribute vec3 inBinormal;
varying vec2 Tex0;
varying vec4 LightDir_Alpha;
varying vec4 LightDif;
varying vec3 ViewDir;
varying vec3 CameraDir;
varying vec4 PosWater;
varying vec4 projCoord;
varying float Depth;
varying float Fog;
void main ()
{
  vec4 tmpvar_1;
  tmpvar_1.w = 1.0;
  tmpvar_1.xyz = inPosition;
  vec4 vPosition_2;
  vPosition_2.xyw = tmpvar_1.xyw;
  vec4 tmpvar_3;
  vec2 tmpvar_4;
  vec4 tmpvar_5;
  vec4 tmpvar_6;
  vec3 tmpvar_7;
  vec3 tmpvar_8;
  vec4 tmpvar_9;
  vec4 tmpvar_10;
  float tmpvar_11;
  float tmpvar_12;
  tmpvar_12 = (vTimer * 10.0);
  vPosition_2.z = ((inPosition.z + (vWaveInfo.y * 
    sin(((vWaveInfo.w * inPosition.y) + tmpvar_12))
  )) + vWaveOrigin.y);
  vPosition_2.z = ((vPosition_2.z + (vWaveInfo.x * 
    sin(((vWaveInfo.z * inPosition.x) + tmpvar_12))
  )) + vWaveOrigin.x);
  vPosition_2.z = (vPosition_2.z + vWaveOrigin.z);
  tmpvar_3 = (matWorldViewProj * vPosition_2);
  tmpvar_9 = (matWaterWorldViewProj * vPosition_2);
  vec3 tmpvar_13;
  tmpvar_13 = (matWorld * vPosition_2).xyz;
  vec4 tmpvar_14;
  tmpvar_14.w = 0.0;
  tmpvar_14.xyz = inNormal;
  vec4 tmpvar_15;
  tmpvar_15.w = 0.0;
  tmpvar_15.xyz = inBinormal;
  vec4 tmpvar_16;
  tmpvar_16.w = 0.0;
  tmpvar_16.xyz = inTangent;
  vec3 tmpvar_17;
  tmpvar_17 = (matWorldView * vPosition_2).xyz;
  mat3 tmpvar_18;
  tmpvar_18[0] = normalize((matWorld * tmpvar_16).xyz);
  tmpvar_18[1] = normalize((matWorld * tmpvar_15).xyz);
  tmpvar_18[2] = normalize((matWorld * tmpvar_14).xyz);
  tmpvar_8 = (tmpvar_18 * normalize((vCameraPos.xyz - tmpvar_13)));
  tmpvar_7.xy = normalize((tmpvar_18 * normalize(
    (vCameraPos.xyz - tmpvar_13)
  ))).xy;
  tmpvar_4 = (inTexCoord * 1.75);
  tmpvar_5.xyz = (tmpvar_18 * -(vSunDir.xyz));
  tmpvar_6 = (vSunColor * inColor0.zyxw);
  tmpvar_5.w = inColor0.w;
  float tmpvar_19;
  tmpvar_19 = (1.0/(exp2((
    sqrt(dot (tmpvar_17, tmpvar_17))
   * fFogDensity))));
  if (use_depth_effects) {
    vec2 tmpvar_20;
    tmpvar_20.x = tmpvar_3.x;
    tmpvar_20.y = -(tmpvar_3.y);
    tmpvar_10.xy = ((tmpvar_20 + tmpvar_3.w) / 2.0);
    tmpvar_10.xy = (tmpvar_10.xy + (vDepthRT_HalfPixel_ViewportSizeInv.xy * tmpvar_3.w));
    tmpvar_10.zw = tmpvar_3.zw;
    tmpvar_11 = (((0.5 * tmpvar_3.z) + 0.5) * far_clip_Inv);
  };
  gl_Position = tmpvar_3;
  Tex0 = tmpvar_4;
  LightDir_Alpha = tmpvar_5;
  LightDif = tmpvar_6;
  ViewDir = tmpvar_7;
  CameraDir = tmpvar_8;
  PosWater = tmpvar_9;
  projCoord = tmpvar_10;
  Depth = tmpvar_11;
  Fog = tmpvar_19;
}

