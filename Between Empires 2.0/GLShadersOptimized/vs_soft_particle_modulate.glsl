uniform vec4 vMaterialColor;
uniform float fFogDensity;
uniform float far_clip_Inv;
uniform bool use_depth_effects;
uniform mat4 matWorldViewProj;
uniform mat4 matWorldView;
uniform vec4 vDepthRT_HalfPixel_ViewportSizeInv;
attribute vec3 inPosition;
attribute vec4 inColor0;
attribute vec2 inTexCoord;
varying vec4 Color;
varying vec2 Tex0;
varying float Fog;
varying vec4 projCoord;
varying float Depth;
void main ()
{
  vec4 tmpvar_1;
  tmpvar_1.w = 1.0;
  tmpvar_1.xyz = inPosition;
  vec4 tmpvar_2;
  vec4 tmpvar_3;
  vec4 tmpvar_4;
  float tmpvar_5;
  tmpvar_2 = (matWorldViewProj * tmpvar_1);
  tmpvar_3 = (inColor0.zyxw * vMaterialColor);
  if (use_depth_effects) {
    tmpvar_4.xy = ((tmpvar_2.xy + tmpvar_2.w) / 2.0);
    tmpvar_4.xy = (tmpvar_4.xy + (vDepthRT_HalfPixel_ViewportSizeInv.xy * tmpvar_2.w));
    tmpvar_4.zw = tmpvar_2.zw;
    tmpvar_5 = (((0.5 * tmpvar_2.z) + 0.5) * far_clip_Inv);
  };
  vec3 tmpvar_6;
  tmpvar_6 = (matWorldView * tmpvar_1).xyz;
  gl_Position = tmpvar_2;
  Color = tmpvar_3;
  Tex0 = inTexCoord;
  Fog = (1.0/(exp2((
    sqrt(dot (tmpvar_6, tmpvar_6))
   * fFogDensity))));
  projCoord = tmpvar_4;
  Depth = tmpvar_5;
}

