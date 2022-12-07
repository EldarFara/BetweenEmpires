uniform sampler2D diffuse_texture;
uniform sampler2D diffuse_texture_2;
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
  vec4 fSpecular_2;
  vec4 total_light_3;
  vec4 tmpvar_4;
  vec3 tmpvar_5;
  tmpvar_5 = ((2.0 * texture2D (normal_texture, Tex0)) - 1.0).xyz;
  vec4 tmpvar_6;
  tmpvar_6.w = 1.0;
  tmpvar_6.xyz = vSunColor.xyz;
  vec4 tmpvar_7;
  tmpvar_7.w = 1.0;
  tmpvar_7.xyz = vSpecularColor.xyz;
  vec4 tmpvar_8;
  tmpvar_8 = ((tmpvar_6 * (tmpvar_7 * 0.1)) * pow (clamp (
    dot (normalize((ViewDir + SunLightDir)), tmpvar_5)
  , 0.0, 1.0), fMaterialPower));
  fSpecular_2.w = tmpvar_8.w;
  vec4 tmpvar_9;
  tmpvar_9 = texture2D (diffuse_texture_2, Tex0);
  vec3 tmpvar_10;
  tmpvar_10 = normalize((SunLightDir + ViewDir));
  float tmpvar_11;
  tmpvar_11 = dot (normalize((vec3(0.0, 1.0, 0.0) + 
    ((-0.362 + tmpvar_9.w) * tmpvar_5)
  )), tmpvar_10);
  float tmpvar_12;
  tmpvar_12 = dot (normalize((vec3(0.0, 1.0, 0.0) + 
    ((-0.246 + tmpvar_9.w) * tmpvar_5)
  )), tmpvar_10);
  fSpecular_2.xyz = (tmpvar_8.xyz + ((
    ((vSunColor.xyz * vec3(0.800118, 0.88902, 0.88902)) * pow (sqrt((1.0 - 
      (tmpvar_11 * tmpvar_11)
    )), 179.2))
   + 
    (((vSunColor.xyz * vec3(0.7326, 0.65934, 0.7326)) * pow (sqrt(
      (1.0 - (tmpvar_12 * tmpvar_12))
    ), 22.4)) * texture2D (diffuse_texture_2, (Tex0 * 10.0)).w)
  ) * clamp (
    ((1.75 * dot (tmpvar_5, SunLightDir)) + 0.25)
  , 0.0, 1.0)));
  vec4 tmpvar_13;
  tmpvar_13.w = 1.0;
  tmpvar_13.xyz = vSunColor.xyz;
  total_light_3 = (mix (vGroundAmbientColor, vAmbientColor, (
    (dot (tmpvar_5, SkyLightDir) + 1.0)
   * 0.5)) + ((
    clamp (dot (SunLightDir, tmpvar_5), 0.0, 1.0)
   + fSpecular_2) * tmpvar_13));
  total_light_3 = (total_light_3 + (clamp (
    dot (SkyLightDir, tmpvar_5)
  , 0.0, 1.0) * vSkyLightColor));
  int tmpvar_14;
  tmpvar_14 = iLightIndices[0];
  total_light_3 = (total_light_3 + ((
    clamp (dot (PointLightDir.xyz, tmpvar_5), 0.0, 1.0)
   * vLightDiffuse[tmpvar_14]) * PointLightDir.w));
  total_light_3.xyz = (total_light_3.xyz + VertexLighting);
  tmpvar_4.xyz = total_light_3.xyz;
  tmpvar_4.w = 1.0;
  tmpvar_4 = (tmpvar_4 * vMaterialColor);
  vec4 tmpvar_15;
  tmpvar_15 = texture2D (diffuse_texture, Tex0);
  tex_col_1.w = tmpvar_15.w;
  tex_col_1.xyz = pow (tmpvar_15.xyz, vec3(2.2, 2.2, 2.2));
  tmpvar_4 = (tmpvar_4 * tex_col_1);
  tmpvar_4 = (tmpvar_4 * VertexColor);
  tmpvar_4.xyz = pow (tmpvar_4.xyz, output_gamma_inv.xyz);
  tmpvar_4.w = (VertexColor.w * tmpvar_15.w);
  tmpvar_4.xyz = mix (vFogColor.xyz, tmpvar_4.xyz, Fog);
  gl_FragColor = tmpvar_4;
}

