
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
	vec4 Pos = mul(matWorldViewProj, vec4(inPosition, 1.0));
	gl_Position = Pos;
	TC = inTexCoord;

	#ifdef VIEW_SPACE
		float4 depth_pos = mul(matWorldView, vec4(inPosition, 1.0));
		Depth = get_depth(depth_pos);
	#else 
		Depth = get_depth(Pos);
	#endif
}
