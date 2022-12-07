uniform sampler2D diffuse_texture;
uniform sampler2D diffuse_texture_2;
uniform sampler2D specular_texture;
uniform sampler2D normal_texture;
uniform sampler2D shadowmap_texture;
uniform vec4 vLightDiffuse[4];
uniform vec4 vMaterialColor;
uniform vec4 vSpecularColor;
uniform vec4 vSunColor;
uniform vec4 vAmbientColor;
uniform vec4 vSkyLightColor;
uniform vec4 vFogColor;
uniform vec4 output_gamma_inv;
uniform float fMaterialPower;
uniform int iLightIndices[4];
uniform float fShadowMapNextPixel;
uniform float fShadowMapSize;
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
  vec4 tex_col_1;
  vec3 point_lighting_2;
  vec3 normal_3;
  vec4 total_light_4;
  vec4 tmpvar_5;
  total_light_4 = vAmbientColor;
  normal_3 = ((2.0 * mix (texture2D (normal_texture, Tex0).xyz, texture2D (specular_texture, Tex0).xyz, VertexColor.w)) - 1.0);
  normal_3 = normalize(normal_3);
  float sun_amount_6;
  sun_amount_6 = 0.0;
  vec2 tmpvar_7;
  tmpvar_7 = fract((ShadowTexCoord.xy * fShadowMapSize));
  vec4 tmpvar_8;
  tmpvar_8 = texture2D (shadowmap_texture, ShadowTexCoord.xy);
  float tmpvar_9;
  if ((tmpvar_8.x < ShadowTexCoord.z)) {
    tmpvar_9 = 0.0;
  } else {
    tmpvar_9 = 1.0;
  };
  vec2 tmpvar_10;
  tmpvar_10.y = 0.0;
  tmpvar_10.x = fShadowMapNextPixel;
  vec4 tmpvar_11;
  tmpvar_11 = texture2D (shadowmap_texture, (ShadowTexCoord.xy + tmpvar_10));
  float tmpvar_12;
  if ((tmpvar_11.x < ShadowTexCoord.z)) {
    tmpvar_12 = 0.0;
  } else {
    tmpvar_12 = 1.0;
  };
  vec2 tmpvar_13;
  tmpvar_13.x = 0.0;
  tmpvar_13.y = fShadowMapNextPixel;
  vec4 tmpvar_14;
  tmpvar_14 = texture2D (shadowmap_texture, (ShadowTexCoord.xy + tmpvar_13));
  float tmpvar_15;
  if ((tmpvar_14.x < ShadowTexCoord.z)) {
    tmpvar_15 = 0.0;
  } else {
    tmpvar_15 = 1.0;
  };
  vec4 tmpvar_16;
  tmpvar_16 = texture2D (shadowmap_texture, (ShadowTexCoord.xy + vec2(fShadowMapNextPixel)));
  float tmpvar_17;
  if ((tmpvar_16.x < ShadowTexCoord.z)) {
    tmpvar_17 = 0.0;
  } else {
    tmpvar_17 = 1.0;
  };
  sun_amount_6 = clamp (mix (mix (tmpvar_9, tmpvar_12, tmpvar_7.x), mix (tmpvar_15, tmpvar_17, tmpvar_7.x), tmpvar_7.y), 0.0, 1.0);
  float tmpvar_18;
  tmpvar_18 = dot (SunLightDir, normal_3);
  vec4 tmpvar_19;
  tmpvar_19.w = 1.0;
  tmpvar_19.xyz = vSunColor.xyz;
  total_light_4 = (vAmbientColor + ((
    clamp (max ((0.2 * (tmpvar_18 + 0.9)), tmpvar_18), 0.0, 1.0)
   * sun_amount_6) * tmpvar_19));
  float tmpvar_20;
  tmpvar_20 = dot (SkyLightDir, normal_3);
  total_light_4 = (total_light_4 + (clamp (
    max ((0.2 * (tmpvar_20 + 0.9)), tmpvar_20)
  , 0.0, 1.0) * vSkyLightColor));
  int tmpvar_21;
  tmpvar_21 = iLightIndices[0];
  float tmpvar_22;
  tmpvar_22 = dot (PointLightDir.xyz, normal_3);
  point_lighting_2 = (((PointLightDir.w * 0.9) * clamp (
    max ((0.2 * (tmpvar_22 + 0.9)), tmpvar_22)
  , 0.0, 1.0)) * vLightDiffuse[tmpvar_21].xyz);
  point_lighting_2 = (point_lighting_2 + VertexLighting);
  total_light_4.xyz = (total_light_4.xyz + point_lighting_2);
  tmpvar_5.xyz = total_light_4.xyz;
  vec4 tmpvar_23;
  tmpvar_23 = mix (texture2D (diffuse_texture, Tex0), texture2D (diffuse_texture_2, Tex0), VertexColor.w);
  tex_col_1.w = tmpvar_23.w;
  tex_col_1.xyz = pow (tmpvar_23.xyz, vec3(2.2, 2.2, 2.2));
  tmpvar_5 = (tmpvar_5 * tex_col_1);
  tmpvar_5.xyz = (tmpvar_5.xyz * (VertexColor.xyz * vMaterialColor.xyz));
  vec4 tmpvar_24;
  tmpvar_24.w = 1.0;
  tmpvar_24.xyz = vSpecularColor.xyz;
  vec4 tmpvar_25;
  tmpvar_25.w = 1.0;
  tmpvar_25.xyz = vSunColor.xyz;
  tmpvar_5 = (tmpvar_5 + vec4((clamp (
    (1.0 - dot (ViewDir, normal_3))
  , 0.0, 1.0) * (
    ((tmpvar_24 * tmpvar_25) * pow (clamp (dot (
      normalize((ViewDir + SunLightDir))
    , normal_3), 0.0, 1.0), fMaterialPower))
   * sun_amount_6).x)));
  tmpvar_5.xyz = clamp (pow (tmpvar_5.xyz, output_gamma_inv.xyz), 0.0, 1.0);
  tmpvar_5.w = vMaterialColor.w;
  tmpvar_5.xyz = mix (vFogColor.xyz, tmpvar_5.xyz, Fog);
  gl_FragColor = tmpvar_5;
}

