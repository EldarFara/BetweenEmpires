
attribute vec3 inPosition;
attribute vec3 inNormal;
attribute vec4 inColor0;
attribute vec4 inColor1;
attribute vec2 inTexCoord;

varying vec3 outNormal;
varying vec4 outColor0;
varying vec4 outColor1;
varying vec2 outTexCoord;
varying float outDepth;

void main()
{
	gl_Position = mul(matWorldViewProj, vec4(inPosition, 1.0));
	outDepth = gl_Position.z / gl_Position.w;
	
	float3 vScreenNormal = mul(matWorldViewProj, vec4(inNormal, 0.0)).xyz; //normal attribute screen space
	outDepth -= vScreenNormal.z * (fShadowBias);
	gl_Position.z += (0.0025);	//extra bias!

	outTexCoord = inTexCoord;
}
