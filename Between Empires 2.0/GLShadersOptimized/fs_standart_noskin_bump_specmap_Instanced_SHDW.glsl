uniform sampler2D diffuse_texture;
uniform sampler2D specular_texture;
uniform sampler2D normal_texture;
uniform sampler2D shadowmap_texture;
uniform vec4 vLightDiffuse[4];
uniform vec4 vMaterialColor;
uniform vec4 vSpecularColor;
uniform vec4 vSunColor;
uniform vec4 vAmbientColor;
uniform vec4 vFogColor;
uniform vec4 output_gamma_inv;
uniform float fMaterialPower;
uniform float spec_coef;
uniform int iLightIndices[4];
uniform float fShadowMapNextPixel;
uniform float fShadowMapSize;
varying float Fog;
varying vec4 VertexColor;
varying vec2 Tex0;
varying vec3 SunLightDir;
varying vec4 PointLightDir;
varying vec4 ShadowTexCoord;
varying vec3 ViewDir;
void main ()
{
  vec4 tex_col_1;
  vec4 total_light_2;
  vec3 normal_3;
  vec4 tmpvar_4;
  tmpvar_4.w = 1.0;
  normal_3 = ((2.0 * texture2D (normal_texture, Tex0)) - 1.0).xyz;
  float sun_amount_5;
  sun_amount_5 = 0.0;
  vec2 tmpvar_6;
  tmpvar_6 = fract((ShadowTexCoord.xy * fShadowMapSize));
  vec4 tmpvar_7;
  tmpvar_7 = texture2D (shadowmap_texture, ShadowTexCoord.xy);
  float tmpvar_8;
  if ((tmpvar_7.x < ShadowTexCoord.z)) {
    tmpvar_8 = 0.0;
  } else {
    tmpvar_8 = 1.0;
  };
  vec2 tmpvar_9;
  tmpvar_9.y = 0.0;
  tmpvar_9.x = fShadowMapNextPixel;
  vec4 tmpvar_10;
  tmpvar_10 = texture2D (shadowmap_texture, (ShadowTexCoord.xy + tmpvar_9));
  float tmpvar_11;
  if ((tmpvar_10.x < ShadowTexCoord.z)) {
    tmpvar_11 = 0.0;
  } else {
    tmpvar_11 = 1.0;
  };
  vec2 tmpvar_12;
  tmpvar_12.x = 0.0;
  tmpvar_12.y = fShadowMapNextPixel;
  vec4 tmpvar_13;
  tmpvar_13 = texture2D (shadowmap_texture, (ShadowTexCoord.xy + tmpvar_12));
  float tmpvar_14;
  if ((tmpvar_13.x < ShadowTexCoord.z)) {
    tmpvar_14 = 0.0;
  } else {
    tmpvar_14 = 1.0;
  };
  vec4 tmpvar_15;
  tmpvar_15 = texture2D (shadowmap_texture, (ShadowTexCoord.xy + vec2(fShadowMapNextPixel)));
  float tmpvar_16;
  if ((tmpvar_15.x < ShadowTexCoord.z)) {
    tmpvar_16 = 0.0;
  } else {
    tmpvar_16 = 1.0;
  };
  sun_amount_5 = clamp (mix (mix (tmpvar_8, tmpvar_11, tmpvar_6.x), mix (tmpvar_14, tmpvar_16, tmpvar_6.x), tmpvar_6.y), 0.0, 1.0);
  total_light_2.w = vAmbientColor.w;
  total_light_2.xyz = (vAmbientColor.xyz + ((vec3(
    clamp (dot (SunLightDir, normal_3), 0.0, 1.0)
  ) * sun_amount_5) * vSunColor.xyz));
  int tmpvar_17;
  tmpvar_17 = iLightIndices[0];
  total_light_2 = (total_light_2 + clamp ((
    (dot (PointLightDir.xyz, normal_3) * vLightDiffuse[tmpvar_17])
   * PointLightDir.w), 0.0, 1.0));
  tmpvar_4.xyz = (total_light_2.xyz * vMaterialColor.xyz);
  vec4 tmpvar_18;
  tmpvar_18 = texture2D (diffuse_texture, Tex0);
  tex_col_1.w = tmpvar_18.w;
  tex_col_1.xyz = pow (tmpvar_18.xyz, vec3(2.2, 2.2, 2.2));
  tmpvar_4.xyz = (tmpvar_4.xyz * tex_col_1.xyz);
  tmpvar_4.xyz = (tmpvar_4.xyz * VertexColor.xyz);
  vec4 tmpvar_19;
  tmpvar_19.w = 1.0;
  tmpvar_19.xyz = vSpecularColor.xyz;
  vec4 tmpvar_20;
  tmpvar_20.w = 1.0;
  tmpvar_20.xyz = vSunColor.xyz;
  tmpvar_4 = (tmpvar_4 + ((
    ((((0.1 * spec_coef) * tmpvar_19) * dot (texture2D (specular_texture, Tex0).xyz, vec3(0.33, 0.33, 0.33))) * tmpvar_20)
   * sun_amount_5) * pow (
    clamp (dot (normalize((ViewDir + SunLightDir)), normal_3), 0.0, 1.0)
  , fMaterialPower)));
  tmpvar_4.xyz = pow (tmpvar_4.xyz, output_gamma_inv.xyz);
  tmpvar_4.xyz = mix (vFogColor.xyz, tmpvar_4.xyz, Fog);
  tmpvar_4.w = VertexColor.w;
  gl_FragColor = tmpvar_4;
}

