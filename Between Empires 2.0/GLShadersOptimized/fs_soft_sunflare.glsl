uniform sampler2D diffuse_texture;
uniform sampler2D depth_texture;
uniform float fFogDensity;
uniform bool use_depth_effects;
varying vec4 Color;
varying vec2 Tex0;
varying vec4 projCoord;
void main ()
{
  vec4 tmpvar_1;
  tmpvar_1 = (Color * texture2D (diffuse_texture, Tex0));
  if (use_depth_effects) {
    tmpvar_1 = (tmpvar_1 * (texture2DProj (depth_texture, projCoord).x * (1.001 - 
      (10.0 * (fFogDensity + 0.001))
    )));
  };
  gl_FragColor = tmpvar_1;
}

