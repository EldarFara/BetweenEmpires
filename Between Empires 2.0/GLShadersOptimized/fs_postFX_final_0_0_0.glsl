uniform vec4 output_gamma;
uniform vec4 output_gamma_inv;
uniform sampler2D postFX_sampler0;
varying vec2 Tex;
void main ()
{
  vec4 color_1;
  vec4 scene_2;
  vec4 tmpvar_3;
  tmpvar_3 = texture2D (postFX_sampler0, Tex);
  scene_2.w = tmpvar_3.w;
  scene_2.xyz = pow (tmpvar_3.xyz, output_gamma.xyz);
  color_1.w = scene_2.w;
  color_1.xyz = pow (scene_2.xyz, output_gamma_inv.xyz);
  gl_FragColor = color_1;
}

