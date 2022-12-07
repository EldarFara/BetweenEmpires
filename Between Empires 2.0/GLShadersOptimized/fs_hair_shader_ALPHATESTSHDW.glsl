uniform sampler2D diffuse_texture;
uniform sampler2D diffuse_texture_2;
uniform sampler2D shadowmap_texture;
uniform vec4 vMaterialColor;
uniform vec4 vMaterialColor2;
uniform vec4 vFogColor;
uniform vec4 output_gamma_inv;
uniform float alpha_test_val;
uniform float fShadowMapNextPixel;
uniform float fShadowMapSize;
varying vec4 Color;
varying vec2 Tex0;
varying vec4 SunLight;
varying vec4 ShadowTexCoord;
varying float Fog;
void main ()
{
  vec4 total_light_1;
  vec4 final_col_2;
  vec4 tex1_col_3;
  vec4 tmpvar_4;
  vec4 tmpvar_5;
  tmpvar_5 = texture2D (diffuse_texture, Tex0);
  tex1_col_3.w = tmpvar_5.w;
  vec4 tmpvar_6;
  tmpvar_6 = texture2D (diffuse_texture_2, Tex0);
  tex1_col_3.xyz = pow (tmpvar_5.xyz, vec3(2.2, 2.2, 2.2));
  final_col_2 = (tex1_col_3 * vMaterialColor);
  float tmpvar_7;
  tmpvar_7 = clamp (((
    (2.0 * vMaterialColor2.w)
   + tmpvar_6.w) - 1.9), 0.0, 1.0);
  final_col_2.xyz = (final_col_2.xyz * (1.0 - tmpvar_7));
  final_col_2.xyz = (final_col_2.xyz + (tmpvar_6.xyz * tmpvar_7));
  total_light_1 = Color;
  float sun_amount_8;
  sun_amount_8 = 0.0;
  vec2 tmpvar_9;
  tmpvar_9 = fract((ShadowTexCoord.xy * fShadowMapSize));
  vec4 tmpvar_10;
  tmpvar_10 = texture2D (shadowmap_texture, ShadowTexCoord.xy);
  float tmpvar_11;
  if ((tmpvar_10.x < ShadowTexCoord.z)) {
    tmpvar_11 = 0.0;
  } else {
    tmpvar_11 = 1.0;
  };
  vec2 tmpvar_12;
  tmpvar_12.y = 0.0;
  tmpvar_12.x = fShadowMapNextPixel;
  vec4 tmpvar_13;
  tmpvar_13 = texture2D (shadowmap_texture, (ShadowTexCoord.xy + tmpvar_12));
  float tmpvar_14;
  if ((tmpvar_13.x < ShadowTexCoord.z)) {
    tmpvar_14 = 0.0;
  } else {
    tmpvar_14 = 1.0;
  };
  vec2 tmpvar_15;
  tmpvar_15.x = 0.0;
  tmpvar_15.y = fShadowMapNextPixel;
  vec4 tmpvar_16;
  tmpvar_16 = texture2D (shadowmap_texture, (ShadowTexCoord.xy + tmpvar_15));
  float tmpvar_17;
  if ((tmpvar_16.x < ShadowTexCoord.z)) {
    tmpvar_17 = 0.0;
  } else {
    tmpvar_17 = 1.0;
  };
  vec4 tmpvar_18;
  tmpvar_18 = texture2D (shadowmap_texture, (ShadowTexCoord.xy + vec2(fShadowMapNextPixel)));
  float tmpvar_19;
  if ((tmpvar_18.x < ShadowTexCoord.z)) {
    tmpvar_19 = 0.0;
  } else {
    tmpvar_19 = 1.0;
  };
  sun_amount_8 = clamp (mix (mix (tmpvar_11, tmpvar_14, tmpvar_9.x), mix (tmpvar_17, tmpvar_19, tmpvar_9.x), tmpvar_9.y), 0.0, 1.0);
  total_light_1.xyz = (Color.xyz + (SunLight.xyz * sun_amount_8));
  tmpvar_4 = (final_col_2 * total_light_1);
  if (((tmpvar_4.w - alpha_test_val) < 0.0)) {
    discard;
  };
  tmpvar_4.xyz = pow (tmpvar_4.xyz, output_gamma_inv.xyz);
  tmpvar_4.xyz = mix (vFogColor.xyz, tmpvar_4.xyz, Fog);
  gl_FragColor = tmpvar_4;
}

