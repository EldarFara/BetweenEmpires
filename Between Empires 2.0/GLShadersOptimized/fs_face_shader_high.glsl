uniform sampler2D diffuse_texture;
uniform sampler2D diffuse_texture_2;
uniform sampler2D normal_texture;
uniform vec4 vLightDiffuse[4];
uniform vec4 vMaterialColor;
uniform vec4 vSunColor;
uniform vec4 vAmbientColor;
uniform vec4 vFogColor;
uniform vec4 output_gamma_inv;
uniform int iLightIndices[4];
varying float Fog;
varying vec4 VertexColor;
varying vec2 Tex0;
varying vec3 SunLightDir;
varying vec4 PointLightDir;
void main ()
{
  vec4 tex_col_1;
  vec3 normal_2;
  vec4 total_light_3;
  vec4 tmpvar_4;
  normal_2 = ((2.0 * texture2D (normal_texture, Tex0).xyz) - 1.0);
  float tmpvar_5;
  tmpvar_5 = dot (SunLightDir, normal_2);
  vec4 tmpvar_6;
  tmpvar_6.w = 1.0;
  tmpvar_6.xyz = vSunColor.xyz;
  total_light_3 = (vAmbientColor + (clamp (
    max ((0.2 * (tmpvar_5 + 0.9)), tmpvar_5)
  , 0.0, 1.0) * tmpvar_6));
  int tmpvar_7;
  tmpvar_7 = iLightIndices[0];
  float tmpvar_8;
  tmpvar_8 = dot (PointLightDir.xyz, normal_2);
  total_light_3.xyz = (total_light_3.xyz + ((
    (PointLightDir.w * 0.9)
   * 
    clamp (max ((0.2 * (tmpvar_8 + 0.9)), tmpvar_8), 0.0, 1.0)
  ) * vLightDiffuse[tmpvar_7].xyz));
  tmpvar_4.xyz = min (total_light_3.xyz, 2.0);
  vec4 tmpvar_9;
  tmpvar_9 = mix (texture2D (diffuse_texture, Tex0), texture2D (diffuse_texture_2, Tex0), VertexColor.w);
  tex_col_1.w = tmpvar_9.w;
  tex_col_1.xyz = pow (tmpvar_9.xyz, vec3(2.2, 2.2, 2.2));
  tmpvar_4 = (tmpvar_4 * tex_col_1);
  tmpvar_4.xyz = (tmpvar_4.xyz * (VertexColor.xyz * vMaterialColor.xyz));
  tmpvar_4.xyz = clamp (pow (tmpvar_4.xyz, output_gamma_inv.xyz), 0.0, 1.0);
  tmpvar_4.w = vMaterialColor.w;
  tmpvar_4.xyz = mix (vFogColor.xyz, tmpvar_4.xyz, Fog);
  gl_FragColor = tmpvar_4;
}

