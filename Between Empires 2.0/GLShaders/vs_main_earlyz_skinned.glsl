
attribute vec3 inPosition;
attribute vec3 inNormal;
attribute vec4 inColor0;
attribute vec2 inTexCoord;
attribute vec3 inTangent;
attribute vec3 inBinormal;
attribute vec4 inBlendWeight;
attribute vec4 inBlendIndices;

varying float2 TC;
varying float Depth;

void main()
{
#ifdef DISABLE_GPU_SKINNING
	float4 vObjectPos = vec4(inPosition, 1.0);
#else
	float4 vObjectPos = skinning_deform(vec4(inPosition, 1.0), inBlendWeight, inBlendIndices);
#endif

	vec4 Pos = mul(matWorldViewProj, vObjectPos);
	gl_Position = Pos;
	TC = inTexCoord;
	
	#ifdef VIEW_SPACE
		float4 depth_pos = mul(matWorldView, vObjectPos);
		Depth = get_depth(depth_pos);
	#else 
		Depth = get_depth(Pos);
	#endif
}
