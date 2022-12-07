uniform sampler2D diffuse_texture;
uniform sampler2D shadowmap_texture;
uniform vec4 vMaterialColor;
uniform vec4 vSunDir;
uniform vec4 vSunColor;
uniform vec4 vAmbientColor;
uniform vec4 vGroundAmbientColor;
uniform vec4 vFogColor;
uniform vec4 output_gamma_inv;
uniform float alpha_test_val;
uniform float fShadowMapNextPixel;
uniform float fShadowMapSize;
varying float Fog;
varying vec4 VertexColor;
varying vec3 VertexLighting;
varying vec2 Tex0;
varying vec3 SunLightDir;
varying vec4 ShadowTexCoord;
void main ()
{
  vec4 tex_col_1;
  vec4 total_light_2;
  vec4 tmpvar_3;
  tmpvar_3.w = 1.0;
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
  vec4 ambientTerm_16;
  ambientTerm_16 = mix ((vGroundAmbientColor * sun_amount_4), vAmbientColor, ((SunLightDir.z + 1.0) * 0.5));
  total_light_2.w = ambientTerm_16.w;
  total_light_2.xyz = (ambientTerm_16.xyz + ((vec3(
    clamp (dot (-(vSunDir.xyz), SunLightDir), 0.0, 1.0)
  ) * sun_amount_4) * vSunColor.xyz));
  total_light_2.xyz = (total_light_2.xyz + VertexLighting);
  tmpvar_3.xyz = (total_light_2.xyz * vMaterialColor.xyz);
  vec4 tmpvar_17;
  tmpvar_17 = texture2D (diffuse_texture, Tex0);
  tex_col_1.w = tmpvar_17.w;
  if (((tmpvar_17.w - alpha_test_val) < 0.0)) {
    discard;
  };
  tex_col_1.xyz = pow (tmpvar_17.xyz, vec3(2.2, 2.2, 2.2));
  tmpvar_3.xyz = (tmpvar_3.xyz * tex_col_1.xyz);
  tmpvar_3.xyz = (tmpvar_3.xyz * VertexColor.xyz);
  tmpvar_3.xyz = pow (tmpvar_3.xyz, output_gamma_inv.xyz);
  tmpvar_3.xyz = mix (vFogColor.xyz, tmpvar_3.xyz, Fog);
  tmpvar_3.w = (VertexColor.w * tmpvar_17.w);
  if (((tmpvar_3.w - alpha_test_val) < 0.0)) {
    discard;
  };
  gl_FragColor = tmpvar_3;
}

