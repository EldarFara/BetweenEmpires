uniform sampler2D diffuse_texture_2;
uniform sampler2D env_texture;
uniform vec4 vSpecularColor;
uniform vec4 vFogColor;
uniform vec4 output_gamma_inv;
varying float Fog;
varying vec4 Color;
varying vec2 Tex0;
void main ()
{
  vec4 tmpvar_1;
  tmpvar_1 = (Color * texture2D (diffuse_texture_2, Tex0));
  tmpvar_1.xyz = (tmpvar_1.xyz * exp2((
    (texture2D (env_texture, Tex0).x * vSpecularColor.x)
   + vSpecularColor.y)));
  tmpvar_1.w = 1.0;
  tmpvar_1.xyz = pow (tmpvar_1.xyz, output_gamma_inv.xyz);
  tmpvar_1.xyz = mix (vFogColor.xyz, tmpvar_1.xyz, Fog);
  if ((Color.w == 0.0)) {
    tmpvar_1.xyz = clamp (tmpvar_1.xyz, 0.0, 1.0);
  };
  tmpvar_1.xyz = mix (vFogColor.xyz, tmpvar_1.xyz, Fog);
  gl_FragColor = tmpvar_1;
}

