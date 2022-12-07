uniform sampler2D specular_texture;
uniform sampler2D env_texture;
uniform vec4 vFogColor;
uniform vec4 output_gamma_inv;
varying float Fog;
varying vec4 Color;
varying vec4 Tex0;
varying vec4 SunLight;
varying vec3 vSpecular;
void main ()
{
  vec4 tmpvar_1;
  vec4 tmpvar_2;
  tmpvar_2 = texture2D (specular_texture, Tex0.xy);
  float tmpvar_3;
  tmpvar_3 = (dot (tmpvar_2.wy, tmpvar_2.wy) * 0.5);
  vec4 vcol_4;
  vcol_4.w = Color.w;
  vcol_4.xyz = (Color.xyz + (SunLight.xyz + (tmpvar_3 * vSpecular)));
  tmpvar_1 = (clamp ((
    ((clamp ((Color + 0.5), 0.0, 1.0) * tmpvar_3) * 2.0)
   + 0.25), 0.0, 1.0) * vcol_4);
  tmpvar_1.xyz = (tmpvar_1.xyz + ((SunLight.xyz + 0.3) * (
    (Color.xyz * texture2D (env_texture, Tex0.zw).xyz)
   * tmpvar_3)));
  tmpvar_1.xyz = pow (tmpvar_1.xyz, output_gamma_inv.xyz);
  tmpvar_1.xyz = mix (vFogColor.xyz, tmpvar_1.xyz, Fog);
  tmpvar_1.w = 1.0;
  gl_FragColor = tmpvar_1;
}

