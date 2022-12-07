uniform vec4 output_gamma;
uniform vec4 output_gamma_inv;
uniform sampler2D postFX_sampler0;
uniform sampler2D postFX_sampler3;
uniform sampler2D postFX_sampler4;
uniform float g_DOF_Focus;
uniform float g_DOF_Range;
varying vec2 Tex;
void main ()
{
  vec4 color_1;
  vec4 scene_2;
  vec4 tmpvar_3;
  tmpvar_3 = texture2D (postFX_sampler0, Tex);
  scene_2.w = tmpvar_3.w;
  scene_2.xyz = pow (tmpvar_3.xyz, output_gamma.xyz);
  vec4 dofColor_4;
  vec2 tmpvar_5;
  tmpvar_5.x = ((Tex.x * 2.0) - 1.0);
  tmpvar_5.y = (Tex.y - 0.6);
  float tmpvar_6;
  tmpvar_6 = clamp (((
    dot (tmpvar_5, tmpvar_5)
   - 0.015) / 0.485), 0.0, 1.0);
  vec4 tmpvar_7;
  tmpvar_7 = texture2D (postFX_sampler3, Tex);
  dofColor_4.w = tmpvar_7.w;
  dofColor_4.xyz = pow (tmpvar_7.xyz, output_gamma.xyz);
  scene_2 = mix (scene_2, dofColor_4, (min (
    clamp ((g_DOF_Range * abs((g_DOF_Focus - texture2D (postFX_sampler4, Tex).x))), 0.0, 1.0)
  , 0.62) * (1.0 - 
    (1.0 - (tmpvar_6 * (tmpvar_6 * (3.0 - 
      (2.0 * tmpvar_6)
    ))))
  )));
  color_1.w = scene_2.w;
  color_1.xyz = pow (scene_2.xyz, output_gamma_inv.xyz);
  gl_FragColor = color_1;
}

