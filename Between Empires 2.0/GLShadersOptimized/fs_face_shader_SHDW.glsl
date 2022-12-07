uniform sampler2D diffuse_texture;
uniform sampler2D diffuse_texture_2;
uniform sampler2D shadowmap_texture;
uniform vec4 vMaterialColor;
uniform vec4 vFogColor;
uniform vec4 output_gamma_inv;
uniform float fShadowMapNextPixel;
uniform float fShadowMapSize;
varying vec4 Color;
varying vec2 Tex0;
varying vec4 SunLight;
varying vec4 ShadowTexCoord;
varying float Fog;
void main ()
{
  vec4 tex_col_1;
  vec4 tmpvar_2;
  tex_col_1 = ((texture2D (diffuse_texture_2, Tex0) * Color.w) + (texture2D (diffuse_texture, Tex0) * (1.0 - Color.w)));
  tex_col_1.xyz = pow (tex_col_1.xyz, vec3(2.2, 2.2, 2.2));
  float sun_amount_3;
  sun_amount_3 = 0.0;
  vec2 tmpvar_4;
  tmpvar_4 = fract((ShadowTexCoord.xy * fShadowMapSize));
  vec4 tmpvar_5;
  tmpvar_5 = texture2D (shadowmap_texture, ShadowTexCoord.xy);
  float tmpvar_6;
  if ((tmpvar_5.x < ShadowTexCoord.z)) {
    tmpvar_6 = 0.0;
  } else {
    tmpvar_6 = 1.0;
  };
  vec2 tmpvar_7;
  tmpvar_7.y = 0.0;
  tmpvar_7.x = fShadowMapNextPixel;
  vec4 tmpvar_8;
  tmpvar_8 = texture2D (shadowmap_texture, (ShadowTexCoord.xy + tmpvar_7));
  float tmpvar_9;
  if ((tmpvar_8.x < ShadowTexCoord.z)) {
    tmpvar_9 = 0.0;
  } else {
    tmpvar_9 = 1.0;
  };
  vec2 tmpvar_10;
  tmpvar_10.x = 0.0;
  tmpvar_10.y = fShadowMapNextPixel;
  vec4 tmpvar_11;
  tmpvar_11 = texture2D (shadowmap_texture, (ShadowTexCoord.xy + tmpvar_10));
  float tmpvar_12;
  if ((tmpvar_11.x < ShadowTexCoord.z)) {
    tmpvar_12 = 0.0;
  } else {
    tmpvar_12 = 1.0;
  };
  vec4 tmpvar_13;
  tmpvar_13 = texture2D (shadowmap_texture, (ShadowTexCoord.xy + vec2(fShadowMapNextPixel)));
  float tmpvar_14;
  if ((tmpvar_13.x < ShadowTexCoord.z)) {
    tmpvar_14 = 0.0;
  } else {
    tmpvar_14 = 1.0;
  };
  sun_amount_3 = clamp (mix (mix (tmpvar_6, tmpvar_9, tmpvar_4.x), mix (tmpvar_12, tmpvar_14, tmpvar_4.x), tmpvar_4.y), 0.0, 1.0);
  tmpvar_2 = (tex_col_1 * (Color + (SunLight * sun_amount_3)));
  tmpvar_2.xyz = pow (tmpvar_2.xyz, output_gamma_inv.xyz);
  tmpvar_2.w = vMaterialColor.w;
  tmpvar_2.xyz = mix (vFogColor.xyz, tmpvar_2.xyz, Fog);
  gl_FragColor = tmpvar_2;
}

