uniform vec4 output_gamma_inv;
uniform bool showing_ranged_data;
uniform vec4 postfx_editor_vector[4];
uniform sampler2D postFX_sampler0;
varying vec2 Tex;
void main ()
{
  vec4 color_1;
  vec4 tmpvar_2;
  tmpvar_2 = texture2D (postFX_sampler0, Tex);
  color_1 = tmpvar_2;
  if (showing_ranged_data) {
    color_1.xyz = (tmpvar_2.xyz * postfx_editor_vector[1].x);
    color_1.xyz = pow (color_1.xyz, output_gamma_inv.xyz);
  };
  gl_FragColor = color_1;
}

