uniform sampler2D postFX_sampler0;
uniform sampler2D postFX_sampler1;
uniform vec4 g_HalfPixel_ViewportSizeInv;
varying vec2 Tex;
void main ()
{
  vec2 sample_pos_1;
  vec3 sample_val_2;
  float sampleDist_3;
  float depth_start_4;
  vec3 tmpvar_5;
  tmpvar_5 = texture2D (postFX_sampler0, Tex).xyz;
  depth_start_4 = texture2D (postFX_sampler1, Tex).x;
  sampleDist_3 = (g_HalfPixel_ViewportSizeInv.x * 3.14);
  sample_val_2 = tmpvar_5;
  vec3 sample_here_6;
  sample_pos_1 = (Tex - vec2(sampleDist_3));
  vec4 tmpvar_7;
  tmpvar_7 = texture2D (postFX_sampler1, sample_pos_1);
  if ((tmpvar_7.x < depth_start_4)) {
    sample_here_6 = tmpvar_5;
  } else {
    sample_here_6 = texture2D (postFX_sampler0, sample_pos_1).xyz;
  };
  sample_val_2 = (tmpvar_5 + sample_here_6);
  vec3 sample_here_8;
  sample_pos_1 = (Tex + (vec2(sampleDist_3) * vec2(0.0, -1.0)));
  vec4 tmpvar_9;
  tmpvar_9 = texture2D (postFX_sampler1, sample_pos_1);
  if ((tmpvar_9.x < depth_start_4)) {
    sample_here_8 = tmpvar_5;
  } else {
    sample_here_8 = texture2D (postFX_sampler0, sample_pos_1).xyz;
  };
  sample_val_2 = (sample_val_2 + sample_here_8);
  vec3 sample_here_10;
  sample_pos_1 = (Tex + (vec2(sampleDist_3) * vec2(1.0, -1.0)));
  vec4 tmpvar_11;
  tmpvar_11 = texture2D (postFX_sampler1, sample_pos_1);
  if ((tmpvar_11.x < depth_start_4)) {
    sample_here_10 = tmpvar_5;
  } else {
    sample_here_10 = texture2D (postFX_sampler0, sample_pos_1).xyz;
  };
  sample_val_2 = (sample_val_2 + sample_here_10);
  vec3 sample_here_12;
  sample_pos_1 = (Tex + (vec2(sampleDist_3) * vec2(-1.0, 0.0)));
  vec4 tmpvar_13;
  tmpvar_13 = texture2D (postFX_sampler1, sample_pos_1);
  if ((tmpvar_13.x < depth_start_4)) {
    sample_here_12 = tmpvar_5;
  } else {
    sample_here_12 = texture2D (postFX_sampler0, sample_pos_1).xyz;
  };
  sample_val_2 = (sample_val_2 + sample_here_12);
  vec3 sample_here_14;
  sample_pos_1 = (Tex + (vec2(sampleDist_3) * vec2(1.0, 0.0)));
  vec4 tmpvar_15;
  tmpvar_15 = texture2D (postFX_sampler1, sample_pos_1);
  if ((tmpvar_15.x < depth_start_4)) {
    sample_here_14 = tmpvar_5;
  } else {
    sample_here_14 = texture2D (postFX_sampler0, sample_pos_1).xyz;
  };
  sample_val_2 = (sample_val_2 + sample_here_14);
  vec3 sample_here_16;
  sample_pos_1 = (Tex + (vec2(sampleDist_3) * vec2(-1.0, 1.0)));
  vec4 tmpvar_17;
  tmpvar_17 = texture2D (postFX_sampler1, sample_pos_1);
  if ((tmpvar_17.x < depth_start_4)) {
    sample_here_16 = tmpvar_5;
  } else {
    sample_here_16 = texture2D (postFX_sampler0, sample_pos_1).xyz;
  };
  sample_val_2 = (sample_val_2 + sample_here_16);
  vec3 sample_here_18;
  sample_pos_1 = (Tex + (vec2(sampleDist_3) * vec2(0.0, 1.0)));
  vec4 tmpvar_19;
  tmpvar_19 = texture2D (postFX_sampler1, sample_pos_1);
  if ((tmpvar_19.x < depth_start_4)) {
    sample_here_18 = tmpvar_5;
  } else {
    sample_here_18 = texture2D (postFX_sampler0, sample_pos_1).xyz;
  };
  sample_val_2 = (sample_val_2 + sample_here_18);
  vec3 sample_here_20;
  sample_pos_1 = (Tex + vec2(sampleDist_3));
  vec4 tmpvar_21;
  tmpvar_21 = texture2D (postFX_sampler1, sample_pos_1);
  if ((tmpvar_21.x < depth_start_4)) {
    sample_here_20 = tmpvar_5;
  } else {
    sample_here_20 = texture2D (postFX_sampler0, sample_pos_1).xyz;
  };
  sample_val_2 = (sample_val_2 + sample_here_20);
  sample_val_2 = (sample_val_2 / 9.0);
  vec4 tmpvar_22;
  tmpvar_22.w = 1.0;
  tmpvar_22.xyz = sample_val_2;
  gl_FragColor = tmpvar_22;
}

