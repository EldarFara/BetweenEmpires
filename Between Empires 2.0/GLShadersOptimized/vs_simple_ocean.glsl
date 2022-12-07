uniform vec4 vSunDir;
uniform vec4 vSunColor;
uniform vec4 vAmbientColor;
uniform vec4 debug_vector;
uniform float fFogDensity;
uniform float time_var;
uniform mat4 matWorldView;
uniform mat4 matWorld;
uniform mat4 matWaterViewProj;
uniform mat4 matViewProj;
uniform vec4 vCameraPos;
attribute vec3 inPosition;
varying vec2 Tex0;
varying vec3 LightDir;
varying vec4 LightDif;
varying vec3 CameraDir;
varying vec4 PosWater;
varying float Fog;
void main ()
{
  vec3 vNormal_1;
  vec4 vWorldPos_2;
  vec4 tmpvar_3;
  tmpvar_3.w = 1.0;
  tmpvar_3.xyz = inPosition;
  vec4 tmpvar_4;
  tmpvar_4 = (matWorld * tmpvar_3);
  vWorldPos_2.xyw = tmpvar_4.xyw;
  vec3 tmpvar_5;
  tmpvar_5 = (vCameraPos.xyz - tmpvar_4.xyz);
  float tmpvar_6;
  tmpvar_6 = (1.0 - clamp ((
    sqrt(dot (tmpvar_5, tmpvar_5))
   * 0.01), 0.0, 1.0));
  vWorldPos_2.z = (tmpvar_4.z + ((
    (debug_vector.z * sin(((
      (tmpvar_4.x + tmpvar_4.y)
     * debug_vector.x) + time_var)))
   * 
    cos((((tmpvar_4.x - tmpvar_4.y) * debug_vector.y) + (time_var + 4.0)))
  ) * tmpvar_6));
  gl_Position = (matViewProj * vWorldPos_2);
  PosWater = (matWaterViewProj * vWorldPos_2);
  if ((tmpvar_6 > 0.0)) {
    vec3 near_wave_heights_0_7;
    vec3 near_wave_heights_1_8;
    near_wave_heights_0_7.xy = (tmpvar_4.xy + vec2(0.1, 0.0));
    near_wave_heights_1_8.xy = (tmpvar_4.xy + vec2(0.0, 1.0));
    float tmpvar_9;
    tmpvar_9 = (time_var + 4.0);
    near_wave_heights_0_7.z = ((debug_vector.z * sin(
      (((near_wave_heights_0_7.x + near_wave_heights_0_7.y) * debug_vector.x) + time_var)
    )) * cos((
      ((near_wave_heights_0_7.x - near_wave_heights_0_7.y) * debug_vector.y)
     + tmpvar_9)));
    near_wave_heights_1_8.z = ((debug_vector.z * sin(
      (((near_wave_heights_1_8.x + near_wave_heights_1_8.y) * debug_vector.x) + time_var)
    )) * cos((
      ((near_wave_heights_1_8.x - near_wave_heights_1_8.y) * debug_vector.y)
     + tmpvar_9)));
    vec3 tmpvar_10;
    tmpvar_10 = normalize((near_wave_heights_0_7 - vWorldPos_2.xyz));
    vec3 tmpvar_11;
    tmpvar_11 = normalize((near_wave_heights_1_8 - vWorldPos_2.xyz));
    vNormal_1 = ((tmpvar_10.yzx * tmpvar_11.zxy) - (tmpvar_10.zxy * tmpvar_11.yzx));
  } else {
    vNormal_1 = vec3(0.0, 0.0, 1.0);
  };
  vec3 tmpvar_12;
  tmpvar_12 = normalize(((vec3(0.0, 0.0, 1.0) * vNormal_1.zxy) - (vec3(0.0, 1.0, 0.0) * vNormal_1.yzx)));
  vec3 tmpvar_13;
  tmpvar_13.x = 1.0;
  tmpvar_13.y = tmpvar_12.x;
  tmpvar_13.z = vNormal_1.x;
  vec3 tmpvar_14;
  tmpvar_14.x = 0.0;
  tmpvar_14.y = tmpvar_12.y;
  tmpvar_14.z = vNormal_1.y;
  vec3 tmpvar_15;
  tmpvar_15.x = 0.0;
  tmpvar_15.y = tmpvar_12.z;
  tmpvar_15.z = vNormal_1.z;
  mat3 tmpvar_16;
  tmpvar_16[0] = tmpvar_13;
  tmpvar_16[1] = tmpvar_14;
  tmpvar_16[2] = tmpvar_15;
  CameraDir = (tmpvar_16 * normalize((vCameraPos.xyz - vWorldPos_2.xyz)));
  Tex0 = vWorldPos_2.xy;
  LightDir = (tmpvar_16 * -(vSunDir.xyz));
  LightDif = (vAmbientColor + vSunColor);
  LightDir = normalize(LightDir);
  vec4 tmpvar_17;
  tmpvar_17.w = 1.0;
  tmpvar_17.xyz = inPosition;
  vec3 tmpvar_18;
  tmpvar_18 = (matWorldView * tmpvar_17).xyz;
  Fog = (1.0/(exp2((
    sqrt(dot (tmpvar_18, tmpvar_18))
   * fFogDensity))));
}

