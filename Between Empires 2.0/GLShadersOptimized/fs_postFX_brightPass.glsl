uniform vec4 postfx_editor_vector[4];
uniform sampler2D postFX_sampler0;
varying vec2 Tex;
void main ()
{
  vec3 color_1;
  color_1 = (texture2D (postFX_sampler0, Tex).xyz * postfx_editor_vector[1].x);
  color_1 = max (vec3(0.0, 0.0, 0.0), (color_1 - postfx_editor_vector[2].xxx));
  color_1 = pow (color_1, postfx_editor_vector[2].yyy);
  float tmpvar_2;
  tmpvar_2 = dot (color_1, color_1);
  if ((tmpvar_2 > 1000.0)) {
    color_1 = vec3(0.0, 0.0, 0.0);
  };
  color_1 = (color_1 * (1.0/(postfx_editor_vector[1].x)));
  vec4 tmpvar_3;
  tmpvar_3.w = 1.0;
  tmpvar_3.xyz = color_1;
  gl_FragColor = tmpvar_3;
}

