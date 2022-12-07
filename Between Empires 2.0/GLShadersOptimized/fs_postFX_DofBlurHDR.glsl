uniform sampler2D postFX_sampler0;
uniform vec4 g_HalfPixel_ViewportSizeInv;
varying vec2 Tex;
void main ()
{
  vec2 sample_pos_1;
  vec3 sample_val_2;
  float sampleDist_3;
  sampleDist_3 = (g_HalfPixel_ViewportSizeInv.x * 3.14);
  sample_pos_1 = (Tex - vec2(sampleDist_3));
  sample_val_2 = (texture2D (postFX_sampler0, Tex).xyz + texture2D (postFX_sampler0, sample_pos_1).xyz);
  sample_pos_1 = (Tex + (vec2(sampleDist_3) * vec2(0.0, -1.0)));
  sample_val_2 = (sample_val_2 + texture2D (postFX_sampler0, sample_pos_1).xyz);
  sample_pos_1 = (Tex + (vec2(sampleDist_3) * vec2(1.0, -1.0)));
  sample_val_2 = (sample_val_2 + texture2D (postFX_sampler0, sample_pos_1).xyz);
  sample_pos_1 = (Tex + (vec2(sampleDist_3) * vec2(-1.0, 0.0)));
  sample_val_2 = (sample_val_2 + texture2D (postFX_sampler0, sample_pos_1).xyz);
  sample_pos_1 = (Tex + (vec2(sampleDist_3) * vec2(1.0, 0.0)));
  sample_val_2 = (sample_val_2 + texture2D (postFX_sampler0, sample_pos_1).xyz);
  sample_pos_1 = (Tex + (vec2(sampleDist_3) * vec2(-1.0, 1.0)));
  sample_val_2 = (sample_val_2 + texture2D (postFX_sampler0, sample_pos_1).xyz);
  sample_pos_1 = (Tex + (vec2(sampleDist_3) * vec2(0.0, 1.0)));
  sample_val_2 = (sample_val_2 + texture2D (postFX_sampler0, sample_pos_1).xyz);
  sample_pos_1 = (Tex + vec2(sampleDist_3));
  sample_val_2 = (sample_val_2 + texture2D (postFX_sampler0, sample_pos_1).xyz);
  sample_val_2 = (sample_val_2 / 9.0);
  vec4 tmpvar_4;
  tmpvar_4.w = 1.0;
  tmpvar_4.xyz = sample_val_2;
  gl_FragColor = tmpvar_4;
}

