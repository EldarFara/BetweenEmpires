uniform sampler2D diffuse_texture;
varying vec4 outColor0;
varying vec2 outTexCoord;
void main ()
{
  vec4 finalColor_1;
  finalColor_1.xyz = (outColor0 * texture2D (diffuse_texture, outTexCoord)).xyz;
  finalColor_1.w = 1.0;
  gl_FragColor = finalColor_1;
}

