uniform sampler2D diffuse_texture;
uniform vec4 vFogColor;
varying float Fog;
varying vec2 Tex0;
varying vec4 Color;
void main ()
{
  vec4 tmpvar_1;
  float sample_val_2;
  float sampleDist_3;
  float tmpvar_4;
  tmpvar_4 = clamp ((1.0 - Tex0.y), 0.0, 1.0);
  sampleDist_3 = (0.0234375 * (tmpvar_4 * tmpvar_4));
  sample_val_2 = texture2D (diffuse_texture, clamp (Tex0, 0.0, 1.0)).x;
  sample_val_2 = (sample_val_2 + texture2D (diffuse_texture, clamp ((Tex0 + 
    (sampleDist_3 * vec2(-1.0, 1.0))
  ), 0.0, 1.0)).x);
  sample_val_2 = (sample_val_2 + texture2D (diffuse_texture, clamp ((Tex0 + vec2(sampleDist_3)), 0.0, 1.0)).x);
  sample_val_2 = (sample_val_2 + texture2D (diffuse_texture, clamp ((Tex0 + 
    (sampleDist_3 * vec2(0.0, 2.0))
  ), 0.0, 1.0)).x);
  sample_val_2 = (sample_val_2 + texture2D (diffuse_texture, clamp ((Tex0 + 
    (sampleDist_3 * vec2(0.0, 3.0))
  ), 0.0, 1.0)).x);
  sample_val_2 = (sample_val_2 / 5.0);
  tmpvar_1.w = (sample_val_2 * Color.w);
  tmpvar_1.xyz = mix (vFogColor.xyz, Color.xyz, Fog);
  gl_FragColor = tmpvar_1;
}

