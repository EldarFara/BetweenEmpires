uniform vec4 vMaterialColor;
uniform float fFogDensity;
uniform mat4 matWorldViewProj;
uniform mat4 matWorld;
attribute vec3 inPosition;
attribute vec4 inColor0;
attribute vec2 inTexCoord;
varying float Fog;
varying vec4 Color;
varying vec2 Tex0;
void main ()
{
  vec4 tmpvar_1;
  tmpvar_1.w = 1.0;
  tmpvar_1.xyz = inPosition;
  vec3 P_2;
  vec4 tmpvar_3;
  vec4 tmpvar_4;
  tmpvar_3 = (matWorldViewProj * tmpvar_1);
  tmpvar_3.z = tmpvar_3.w;
  P_2.xy = tmpvar_1.xy;
  tmpvar_4 = (inColor0.zyxw * vMaterialColor);
  P_2.z = (inPosition.z * 0.2);
  vec4 tmpvar_5;
  tmpvar_5 = (matWorld * tmpvar_1);
  float tmpvar_6;
  tmpvar_6 = (1.0/(exp2((
    sqrt(dot (P_2, P_2))
   * fFogDensity))));
  float tmpvar_7;
  if ((tmpvar_5.z < -10.0)) {
    tmpvar_7 = 0.0;
  } else {
    tmpvar_7 = 1.0;
  };
  tmpvar_4.w = tmpvar_7;
  gl_Position = tmpvar_3;
  Fog = tmpvar_6;
  Color = tmpvar_4;
  Tex0 = inTexCoord;
}

