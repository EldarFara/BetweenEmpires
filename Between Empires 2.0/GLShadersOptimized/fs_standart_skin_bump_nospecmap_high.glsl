uniform sampler2D diffuse_texture;
uniform sampler2D normal_texture;
uniform vec4 vLightDiffuse[4];
uniform vec4 vMaterialColor;
uniform vec4 vSpecularColor;
uniform vec4 vSunColor;
uniform vec4 vAmbientColor;
uniform vec4 vGroundAmbientColor;
uniform vec4 vSkyLightColor;
uniform vec4 vFogColor;
uniform vec4 output_gamma_inv;
uniform float fMaterialPower;
uniform float spec_coef;
uniform int iLightIndices[4];
varying float Fog;
varying vec4 VertexColor;
varying vec2 Tex0;
varying vec3 SunLightDir;
varying vec3 SkyLightDir;
varying vec4 PointLightDir;
varying vec4 ShadowTexCoord;
varying vec3 ViewDir;
void main ()
{
  vec4 tex_col_1;
  vec4 total_light_2;
  vec3 normal_3;
  vec4 tmpvar_4;
  tmpvar_4.w = 1.0;
  normal_3 = ((2.0 * texture2D (normal_texture, Tex0)) - 1.0).xyz;
  vec4 ambientTerm_5;
  ambientTerm_5 = mix (vGroundAmbientColor, vAmbientColor, ((
    dot (normal_3, SkyLightDir)
   + 1.0) * 0.5));
  total_light_2.w = ambientTerm_5.w;
  total_light_2.xyz = (ambientTerm_5.xyz + (vec3(clamp (
    dot (SunLightDir, normal_3)
  , 0.0, 1.0)) * vSunColor.xyz));
  total_light_2 = (total_light_2 + (clamp (
    dot (SkyLightDir, normal_3)
  , 0.0, 1.0) * vSkyLightColor));
  int tmpvar_6;
  tmpvar_6 = iLightIndices[0];
  total_light_2 = (total_light_2 + clamp ((
    (dot (PointLightDir.xyz, normal_3) * vLightDiffuse[tmpvar_6])
   * PointLightDir.w), 0.0, 1.0));
  tmpvar_4.xyz = min (total_light_2.xyz, 2.0);
  tmpvar_4.xyz = (tmpvar_4.xyz * vMaterialColor.xyz);
  vec4 tmpvar_7;
  tmpvar_7 = texture2D (diffuse_texture, Tex0);
  tex_col_1.w = tmpvar_7.w;
  tex_col_1.xyz = pow (tmpvar_7.xyz, vec3(2.2, 2.2, 2.2));
  tmpvar_4.xyz = (tmpvar_4.xyz * tex_col_1.xyz);
  tmpvar_4.xyz = (tmpvar_4.xyz * VertexColor.xyz);
  vec4 specColor_8;
  vec4 fSpecular_9;
  vec4 tmpvar_10;
  tmpvar_10.w = 1.0;
  tmpvar_10.xyz = vSpecularColor.xyz;
  specColor_8 = (((0.1 * spec_coef) * tmpvar_10) * tmpvar_7.w);
  vec4 tmpvar_11;
  tmpvar_11.w = 1.0;
  tmpvar_11.xyz = vSunColor.xyz;
  fSpecular_9 = ((specColor_8 * tmpvar_11) * pow (clamp (
    dot (normalize((ViewDir + SunLightDir)), normal_3)
  , 0.0, 1.0), fMaterialPower));
  fSpecular_9 = (fSpecular_9 * VertexColor);
  fSpecular_9.xyz = (fSpecular_9.xyz + (specColor_8.xyz * ShadowTexCoord.xyz));
  int tmpvar_12;
  tmpvar_12 = iLightIndices[0];
  fSpecular_9 = (fSpecular_9 + ((
    (specColor_8 * vLightDiffuse[tmpvar_12])
   * 
    (PointLightDir.w * 0.5)
  ) * pow (
    clamp (dot (normalize((ViewDir + PointLightDir.xyz)), normal_3), 0.0, 1.0)
  , fMaterialPower)));
  tmpvar_4 = (tmpvar_4 + fSpecular_9);
  tmpvar_4.xyz = pow (tmpvar_4.xyz, output_gamma_inv.xyz);
  tmpvar_4.xyz = mix (vFogColor.xyz, tmpvar_4.xyz, Fog);
  tmpvar_4.w = (VertexColor.w * tmpvar_7.w);
  gl_FragColor = tmpvar_4;
}

