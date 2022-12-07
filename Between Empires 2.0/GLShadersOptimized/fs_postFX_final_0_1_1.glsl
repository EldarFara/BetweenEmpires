uniform vec4 output_gamma;
uniform vec4 output_gamma_inv;
uniform vec4 postfx_editor_vector[4];
uniform sampler2D postFX_sampler0;
uniform sampler2D postFX_sampler1;
uniform sampler2D postFX_sampler2;
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
  vec2 luminanceAvgMax_5;
  vec4 tmpvar_6;
  tmpvar_6 = texture2D (postFX_sampler1, Tex);
  blur_1.w = tmpvar_6.w;
  blur_1.xyz = pow (tmpvar_6.xyz, postfx_editor_vector[2].zzz);
  blur_1.xyz = (blur_1.xyz * postfx_editor_vector[1].x);
  luminanceAvgMax_5 = texture2D (postFX_sampler2, vec2(0.5, 0.5)).xy;
  color_2 = (scene_3 + (blur_1 * postfx_editor_vector[2].w));
  float tonemapOp_7;
  tonemapOp_7 = postfx_editor_vector[0].x;
  vec3 final_color_8;
  float tmpvar_9;
  tmpvar_9 = (luminanceAvgMax_5.x * postfx_editor_vector[1].z);
  float tmpvar_10;
  tmpvar_10 = (luminanceAvgMax_5.y * postfx_editor_vector[1].w);
  float tmpvar_11;
  tmpvar_11 = clamp (((0.85 / 
    (1e-05 + tmpvar_9)
  ) * postfx_editor_vector[1].y), 0.15, 3.0);
  vec3 tmpvar_12;
  tmpvar_12 = (color_2.xyz * tmpvar_11);
  if ((tonemapOp_7 < 1.0)) {
    final_color_8 = tmpvar_12;
  } else {
    if ((tonemapOp_7 < 2.0)) {
      final_color_8 = (1.0 - exp2(-(tmpvar_12)));
    } else {
      if ((tonemapOp_7 < 3.0)) {
        final_color_8 = (tmpvar_12 / (tmpvar_12 + 1.0));
      } else {
        float tmpvar_13;
        tmpvar_13 = ((tmpvar_11 / tmpvar_9) * max (tmpvar_12.x, max (tmpvar_12.y, tmpvar_12.z)));
        final_color_8 = (tmpvar_12 * ((tmpvar_13 * 
          (1.0 + (tmpvar_13 / tmpvar_10))
        ) / (1.0 + tmpvar_13)));
      };
    };
  };
  color_2.xyz = pow (final_color_8, output_gamma_inv.xyz);
  gl_FragColor = color_2;
}

