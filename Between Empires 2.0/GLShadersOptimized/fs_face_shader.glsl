uniform sampler2D diffuse_texture;
uniform sampler2D diffuse_texture_2;
uniform vec4 vMaterialColor;
uniform vec4 vFogColor;
uniform vec4 output_gamma_inv;
varying vec4 Color;
varying vec2 Tex0;
varying vec4 SunLight;
varying float Fog;
void main ()
{
  vec4 tex_col_1;
  vec4 tmpvar_2;
  tex_col_1 = ((texture2D (diffuse_texture_2, Tex0) * Color.w) + (texture2D (diffuse_texture, Tex0) * (1.0 - Color.w)));
  tex_col_1.xyz = pow (tex_col_1.xyz, vec3(2.2, 2.2, 2.2));
  tmpvar_2 = (tex_col_1 * (Color + SunLight));
  tmpvar_2.xyz = pow (tmpvar_2.xyz, output_gamma_inv.xyz);
  tmpvar_2.w = vMaterialColor.w;
  tmpvar_2.xyz = mix (vFogColor.xyz, tmpvar_2.xyz, Fog);
  gl_FragColor = tmpvar_2;
}

