
attribute vec3 inPosition;
attribute vec3 inNormal;
attribute vec4 inColor0;
attribute vec4 inColor1;
attribute vec2 inTexCoord;

varying vec4 outColor0;
varying vec2 outTexCoord;
varying float outFog;

void main()
{
	gl_Position = mul(matWorldViewProj, vec4(inPosition, 1.0));
}