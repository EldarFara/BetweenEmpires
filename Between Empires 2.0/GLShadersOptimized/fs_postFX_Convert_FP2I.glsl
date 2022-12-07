uniform vec4 postfx_editor_vector[4];
uniform sampler2D postFX_sampler4;
varying vec2 texCoord0;
varying vec2 texCoord1;
varying vec2 texCoord2;
varying vec2 texCoord3;
void main ()
{
  vec3 rt_1;
  rt_1 = (texture2D (postFX_sampler4, texCoord0).xyz + texture2D (postFX_sampler4, texCoord1).xyz);
  rt_1 = (rt_1 + texture2D (postFX_sampler4, texCoord2).xyz);
  rt_1 = (rt_1 + texture2D (postFX_sampler4, texCoord3).xyz);
  rt_1 = (rt_1 * 0.25);
  rt_1 = (rt_1 * (1.0/(postfx_editor_vector[1].x)));
  vec4 tmpvar_2;
  tmpvar_2.w = 1.0;
  tmpvar_2.xyz = rt_1;
  gl_FragColor = tmpvar_2;
}

