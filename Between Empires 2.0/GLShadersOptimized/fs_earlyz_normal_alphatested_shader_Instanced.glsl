uniform sampler2D diffuse_texture;
varying vec2 TC;
varying float Depth;
void main ()
{
  vec4 tmpvar_1;
  tmpvar_1 = texture2D (diffuse_texture, TC);
  if (((tmpvar_1.w - 0.03137255) < 0.0)) {
    discard;
  };
  gl_FragColor = vec4(Depth);
}

