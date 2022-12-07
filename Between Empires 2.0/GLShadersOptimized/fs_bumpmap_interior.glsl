uniform sampler2D diffuse_texture;
uniform sampler2D normal_texture;
uniform vec4 vLightDiffuse[4];
uniform vec4 vAmbientColor;
uniform vec4 vFogColor;
uniform vec4 output_gamma_inv;
uniform int iLightIndices[4];
varying vec4 VertexColor;
varying vec2 Tex0;
varying vec3 vec_to_light_0;
varying vec3 vec_to_light_1;
varying vec3 vec_to_light_2;
varying float Fog;
void main ()
{
  vec4 tex_col_1;
  vec3 normal_2;
  vec4 total_light_3;
  vec4 tmpvar_4;
  normal_2.xy = ((2.0 * texture2D (normal_texture, Tex0).wy) - 1.0);
  normal_2.z = sqrt((1.0 - dot (normal_2.xy, normal_2.xy)));
  total_light_3 = (vAmbientColor + ((
    clamp (dot (normal_2, normalize(vec_to_light_0)), 0.0, 1.0)
   * vLightDiffuse[iLightIndices[0]]) / max (1e-06, 
    dot (vec_to_light_0, vec_to_light_0)
  )));
  total_light_3 = (total_light_3 + ((
    clamp (dot (normal_2, normalize(vec_to_light_1)), 0.0, 1.0)
   * vLightDiffuse[iLightIndices[1]]) / dot (vec_to_light_1, vec_to_light_1)));
  total_light_3 = (total_light_3 + ((
    clamp (dot (normal_2, normalize(vec_to_light_2)), 0.0, 1.0)
   * vLightDiffuse[iLightIndices[2]]) / dot (vec_to_light_2, vec_to_light_2)));
  vec4 tmpvar_5;
  tmpvar_5.w = 1.0;
  tmpvar_5.xyz = total_light_3.xyz;
  vec4 tmpvar_6;
  tmpvar_6 = texture2D (diffuse_texture, Tex0);
  tex_col_1.w = tmpvar_6.w;
  tex_col_1.xyz = pow (tmpvar_6.xyz, vec3(2.2, 2.2, 2.2));
  tmpvar_4 = (tmpvar_5 * tex_col_1);
  tmpvar_4 = (tmpvar_4 * VertexColor);
  tmpvar_4.xyz = clamp (pow (tmpvar_4.xyz, output_gamma_inv.xyz), 0.0, 1.0);
  tmpvar_4.w = VertexColor.w;
  tmpvar_4.xyz = mix (vFogColor.xyz, tmpvar_4.xyz, Fog);
  gl_FragColor = tmpvar_4;
}

