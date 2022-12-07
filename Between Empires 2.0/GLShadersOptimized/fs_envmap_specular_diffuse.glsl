uniform sampler2D diffuse_texture;
uniform sampler2D specular_texture;
uniform sampler2D env_texture;
uniform vec4 vFogColor;
uniform vec4 output_gamma_inv;
uniform bool bUseMotionBlur;
varying float Fog;
varying vec4 Color;
varying vec4 Tex0;
varying vec4 SunLight;
varying vec3 vSpecular;
void main ()
{
  vec4 texColor_1;
  vec4 tmpvar_2;
  vec4 tmpvar_3;
  tmpvar_3 = texture2D (diffuse_texture, Tex0.xy);
  texColor_1.w = tmpvar_3.w;
  texColor_1.xyz = pow (tmpvar_3.xyz, vec3(2.2, 2.2, 2.2));
  vec4 tmpvar_4;
  tmpvar_4 = texture2D (specular_texture, Tex0.xy);
  vec4 vcol_5;
  vcol_5.w = Color.w;
  vcol_5.xyz = (Color.xyz + (SunLight.xyz + (tmpvar_4.xyz * vSpecular)));
  tmpvar_2 = (texColor_1 * vcol_5);
  tmpvar_2.xyz = (tmpvar_2.xyz + ((SunLight.xyz + 0.3) * (
    (Color.xyz * texture2D (env_texture, Tex0.zw).xyz)
   * tmpvar_4.xyz)));
  tmpvar_2.xyz = pow (tmpvar_2.xyz, output_gamma_inv.xyz);
  tmpvar_2.xyz = mix (vFogColor.xyz, tmpvar_2.xyz, Fog);
  tmpvar_2.w = 1.0;
  if (bUseMotionBlur) {
    tmpvar_2.w = SunLight.w;
  };
  gl_FragColor = tmpvar_2;
}

