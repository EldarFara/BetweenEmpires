uniform mat4 matWorldViewProj;
attribute vec3 inPosition;
attribute vec3 inNormal;
attribute vec2 inTexCoord;
varying vec2 outTexCoord;
varying float outDepth;
void main ()
{
  vec4 tmpvar_1;
  tmpvar_1.w = 1.0;
  tmpvar_1.xyz = inPosition;
  gl_Position = (matWorldViewProj * tmpvar_1);
  outDepth = (gl_Position.z / gl_Position.w);
  vec4 tmpvar_2;
  tmpvar_2.w = 0.0;
  tmpvar_2.xyz = inNormal;
  outDepth = (outDepth - ((matWorldViewProj * tmpvar_2).z * 2e-05));
  outTexCoord = inTexCoord;
}

