uniform sampler2D diffuse_texture;
uniform sampler2D diffuse_texture_2;
uniform sampler2D shadowmap_texture;
uniform vec4 vLightDiffuse[4];
uniform vec4 vMaterialColor;
uniform vec4 vSunDir;
uniform vec4 vSunColor;
uniform vec4 vAmbientColor;
uniform vec4 vFogColor;
uniform vec4 output_gamma_inv;
uniform int iLightIndices[4];
uniform float fShadowMapNextPixel;
uniform float fShadowMapSize;
varying float Fog;
varying vec4 VertexColor;
varying vec2 Tex0;
varying vec3 SunLightDir;
varying vec4 PointLightDir;
varying vec4 ShadowTexCoord;
void main ()
{
  vec4 tex_col_1;
  vec4 total_light_2;
  vec4 tmpvar_3;
  total_light_2 = vAmbientColor;
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
  float tmpvar_16;
  tmpvar_16 = dot (-(vSunDir.xyz), SunLightDir);
  vec4 tmpvar_17;
  tmpvar_17.w = 1.0;
  tmpvar_17.xyz = vSunColor.xyz;
  total_light_2 = (vAmbientColor + ((
    clamp (max ((0.2 * (tmpvar_16 + 0.9)), tmpvar_16), 0.0, 1.0)
   * sun_amount_4) * tmpvar_17));
  int tmpvar_18;
  tmpvar_18 = iLightIndices[0];
  float tmpvar_19;
  tmpvar_19 = dot (PointLightDir.xyz, SunLightDir);
  total_light_2.xyz = (total_light_2.xyz + ((
    (PointLightDir.w * 0.9)
   * 
    clamp (max ((0.2 * (tmpvar_19 + 0.9)), tmpvar_19), 0.0, 1.0)
  ) * vLightDiffuse[tmpvar_18].xyz));
  tmpvar_3.xyz = total_light_2.xyz;
  vec4 tmpvar_20;
  tmpvar_20 = mix (texture2D (diffuse_texture, Tex0), texture2D (diffuse_texture_2, Tex0), VertexColor.w);
  tex_col_1.w = tmpvar_20.w;
  tex_col_1.xyz = pow (tmpvar_20.xyz, vec3(2.2, 2.2, 2.2));
  tmpvar_3 = (tmpvar_3 * tex_col_1);
  tmpvar_3.xyz = (tmpvar_3.xyz * (VertexColor.xyz * vMaterialColor.xyz));
  tmpvar_3.xyz = clamp (pow (tmpvar_3.xyz, output_gamma_inv.xyz), 0.0, 1.0);
  tmpvar_3.w = vMaterialColor.w;
  tmpvar_3.xyz = mix (vFogColor.xyz, tmpvar_3.xyz, Fog);
  gl_FragColor = tmpvar_3;
}

