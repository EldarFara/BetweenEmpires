uniform sampler2D diffuse_texture;
uniform vec4 vMaterialColor;
uniform vec4 vSunDir;
uniform vec4 vSunColor;
uniform vec4 vAmbientColor;
uniform vec4 vGroundAmbientColor;
uniform vec4 vFogColor;
uniform vec4 output_gamma_inv;
varying float Fog;
varying vec4 VertexColor;
varying vec3 VertexLighting;
varying vec2 Tex0;
varying vec3 SunLightDir;
void main ()
{
  vec4 tex_col_1;
  vec4 total_light_2;
  vec4 tmpvar_3;
  tmpvar_3.w = 1.0;
  vec4 ambientTerm_4;
  ambientTerm_4 = mix (vGroundAmbientColor, vAmbientColor, ((SunLightDir.z + 1.0) * 0.5));
  total_light_2.w = ambientTerm_4.w;
  total_light_2.xyz = (ambientTerm_4.xyz + (vec3(clamp (
    dot (-(vSunDir.xyz), SunLightDir)
  , 0.0, 1.0)) * vSunColor.xyz));
  total_light_2.xyz = (total_light_2.xyz + VertexLighting);
  tmpvar_3.xyz = min (total_light_2.xyz, 2.0);
  tmpvar_3.xyz = (tmpvar_3.xyz * vMaterialColor.xyz);
  vec4 tmpvar_5;
  tmpvar_5 = texture2D (diffuse_texture, Tex0);
  tex_col_1.w = tmpvar_5.w;
  tex_col_1.xyz = pow (tmpvar_5.xyz, vec3(2.2, 2.2, 2.2));
  tmpvar_3.xyz = (tmpvar_3.xyz * tex_col_1.xyz);
  tmpvar_3.xyz = (tmpvar_3.xyz * VertexColor.xyz);
  tmpvar_3.xyz = pow (tmpvar_3.xyz, output_gamma_inv.xyz);
  tmpvar_3.xyz = mix (vFogColor.xyz, tmpvar_3.xyz, Fog);
  tmpvar_3.w = (VertexColor.w * tmpvar_5.w);
  gl_FragColor = tmpvar_3;
}

