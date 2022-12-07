uniform sampler2D diffuse_texture;
uniform sampler2D diffuse_texture_2;
uniform vec4 vLightDiffuse[4];
uniform vec4 vMaterialColor;
uniform vec4 vSunDir;
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
  vec4 total_light_2;
  vec4 tmpvar_3;
  float tmpvar_4;
  tmpvar_4 = dot (-(vSunDir.xyz), SunLightDir);
  vec4 tmpvar_5;
  tmpvar_5.w = 1.0;
  tmpvar_5.xyz = vSunColor.xyz;
  total_light_2 = (vAmbientColor + (clamp (
    max ((0.2 * (tmpvar_4 + 0.9)), tmpvar_4)
  , 0.0, 1.0) * tmpvar_5));
  int tmpvar_6;
  tmpvar_6 = iLightIndices[0];
  float tmpvar_7;
  tmpvar_7 = dot (PointLightDir.xyz, SunLightDir);
  total_light_2.xyz = (total_light_2.xyz + ((
    (PointLightDir.w * 0.9)
   * 
    clamp (max ((0.2 * (tmpvar_7 + 0.9)), tmpvar_7), 0.0, 1.0)
  ) * vLightDiffuse[tmpvar_6].xyz));
  tmpvar_3.xyz = min (total_light_2.xyz, 2.0);
  vec4 tmpvar_8;
  tmpvar_8 = mix (texture2D (diffuse_texture, Tex0), texture2D (diffuse_texture_2, Tex0), VertexColor.w);
  tex_col_1.w = tmpvar_8.w;
  tex_col_1.xyz = pow (tmpvar_8.xyz, vec3(2.2, 2.2, 2.2));
  tmpvar_3 = (tmpvar_3 * tex_col_1);
  tmpvar_3.xyz = (tmpvar_3.xyz * (VertexColor.xyz * vMaterialColor.xyz));
  tmpvar_3.xyz = clamp (pow (tmpvar_3.xyz, output_gamma_inv.xyz), 0.0, 1.0);
  tmpvar_3.w = vMaterialColor.w;
  tmpvar_3.xyz = mix (vFogColor.xyz, tmpvar_3.xyz, Fog);
  gl_FragColor = tmpvar_3;
}

