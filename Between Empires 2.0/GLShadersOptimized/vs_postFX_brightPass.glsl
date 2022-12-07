attribute vec3 inPosition;
varying vec2 Tex;
void main ()
{
  vec4 tmpvar_1;
  tmpvar_1.w = 1.0;
  tmpvar_1.xyz = inPosition;
  gl_Position = tmpvar_1;
  Tex = ((inPosition.xy * 0.5) + 0.5);
}

