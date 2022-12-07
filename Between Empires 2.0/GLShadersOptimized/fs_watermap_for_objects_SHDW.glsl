uniform sampler2D specular_texture;
uniform sampler2D env_texture;
uniform sampler2D shadowmap_texture;
uniform vec4 vFogColor;
uniform vec4 output_gamma_inv;
uniform float fShadowMapNextPixel;
uniform float fShadowMapSize;
varying float Fog;
varying vec4 Color;
varying vec4 Tex0;
varying vec4 SunLight;
varying vec4 ShadowTexCoord;
varying vec3 vSpecular;
void main ()
{
  vec4 tmpvar_1;
  tmpvar_1 = Color;
  vec4 tmpvar_2;
  vec4 tmpvar_3;
  tmpvar_3 = texture2D (specular_texture, Tex0.xy);
  float tmpvar_4;
  tmpvar_4 = (dot (tmpvar_3.wy, tmpvar_3.wy) * 0.5);
  vec3 tmpvar_5;
  tmpvar_5 = (tmpvar_4 * vSpecular);
  vec4 tmpvar_6;
  tmpvar_6 = clamp (((
    (clamp ((Color + 0.5), 0.0, 1.0) * tmpvar_4)
   * 2.0) + 0.25), 0.0, 1.0);
  vec4 tmpvar_7;
  tmpvar_7 = texture2D (env_texture, Tex0.zw);
  vec4 vcol_8;
  float sun_amount_9;
  sun_amount_9 = 0.0;
  vec2 tmpvar_10;
  tmpvar_10 = fract((ShadowTexCoord.xy * fShadowMapSize));
  vec4 tmpvar_11;
  tmpvar_11 = texture2D (shadowmap_texture, ShadowTexCoord.xy);
  float tmpvar_12;
  if ((tmpvar_11.x < ShadowTexCoord.z)) {
    tmpvar_12 = 0.0;
  } else {
    tmpvar_12 = 1.0;
  };
  vec2 tmpvar_13;
  tmpvar_13.y = 0.0;
  tmpvar_13.x = fShadowMapNextPixel;
  vec4 tmpvar_14;
  tmpvar_14 = texture2D (shadowmap_texture, (ShadowTexCoord.xy + tmpvar_13));
  float tmpvar_15;
  if ((tmpvar_14.x < ShadowTexCoord.z)) {
    tmpvar_15 = 0.0;
  } else {
    tmpvar_15 = 1.0;
  };
  vec2 tmpvar_16;
  tmpvar_16.x = 0.0;
  tmpvar_16.y = fShadowMapNextPixel;
  vec4 tmpvar_17;
  tmpvar_17 = texture2D (shadowmap_texture, (ShadowTexCoord.xy + tmpvar_16));
  float tmpvar_18;
  if ((tmpvar_17.x < ShadowTexCoord.z)) {
    tmpvar_18 = 0.0;
  } else {
    tmpvar_18 = 1.0;
  };
  vec4 tmpvar_19;
  tmpvar_19 = texture2D (shadowmap_texture, (ShadowTexCoord.xy + vec2(fShadowMapNextPixel)));
  float tmpvar_20;
  if ((tmpvar_19.x < ShadowTexCoord.z)) {
    tmpvar_20 = 0.0;
  } else {
    tmpvar_20 = 1.0;
  };
  sun_amount_9 = clamp (mix (mix (tmpvar_12, tmpvar_15, tmpvar_10.x), mix (tmpvar_18, tmpvar_20, tmpvar_10.x), tmpvar_10.y), 0.0, 1.0);
  vcol_8.w = tmpvar_1.w;
  vcol_8.xyz = (Color.xyz + ((SunLight.xyz + tmpvar_5) * sun_amount_9));
  tmpvar_2 = (tmpvar_6 * vcol_8);
  tmpvar_2.xyz = (tmpvar_2.xyz + ((
    (SunLight.xyz * sun_amount_9)
   + 0.3) * (
    (Color.xyz * tmpvar_7.xyz)
   * tmpvar_4)));
  tmpvar_2.xyz = pow (tmpvar_2.xyz, output_gamma_inv.xyz);
  tmpvar_2.xyz = mix (vFogColor.xyz, tmpvar_2.xyz, Fog);
  tmpvar_2.w = 1.0;
  gl_FragColor = tmpvar_2;
}

