uniform vec4 output_gamma;
uniform vec4 output_gamma_inv;
uniform vec4 postfx_editor_vector[4];
uniform sampler2D postFX_sampler0;
uniform sampler2D postFX_sampler1;
uniform sampler2D postFX_sampler3;
uniform sampler2D postFX_sampler4;
uniform float g_DOF_Focus;
uniform float g_DOF_Range;
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
  vec4 dofColor_5;
  vec2 tmpvar_6;
  tmpvar_6.x = ((Tex.x * 2.0) - 1.0);
  tmpvar_6.y = (Tex.y - 0.6);
  float tmpvar_7;
  tmpvar_7 = clamp (((
    dot (tmpvar_6, tmpvar_6)
   - 0.015) / 0.485), 0.0, 1.0);
  dofColor_5 = (texture2D (postFX_sampler3, Tex) * postfx_editor_vector[1].x);
  dofColor_5.xyz = pow (dofColor_5.xyz, output_gamma.xyz);
  scene_3 = mix (scene_3, dofColor_5, (min (
    clamp ((g_DOF_Range * abs((g_DOF_Focus - texture2D (postFX_sampler4, Tex).x))), 0.0, 1.0)
  , 0.62) * (1.0 - 
    (1.0 - (tmpvar_7 * (tmpvar_7 * (3.0 - 
      (2.0 * tmpvar_7)
    ))))
  )));
  vec4 tmpvar_8;
  tmpvar_8 = texture2D (postFX_sampler1, Tex);
  blur_1.w = tmpvar_8.w;
  blur_1.xyz = pow (tmpvar_8.xyz, postfx_editor_vector[2].zzz);
  blur_1.xyz = (blur_1.xyz * postfx_editor_vector[1].x);
  color_2 = (scene_3 + (blur_1 * postfx_editor_vector[2].w));
  float tonemapOp_9;
  tonemapOp_9 = postfx_editor_vector[0].x;
  vec3 final_color_10;
  float tmpvar_11;
  tmpvar_11 = (0.5 * postfx_editor_vector[1].z);
  float tmpvar_12;
  tmpvar_12 = (10.2 * postfx_editor_vector[1].w);
  float tmpvar_13;
  tmpvar_13 = clamp (((0.85 / 
    (1e-05 + tmpvar_11)
  ) * postfx_editor_vector[1].y), 0.15, 3.0);
  vec3 tmpvar_14;
  tmpvar_14 = (color_2.xyz * tmpvar_13);
  if ((tonemapOp_9 < 1.0)) {
    final_color_10 = tmpvar_14;
  } else {
    if ((tonemapOp_9 < 2.0)) {
      final_color_10 = (1.0 - exp2(-(tmpvar_14)));
    } else {
      if ((tonemapOp_9 < 3.0)) {
        final_color_10 = (tmpvar_14 / (tmpvar_14 + 1.0));
      } else {
        float tmpvar_15;
        tmpvar_15 = ((tmpvar_13 / tmpvar_11) * max (tmpvar_14.x, max (tmpvar_14.y, tmpvar_14.z)));
        final_color_10 = (tmpvar_14 * ((tmpvar_15 * 
          (1.0 + (tmpvar_15 / tmpvar_12))
        ) / (1.0 + tmpvar_15)));
      };
    };
  };
  color_2.xyz = pow (final_color_10, output_gamma_inv.xyz);
  gl_FragColor = color_2;
}

