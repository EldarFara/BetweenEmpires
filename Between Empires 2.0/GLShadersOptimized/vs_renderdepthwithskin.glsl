uniform mat4 matWorldViewProj;
uniform mat4 matWorldArray[32];
attribute vec3 inPosition;
attribute vec2 inTexCoord;
attribute vec4 inBlendWeight;
attribute vec4 inBlendIndices;
varying vec2 outTexCoord;
varying float outDepth;
void main ()
{
  vec4 tmpvar_1;
  tmpvar_1.w = 1.0;
  tmpvar_1.xyz = inPosition;
  gl_Position = (matWorldViewProj * ((
    (((matWorldArray[int(inBlendIndices.x)] * tmpvar_1) * inBlendWeight.x) + ((matWorldArray[int(inBlendIndices.y)] * tmpvar_1) * inBlendWeight.y))
   + 
    ((matWorldArray[int(inBlendIndices.z)] * tmpvar_1) * inBlendWeight.z)
  ) + (
    (matWorldArray[int(inBlendIndices.w)] * tmpvar_1)
   * inBlendWeight.w)));
  outDepth = (gl_Position.z / gl_Position.w);
  outTexCoord = inTexCoord;
}

