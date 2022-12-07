uniform float far_clip;
uniform mat4 matWorldViewProj;
attribute vec3 inPosition;
attribute vec2 inTexCoord;
varying vec2 TC;
varying float Depth;
void main ()
{
  vec4 tmpvar_1;
  tmpvar_1.w = 1.0;
  tmpvar_1.xyz = inPosition;
  vec4 tmpvar_2;
  tmpvar_2 = (matWorldViewProj * tmpvar_1);
  gl_Position = tmpvar_2;
  TC = inTexCoord;
  Depth = (((tmpvar_2.z * 0.5) + 0.5) / far_clip);
}

