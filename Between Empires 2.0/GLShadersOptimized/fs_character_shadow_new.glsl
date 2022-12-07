uniform sampler2D diffuse_texture;
uniform vec4 vFogColor;
varying float Fog;
varying vec2 Tex0;
varying vec4 Color;
void main ()
{
  vec4 tmpvar_1;
  tmpvar_1.w = (texture2D (diffuse_texture, Tex0).x * Color.w);
  tmpvar_1.xyz = mix (vFogColor.xyz, Color.xyz, Fog);
  gl_FragColor = tmpvar_1;
}

