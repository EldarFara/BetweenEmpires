uniform sampler2D diffuse_texture;
uniform sampler2D shadowmap_texture;
uniform vec4 vFogColor;
uniform vec4 output_gamma_inv;
uniform float fShadowMapNextPixel;
uniform float fShadowMapSize;
varying float Fog;
varying vec4 Color;
varying vec3 Tex0;
varying vec4 SunLight;
varying vec4 ShadowTexCoord;
varying vec3 ViewDir;
varying vec3 WorldNormal;
void main ()
{
  vec4 tex_col_1;
  vec4 tmpvar_2;
  vec4 tmpvar_3;
  tmpvar_3 = texture2D (diffuse_texture, Tex0.xy);
  tex_col_1.w = tmpvar_3.w;
  tex_col_1.xyz = pow (tmpvar_3.xyz, vec3(2.2, 2.2, 2.2));
  tex_col_1.xyz = (tex_col_1.xyz + clamp ((
    (Tex0.z * tmpvar_3.w)
   - 1.5), 0.0, 1.0));
  tex_col_1.w = 1.0;
  float sun_amount_4;
  sun_amount_4 = 0.0;
  vec2 tmpvar_5;
  tmpvar_5 = fract((ShadowTexCoord.xy * fShadowMapSize));
  vec4 tmpvar_6;
  tmpvar_6 = texture2D (shadowmap_texture, ShadowTexCoord.xy);
  float tmpvar_7;
  if ((tmpvar_6.x < ShadowTexCoord.z)) {
    tmpvar_7 = 0.0;
  } else {
    tmpvar_7 = 1.0;
  };
  vec2 tmpvar_8;
  tmpvar_8.y = 0.0;
  tmpvar_8.x = fShadowMapNextPixel;
  vec4 tmpvar_9;
  tmpvar_9 = texture2D (shadowmap_texture, (ShadowTexCoord.xy + tmpvar_8));
  float tmpvar_10;
  if ((tmpvar_9.x < ShadowTexCoord.z)) {
    tmpvar_10 = 0.0;
  } else {
    tmpvar_10 = 1.0;
  };
  vec2 tmpvar_11;
  tmpvar_11.x = 0.0;
  tmpvar_11.y = fShadowMapNextPixel;
  vec4 tmpvar_12;
  tmpvar_12 = texture2D (shadowmap_texture, (ShadowTexCoord.xy + tmpvar_11));
  float tmpvar_13;
  if ((tmpvar_12.x < ShadowTexCoord.z)) {
    tmpvar_13 = 0.0;
  } else {
    tmpvar_13 = 1.0;
  };
  vec4 tmpvar_14;
  tmpvar_14 = texture2D (shadowmap_texture, (ShadowTexCoord.xy + vec2(fShadowMapNextPixel)));
  float tmpvar_15;
  if ((tmpvar_14.x < ShadowTexCoord.z)) {
    tmpvar_15 = 0.0;
  } else {
    tmpvar_15 = 1.0;
  };
  sun_amount_4 = clamp (mix (mix (tmpvar_7, tmpvar_10, tmpvar_5.x), mix (tmpvar_13, tmpvar_15, tmpvar_5.x), tmpvar_5.y), 0.0, 1.0);
  tmpvar_2.xyz = (clamp (tex_col_1, 0.0, 1.0) * (Color + (SunLight * sun_amount_4))).xyz;
  tmpvar_2.w = Color.w;
  tmpvar_2.xyz = (tmpvar_2.xyz * max (0.6, (
    (1.0 - clamp (dot (ViewDir, WorldNormal), 0.0, 1.0))
   + 0.1)));
  tmpvar_2.xyz = pow (tmpvar_2.xyz, output_gamma_inv.xyz);
  tmpvar_2.xyz = mix (vFogColor.xyz, tmpvar_2.xyz, Fog);
  gl_FragColor = tmpvar_2;
}

