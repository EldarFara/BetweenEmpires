uniform sampler2D diffuse_texture;
uniform sampler2D normal_texture;
uniform vec4 vLightDiffuse[4];
uniform vec4 vMaterialColor;
uniform vec4 vSunColor;
uniform vec4 vAmbientColor;
uniform vec4 vSkyLightColor;
uniform vec4 vFogColor;
uniform vec4 output_gamma_inv;
uniform int iLightIndices[4];
varying float Fog;
varying vec4 VertexColor;
varying vec2 Tex0;
varying vec3 SunLightDir;
varying vec3 SkyLightDir;
varying vec4 PointLightDir;
void main ()
{
  vec4 tex_col_1;
  vec4 total_light_2;
  vec3 normal_3;
  vec4 tmpvar_4;
  tmpvar_4.w = 1.0;
  normal_3 = ((2.0 * texture2D (normal_texture, Tex0)) - 1.0).xyz;
  total_light_2.w = vAmbientColor.w;
  total_light_2.xyz = (vAmbientColor.xyz + (vec3(clamp (
    dot (SunLightDir, normal_3)
  , 0.0, 1.0)) * vSunColor.xyz));
  total_light_2 = (total_light_2 + (clamp (
    dot (SkyLightDir, normal_3)
  , 0.0, 1.0) * vSkyLightColor));
  int tmpvar_5;
  tmpvar_5 = iLightIndices[0];
  total_light_2 = (total_light_2 + clamp ((
    (dot (PointLightDir.xyz, normal_3) * vLightDiffuse[tmpvar_5])
   * PointLightDir.w), 0.0, 1.0));
  tmpvar_4.xyz = min (total_light_2.xyz, 2.0);
  tmpvar_4.xyz = (tmpvar_4.xyz * vMaterialColor.xyz);
  vec4 tmpvar_6;
  tmpvar_6 = texture2D (diffuse_texture, Tex0);
  tex_col_1.w = tmpvar_6.w;
  tex_col_1.xyz = pow (tmpvar_6.xyz, vec3(2.2, 2.2, 2.2));
  tmpvar_4.xyz = (tmpvar_4.xyz * tex_col_1.xyz);
  tmpvar_4.xyz = (tmpvar_4.xyz * VertexColor.xyz);
  tmpvar_4.xyz = pow (tmpvar_4.xyz, output_gamma_inv.xyz);
  tmpvar_4.xyz = mix (vFogColor.xyz, tmpvar_4.xyz, Fog);
  tmpvar_4.w = (VertexColor.w * tmpvar_6.w);
  gl_FragColor = tmpvar_4;
}

