uniform sampler2D diffuse_texture;
varying vec4 outColor0;
varying vec2 outTexCoord;
void main ()
{
  vec4 finalColor_1;
  finalColor_1.xyz = outColor0.xyz;
  finalColor_1.w = (outColor0.w * texture2D (diffuse_texture, outTexCoord).w);
  gl_FragColor = finalColor_1;
}

