uniform vec4 postfx_editor_vector[4];
uniform sampler2D postFX_sampler0;
uniform sampler2D postFX_sampler4;
varying vec2 Tex;
void main ()
{
  vec3 color_1;
  color_1 = (texture2D (postFX_sampler0, Tex).xyz * postfx_editor_vector[1].x);
  color_1 = (color_1 * clamp ((
    (0.85 + ((0.85 / (1e-05 + texture2D (postFX_sampler4, vec2(0.5, 0.5)).x)) * 0.15))
   * postfx_editor_vector[1].y), 0.15, 3.0));
  color_1 = clamp ((color_1 - postfx_editor_vector[2].xxx), 0.0, 100.0);
  float tmpvar_2;
  tmpvar_2 = (dot (color_1, vec3(0.5, 0.5, 0.5)) + 1e-05);
  color_1 = (color_1 * (pow (tmpvar_2, postfx_editor_vector[2].y) / tmpvar_2));
  float tmpvar_3;
  tmpvar_3 = dot (color_1, color_1);
  if ((tmpvar_3 > 1000.0)) {
    color_1 = vec3(0.0, 0.0, 0.0);
  };
  color_1 = (color_1 * (1.0/(postfx_editor_vector[1].x)));
  vec4 tmpvar_4;
  tmpvar_4.w = 1.0;
  tmpvar_4.xyz = color_1;
  gl_FragColor = tmpvar_4;
}

