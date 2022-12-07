uniform sampler2D diffuse_texture;
uniform vec4 vFogColor;
uniform vec4 output_gamma_inv;
uniform float alpha_test_val;
varying float Fog;
varying vec4 Color;
varying vec2 Tex0;
varying float Map;
void main ()
{
  vec4 tex_col_1;
  vec4 tmpvar_2;
  vec4 tmpvar_3;
  tmpvar_3 = texture2D (diffuse_texture, Tex0);
  tex_col_1.w = tmpvar_3.w;
  tex_col_1.xyz = pow (tmpvar_3.xyz, vec3(2.2, 2.2, 2.2));
  tmpvar_2 = (Color * tex_col_1);
  float tmpvar_4;
  tmpvar_4 = clamp ((Map / 100.0), 0.0, 1.0);
  if ((tmpvar_4 > 0.4)) {
    float alphaval_5;
    float tmpvar_6;
    tmpvar_6 = (tmpvar_4 - 0.15);
    alphaval_5 = (tmpvar_6 * (1.0 + tmpvar_6));
    float tmpvar_7;
    tmpvar_7 = min (alphaval_5, 0.85);
    alphaval_5 = tmpvar_7;
    tmpvar_2.w = (tmpvar_2.w * clamp (tmpvar_7, 0.0, 1.0));
  } else {
    tmpvar_2.w = 0.0;
  };
  tmpvar_2.xyz = pow (tmpvar_2.xyz, output_gamma_inv.xyz);
  if (((tmpvar_2.w - (alpha_test_val * 1.25)) < 0.0)) {
    discard;
  };
  tmpvar_2.xyz = mix (vFogColor.xyz, tmpvar_2.xyz, Fog);
  gl_FragColor = tmpvar_2;
}

