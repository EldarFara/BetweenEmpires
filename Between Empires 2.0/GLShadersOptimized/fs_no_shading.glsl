uniform sampler2D diffuse_texture;
varying vec4 outColor0;
varying vec2 outTexCoord;
void main ()
{
  gl_FragColor = (outColor0 * texture2D (diffuse_texture, outTexCoord));
}

