uniform sampler2D diffuse_texture;
uniform sampler2D diffuse_texture_2;
uniform vec4 vMaterialColor;
uniform vec4 vMaterialColor2;
uniform vec4 vFogColor;
uniform vec4 output_gamma_inv;
varying vec4 Color;
varying vec2 Tex0;
varying vec4 SunLight;
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
  total_light_1.w = Color.w;
  total_light_1.xyz = (Color.xyz + SunLight.xyz);
  tmpvar_4 = (final_col_2 * total_light_1);
  tmpvar_4.xyz = pow (tmpvar_4.xyz, output_gamma_inv.xyz);
  tmpvar_4.xyz = mix (vFogColor.xyz, tmpvar_4.xyz, Fog);
  gl_FragColor = tmpvar_4;
}

