uniform sampler2D diffuse_texture;
uniform sampler2D normal_texture;
uniform vec4 vMaterialColor;
uniform vec4 vSunColor;
uniform vec4 vAmbientColor;
uniform vec4 vSkyLightColor;
uniform vec4 vPointLightColor;
uniform vec4 vFogColor;
uniform vec4 output_gamma_inv;
varying vec4 VertexColor;
varying vec2 Tex0;
varying vec3 SunLightDir;
varying vec3 SkyLightDir;
varying vec4 PointLightDir;
varying float Fog;
void main ()
{
  vec4 tex_col_1;
  vec3 normal_2;
  vec4 total_light_3;
  vec4 tmpvar_4;
  normal_2.xy = ((2.0 * texture2D (normal_texture, Tex0).wy) - 1.0);
  normal_2.z = sqrt((1.0 - dot (normal_2.xy, normal_2.xy)));
  vec4 tmpvar_5;
  tmpvar_5.w = 1.0;
  tmpvar_5.xyz = vSunColor.xyz;
  total_light_3 = (vAmbientColor + (clamp (
    dot (SunLightDir, normal_2)
  , 0.0, 1.0) * tmpvar_5));
  total_light_3 = (total_light_3 + (clamp (
    dot (SkyLightDir, normal_2)
  , 0.0, 1.0) * vSkyLightColor));
  vec4 tmpvar_6;
  tmpvar_6.w = 1.0;
  tmpvar_6.xyz = vPointLightColor.xyz;
  total_light_3 = (total_light_3 + (clamp (
    dot (PointLightDir.xyz, normal_2)
  , 0.0, 1.0) * tmpvar_6));
  tmpvar_4.xyz = total_light_3.xyz;
  tmpvar_4.w = 1.0;
  tmpvar_4 = (tmpvar_4 * vMaterialColor);
  vec4 tmpvar_7;
  tmpvar_7 = texture2D (diffuse_texture, Tex0);
  tex_col_1.w = tmpvar_7.w;
  tex_col_1.xyz = pow (tmpvar_7.xyz, vec3(2.2, 2.2, 2.2));
  tmpvar_4 = (tmpvar_4 * tex_col_1);
  tmpvar_4 = (tmpvar_4 * VertexColor);
  tmpvar_4.xyz = pow (tmpvar_4.xyz, output_gamma_inv.xyz);
  tmpvar_4.xyz = mix (vFogColor.xyz, tmpvar_4.xyz, Fog);
  gl_FragColor = tmpvar_4;
}

