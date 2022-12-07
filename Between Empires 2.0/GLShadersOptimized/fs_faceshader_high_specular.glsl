uniform sampler2D diffuse_texture;
uniform sampler2D diffuse_texture_2;
uniform sampler2D specular_texture;
uniform sampler2D normal_texture;
uniform vec4 vLightDiffuse[4];
uniform vec4 vMaterialColor;
uniform vec4 vSpecularColor;
uniform vec4 vSunColor;
uniform vec4 vAmbientColor;
uniform vec4 vSkyLightColor;
uniform vec4 vFogColor;
uniform vec4 output_gamma_inv;
uniform float fMaterialPower;
uniform int iLightIndices[4];
varying float Fog;
varying vec4 VertexColor;
varying vec3 VertexLighting;
varying vec2 Tex0;
varying vec3 SunLightDir;
varying vec3 SkyLightDir;
varying vec4 PointLightDir;
varying vec3 ViewDir;
void main ()
{
  vec4 tex_col_1;
  vec3 point_lighting_2;
  vec3 normal_3;
  vec4 total_light_4;
  vec4 tmpvar_5;
  normal_3 = ((2.0 * mix (texture2D (normal_texture, Tex0).xyz, texture2D (specular_texture, Tex0).xyz, VertexColor.w)) - 1.0);
  normal_3 = normalize(normal_3);
  float tmpvar_6;
  tmpvar_6 = dot (SunLightDir, normal_3);
  vec4 tmpvar_7;
  tmpvar_7.w = 1.0;
  tmpvar_7.xyz = vSunColor.xyz;
  total_light_4 = (vAmbientColor + (clamp (
    max ((0.2 * (tmpvar_6 + 0.9)), tmpvar_6)
  , 0.0, 1.0) * tmpvar_7));
  float tmpvar_8;
  tmpvar_8 = dot (SkyLightDir, normal_3);
  total_light_4 = (total_light_4 + (clamp (
    max ((0.2 * (tmpvar_8 + 0.9)), tmpvar_8)
  , 0.0, 1.0) * vSkyLightColor));
  int tmpvar_9;
  tmpvar_9 = iLightIndices[0];
  float tmpvar_10;
  tmpvar_10 = dot (PointLightDir.xyz, normal_3);
  point_lighting_2 = (((PointLightDir.w * 0.9) * clamp (
    max ((0.2 * (tmpvar_10 + 0.9)), tmpvar_10)
  , 0.0, 1.0)) * vLightDiffuse[tmpvar_9].xyz);
  point_lighting_2 = (point_lighting_2 + VertexLighting);
  total_light_4.xyz = (total_light_4.xyz + point_lighting_2);
  tmpvar_5.xyz = min (total_light_4.xyz, 2.0);
  vec4 tmpvar_11;
  tmpvar_11 = mix (texture2D (diffuse_texture, Tex0), texture2D (diffuse_texture_2, Tex0), VertexColor.w);
  tex_col_1.w = tmpvar_11.w;
  tex_col_1.xyz = pow (tmpvar_11.xyz, vec3(2.2, 2.2, 2.2));
  tmpvar_5 = (tmpvar_5 * tex_col_1);
  tmpvar_5.xyz = (tmpvar_5.xyz * (VertexColor.xyz * vMaterialColor.xyz));
  vec4 tmpvar_12;
  tmpvar_12.w = 1.0;
  tmpvar_12.xyz = vSpecularColor.xyz;
  vec4 tmpvar_13;
  tmpvar_13.w = 1.0;
  tmpvar_13.xyz = vSunColor.xyz;
  tmpvar_5 = (tmpvar_5 + vec4((clamp (
    (1.0 - dot (ViewDir, normal_3))
  , 0.0, 1.0) * (
    (tmpvar_12 * tmpvar_13)
   * 
    pow (clamp (dot (normalize(
      (ViewDir + SunLightDir)
    ), normal_3), 0.0, 1.0), fMaterialPower)
  ).x)));
  tmpvar_5.xyz = clamp (pow (tmpvar_5.xyz, output_gamma_inv.xyz), 0.0, 1.0);
  tmpvar_5.w = vMaterialColor.w;
  tmpvar_5.xyz = mix (vFogColor.xyz, tmpvar_5.xyz, Fog);
  gl_FragColor = tmpvar_5;
}

