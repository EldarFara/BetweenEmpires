uniform sampler2D normal_texture;
uniform sampler2D env_texture;
uniform sampler2D depth_texture;
uniform vec4 vFogColor;
uniform vec4 output_gamma;
uniform vec4 output_gamma_inv;
uniform bool use_depth_effects;
varying vec2 Tex0;
varying vec4 LightDir_Alpha;
varying vec4 LightDif;
varying vec3 CameraDir;
varying vec4 PosWater;
varying float Fog;
varying vec4 projCoord;
varying float Depth;
void main ()
{
  float fog_fresnel_factor_1;
  vec4 tex_2;
  vec3 normal_3;
  vec4 tmpvar_4;
  normal_3.xy = ((2.0 * texture2D (normal_texture, Tex0).wy) - 1.0);
  normal_3.z = sqrt((1.0 - dot (normal_3.xy, normal_3.xy)));
  vec3 tmpvar_5;
  tmpvar_5 = normalize(CameraDir);
  vec2 tmpvar_6;
  tmpvar_6.x = (0.5 + (0.5 * (PosWater.x / PosWater.w)));
  tmpvar_6.y = (0.5 - (0.5 * (PosWater.y / PosWater.w)));
  vec2 tmpvar_7;
  tmpvar_7 = ((0.25 * normal_3.xy) + tmpvar_6);
  vec2 tmpvar_8;
  tmpvar_8.x = tmpvar_7.x;
  tmpvar_8.y = (1.0 - tmpvar_7.y);
  tex_2 = texture2D (env_texture, tmpvar_8);
  tex_2.xyz = pow (tex_2.xyz, output_gamma.xyz);
  tmpvar_4 = ((0.01 * clamp (
    dot (normal_3, LightDir_Alpha.xyz)
  , 0.0, 1.0)) * LightDif);
  float tmpvar_9;
  tmpvar_9 = (1.0 - clamp (dot (tmpvar_5, normal_3), 0.0, 1.0));
  tmpvar_4.xyz = (tmpvar_4.xyz + (tex_2.xyz * (0.0204 + 
    (((0.9796 * tmpvar_9) * (tmpvar_9 * tmpvar_9)) * (tmpvar_9 * tmpvar_9))
  )));
  tmpvar_4.w = (1.0 - (0.3 * CameraDir.z));
  tmpvar_4.w = (tmpvar_4.w * LightDir_Alpha.w);
  float tmpvar_10;
  tmpvar_10 = clamp (dot (CameraDir, normal_3), 0.0, 1.0);
  fog_fresnel_factor_1 = (tmpvar_10 * tmpvar_10);
  fog_fresnel_factor_1 = (fog_fresnel_factor_1 * fog_fresnel_factor_1);
  tmpvar_4.xyz = (tmpvar_4.xyz + (mix (vec3(0.003921569, 0.01960784, 0.03921569), vec3(0.003921569, 0.01568628, 0.02352941), 
    clamp (dot (tmpvar_5, normal_3), 0.0, 1.0)
  ) * fog_fresnel_factor_1));
  if (use_depth_effects) {
    float alpha_factor_11;
    vec2 tmpvar_12;
    tmpvar_12 = (projCoord.xy / projCoord.w);
    vec2 tmpvar_13;
    tmpvar_13.x = tmpvar_12.x;
    tmpvar_13.y = (1.0 - tmpvar_12.y);
    vec4 tmpvar_14;
    tmpvar_14 = texture2D (depth_texture, tmpvar_13);
    if (((tmpvar_14.x + 0.0005) < Depth)) {
      alpha_factor_11 = 1.0;
    } else {
      alpha_factor_11 = clamp (((tmpvar_14.x - Depth) * 2048.0), 0.0, 1.0);
    };
    tmpvar_4.w = (tmpvar_4.w * alpha_factor_11);
    tmpvar_4.w = (tmpvar_4.w + clamp ((
      (tmpvar_14.x - Depth)
     * 32.0), 0.0, 1.0));
  };
  tmpvar_4.xyz = pow (tmpvar_4.xyz, output_gamma_inv.xyz);
  tmpvar_4.w = clamp (tmpvar_4.w, 0.0, 1.0);
  tmpvar_4.xyz = mix (vFogColor.xyz, tmpvar_4.xyz, Fog);
  gl_FragColor = tmpvar_4;
}

