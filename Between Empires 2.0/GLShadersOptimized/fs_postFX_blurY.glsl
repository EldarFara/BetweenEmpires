uniform sampler2D postFX_sampler0;
uniform vec4 g_HalfPixel_ViewportSizeInv;
varying vec2 Tex;
void main ()
{
  vec4 color_1;
  vec2 tmpvar_2;
  tmpvar_2.x = 0.0;
  tmpvar_2.y = g_HalfPixel_ViewportSizeInv.w;
  vec4 tmpvar_3;
  tmpvar_3 = texture2D (postFX_sampler0, Tex);
  color_1 = (tmpvar_3 * 0.256);
  color_1 = (color_1 + (tmpvar_3 * 0.256));
  color_1 = (color_1 + (texture2D (postFX_sampler0, (Tex + tmpvar_2)) * 0.24));
  color_1 = (color_1 + (texture2D (postFX_sampler0, (Tex - tmpvar_2)) * 0.24));
  color_1 = (color_1 + (texture2D (postFX_sampler0, (Tex + 
    (tmpvar_2 * 2.0)
  )) * 0.144));
  color_1 = (color_1 + (texture2D (postFX_sampler0, (Tex - 
    (tmpvar_2 * 2.0)
  )) * 0.144));
  color_1 = (color_1 + (texture2D (postFX_sampler0, (Tex + 
    (tmpvar_2 * 3.0)
  )) * 0.135));
  color_1 = (color_1 + (texture2D (postFX_sampler0, (Tex - 
    (tmpvar_2 * 3.0)
  )) * 0.135));
  color_1 = (color_1 + (texture2D (postFX_sampler0, (Tex + 
    (tmpvar_2 * 4.0)
  )) * 0.12));
  color_1 = (color_1 + (texture2D (postFX_sampler0, (Tex - 
    (tmpvar_2 * 4.0)
  )) * 0.12));
  color_1 = (color_1 + (texture2D (postFX_sampler0, (Tex + 
    (tmpvar_2 * 5.0)
  )) * 0.065));
  color_1 = (color_1 + (texture2D (postFX_sampler0, (Tex - 
    (tmpvar_2 * 5.0)
  )) * 0.065));
  color_1 = (color_1 + (texture2D (postFX_sampler0, (Tex + 
    (tmpvar_2 * 6.0)
  )) * 0.03));
  color_1 = (color_1 + (texture2D (postFX_sampler0, (Tex - 
    (tmpvar_2 * 6.0)
  )) * 0.03));
  color_1 = (color_1 + (texture2D (postFX_sampler0, (Tex + 
    (tmpvar_2 * 7.0)
  )) * 0.01));
  color_1 = (color_1 + (texture2D (postFX_sampler0, (Tex - 
    (tmpvar_2 * 7.0)
  )) * 0.01));
  gl_FragColor = color_1;
}

