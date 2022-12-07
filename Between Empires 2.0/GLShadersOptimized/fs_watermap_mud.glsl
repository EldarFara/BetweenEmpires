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
  float fresnel_2;
  vec4 tex_3;
  vec3 normal_4;
  vec4 tmpvar_5;
  normal_4.xy = ((2.0 * texture2D (normal_texture, Tex0).wy) - 1.0);
  normal_4.z = sqrt((1.0 - dot (normal_4.xy, normal_4.xy)));
  vec3 tmpvar_6;
  tmpvar_6 = normalize(CameraDir);
  vec2 tmpvar_7;
  tmpvar_7.x = (0.5 + (0.5 * (PosWater.x / PosWater.w)));
  tmpvar_7.y = (0.5 - (0.5 * (PosWater.y / PosWater.w)));
  vec2 tmpvar_8;
  tmpvar_8 = ((0.25 * normal_4.xy) + tmpvar_7);
  vec2 tmpvar_9;
  tmpvar_9.x = tmpvar_8.x;
  tmpvar_9.y = (1.0 - tmpvar_8.y);
  tex_3 = texture2D (env_texture, tmpvar_9);
  tex_3.xyz = pow (tex_3.xyz, output_gamma.xyz);
  tmpvar_5 = ((0.01 * clamp (
    dot (normal_4, LightDir_Alpha.xyz)
  , 0.0, 1.0)) * LightDif);
  tmpvar_5 = (tmpvar_5 * 0.125);
  float tmpvar_10;
  tmpvar_10 = (1.0 - clamp (dot (tmpvar_6, normal_4), 0.0, 1.0));
  fresnel_2 = (0.0204 + ((
    (0.9796 * tmpvar_10)
   * 
    (tmpvar_10 * tmpvar_10)
  ) * (tmpvar_10 * tmpvar_10)));
  tmpvar_5.xyz = (tmpvar_5.xyz + mix ((
    (tex_3.xyz * vec3(0.105, 0.175, 0.16))
   * fresnel_2), tex_3.xyz, fresnel_2));
  tmpvar_5.w = 1.0;
  float tmpvar_11;
  tmpvar_11 = clamp (dot (CameraDir, normal_4), 0.0, 1.0);
  fog_fresnel_factor_1 = (tmpvar_11 * tmpvar_11);
  fog_fresnel_factor_1 = (fog_fresnel_factor_1 * fog_fresnel_factor_1);
  tmpvar_5.xyz = (tmpvar_5.xyz + (mix (vec3(0.01960784, 0.02745098, 0.02745098), vec3(0.01764706, 0.03137255, 0.02352941), 
    clamp (dot (tmpvar_6, normal_4), 0.0, 1.0)
  ) * fog_fresnel_factor_1));
  tmpvar_5.xyz = (tmpvar_5.xyz + (vec3(0.022, 0.02, 0.005) * (1.0 - 
    clamp (dot (tmpvar_6, normal_4), 0.0, 1.0)
  )));
  if (use_depth_effects) {
    float alpha_factor_12;
    vec2 tmpvar_13;
    tmpvar_13 = (projCoord.xy / projCoord.w);
    vec2 tmpvar_14;
    tmpvar_14.x = tmpvar_13.x;
    tmpvar_14.y = (1.0 - tmpvar_13.y);
    vec4 tmpvar_15;
    tmpvar_15 = texture2D (depth_texture, tmpvar_14);
    if (((tmpvar_15.x + 0.0005) < Depth)) {
      alpha_factor_12 = 1.0;
    } else {
      alpha_factor_12 = clamp (((tmpvar_15.x - Depth) * 2048.0), 0.0, 1.0);
    };
    tmpvar_5.w = (alpha_factor_12 + clamp ((
      (tmpvar_15.x - Depth)
     * 32.0), 0.0, 1.0));
  };
  tmpvar_5.xyz = pow (tmpvar_5.xyz, output_gamma_inv.xyz);
  tmpvar_5.w = clamp (tmpvar_5.w, 0.0, 1.0);
  tmpvar_5.xyz = mix (vFogColor.xyz, tmpvar_5.xyz, Fog);
  gl_FragColor = tmpvar_5;
}

