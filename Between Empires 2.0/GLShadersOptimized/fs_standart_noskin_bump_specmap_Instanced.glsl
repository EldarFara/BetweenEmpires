uniform sampler2D diffuse_texture;
uniform sampler2D specular_texture;
uniform sampler2D normal_texture;
uniform vec4 vLightDiffuse[4];
uniform vec4 vMaterialColor;
uniform vec4 vSpecularColor;
uniform vec4 vSunColor;
uniform vec4 vAmbientColor;
uniform vec4 vFogColor;
uniform vec4 output_gamma_inv;
uniform float fMaterialPower;
uniform float spec_coef;
uniform int iLightIndices[4];
varying float Fog;
varying vec4 VertexColor;
varying vec2 Tex0;
varying vec3 SunLightDir;
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
  total_light_2.w = vAmbientColor.w;
  total_light_2.xyz = (vAmbientColor.xyz + (vec3(clamp (
    dot (SunLightDir, normal_3)
  , 0.0, 1.0)) * vSunColor.xyz));
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
  vec4 specColor_7;
  vec4 fSpecular_8;
  vec4 tmpvar_9;
  tmpvar_9.w = 1.0;
  tmpvar_9.xyz = vSpecularColor.xyz;
  specColor_7 = (((0.1 * spec_coef) * tmpvar_9) * dot (texture2D (specular_texture, Tex0).xyz, vec3(0.33, 0.33, 0.33)));
  vec4 tmpvar_10;
  tmpvar_10.w = 1.0;
  tmpvar_10.xyz = vSunColor.xyz;
  fSpecular_8 = ((specColor_7 * tmpvar_10) * pow (clamp (
    dot (normalize((ViewDir + SunLightDir)), normal_3)
  , 0.0, 1.0), fMaterialPower));
  fSpecular_8 = (fSpecular_8 * VertexColor);
  fSpecular_8.xyz = (fSpecular_8.xyz + (specColor_7.xyz * ShadowTexCoord.xyz));
  int tmpvar_11;
  tmpvar_11 = iLightIndices[0];
  fSpecular_8 = (fSpecular_8 + ((
    (specColor_7 * vLightDiffuse[tmpvar_11])
   * 
    (PointLightDir.w * 0.5)
  ) * pow (
    clamp (dot (normalize((ViewDir + PointLightDir.xyz)), normal_3), 0.0, 1.0)
  , fMaterialPower)));
  tmpvar_4 = (tmpvar_4 + fSpecular_8);
  tmpvar_4.xyz = pow (tmpvar_4.xyz, output_gamma_inv.xyz);
  tmpvar_4.xyz = mix (vFogColor.xyz, tmpvar_4.xyz, Fog);
  tmpvar_4.w = VertexColor.w;
  gl_FragColor = tmpvar_4;
}

