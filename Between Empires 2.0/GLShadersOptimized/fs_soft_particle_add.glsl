uniform sampler2D diffuse_texture;
uniform sampler2D depth_texture;
uniform bool use_depth_effects;
varying vec4 Color;
varying vec2 Tex0;
varying vec4 projCoord;
varying float Depth;
void main ()
{
  vec4 tmpvar_1;
  tmpvar_1 = (Color * texture2D (diffuse_texture, Tex0));
  if (use_depth_effects) {
    tmpvar_1 = (tmpvar_1 * clamp ((
      (texture2DProj (depth_texture, projCoord).x - Depth)
     * 4096.0), 0.0, 1.0));
  };
  gl_FragColor = tmpvar_1;
}

