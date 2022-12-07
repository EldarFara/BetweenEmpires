uniform vec4 vLightDiffuse[4];
uniform vec4 vSunDir;
uniform vec4 vSunColor;
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
attribute vec3 inPosition;
attribute vec3 inNormal;
attribute vec4 inColor0;
attribute vec2 inTexCoord;
varying vec4 Color;
varying vec2 Tex0;
varying vec4 SunLight;
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
  tmpvar_5.w = 0.0;
  tmpvar_5.xyz = inNormal;
  vec3 tmpvar_6;
  tmpvar_6 = normalize((matWorld * tmpvar_5).xyz);
  vec3 tmpvar_7;
  tmpvar_7 = (matWorldView * tmpvar_1).xyz;
  diffuse_light_2.w = vAmbientColor.w;
  diffuse_light_2.xyz = (vAmbientColor.xyz + (clamp (
    dot (tmpvar_6, -(vSkyLightDir.xyz))
  , 0.0, 1.0) * vSkyLightColor.xyz));
  vec4 vWorldPos_8;
  vWorldPos_8 = (matWorld * tmpvar_1);
  vec3 vWorldN_9;
  vWorldN_9 = tmpvar_6;
  vec4 total_11;
  total_11 = vec4(0.0, 0.0, 0.0, 0.0);
  for (int j_10 = 0; j_10 < iLightPointCount; j_10++) {
    int tmpvar_12;
    tmpvar_12 = iLightIndices[j_10];
    vec3 tmpvar_13;
    tmpvar_13 = (vLightPosDir[tmpvar_12].xyz - vWorldPos_8.xyz);
    float tmpvar_14;
    tmpvar_14 = dot (vWorldN_9, normalize(tmpvar_13));
    total_11 = (total_11 + ((
      max ((0.2 * (tmpvar_14 + 0.9)), tmpvar_14)
     * vLightDiffuse[tmpvar_12]) * (1.0/(
      dot (tmpvar_13, tmpvar_13)
    ))));
  };
  diffuse_light_2 = (diffuse_light_2 + total_11);
  float tmpvar_15;
  tmpvar_15 = dot (tmpvar_6, -(vSunDir.xyz));
  vec4 tmpvar_16;
  tmpvar_16.w = 1.0;
  tmpvar_16.xyz = (vSunColor.xyz * clamp (max (
    (0.2 * (tmpvar_15 + 0.9))
  , tmpvar_15), 0.0, 1.0));
  gl_Position = tmpvar_3;
  Color = (inColor0 * diffuse_light_2);
  Tex0 = inTexCoord;
  SunLight = (tmpvar_16 * inColor0.zyxw);
  ShadowTexCoord = tmpvar_4;
  Fog = (1.0/(exp2((
    sqrt(dot (tmpvar_7, tmpvar_7))
   * fFogDensity))));
}

