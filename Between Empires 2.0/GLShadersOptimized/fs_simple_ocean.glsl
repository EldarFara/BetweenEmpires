uniform sampler2D normal_texture;
uniform sampler2D env_texture;
uniform vec4 vSunColor;
uniform vec4 output_gamma;
uniform vec4 output_gamma_inv;
varying vec2 Tex0;
varying vec3 LightDir;
varying vec4 LightDif;
varying vec3 CameraDir;
varying vec4 PosWater;
void main ()
{
  float fog_fresnel_factor_1;
  vec4 finalColor_2;
  vec4 tex_3;
  vec3 normal_4;
  normal_4.xy = ((2.0 * texture2D (normal_texture, Tex0).wy) - 1.0);
  normal_4.z = sqrt((1.0 - dot (normal_4.xy, normal_4.xy)));
  vec2 tmpvar_5;
  tmpvar_5.x = (0.5 + (0.5 * (PosWater.x / PosWater.w)));
  tmpvar_5.y = (0.5 - (0.5 * (PosWater.y / PosWater.w)));
  vec4 tmpvar_6;
  tmpvar_6 = texture2D (env_texture, ((0.5 * normal_4.xy) + tmpvar_5));
  tex_3.w = tmpvar_6.w;
  tex_3.xyz = pow (tmpvar_6.xyz, output_gamma.xyz);
  float tmpvar_7;
  tmpvar_7 = (1.0 - clamp (dot (
    normalize(CameraDir)
  , normal_4), 0.0, 1.0));
  finalColor_2.xyz = (((0.01 * 
    clamp (dot (normal_4, LightDir), 0.0, 1.0)
  ) * LightDif).xyz + (tex_3.xyz * (0.0204 + 
    (((0.9796 * tmpvar_7) * (tmpvar_7 * tmpvar_7)) * (tmpvar_7 * tmpvar_7))
  )));
  finalColor_2.w = (1.0 - (0.3 * CameraDir.z));
  float tmpvar_8;
  tmpvar_8 = clamp (dot (CameraDir, normal_4), 0.0, 1.0);
  fog_fresnel_factor_1 = (tmpvar_8 * tmpvar_8);
  fog_fresnel_factor_1 = (fog_fresnel_factor_1 * fog_fresnel_factor_1);
  finalColor_2.xyz = (finalColor_2.xyz + ((vec3(0.1568628, 0.3529412, 0.7843137) * vSunColor.xyz) * fog_fresnel_factor_1));
  finalColor_2.xyz = pow (finalColor_2.xyz, output_gamma_inv.xyz);
  finalColor_2.w = 1.0;
  gl_FragColor = finalColor_2;
}

