uniform sampler2D diffuse_texture;
uniform sampler2D diffuse_texture_2;
uniform sampler2D shadowmap_texture;
uniform vec4 vMaterialColor;
uniform vec4 vMaterialColor2;
uniform vec4 vSunDir;
uniform vec4 vSunColor;
uniform vec4 vAmbientColor;
uniform vec4 vFogColor;
uniform vec4 output_gamma_inv;
uniform float fShadowMapNextPixel;
uniform float fShadowMapSize;
varying vec2 Tex0;
varying vec4 VertexLighting;
varying vec3 viewVec;
varying vec3 normal;
varying vec3 tangent;
varying vec4 VertexColor;
varying vec4 ShadowTexCoord;
varying float Fog;
void main ()
{
  vec4 total_light_1;
  vec4 final_col_2;
  vec4 tex1_col_3;
  vec4 tmpvar_4;
  vec3 tmpvar_5;
  tmpvar_5 = -(vSunDir.xyz);
  vec3 tmpvar_6;
  tmpvar_6 = (((vMaterialColor.xyz * vSunColor.xyz) * VertexColor.xyz) * clamp ((
    (0.75 * dot (normal, tmpvar_5))
   + 0.25), 0.0, 1.0));
  vec4 tmpvar_7;
  tmpvar_7 = texture2D (diffuse_texture, Tex0);
  tex1_col_3.w = tmpvar_7.w;
  tex1_col_3.xyz = pow (tmpvar_7.xyz, vec3(2.2, 2.2, 2.2));
  final_col_2.w = tex1_col_3.w;
  final_col_2.xyz = (tex1_col_3.xyz * vMaterialColor.xyz);
  vec4 tmpvar_8;
  tmpvar_8 = texture2D (diffuse_texture_2, Tex0);
  float tmpvar_9;
  tmpvar_9 = clamp (((
    (2.0 * vMaterialColor2.w)
   + tmpvar_8.w) - 1.9), 0.0, 1.0);
  final_col_2.xyz = (final_col_2.xyz * (1.0 - tmpvar_9));
  final_col_2.xyz = (final_col_2.xyz + (tmpvar_8.xyz * tmpvar_9));
  float sun_amount_10;
  sun_amount_10 = 0.0;
  vec2 tmpvar_11;
  tmpvar_11 = fract((ShadowTexCoord.xy * fShadowMapSize));
  vec4 tmpvar_12;
  tmpvar_12 = texture2D (shadowmap_texture, ShadowTexCoord.xy);
  float tmpvar_13;
  if ((tmpvar_12.x < ShadowTexCoord.z)) {
    tmpvar_13 = 0.0;
  } else {
    tmpvar_13 = 1.0;
  };
  vec2 tmpvar_14;
  tmpvar_14.y = 0.0;
  tmpvar_14.x = fShadowMapNextPixel;
  vec4 tmpvar_15;
  tmpvar_15 = texture2D (shadowmap_texture, (ShadowTexCoord.xy + tmpvar_14));
  float tmpvar_16;
  if ((tmpvar_15.x < ShadowTexCoord.z)) {
    tmpvar_16 = 0.0;
  } else {
    tmpvar_16 = 1.0;
  };
  vec2 tmpvar_17;
  tmpvar_17.x = 0.0;
  tmpvar_17.y = fShadowMapNextPixel;
  vec4 tmpvar_18;
  tmpvar_18 = texture2D (shadowmap_texture, (ShadowTexCoord.xy + tmpvar_17));
  float tmpvar_19;
  if ((tmpvar_18.x < ShadowTexCoord.z)) {
    tmpvar_19 = 0.0;
  } else {
    tmpvar_19 = 1.0;
  };
  vec4 tmpvar_20;
  tmpvar_20 = texture2D (shadowmap_texture, (ShadowTexCoord.xy + vec2(fShadowMapNextPixel)));
  float tmpvar_21;
  if ((tmpvar_20.x < ShadowTexCoord.z)) {
    tmpvar_21 = 0.0;
  } else {
    tmpvar_21 = 1.0;
  };
  sun_amount_10 = clamp (mix (mix (tmpvar_13, tmpvar_16, tmpvar_11.x), mix (tmpvar_19, tmpvar_21, tmpvar_11.x), tmpvar_11.y), 0.0, 1.0);
  vec4 tmpvar_22;
  tmpvar_22 = texture2D (diffuse_texture_2, Tex0);
  vec3 tmpvar_23;
  tmpvar_23 = normalize((tmpvar_5 + viewVec));
  float tmpvar_24;
  tmpvar_24 = dot (normalize((tangent + 
    ((-0.362 + tmpvar_22.w) * normal)
  )), tmpvar_23);
  float tmpvar_25;
  tmpvar_25 = dot (normalize((tangent + 
    ((-0.246 + tmpvar_22.w) * normal)
  )), tmpvar_23);
  total_light_1.w = vAmbientColor.w;
  total_light_1.xyz = (vAmbientColor.xyz + ((tmpvar_6 + 
    ((((vSunColor.xyz * vec3(0.800118, 0.88902, 0.88902)) * pow (
      sqrt((1.0 - (tmpvar_24 * tmpvar_24)))
    , 179.2)) + ((
      (vSunColor.xyz * vec3(0.7326, 0.65934, 0.7326))
     * 
      pow (sqrt((1.0 - (tmpvar_25 * tmpvar_25))), 22.4)
    ) * texture2D (diffuse_texture_2, (Tex0 * 10.0)).w)) * clamp (((1.75 * 
      dot (normal, tmpvar_5)
    ) + 0.25), 0.0, 1.0))
  ) * sun_amount_10));
  total_light_1.xyz = (total_light_1.xyz + VertexLighting.xyz);
  tmpvar_4.xyz = (total_light_1.xyz * final_col_2.xyz);
  tmpvar_4.xyz = pow (tmpvar_4.xyz, output_gamma_inv.xyz);
  tmpvar_4.w = (tmpvar_7.w * vMaterialColor.w);
  tmpvar_4.xyz = mix (vFogColor.xyz, tmpvar_4.xyz, Fog);
  vec4 tmpvar_26;
  tmpvar_26 = clamp (tmpvar_4, 0.0, 1.0);
  tmpvar_4 = tmpvar_26;
  gl_FragColor = tmpvar_26;
}

