uniform vec4 postfx_editor_vector[4];
uniform sampler2D postFX_sampler0;
uniform vec4 g_HalfPixel_ViewportSizeInv;
varying vec2 Tex;
void main ()
{
  float _log_sum_1;
  float _max_2;
  float tmpvar_3;
  tmpvar_3 = dot ((texture2D (postFX_sampler0, (Tex + 
    (vec2(-1.5, -1.5) * g_HalfPixel_ViewportSizeInv.yw)
  )).xyz * postfx_editor_vector[1].x), vec3(0.299, 0.587, 0.114));
  _max_2 = max (0.0, tmpvar_3);
  float tmpvar_4;
  tmpvar_4 = dot ((texture2D (postFX_sampler0, (Tex + 
    (vec2(-1.5, -0.5) * g_HalfPixel_ViewportSizeInv.yw)
  )).xyz * postfx_editor_vector[1].x), vec3(0.299, 0.587, 0.114));
  _log_sum_1 = (tmpvar_3 + tmpvar_4);
  _max_2 = max (_max_2, tmpvar_4);
  float tmpvar_5;
  tmpvar_5 = dot ((texture2D (postFX_sampler0, (Tex + 
    (vec2(-1.5, 0.5) * g_HalfPixel_ViewportSizeInv.yw)
  )).xyz * postfx_editor_vector[1].x), vec3(0.299, 0.587, 0.114));
  _log_sum_1 = (_log_sum_1 + tmpvar_5);
  _max_2 = max (_max_2, tmpvar_5);
  float tmpvar_6;
  tmpvar_6 = dot ((texture2D (postFX_sampler0, (Tex + 
    (vec2(-1.5, 1.5) * g_HalfPixel_ViewportSizeInv.yw)
  )).xyz * postfx_editor_vector[1].x), vec3(0.299, 0.587, 0.114));
  _log_sum_1 = (_log_sum_1 + tmpvar_6);
  _max_2 = max (_max_2, tmpvar_6);
  float tmpvar_7;
  tmpvar_7 = dot ((texture2D (postFX_sampler0, (Tex + 
    (vec2(-0.5, -1.5) * g_HalfPixel_ViewportSizeInv.yw)
  )).xyz * postfx_editor_vector[1].x), vec3(0.299, 0.587, 0.114));
  _log_sum_1 = (_log_sum_1 + tmpvar_7);
  _max_2 = max (_max_2, tmpvar_7);
  float tmpvar_8;
  tmpvar_8 = dot ((texture2D (postFX_sampler0, (Tex + 
    (vec2(-0.5, -0.5) * g_HalfPixel_ViewportSizeInv.yw)
  )).xyz * postfx_editor_vector[1].x), vec3(0.299, 0.587, 0.114));
  _log_sum_1 = (_log_sum_1 + tmpvar_8);
  _max_2 = max (_max_2, tmpvar_8);
  float tmpvar_9;
  tmpvar_9 = dot ((texture2D (postFX_sampler0, (Tex + 
    (vec2(-0.5, 0.5) * g_HalfPixel_ViewportSizeInv.yw)
  )).xyz * postfx_editor_vector[1].x), vec3(0.299, 0.587, 0.114));
  _log_sum_1 = (_log_sum_1 + tmpvar_9);
  _max_2 = max (_max_2, tmpvar_9);
  float tmpvar_10;
  tmpvar_10 = dot ((texture2D (postFX_sampler0, (Tex + 
    (vec2(-0.5, 1.5) * g_HalfPixel_ViewportSizeInv.yw)
  )).xyz * postfx_editor_vector[1].x), vec3(0.299, 0.587, 0.114));
  _log_sum_1 = (_log_sum_1 + tmpvar_10);
  _max_2 = max (_max_2, tmpvar_10);
  float tmpvar_11;
  tmpvar_11 = dot ((texture2D (postFX_sampler0, (Tex + 
    (vec2(0.5, -1.5) * g_HalfPixel_ViewportSizeInv.yw)
  )).xyz * postfx_editor_vector[1].x), vec3(0.299, 0.587, 0.114));
  _log_sum_1 = (_log_sum_1 + tmpvar_11);
  _max_2 = max (_max_2, tmpvar_11);
  float tmpvar_12;
  tmpvar_12 = dot ((texture2D (postFX_sampler0, (Tex + 
    (vec2(0.5, -0.5) * g_HalfPixel_ViewportSizeInv.yw)
  )).xyz * postfx_editor_vector[1].x), vec3(0.299, 0.587, 0.114));
  _log_sum_1 = (_log_sum_1 + tmpvar_12);
  _max_2 = max (_max_2, tmpvar_12);
  float tmpvar_13;
  tmpvar_13 = dot ((texture2D (postFX_sampler0, (Tex + 
    (vec2(0.5, 0.5) * g_HalfPixel_ViewportSizeInv.yw)
  )).xyz * postfx_editor_vector[1].x), vec3(0.299, 0.587, 0.114));
  _log_sum_1 = (_log_sum_1 + tmpvar_13);
  _max_2 = max (_max_2, tmpvar_13);
  float tmpvar_14;
  tmpvar_14 = dot ((texture2D (postFX_sampler0, (Tex + 
    (vec2(0.5, 1.5) * g_HalfPixel_ViewportSizeInv.yw)
  )).xyz * postfx_editor_vector[1].x), vec3(0.299, 0.587, 0.114));
  _log_sum_1 = (_log_sum_1 + tmpvar_14);
  _max_2 = max (_max_2, tmpvar_14);
  float tmpvar_15;
  tmpvar_15 = dot ((texture2D (postFX_sampler0, (Tex + 
    (vec2(1.5, -1.5) * g_HalfPixel_ViewportSizeInv.yw)
  )).xyz * postfx_editor_vector[1].x), vec3(0.299, 0.587, 0.114));
  _log_sum_1 = (_log_sum_1 + tmpvar_15);
  _max_2 = max (_max_2, tmpvar_15);
  float tmpvar_16;
  tmpvar_16 = dot ((texture2D (postFX_sampler0, (Tex + 
    (vec2(1.5, -0.5) * g_HalfPixel_ViewportSizeInv.yw)
  )).xyz * postfx_editor_vector[1].x), vec3(0.299, 0.587, 0.114));
  _log_sum_1 = (_log_sum_1 + tmpvar_16);
  _max_2 = max (_max_2, tmpvar_16);
  float tmpvar_17;
  tmpvar_17 = dot ((texture2D (postFX_sampler0, (Tex + 
    (vec2(1.5, 0.5) * g_HalfPixel_ViewportSizeInv.yw)
  )).xyz * postfx_editor_vector[1].x), vec3(0.299, 0.587, 0.114));
  _log_sum_1 = (_log_sum_1 + tmpvar_17);
  _max_2 = max (_max_2, tmpvar_17);
  float tmpvar_18;
  tmpvar_18 = dot ((texture2D (postFX_sampler0, (Tex + 
    (vec2(1.5, 1.5) * g_HalfPixel_ViewportSizeInv.yw)
  )).xyz * postfx_editor_vector[1].x), vec3(0.299, 0.587, 0.114));
  _log_sum_1 = (_log_sum_1 + tmpvar_18);
  _max_2 = max (_max_2, tmpvar_18);
  vec4 tmpvar_19;
  tmpvar_19.zw = vec2(0.0, 1.0);
  tmpvar_19.x = (_log_sum_1 / 16.0);
  tmpvar_19.y = _max_2;
  gl_FragColor = tmpvar_19;
}

