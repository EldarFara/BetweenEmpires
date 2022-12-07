uniform float far_clip;
uniform mat4 matWorldViewProj;
uniform mat4 matWorldArray[32];
attribute vec3 inPosition;
attribute vec2 inTexCoord;
attribute vec4 inBlendWeight;
attribute vec4 inBlendIndices;
varying vec2 TC;
varying float Depth;
void main ()
{
  vec4 tmpvar_1;
  tmpvar_1.w = 1.0;
  tmpvar_1.xyz = inPosition;
  vec4 tmpvar_2;
  tmpvar_2 = (matWorldViewProj * ((
    (((matWorldArray[int(inBlendIndices.x)] * tmpvar_1) * inBlendWeight.x) + ((matWorldArray[int(inBlendIndices.y)] * tmpvar_1) * inBlendWeight.y))
   + 
    ((matWorldArray[int(inBlendIndices.z)] * tmpvar_1) * inBlendWeight.z)
  ) + (
    (matWorldArray[int(inBlendIndices.w)] * tmpvar_1)
   * inBlendWeight.w)));
  gl_Position = tmpvar_2;
  TC = inTexCoord;
  Depth = (((tmpvar_2.z * 0.5) + 0.5) / far_clip);
}

