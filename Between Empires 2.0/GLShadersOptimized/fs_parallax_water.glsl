uniform sampler2D diffuse_texture;
uniform sampler2D diffuse_texture_2;
uniform sampler2D specular_texture;
uniform sampler2D normal_texture;
uniform sampler2D env_texture;
uniform sampler2D depth_texture;
uniform vec4 vSpecularColor;
uniform vec4 vFogColor;
uniform vec4 output_gamma;
uniform vec4 output_gamma_inv;
uniform bool use_depth_effects;
uniform float time_var;
varying vec2 Tex0;
varying vec4 LightDir_Alpha;
varying vec4 LightDif;
varying vec3 ViewDir;
varying vec3 CameraDir;
varying vec4 PosWater;
varying vec4 projCoord;
varying float Depth;
varying float Fog;
void main ()
{
  vec2 tmpvar_1;
  float fog_fresnel_factor_2;
  vec4 tex_3;
  vec3 normal2_4;
  vec3 normal_5;
  vec4 tmpvar_6;
  tmpvar_1 = (Tex0 * 0.5);
  float tmpvar_7;
  tmpvar_7 = (0.5 * time_var);
  vec3 tmpvar_8;
  tmpvar_8 = normalize(ViewDir);
  float tmpvar_9;
  tmpvar_9 = (0.01 * vSpecularColor.x);
  float tmpvar_10;
  tmpvar_10 = (tmpvar_9 * 5.0);
  float tmpvar_11;
  tmpvar_11 = (tmpvar_9 * -2.5);
  vec2 tmpvar_12;
  tmpvar_12.x = tmpvar_1.x;
  tmpvar_12.y = (tmpvar_1.y + (0.1 * tmpvar_7));
  vec2 tmpvar_13;
  tmpvar_13.x = (tmpvar_1.x + (0.15 * tmpvar_7));
  tmpvar_13.y = (tmpvar_1.y + (0.25 * tmpvar_7));
  tmpvar_1 = (tmpvar_1 + ((
    (texture2D (diffuse_texture, tmpvar_12).w * tmpvar_10)
   + tmpvar_11) * tmpvar_8.xy));
  tmpvar_1 = (tmpvar_1 + ((
    (texture2D (specular_texture, tmpvar_13).w * (0.5 * tmpvar_10))
   + 
    (0.5 * tmpvar_11)
  ) * tmpvar_8.xy));
  vec2 tmpvar_14;
  tmpvar_14.x = tmpvar_1.x;
  tmpvar_14.y = (tmpvar_1.y + (0.1 * tmpvar_7));
  normal_5.xy = ((2.0 * texture2D (diffuse_texture_2, tmpvar_14).wy) - 1.0);
  normal_5.z = sqrt((1.0 - dot (normal_5.xy, normal_5.xy)));
  vec2 tmpvar_15;
  tmpvar_15.x = tmpvar_1.x;
  tmpvar_15.y = (tmpvar_1.y + (0.25 * tmpvar_7));
  normal2_4.xy = ((2.0 * texture2D (normal_texture, tmpvar_15).wy) - 1.0);
  normal2_4.z = sqrt((1.0 - dot (normal2_4.xy, normal2_4.xy)));
  normal_5 = mix (normal_5, normal2_4, 0.35);
  vec3 tmpvar_16;
  tmpvar_16 = normalize(CameraDir);
  vec2 tmpvar_17;
  tmpvar_17.x = (0.5 + (0.5 * (PosWater.x / PosWater.w)));
  tmpvar_17.y = (0.5 - (0.5 * (PosWater.y / PosWater.w)));
  vec2 tmpvar_18;
  tmpvar_18 = ((0.25 * normal_5.xy) + tmpvar_17);
  vec2 tmpvar_19;
  tmpvar_19.x = tmpvar_18.x;
  tmpvar_19.y = (1.0 - tmpvar_18.y);
  tex_3 = texture2D (env_texture, tmpvar_19);
  tex_3.xyz = pow (tex_3.xyz, output_gamma.xyz);
  tmpvar_6 = ((0.01 * clamp (
    dot (normal_5, LightDir_Alpha.xyz)
  , 0.0, 1.0)) * LightDif);
  float tmpvar_20;
  tmpvar_20 = (1.0 - clamp (dot (tmpvar_16, normal_5), 0.0, 1.0));
  tmpvar_6.xyz = (tmpvar_6.xyz + (tex_3.xyz * (0.0204 + 
    (((0.9796 * tmpvar_20) * (tmpvar_20 * tmpvar_20)) * (((tmpvar_20 * tmpvar_20) * (tmpvar_20 * tmpvar_20)) * (tmpvar_20 * tmpvar_20)))
  )));
  tmpvar_6.w = (1.0 - (0.3 * CameraDir.z));
  tmpvar_6.w = (tmpvar_6.w * LightDir_Alpha.w);
  float tmpvar_21;
  tmpvar_21 = clamp (dot (CameraDir, normal_5), 0.0, 1.0);
  fog_fresnel_factor_2 = (tmpvar_21 * tmpvar_21);
  fog_fresnel_factor_2 = (fog_fresnel_factor_2 * fog_fresnel_factor_2);
  tmpvar_6.xyz = (tmpvar_6.xyz + (mix (vec3(0.003921569, 0.01960784, 0.03921569), vec3(0.003921569, 0.01568628, 0.02352941), 
    clamp (dot (tmpvar_16, normal_5), 0.0, 1.0)
  ) * fog_fresnel_factor_2));
  if (use_depth_effects) {
    float alpha_factor_22;
    vec2 tmpvar_23;
    tmpvar_23 = (projCoord.xy / projCoord.w);
    vec2 tmpvar_24;
    tmpvar_24.x = tmpvar_23.x;
    tmpvar_24.y = (1.0 - tmpvar_23.y);
    vec4 tmpvar_25;
    tmpvar_25 = texture2D (depth_texture, tmpvar_24);
    if (((tmpvar_25.x + 0.0005) < Depth)) {
      alpha_factor_22 = 1.0;
    } else {
      alpha_factor_22 = clamp (((tmpvar_25.x - Depth) * 2048.0), 0.0, 1.0);
    };
    tmpvar_6.w = (tmpvar_6.w * alpha_factor_22);
    tmpvar_6.w = (tmpvar_6.w + clamp ((
      (tmpvar_25.x - Depth)
     * 32.0), 0.0, 1.0));
  };
  tmpvar_6.xyz = pow (tmpvar_6.xyz, output_gamma_inv.xyz);
  tmpvar_6.w = clamp (tmpvar_6.w, 0.0, 1.0);
  tmpvar_6.xyz = mix (vFogColor.xyz, tmpvar_6.xyz, Fog);
  gl_FragColor = tmpvar_6;
}

