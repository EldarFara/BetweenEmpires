uniform vec4 output_gamma;
uniform vec4 output_gamma_inv;
uniform vec4 postfx_editor_vector[4];
uniform sampler2D postFX_sampler0;
uniform sampler2D postFX_sampler1;
varying vec2 Tex;
void main ()
{
  vec4 blur_1;
  vec4 color_2;
  vec4 scene_3;
  vec4 tmpvar_4;
  tmpvar_4 = texture2D (postFX_sampler0, Tex);
  scene_3.w = tmpvar_4.w;
  scene_3.xyz = pow (tmpvar_4.xyz, output_gamma.xyz);
  vec4 tmpvar_5;
  tmpvar_5 = texture2D (postFX_sampler1, Tex);
  blur_1.w = tmpvar_5.w;
  blur_1.xyz = pow (tmpvar_5.xyz, postfx_editor_vector[2].zzz);
  blur_1.xyz = (blur_1.xyz * postfx_editor_vector[1].x);
  color_2 = (scene_3 + (blur_1 * postfx_editor_vector[2].w));
  float tonemapOp_6;
  tonemapOp_6 = postfx_editor_vector[0].x;
  vec3 final_color_7;
  float tmpvar_8;
  tmpvar_8 = (0.5 * postfx_editor_vector[1].z);
  float tmpvar_9;
  tmpvar_9 = (10.2 * postfx_editor_vector[1].w);
  float tmpvar_10;
  tmpvar_10 = clamp (((0.85 / 
    (1e-05 + tmpvar_8)
  ) * postfx_editor_vector[1].y), 0.15, 3.0);
  vec3 tmpvar_11;
  tmpvar_11 = (color_2.xyz * tmpvar_10);
  if ((tonemapOp_6 < 1.0)) {
    final_color_7 = tmpvar_11;
  } else {
    if ((tonemapOp_6 < 2.0)) {
      final_color_7 = (1.0 - exp2(-(tmpvar_11)));
    } else {
      if ((tonemapOp_6 < 3.0)) {
        final_color_7 = (tmpvar_11 / (tmpvar_11 + 1.0));
      } else {
        float tmpvar_12;
        tmpvar_12 = ((tmpvar_10 / tmpvar_8) * max (tmpvar_11.x, max (tmpvar_11.y, tmpvar_11.z)));
        final_color_7 = (tmpvar_11 * ((tmpvar_12 * 
          (1.0 + (tmpvar_12 / tmpvar_9))
        ) / (1.0 + tmpvar_12)));
      };
    };
  };
  color_2.xyz = pow (final_color_7, output_gamma_inv.xyz);
  gl_FragColor = color_2;
}

