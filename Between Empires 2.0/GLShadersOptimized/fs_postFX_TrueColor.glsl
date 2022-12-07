uniform vec4 color_value;
varying vec2 Tex;
void main ()
{
  vec4 ret_1;
  ret_1.xyz = color_value.xyz;
  vec2 pos_2;
  pos_2 = (((Tex * vec2(2.0, 2.0)) - vec2(1.0, 1.0)) * 0.5);
  float tmpvar_3;
  tmpvar_3 = clamp (((
    dot (pos_2, pos_2)
   - 0.015) / 1.235), 0.0, 1.0);
  ret_1.w = clamp ((color_value.w + (color_value.w * 
    (1.0 - (1.0 - (tmpvar_3 * (tmpvar_3 * 
      (3.0 - (2.0 * tmpvar_3))
    ))))
  )), 0.0, 1.0);
  gl_FragColor = ret_1;
}

