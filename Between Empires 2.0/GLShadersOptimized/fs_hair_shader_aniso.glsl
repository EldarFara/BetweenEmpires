uniform sampler2D diffuse_texture;
uniform sampler2D diffuse_texture_2;
uniform vec4 vMaterialColor;
uniform vec4 vMaterialColor2;
uniform vec4 vSunDir;
uniform vec4 vSunColor;
uniform vec4 vAmbientColor;
uniform vec4 vFogColor;
uniform vec4 output_gamma_inv;
varying vec2 Tex0;
varying vec4 VertexLighting;
varying vec3 viewVec;
varying vec3 normal;
varying vec3 tangent;
varying vec4 VertexColor;
varying float Fog;
void main ()
{
  vec4 total_light_1;
  vec4 final_col_2;
  vec4 tex1_col_3;
  vec4 tmpvar_4;
  vec3 tmpvar_5;
  tmpvar_5 = -(vSunDir.xyz);
  vec4 tmpvar_6;
  tmpvar_6 = texture2D (diffuse_texture, Tex0);
  tex1_col_3.w = tmpvar_6.w;
  tex1_col_3.xyz = pow (tmpvar_6.xyz, vec3(2.2, 2.2, 2.2));
  final_col_2.w = tex1_col_3.w;
  final_col_2.xyz = (tex1_col_3.xyz * vMaterialColor.xyz);
  vec4 tmpvar_7;
  tmpvar_7 = texture2D (diffuse_texture_2, Tex0);
  float tmpvar_8;
  tmpvar_8 = clamp (((
    (2.0 * vMaterialColor2.w)
   + tmpvar_7.w) - 1.9), 0.0, 1.0);
  final_col_2.xyz = (final_col_2.xyz * (1.0 - tmpvar_8));
  final_col_2.xyz = (final_col_2.xyz + (tmpvar_7.xyz * tmpvar_8));
  vec3 tmpvar_9;
  tmpvar_9 = normalize((tmpvar_5 + viewVec));
  float tmpvar_10;
  tmpvar_10 = dot (normalize((tangent + 
    ((-0.362 + tmpvar_7.w) * normal)
  )), tmpvar_9);
  float tmpvar_11;
  tmpvar_11 = dot (normalize((tangent + 
    ((-0.246 + tmpvar_7.w) * normal)
  )), tmpvar_9);
  total_light_1.w = vAmbientColor.w;
  total_light_1.xyz = (vAmbientColor.xyz + ((
    ((vMaterialColor.xyz * vSunColor.xyz) * VertexColor.xyz)
   * 
    clamp (((0.75 * dot (normal, tmpvar_5)) + 0.25), 0.0, 1.0)
  ) + (
    (((vSunColor.xyz * vec3(0.800118, 0.88902, 0.88902)) * pow (sqrt(
      (1.0 - (tmpvar_10 * tmpvar_10))
    ), 179.2)) + (((vSunColor.xyz * vec3(0.7326, 0.65934, 0.7326)) * pow (
      sqrt((1.0 - (tmpvar_11 * tmpvar_11)))
    , 22.4)) * texture2D (diffuse_texture_2, (Tex0 * 10.0)).w))
   * 
    clamp (((1.75 * dot (normal, tmpvar_5)) + 0.25), 0.0, 1.0)
  )));
  total_light_1.xyz = (total_light_1.xyz + VertexLighting.xyz);
  tmpvar_4.xyz = (total_light_1.xyz * final_col_2.xyz);
  tmpvar_4.xyz = pow (tmpvar_4.xyz, output_gamma_inv.xyz);
  tmpvar_4.w = (tmpvar_6.w * vMaterialColor.w);
  tmpvar_4.xyz = mix (vFogColor.xyz, tmpvar_4.xyz, Fog);
  vec4 tmpvar_12;
  tmpvar_12 = clamp (tmpvar_4, 0.0, 1.0);
  tmpvar_4 = tmpvar_12;
  gl_FragColor = tmpvar_12;
}

