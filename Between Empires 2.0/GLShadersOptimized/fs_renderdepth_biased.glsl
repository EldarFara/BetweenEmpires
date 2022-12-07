uniform sampler2D diffuse_texture;
varying vec2 outTexCoord;
varying float outDepth;
void main ()
{
  vec4 finalColor_1;
  finalColor_1.w = texture2D (diffuse_texture, outTexCoord).w;
  finalColor_1.w = (finalColor_1.w - 0.5);
  if ((finalColor_1.w < 0.0)) {
    discard;
  };
  finalColor_1 = vec4(outDepth);
  gl_FragColor = finalColor_1;
}

