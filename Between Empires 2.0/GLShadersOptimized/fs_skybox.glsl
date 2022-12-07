uniform sampler2D diffuse_texture;
uniform vec4 vFogColor;
varying float Fog;
varying vec4 Color;
varying vec2 Tex0;
void main ()
{
  vec4 tmpvar_1;
  tmpvar_1 = (Color * texture2D (diffuse_texture, Tex0));
  tmpvar_1.xyz = mix (vFogColor.xyz, tmpvar_1.xyz, Fog);
  gl_FragColor = tmpvar_1;
}

