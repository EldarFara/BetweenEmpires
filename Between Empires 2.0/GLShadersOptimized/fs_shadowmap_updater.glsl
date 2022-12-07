uniform sampler2D postFX_sampler0;
uniform sampler2D postFX_sampler1;
varying vec2 Tex;
void main ()
{
  gl_FragColor = vec4(min (texture2D (postFX_sampler0, Tex).x, texture2D (postFX_sampler1, Tex).x));
}

