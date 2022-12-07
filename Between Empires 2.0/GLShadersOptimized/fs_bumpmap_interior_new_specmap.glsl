uniform sampler2D diffuse_texture;
uniform sampler2D specular_texture;
uniform sampler2D normal_texture;
uniform vec4 vLightDiffuse[4];
uniform vec4 vSpecularColor;
uniform vec4 vAmbientColor;
uniform vec4 vFogColor;
uniform vec4 output_gamma_inv;
uniform float fMaterialPower;
uniform float spec_coef;
uniform int iLightIndices[4];
varying vec4 VertexColor;
varying vec2 Tex0;
varying vec3 vec_to_light_0;
varying vec3 vec_to_light_1;
varying vec3 vec_to_light_2;
varying vec3 ViewDir;
varying float Fog;
void main ()
{
  vec4 tex_col_1;
  vec4 total_light_2;
  vec4 tmpvar_3;
  vec3 tmpvar_4;
  tmpvar_4 = ((2.0 * texture2D (normal_texture, Tex0).xyz) - 1.0);
  float tmpvar_5;
  tmpvar_5 = clamp ((1.0/(max (1e-06, 
    dot (vec_to_light_0, vec_to_light_0)
  ))), 0.0, 1.0);
  vec3 tmpvar_6;
  tmpvar_6 = normalize(vec_to_light_0);
  total_light_2 = (vAmbientColor + ((
    clamp (dot (tmpvar_4, tmpvar_6), 0.0, 1.0)
   * vLightDiffuse[iLightIndices[0]]) * tmpvar_5));
  total_light_2 = (total_light_2 + ((
    clamp (dot (tmpvar_4, normalize(vec_to_light_1)), 0.0, 1.0)
   * vLightDiffuse[iLightIndices[1]]) * clamp (
    (1.0/(max (1e-06, dot (vec_to_light_1, vec_to_light_1))))
  , 0.0, 1.0)));
  total_light_2 = (total_light_2 + ((
    clamp (dot (tmpvar_4, normalize(vec_to_light_2)), 0.0, 1.0)
   * vLightDiffuse[iLightIndices[2]]) * clamp (
    (1.0/(max (1e-06, dot (vec_to_light_2, vec_to_light_2))))
  , 0.0, 1.0)));
  vec4 tmpvar_7;
  tmpvar_7.w = 1.0;
  tmpvar_7.xyz = total_light_2.xyz;
  vec4 tmpvar_8;
  tmpvar_8 = texture2D (diffuse_texture, Tex0);
  tex_col_1.w = tmpvar_8.w;
  tex_col_1.xyz = pow (tmpvar_8.xyz, vec3(2.2, 2.2, 2.2));
  tmpvar_3 = (tmpvar_7 * tex_col_1);
  tmpvar_3 = (tmpvar_3 * VertexColor);
  vec4 tmpvar_9;
  tmpvar_9.w = 1.0;
  tmpvar_9.xyz = vSpecularColor.xyz;
  tmpvar_3 = (tmpvar_3 + ((
    ((0.1 * spec_coef) * tmpvar_9)
   * 
    dot (texture2D (specular_texture, Tex0).xyz, vec3(0.33, 0.33, 0.33))
  ) * (
    (vLightDiffuse[iLightIndices[0]] * tmpvar_5)
   * 
    pow (clamp (dot (normalize(
      (ViewDir + tmpvar_6)
    ), tmpvar_4), 0.0, 1.0), fMaterialPower)
  )));
  tmpvar_3.xyz = pow (tmpvar_3.xyz, output_gamma_inv.xyz);
  tmpvar_3.xyz = clamp (tmpvar_3, 0.0, 1.0).xyz;
  tmpvar_3.w = VertexColor.w;
  tmpvar_3.xyz = mix (vFogColor.xyz, tmpvar_3.xyz, Fog);
  gl_FragColor = tmpvar_3;
}

