uniform sampler2D diffuse_texture;
uniform sampler2D specular_texture;
uniform vec4 vFogColor;
uniform vec4 output_gamma_inv;
uniform float vSeason;
varying vec4 outColor0;
varying vec2 outTexCoord;
varying float outFog;
void main ()
{
  vec4 tex_col_1;
  vec4 tmpvar_2;
  vec4 tmpvar_3;
  tmpvar_3 = texture2D (diffuse_texture, outTexCoord);
  tex_col_1.w = tmpvar_3.w;
  if (((tmpvar_3.w - 0.5) < 0.0)) {
    discard;
  };
  tex_col_1.xyz = pow (tmpvar_3.xyz, vec3(2.2, 2.2, 2.2));
  if ((vSeason < 0.5)) {
    tex_col_1.xyz = clamp ((tex_col_1.xyz * vec3(0.9, 1.1, 0.9)), 0.0, 1.0);
  } else {
    if (((vSeason > 0.5) && (vSeason < 1.5))) {
      tex_col_1.xyz = clamp (tex_col_1.xyz, 0.0, 1.0);
    } else {
      if (((vSeason > 1.5) && (vSeason < 2.5))) {
        tex_col_1.xyz = clamp ((tex_col_1.xyz * vec3(1.1, 0.9, 0.9)), 0.0, 1.0);
      } else {
        if ((vSeason > 2.5)) {
          tex_col_1 = texture2D (specular_texture, outTexCoord);
        };
      };
    };
  };
  tmpvar_2 = (outColor0 * tex_col_1);
  tmpvar_2.xyz = pow (tmpvar_2.xyz, output_gamma_inv.xyz);
  tmpvar_2.xyz = mix (vFogColor.xyz, tmpvar_2.xyz, outFog);
  gl_FragColor = tmpvar_2;
}

