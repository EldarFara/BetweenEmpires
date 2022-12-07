
attribute vec3 inPosition;
attribute vec3 inNormal;
attribute vec4 inColor0;
attribute vec2 inTexCoord;
attribute vec4 inBlendWeight;
attribute vec4 inBlendIndices;

varying vec3 outNormal;
varying vec4 outColor0;
varying vec4 outColor1;
varying vec2 outTexCoord;
varying float outDepth;

void main()
{
#ifdef DISABLE_GPU_SKINNING
	float4 vObjectPos = vec4(inPosition, 1.0);
#else
	float4 vObjectPos = skinning_deform(vec4(inPosition, 1.0), inBlendWeight, inBlendIndices);
#endif

	gl_Position = mul(matWorldViewProj, vObjectPos);
	outDepth = gl_Position.z / gl_Position.w;
	outTexCoord = inTexCoord;
}
